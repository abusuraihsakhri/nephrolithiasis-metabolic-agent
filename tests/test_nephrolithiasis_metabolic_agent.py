"""
Automated Pytest Test Suite for Nephrolithiasis Metabolic Agent.
Domain: Nephrology & Dialysis Systems
Standard: KDIGO / KDOQI Clinical Practice Guidelines
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_phi_guard_redaction():
    redacted = PHIGuard.redact_phi("Contact patient at 555-123-4567 for follow-up")
    assert "555-123-4567" not in redacted
    assert "[REDACTED_IDENTIFIER]" in redacted


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_metric_validation_rejects_nan():
    with pytest.raises(Exception):  # ValidationError
        SystemTaskPayload(task_id="T-NAN", target_identifier="KEY-01", primary_metric=math.nan)


def test_metric_validation_rejects_infinity():
    with pytest.raises(Exception):  # ValidationError
        SystemTaskPayload(task_id="T-INF", target_identifier="KEY-01", primary_metric=math.inf)


def test_metric_validation_rejects_extreme_values():
    with pytest.raises(Exception):  # ValidationError
        SystemTaskPayload(task_id="T-EXTREME", target_identifier="KEY-01", primary_metric=1e10)


def test_metric_validation_accepts_normal_values():
    p = SystemTaskPayload(task_id="T-OK", target_identifier="KEY-01", primary_metric=25.0, secondary_metric=10.0)
    assert p.primary_metric == 25.0
    assert p.secondary_metric == 10.0


def test_batch_file_not_found():
    result = main(["batch", "-i", "nonexistent_file.csv"])
    assert result == 1


def test_phi_guard_blocks_ssn():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient SSN: 123-45-6789")


def test_phi_guard_blocks_email():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Contact patient@example.com for results")

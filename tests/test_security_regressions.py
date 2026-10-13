"""Regression coverage for audit integrity and nested metadata screening."""
import pytest
from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor

KEY = "test-" + "7" * 60

def test_audit_hmac_validates_every_entry():
    trail = AuditTrail(secret_key=KEY)
    trail.log("worker", "system", "EVALUATED", {"status": "SUCCESS"})
    trail.log("worker", "system", "COMPLETE", {"status": "SUCCESS"})
    assert trail.verify_integrity()
    trail.logs[0]["event_type"] = "TAMPERED"
    assert not trail.verify_integrity()

def test_returned_audit_entries_are_defensive_copies():
    trail = AuditTrail(secret_key=KEY)
    trail.log("worker", "system", "COMPLETE", {"status": "SUCCESS"})
    copy = trail.get_trail()
    copy[0]["payload_hash"] = "FAKE"
    assert trail.verify_integrity()

def test_phi_in_nested_attributes_rejected():
    supervisor = SystemSupervisor()
    payload = SystemTaskPayload(
        task_id="T-01",
        target_identifier="SPEC-01",
        primary_metric=1.0,
        attributes={"note": "Contact subject at patient@example.com"},
    )
    with pytest.raises(SecurityException):
        supervisor.process_task(payload)

def test_audit_fields_cannot_be_repartitioned_at_delimiters():
    trail = AuditTrail(secret_key=KEY)
    trail.log("alice|admin", "service", "COMPLETE", {"status": "SUCCESS"})
    assert trail.verify_integrity()
    # With naive pipe-joined signatures these two rows had identical signed bytes.
    trail.logs[0]["actor"] = "alice"
    trail.logs[0]["actor_tier"] = "admin|service"
    assert not trail.verify_integrity()

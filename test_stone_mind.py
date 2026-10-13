import pytest
from stone_mind import SupersaturationIndexAgent, DietaryMetabolicEvaluatorAgent, PharmacologicPreventionAgent, StoneCoordinator, main


def test_sub_agents():
    a1 = SupersaturationIndexAgent()
    alerts1 = a1.evaluate({"metric_primary": 35.0})
    assert len(alerts1) == 1

    a2 = DietaryMetabolicEvaluatorAgent()
    alerts2 = a2.evaluate({"critical_flag": True})
    assert len(alerts2) == 1

    a3 = PharmacologicPreventionAgent()
    alerts3 = a3.evaluate({"status_text": "DISCORDANT_FINDING"})
    assert len(alerts3) == 1


def test_coordinator():
    coord = StoneCoordinator()
    dossier = coord.audit_case({"case_id": "TEST-100", "metric_primary": 10.0, "metric_secondary": 2.0})
    assert dossier["overall_status"] == "CONCORDANT_NORMAL"
    assert dossier["total_alerts"] == 0

    ans = coord.query_assistant("What are the guidelines?")
    assert "guidelines" in ans or "standards" in ans


def test_cli():
    assert main(["audit", "--case-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0


def test_domain_registry():
    from stone_mind import DomainKnowledgeRegistry
    assert DomainKnowledgeRegistry.ZERO_PHI_COMPLIANCE is False
    assert "PRO" in DomainKnowledgeRegistry.SYSTEM_VERSION

def test_legacy_string_false_is_not_critical():
    coord = StoneCoordinator()
    dossier = coord.audit_case({"metric_primary": 2.0, "metric_secondary": 2.0, "critical_flag": "False"})
    assert dossier["overall_status"] == "CONCORDANT_NORMAL"

def test_legacy_advisory_is_not_reported_normal():
    coord = StoneCoordinator()
    dossier = coord.audit_case({"metric_primary": 2.0, "metric_secondary": 2.0, "status_text": "DISCORDANT"})
    assert dossier["overall_status"] == "ADVISORY_ACTIVE"

def test_legacy_rejects_nonfinite_numbers():
    coord = StoneCoordinator()
    with pytest.raises(ValueError):
        coord.audit_case({"metric_primary": float("nan")})
    with pytest.raises(ValueError):
        coord.audit_case({"metric_secondary": float("inf")})

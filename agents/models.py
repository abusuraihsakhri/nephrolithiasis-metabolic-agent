"""
Pydantic v2 schemas and data definitions for Nephrolithiasis Metabolic Agent.
Domain: Nephrology & Dialysis Systems
Standard: KDIGO / KDOQI Clinical Practice Guidelines
"""
import datetime
import math
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    ELEVATED = "ELEVATED_RISK"
    CRITICAL_STAT = "CRITICAL_STAT_PANIC"


class SystemIntegrityStatus(str, Enum):
    VALIDATED = "VALIDATED_OPTIMAL"
    DISCORDANT = "DISCORDANT_ANOMALY"
    RECALIBRATION_REQUIRED = "RECALIBRATION_REQUIRED"


class SystemTaskPayload(BaseModel):
    task_id: str = Field(..., description="Unique task / case identifier")
    target_identifier: str = Field(..., description="Entity, patient key, or genomic/cryptographic target")
    primary_metric: float = Field(..., description="Primary domain measurement or score")
    secondary_metric: float = Field(default=0.0, description="Secondary kinetic or confidence score")
    status_descriptor: str = Field(default="NOMINAL", description="Status code or phenotype descriptor")
    is_critical_flag: bool = Field(default=False, description="Emergency escalation or high priority trigger")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value pairs")
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    @field_validator("task_id", "target_identifier", "status_descriptor")
    @classmethod
    def validate_no_phi_in_fields(cls, v: str) -> str:
        """Prevent PHI leakage through identifier fields."""
        if not isinstance(v, str):
            return v
        if len(v) > 256:
            raise ValueError("Field exceeds maximum allowed length (256 characters)")
        return v.strip()

    @field_validator("primary_metric", "secondary_metric")
    @classmethod
    def validate_metric_values(cls, v: float) -> float:
        """Ensure metric values are finite and within safe computational bounds."""
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Metric value must be a finite number (not NaN or Infinity)")
        if abs(v) > 1e9:
            raise ValueError("Metric value exceeds safe computational bounds (|value| > 1e9)")
        return v


class AgentAlert(BaseModel):
    alert_id: str
    origin_worker: str
    urgency: UrgencyLevel
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "KDIGO / KDOQI Clinical Practice Guidelines"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class ConsensusDossier(BaseModel):
    dossier_id: str
    system_slug: str = "nephrolithiasis-metabolic-agent"
    domain: str = "Nephrology & Dialysis Systems"
    task_id: str
    target_identifier: str
    overall_urgency: UrgencyLevel
    integrity_status: SystemIntegrityStatus
    total_alerts: int
    critical_alerts_count: int
    alerts: List[AgentAlert]
    standard_reference: str = "KDIGO / KDOQI Clinical Practice Guidelines"
    consensus_summary: str
    audit_hash: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

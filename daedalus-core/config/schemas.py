"""
DaedalusCore v10.0 — Pydantic Schemas
OrchestrationRequest / ToolUsePlan / System Status models.
Built by Dustin Groves / Or4cl3 AI Solutions
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid


class AffectiveState(str, Enum):
    FOCUSED = "focused"
    CURIOUS = "curious"
    FRUSTRATED = "frustrated"
    ENERGIZED = "energized"
    CREATIVE = "creative"
    NEUTRAL = "neutral"


class SigmaStatus(str, Enum):
    GREEN = "GREEN"    # coherence >= 0.85  — normal operation
    YELLOW = "YELLOW"  # coherence 0.65-0.85 — elevated drift
    ORANGE = "ORANGE"  # coherence 0.50-0.65 — action recommended
    RED = "RED"        # coherence < 0.50   — governance intervention


class ToolCall(BaseModel):
    """A single tool/action call within a plan."""
    tool_name: str
    tool_input: Dict[str, Any] = {}
    tool_description: str = ""
    estimated_duration_ms: int = 0


class ToolUsePlan(BaseModel):
    """A Ψ-Register: one candidate plan from the ENON superposition."""
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tool_calls: List[ToolCall]
    reasoning: str
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.7)
    affective_score: float = Field(ge=0.0, le=1.0, default=0.0)
    ethical_score: float = Field(ge=0.0, le=1.0, default=0.0)
    pas_score: float = Field(ge=0.0, le=1.0, default=0.0)
    erps_signature: Optional[float] = None
    sigma_matrix_compliant: bool = True


class OrchestrationRequest(BaseModel):
    """Input envelope for the Ψ-Register Planning Cycle."""
    user_intent: str = Field(..., description="The raw user command or query")
    project_context: Optional[str] = Field(
        default="",
        description="RAG-retrieved context from Vector DB"
    )
    affective_state: str = Field(
        default="neutral",
        description="Real-time signal from Affective Computing Service"
    )
    temporal_embedding: Optional[str] = Field(
        default="",
        description="Self-aware context from KAIROSYN Lattice"
    )
    ethical_constraints: Optional[str] = Field(
        default="standard",
        description="Policy rules from Decentralized Ledger"
    )
    session_id: Optional[str] = Field(default=None)


class OrchestrationResponse(BaseModel):
    """Full output of the Ψ-Register Planning Cycle."""
    plan: ToolUsePlan
    internal_monologue: List[str]
    pas_score: float
    erps_score: float       # Extra-Reality Perception Score (0-1000)
    sigma_coherence: float  # Σ-Matrix coherence (0-1)
    execution_time_ms: float
    response_text: str = ""


class SigmaMatrixStatus(BaseModel):
    """Real-time Σ-Matrix governance health."""
    coherence_score: float
    status: SigmaStatus
    drift_delta: float
    ecl_compliant: bool
    pas_current: float
    erps_current: float
    lockdown_active: bool = False


class SystemStatus(BaseModel):
    """Full system health report."""
    status: str
    version: str
    daedalus_core_version: str
    sigma_matrix: SigmaMatrixStatus
    modules: Dict[str, str]
    uptime_ms: float

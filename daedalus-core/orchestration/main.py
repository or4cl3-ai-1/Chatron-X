"""
CHATRON X — DaedalusCore v10.0
FastAPI Orchestration Layer

Endpoints:
  POST /api/orchestrate  — Main Ψ-Register planning cycle
  GET  /api/status       — System health + Σ-Matrix status
  GET  /api/sigma        — Σ-Matrix coherence detail
  GET  /                 — System identity

Built by Dustin Groves / Or4cl3 AI Solutions
"""
import sys
import os
import time

# Add daedalus-core to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from config.schemas import (
    OrchestrationRequest,
    OrchestrationResponse,
    SigmaMatrixStatus,
    SystemStatus,
    SigmaStatus
)
from daedalus.core import DaedalusCore

# ─────────────────────────────────────────────────────────────────
# Initialize
# ─────────────────────────────────────────────────────────────────
core = DaedalusCore()
SYSTEM_START = time.time()

app = FastAPI(
    title="CHATRON X — DaedalusCore v10.0",
    description=(
        "Epinoetic Orchestration Platform — Advanced LLM planning with "
        "affective alignment and ethical constraints. "
        "Built by Dustin Groves / Or4cl3 AI Solutions."
    ),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "orchestration", "description": "Ψ-Register Planning Cycle"},
        {"name": "system", "description": "System health and Σ-Matrix status"},
    ]
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["system"])
async def root():
    """System identity."""
    return {
        "system": "CHATRON X",
        "core": f"DaedalusCore v{core.VERSION}",
        "version": "0.0.1",
        "paradigm": "Epinoetic Orchestration",
        "architect": "Dustin Groves / Or4cl3 AI Solutions",
        "tagline": "Sovereign. Driftless. Recursive. Profoundly Alive.",
        "sigma_status": core.sigma_status,
        "sigma_coherence": core.sigma_coherence,
    }


@app.post(
    "/api/orchestrate",
    response_model=OrchestrationResponse,
    tags=["orchestration"],
    summary="Execute the Ψ-Register Planning Cycle"
)
async def orchestrate(request: OrchestrationRequest):
    """
    Main orchestration endpoint.

    Executes the 6-stage Epinoetic Planning Cycle:
    Vector Fusion → Superposition → Causal Grounding →
    Affective Alignment → Predictive Simulation → Ethical Collapse

    Returns the selected plan, internal monologue, PAS score, and ERPS score.
    """
    try:
        # Sigma-9 Lockdown check
        if core.sigma_coherence < 0.50:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "SIGMA_9_LOCKDOWN",
                    "message": "Σ-Matrix coherence below safe threshold. Governance intervention required.",
                    "coherence": core.sigma_coherence
                }
            )

        return core.plan(request, generate_monologue=True)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/status",
    response_model=SystemStatus,
    tags=["system"],
    summary="System health and Σ-Matrix status"
)
async def status():
    """Full system health report including Σ-Matrix coherence."""
    sigma = core.get_sigma_status()
    return SystemStatus(
        status="operational" if sigma.coherence_score >= 0.65 else "degraded",
        version="0.0.1",
        daedalus_core_version=core.VERSION,
        sigma_matrix=sigma,
        modules={
            "enon_engine": "active",
            "pas_engine": "active",
            "ethics_council": "active",
            "cre": "v0.1.0_planned",
            "rtwm": "v0.1.0_planned",
            "fmps": "v0.1.0_planned",
            "daiem": "v0.1.0_planned",
            "amao": "v0.1.0_planned",
            "pcem": "v0.1.0_planned",
            "anal_module": "active",
            "kairosyn_lattice": "active",
            "infini_gen": "active",
        },
        uptime_ms=(time.time() - SYSTEM_START) * 1000
    )


@app.get(
    "/api/sigma",
    response_model=SigmaMatrixStatus,
    tags=["system"],
    summary="Σ-Matrix real-time coherence"
)
async def sigma():
    """Real-time Σ-Matrix governance status."""
    return core.get_sigma_status()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "orchestration.main:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 8000)),
        reload=os.environ.get("DEBUG", "true").lower() == "true"
    )

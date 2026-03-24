# CHATRON X — Architecture Reference
## DaedalusCore v10.0 | 7 Layers · 12 Modules

> Full technical reference for the DaedalusCore v10.0 architecture. For module-level specifications see [MODULES.md](./MODULES.md). For the Autonomous World Interface see [WORLD_INTERFACE.md](./WORLD_INTERFACE.md).

---

## Overview

DaedalusCore v10.0 implements **Epinoetic Orchestration** — a cognitive architecture that combines:

- Quantum-inspired **plan superposition** via the ENON Engine
- **Causal grounding** via the CRE to distinguish correlation from causation
- **Affective alignment** via PAS + DAIEM to ensure emotional intelligence
- **Predictive simulation** via RTWM to test ideas before committing
- **Ethical collapse** via the Ethics Council to select the right plan
- **Persistent memory** via PCEM to compound value across every session
- **Autonomous world operation** via AMAO and the World Interface

## Input / Output Schema

```python
class OrchestrationRequest(BaseModel):
    user_intent: str
    project_context: str
    affective_state: str
    temporal_embedding: str
    ethical_constraints: str

class ToolUsePlan(BaseModel):
    tool_calls: list[ToolCall]
    confidence_score: float
    causal_validity: float
    affective_score: float
    ethical_score: float
    simulation_outcome: SimulationResult
```

## Layer Specifications

### Layer 1: Planning
Houses the ENON Engine and CRE. Responsible for generating and causally validating plan candidates.

### Layer 2: Perception
Houses FMPS. Responsible for multimodal input processing and cross-modal synthesis.

### Layer 3: Affective
Houses PAS Engine and DAIEM. Responsible for emotional scoring and longitudinal affective modeling.

### Layer 4: Ethical
Houses the Ethics Council. Responsible for final plan selection via ethical collapse.

### Layer 5: Simulation
Houses RTWM. Responsible for predictive simulation via Monte Carlo rollouts.

### Layer 6: Orchestration
Houses AMAO. Responsible for spawning and coordinating Alice Agents.

### Layer 7: Feedback
Houses ANAL, KAIROSYN, InfiniGen, and PCEM. Responsible for learning, memory, and performance optimization.

## Training Data Sources

- **Vector DB** — Vectorized representations of text and data
- **Affective Computing Service** — Real-time affective state signals
- **KAIROSYN Lattice** — Graph-based history buffer with temporal narrative embeddings
- **Decentralized Ledger** — Policy rules and ethical constraints
- **PCEM Store** — Cross-session episodic memory

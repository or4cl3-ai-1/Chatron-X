"""
KAIROSYN Lattice — Feedback Layer
Graph-based Temporal Narrative Embeddings.
Maintains co-evolutionary experience for continuous learning.

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
from typing import List, Dict, Optional
from datetime import datetime
import json


class KAIROSYNLattice:
    """
    KAIROSYN Lattice — Temporal Narrative Embedding graph.

    Maintains the time-aware representation of interaction history.
    Provides temporal_embedding context back into OrchestrationRequest.
    Each node stores: timestamp, session, intent, outcome, affect_delta.
    """

    def __init__(self, max_nodes: int = 1000):
        self.nodes: List[dict] = []
        self.session_index: Dict[str, List[int]] = {}
        self.max_nodes = max_nodes

    def embed(
        self,
        session_id: str,
        intent: str,
        plan_summary: str,
        affect_delta: float,
        pas_score: float = 0.0
    ) -> str:
        """Add a Temporal Narrative Embedding to the lattice."""
        node = {
            "idx": len(self.nodes),
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "intent": intent[:200],
            "plan_summary": plan_summary[:500],
            "affect_delta": affect_delta,
            "pas_score": pas_score
        }
        self.nodes.append(node)

        if session_id not in self.session_index:
            self.session_index[session_id] = []
        self.session_index[session_id].append(node["idx"])

        # Prune if over limit
        if len(self.nodes) > self.max_nodes:
            self.nodes = self.nodes[-self.max_nodes:]

        return json.dumps({"embedded": node["idx"], "session": session_id})

    def get_context(
        self,
        session_id: str,
        limit: int = 5
    ) -> str:
        """Retrieve recent temporal context for OrchestrationRequest.temporal_embedding."""
        if session_id not in self.session_index:
            return ""

        indices = self.session_index[session_id][-limit:]
        recent = [self.nodes[i] for i in indices if i < len(self.nodes)]

        if not recent:
            return ""

        summary = [
            f"[{n['timestamp'][:10]}] {n['intent'][:80]} (PAS={n['pas_score']:.2f})"
            for n in recent
        ]
        return " | ".join(summary)

    def lattice_size(self) -> int:
        return len(self.nodes)

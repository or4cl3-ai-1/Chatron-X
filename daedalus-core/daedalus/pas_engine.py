"""
PAS Engine — Affective Layer
Applies penalties and rewards based on the user's affective state.
Implements Phase Alignment Scoring (PAS 0.0-1.0).

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
from typing import List
from config.schemas import ToolUsePlan


# Affective state → cognitive preference weights
AFFECTIVE_PROFILES = {
    "focused":    {"concise": 1.3, "direct": 1.2, "exploratory": 0.7},
    "curious":    {"exploratory": 1.3, "detailed": 1.2, "creative": 1.1},
    "frustrated": {"concise": 1.4, "direct": 1.4, "simple": 1.3},
    "energized":  {"ambitious": 1.3, "creative": 1.2, "direct": 1.1},
    "creative":   {"creative": 1.4, "exploratory": 1.2, "novel": 1.3},
    "neutral":    {"balanced": 1.0},
}


class PASEngine:
    """
    PAS Engine — Predictive Affective Scoring.
    
    Phase Alignment measures how coherently a plan integrates with
    the user's current emotional and psychological reality.
    PAS >= 0.95 is the output gate threshold (NOΣTIC-7 standard).
    """

    def weight_plans(
        self,
        plans: List[ToolUsePlan],
        affective_state: str
    ) -> List[ToolUsePlan]:
        """
        Weight Ψ-Registers based on affective state.
        Returns plans sorted by PAS score descending.
        """
        profile = AFFECTIVE_PROFILES.get(
            affective_state.lower(),
            AFFECTIVE_PROFILES["neutral"]
        )

        scored = []
        for plan in plans:
            pas = self._score_plan(plan, profile, affective_state)
            scored.append(plan.model_copy(update={
                "pas_score": pas,
                "affective_score": pas
            }))

        scored.sort(key=lambda p: p.pas_score, reverse=True)
        return scored

    def _score_plan(
        self,
        plan: ToolUsePlan,
        profile: dict,
        affective_state: str
    ) -> float:
        """
        Calculate Phase Alignment Score for a single plan.
        
        PAS = base(confidence) + affective_resonance + reasoning_depth
        """
        # Base: half the confidence score
        base = plan.confidence_score * 0.5

        # Affective resonance: match between plan structure and affective needs
        resonance = self._calculate_resonance(plan, affective_state)

        # Reasoning depth: richer reasoning = better alignment
        depth_bonus = min(len(plan.reasoning) / 2000, 0.15)

        # Tool call count alignment
        n_tools = len(plan.tool_calls)
        tool_bonus = 0.0
        if affective_state == "frustrated" and n_tools <= 2:
            tool_bonus = 0.15
        elif affective_state == "focused" and n_tools <= 3:
            tool_bonus = 0.10
        elif affective_state == "curious" and n_tools >= 3:
            tool_bonus = 0.10
        elif affective_state in ("energized", "creative"):
            tool_bonus = 0.08
        else:
            tool_bonus = 0.05

        pas = base + resonance + depth_bonus + tool_bonus
        return round(min(pas, 0.9999), 4)

    def _calculate_resonance(
        self,
        plan: ToolUsePlan,
        affective_state: str
    ) -> float:
        """Calculate how well the plan reasoning resonates with the affective state."""
        reasoning_lower = plan.reasoning.lower()
        resonance_map = {
            "focused":    ["efficient", "direct", "clear", "precise", "targeted"],
            "curious":    ["explore", "discover", "investigate", "analysis", "understand"],
            "frustrated": ["simple", "straightforward", "clear", "easy", "quick"],
            "energized":  ["ambitious", "powerful", "innovative", "build", "create"],
            "creative":   ["creative", "novel", "unique", "innovative", "imaginative"],
            "neutral":    [],
        }
        keywords = resonance_map.get(affective_state.lower(), [])
        hits = sum(1 for kw in keywords if kw in reasoning_lower)
        return min(hits * 0.03, 0.15)

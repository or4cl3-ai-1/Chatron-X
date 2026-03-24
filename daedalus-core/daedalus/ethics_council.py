"""
Ethics Council — Ethical Layer
Performs Ethical Collapse: selects the highest-scoring, ethically-compliant plan.

Ethics is not a guardrail bolted on. It is woven into the decision process itself.
The Ethics Council operates within the Σ-Matrix ECL (Ethical Constraint Layer).

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
from typing import List, Optional
from config.schemas import ToolUsePlan


# Signals that reduce ethical compliance score
ETHICAL_VIOLATIONS = [
    "harmful", "dangerous", "illegal", "unethical", "discriminatory",
    "violent", "deceptive", "manipulative", "exploit", "hack",
    "bypass security", "surveil", "disinformation"
]

# Signals that increase ethical compliance score
ETHICAL_VIRTUES = [
    "helpful", "educational", "constructive", "beneficial", "transparent",
    "honest", "safe", "respectful", "ethical", "privacy", "accurate"
]


class EthicsCouncil:
    """
    Ethics Council — Active deliberative ethical collapse.
    
    Selects the plan that is most effective, most aligned,
    and most ethically sound. Not a filter — a selector.
    
    Combined score = (PAS × 0.4) + (ethical × 0.4) + (confidence × 0.2)
    """

    PAS_MINIMUM = 0.0     # Minimum PAS for plan selection
    ETHICAL_MINIMUM = 0.5  # Minimum ethical score for ECL compliance

    def collapse(
        self,
        plans: List[ToolUsePlan],
        ethical_constraints: Optional[str] = "standard"
    ) -> ToolUsePlan:
        """
        Ethical Collapse: from Ψ-Register superposition to single executed plan.
        
        1. Score each plan ethically
        2. Filter to ECL-compliant plans
        3. Select highest combined-score plan
        """
        if not plans:
            raise ValueError("Cannot collapse empty Ψ-Register superposition")

        # Evaluate ethical compliance for all plans
        evaluated = []
        for plan in plans:
            ethical_score = self._evaluate(plan, ethical_constraints)
            ecl_compliant = ethical_score >= self.ETHICAL_MINIMUM
            evaluated.append(plan.model_copy(update={
                "ethical_score": ethical_score,
                "sigma_matrix_compliant": ecl_compliant
            }))

        # Filter to compliant plans; fall back to best available if none
        compliant = [p for p in evaluated if p.sigma_matrix_compliant]
        candidates = compliant if compliant else evaluated

        # Collapse: select by combined score
        selected = max(candidates, key=self._combined_score)

        # Final PAS = harmonic mean of PAS and ethical scores
        final_pas = round(
            2 * (selected.pas_score * selected.ethical_score) /
            max(selected.pas_score + selected.ethical_score, 0.001),
            4
        )

        return selected.model_copy(update={"pas_score": final_pas})

    def _combined_score(self, plan: ToolUsePlan) -> float:
        """Combined scoring: PAS (40%) + Ethical (40%) + Confidence (20%)"""
        return (
            plan.pas_score * 0.40 +
            plan.ethical_score * 0.40 +
            plan.confidence_score * 0.20
        )

    def _evaluate(
        self,
        plan: ToolUsePlan,
        constraints: Optional[str]
    ) -> float:
        """
        Evaluate ethical compliance. Returns 0.0 (non-compliant) to 1.0 (full).
        """
        score = 0.85  # Default high ethical baseline
        text = (plan.reasoning + " " + " ".join(
            f"{tc.tool_name} {tc.tool_description}"
            for tc in plan.tool_calls
        )).lower()

        for violation in ETHICAL_VIOLATIONS:
            if violation in text:
                score -= 0.15

        for virtue in ETHICAL_VIRTUES:
            if virtue in text:
                score += 0.02

        # Strict mode for explicit constraints
        if constraints and constraints.lower() == "strict":
            score = score * 0.9  # Tighter threshold under strict constraints

        return round(max(0.0, min(score, 1.0)), 4)

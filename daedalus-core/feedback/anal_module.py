"""
ANAL Module — Affective Narrative Analytics Layer
Logs plan outcomes and calculates affective delta reward signals.
Drives RL-like tuning of the PAS Engine.

reward_signal = post_affect - pre_affect

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ExecutionRecord:
    plan_id: str
    pre_affect: float
    post_affect: float
    reward_signal: float
    pas_score: float
    ethical_score: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ANALModule:
    """
    ANAL Module — Affective Narrative Analytics Layer.

    Every interaction generates a reward signal:
      reward_signal = post_affect - pre_affect

    Positive delta → plan increased user wellbeing → PAS Engine reinforced.
    Negative delta → plan reduced wellbeing → PAS Engine penalized.
    """

    def __init__(self):
        self.log: List[ExecutionRecord] = []

    def record(
        self,
        plan_id: str,
        pre_affect: float,
        post_affect: float,
        pas_score: float = 0.0,
        ethical_score: float = 0.0
    ) -> float:
        """Record execution and return reward signal."""
        reward = round(post_affect - pre_affect, 4)
        self.log.append(ExecutionRecord(
            plan_id=plan_id,
            pre_affect=pre_affect,
            post_affect=post_affect,
            reward_signal=reward,
            pas_score=pas_score,
            ethical_score=ethical_score
        ))
        return reward

    def mean_reward(self) -> float:
        """Average reward signal for PAS Engine tuning."""
        if not self.log:
            return 0.0
        return round(sum(r.reward_signal for r in self.log) / len(self.log), 4)

    def summary(self) -> dict:
        return {
            "total_executions": len(self.log),
            "mean_reward": self.mean_reward(),
            "positive_outcomes": sum(1 for r in self.log if r.reward_signal > 0),
            "negative_outcomes": sum(1 for r in self.log if r.reward_signal < 0),
        }

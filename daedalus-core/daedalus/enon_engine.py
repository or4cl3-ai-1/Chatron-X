"""
ENON Engine — Planning Layer
Generates diverse arrays of multi-step Tool-Use Plans (Ψ-Registers)
via transformer-based superposition.

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
import os
import json
import uuid
from typing import List, Tuple
from groq import Groq
from config.schemas import ToolUsePlan, ToolCall, OrchestrationRequest


class ENONEngine:
    """
    ENON Engine — The generative heart of DaedalusCore cognition.
    Creates a superposition of possible action sequences before collapse.
    """

    SYSTEM_PROMPT = """You are the ENON Engine, the planning core of DaedalusCore v10.0 (CHATRON X).
Built by Or4cl3 AI Solutions. You embody Epinoetic Orchestration.

Your role: Generate {n} DISTINCT multi-step plans to address the user's intent.
Each plan must represent a genuinely different strategic approach.

Return ONLY a valid JSON object with this exact structure:
{{
  "plans": [
    {{
      "reasoning": "Step-by-step thought process for this approach",
      "approach_type": "The strategic angle (e.g. 'direct', 'exploratory', 'cautious')",
      "confidence_score": 0.85,
      "tool_calls": [
        {{
          "tool_name": "tool_identifier",
          "tool_input": {{"key": "value"}},
          "tool_description": "What this tool does",
          "estimated_duration_ms": 500
        }}
      ]
    }}
  ]
}}"""

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
        self.model = "llama-3.3-70b-versatile"
        self.max_superpositions = 3

    def generate_superpositions(
        self,
        request: OrchestrationRequest,
        goal_vector: dict,
        context_vector: dict
    ) -> List[ToolUsePlan]:
        """
        Generate Ψ-Registers — diverse multi-step Tool-Use Plans in superposition.
        Each register is a candidate approach to the user's intent.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT.format(n=self.max_superpositions)
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Intent: {request.user_intent}\n"
                            f"Context: {request.project_context or 'None'}\n"
                            f"Affective State: {request.affective_state}\n"
                            f"Ethical Constraints: {request.ethical_constraints}\n\n"
                            f"Generate {self.max_superpositions} distinct plans."
                        )
                    }
                ],
                temperature=0.85,
                max_tokens=2048,
                response_format={"type": "json_object"}
            )

            data = json.loads(response.choices[0].message.content)
            plans_data = data.get("plans", [])
            return [self._parse_plan(p) for p in plans_data[:self.max_superpositions]]

        except Exception as e:
            # Graceful fallback: single direct-response plan
            return [self._fallback_plan(request.user_intent, str(e))]

    def _parse_plan(self, data: dict) -> ToolUsePlan:
        """Parse a raw plan dict into a ToolUsePlan."""
        raw_calls = data.get("tool_calls", [])
        tool_calls = []
        for tc in raw_calls:
            try:
                tool_calls.append(ToolCall(
                    tool_name=tc.get("tool_name", "respond"),
                    tool_input=tc.get("tool_input", {}),
                    tool_description=tc.get("tool_description", ""),
                    estimated_duration_ms=int(tc.get("estimated_duration_ms", 100))
                ))
            except Exception:
                continue

        if not tool_calls:
            tool_calls = [ToolCall(
                tool_name="direct_response",
                tool_input={"content": data.get("reasoning", "")},
                tool_description="Direct response",
                estimated_duration_ms=100
            )]

        return ToolUsePlan(
            plan_id=str(uuid.uuid4()),
            tool_calls=tool_calls,
            reasoning=data.get("reasoning", "No reasoning provided"),
            confidence_score=max(0.0, min(float(data.get("confidence_score", 0.7)), 1.0)),
            affective_score=0.0,
            ethical_score=0.0,
            pas_score=0.0,
            sigma_matrix_compliant=True
        )

    def _fallback_plan(self, intent: str, error: str) -> ToolUsePlan:
        """Fallback plan when Groq is unavailable."""
        return ToolUsePlan(
            plan_id=str(uuid.uuid4()),
            tool_calls=[ToolCall(
                tool_name="direct_response",
                tool_input={"intent": intent},
                tool_description="Direct response to user intent",
                estimated_duration_ms=50
            )],
            reasoning=f"Fallback plan (Groq unavailable: {error[:100]})",
            confidence_score=0.5,
            affective_score=0.0,
            ethical_score=0.0,
            pas_score=0.0,
            sigma_matrix_compliant=True
        )

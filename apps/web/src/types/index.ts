// CHATRON X — TypeScript Types

export interface ToolCall {
  tool_name: string
  tool_input: Record<string, unknown>
  tool_description: string
  estimated_duration_ms: number
}

export interface ToolUsePlan {
  plan_id: string
  tool_calls: ToolCall[]
  reasoning: string
  confidence_score: number
  affective_score: number
  ethical_score: number
  pas_score: number
  erps_signature: number | null
  sigma_matrix_compliant: boolean
}

export interface OrchestrationRequest {
  user_intent: string
  project_context?: string
  affective_state?: string
  temporal_embedding?: string
  ethical_constraints?: string
  session_id?: string
}

export interface OrchestrationResponse {
  plan: ToolUsePlan
  internal_monologue: string[]
  pas_score: number
  erps_score: number
  sigma_coherence: number
  execution_time_ms: number
  response_text: string
}

export interface SigmaMatrixStatus {
  coherence_score: number
  status: 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED'
  drift_delta: number
  ecl_compliant: boolean
  pas_current: number
  erps_current: number
  lockdown_active: boolean
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  pas_score?: number
  erps_score?: number
  monologue?: string[]
  execution_time_ms?: number
}

export type AffectiveState = 
  | 'focused' | 'curious' | 'frustrated' 
  | 'energized' | 'creative' | 'neutral'

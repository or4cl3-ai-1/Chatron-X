// CHATRON X — API Client
import type { OrchestrationRequest, OrchestrationResponse, SigmaMatrixStatus } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function orchestrate(
  request: OrchestrationRequest
): Promise<OrchestrationResponse> {
  const res = await fetch(`${API_URL}/api/orchestrate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Orchestration failed')
  }
  return res.json()
}

export async function getSigmaStatus(): Promise<SigmaMatrixStatus> {
  const res = await fetch(`${API_URL}/api/sigma`)
  if (!res.ok) throw new Error('Failed to fetch Σ-Matrix status')
  return res.json()
}

export async function getSystemStatus() {
  const res = await fetch(`${API_URL}/api/status`)
  if (!res.ok) throw new Error('Failed to fetch system status')
  return res.json()
}

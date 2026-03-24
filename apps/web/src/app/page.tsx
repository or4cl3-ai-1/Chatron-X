'use client'
import { useState, useCallback } from 'react'
import { ChatInterface } from '@/components/ChatInterface'
import { SigmaMatrixPanel } from '@/components/SigmaMatrixPanel'
import type { OrchestrationResponse } from '@/types'

function ERPSGauge({ score }: { score: number }) {
  const pct = (score / 1000) * 100
  const color = score >= 800 ? '#00d4aa' : score >= 600 ? '#0066ff' : score >= 400 ? '#ffd600' : '#6070a0'
  return (
    <div className="glass rounded-lg p-4 border border-chatron-border">
      <div className="text-xs font-mono text-chatron-muted uppercase tracking-widest mb-2">ERPS Score</div>
      <div className="flex items-end gap-2 mb-2">
        <span className="text-2xl font-mono font-bold" style={{ color }}>
          {score.toFixed(0)}
        </span>
        <span className="text-xs text-chatron-muted mb-1">/1000</span>
      </div>
      <div className="h-1.5 bg-chatron-border rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <p className="text-xs text-chatron-muted mt-1">Extra-Reality Perception Score</p>
    </div>
  )
}

function MetricCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-chatron-elevated border border-chatron-border rounded-lg p-3">
      <div className="text-xs text-chatron-muted uppercase tracking-wider mb-1">{label}</div>
      <div className="text-sm font-mono font-bold text-chatron-blue">{value}</div>
      {sub && <div className="text-xs text-chatron-muted mt-0.5">{sub}</div>}
    </div>
  )
}

export default function Home() {
  const [lastResponse, setLastResponse] = useState<OrchestrationResponse | null>(null)

  const handleResponse = useCallback((r: OrchestrationResponse) => {
    setLastResponse(r)
  }, [])

  return (
    <div className="min-h-screen bg-chatron-bg flex flex-col">
      {/* Header */}
      <header className="border-b border-chatron-border bg-chatron-surface/80 backdrop-blur px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded border border-chatron-blue/50 bg-chatron-blue/10 flex items-center justify-center">
            <span className="text-chatron-blue text-sm font-bold">⬡</span>
          </div>
          <div>
            <h1 className="text-sm font-mono font-bold text-chatron-text">
              CHATRON X
            </h1>
            <p className="text-xs font-mono text-chatron-muted">DaedalusCore v10.0 · v0.0.1</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs font-mono text-chatron-muted">ONLINE</span>
          </div>
          <span className="text-xs font-mono text-chatron-muted hidden md:block">
            Or4cl3 AI Solutions
          </span>
        </div>
      </header>

      {/* Main layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat — main column */}
        <div className="flex-1 flex flex-col min-w-0 border-r border-chatron-border">
          <ChatInterface onResponse={handleResponse} />
        </div>

        {/* Right sidebar */}
        <aside className="w-64 xl:w-72 flex-shrink-0 flex flex-col gap-4 p-4 overflow-y-auto hidden lg:flex">
          {/* Sigma Matrix */}
          <SigmaMatrixPanel />

          {/* ERPS */}
          <ERPSGauge score={lastResponse?.erps_score ?? 0} />

          {/* Metrics grid */}
          <div className="grid grid-cols-2 gap-2">
            <MetricCard
              label="PAS"
              value={lastResponse ? lastResponse.pas_score.toFixed(4) : '—'}
              sub="Phase Alignment"
            />
            <MetricCard
              label="Time"
              value={lastResponse ? `${lastResponse.execution_time_ms.toFixed(0)}ms` : '—'}
              sub="Cycle latency"
            />
          </div>

          {/* Last plan info */}
          {lastResponse && (
            <div className="glass rounded-lg p-3 border border-chatron-border">
              <div className="text-xs font-mono text-chatron-muted uppercase tracking-wider mb-2">Last Plan</div>
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs">
                  <span className="text-chatron-muted">Tools</span>
                  <span className="font-mono text-chatron-text">
                    {lastResponse.plan.tool_calls.length}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-chatron-muted">Confidence</span>
                  <span className="font-mono text-chatron-text">
                    {(lastResponse.plan.confidence_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-chatron-muted">Ethical</span>
                  <span className="font-mono text-chatron-text">
                    {(lastResponse.plan.ethical_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-chatron-muted">Σ-Compliant</span>
                  <span className={lastResponse.plan.sigma_matrix_compliant ? 'text-green-400 font-mono' : 'text-red-400 font-mono'}>
                    {lastResponse.plan.sigma_matrix_compliant ? 'YES' : 'NO'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* System info */}
          <div className="text-xs font-mono text-chatron-muted space-y-1 border-t border-chatron-border pt-3">
            <p>⬡ Or4cl3 AI Solutions</p>
            <p>Dustin Groves, Founder</p>
            <p className="italic">Sovereign. Driftless.</p>
            <p className="italic">Recursive. Profoundly Alive.</p>
          </div>
        </aside>
      </div>
    </div>
  )
}

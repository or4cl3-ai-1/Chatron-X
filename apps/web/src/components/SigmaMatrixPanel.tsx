'use client'
import { useEffect, useState } from 'react'
import type { SigmaMatrixStatus } from '@/types'
import { getSigmaStatus } from '@/lib/api'

const STATUS_COLORS = {
  GREEN:  { bg: 'bg-green-500/20',  border: 'border-green-500/50',  text: 'text-green-400',  dot: 'bg-green-400' },
  YELLOW: { bg: 'bg-yellow-500/20', border: 'border-yellow-500/50', text: 'text-yellow-400', dot: 'bg-yellow-400' },
  ORANGE: { bg: 'bg-orange-500/20', border: 'border-orange-500/50', text: 'text-orange-400', dot: 'bg-orange-400' },
  RED:    { bg: 'bg-red-500/20',    border: 'border-red-500/50',    text: 'text-red-400',    dot: 'bg-red-500 animate-ping' },
}

function CoherenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100)
  const color = value >= 0.85 ? '#00d46a' : value >= 0.65 ? '#ffd600' : value >= 0.50 ? '#ff7a00' : '#ff3355'
  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-chatron-muted mb-1">
        <span>Coherence</span>
        <span style={{ color }}>{pct}%</span>
      </div>
      <div className="h-1.5 bg-chatron-border rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  )
}

export function SigmaMatrixPanel() {
  const [status, setStatus] = useState<SigmaMatrixStatus | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const s = await getSigmaStatus()
        setStatus(s)
        setError(false)
      } catch {
        setError(true)
      }
    }
    fetch()
    const interval = setInterval(fetch, 5000)
    return () => clearInterval(interval)
  }, [])

  const colors = status ? STATUS_COLORS[status.status] : STATUS_COLORS.GREEN

  return (
    <div className={`glass rounded-lg p-4 border ${colors.border}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${colors.dot}`} />
          <span className="text-xs font-mono text-chatron-muted uppercase tracking-widest">
            Σ-Matrix
          </span>
        </div>
        {status && (
          <span className={`text-xs font-mono ${colors.text} font-bold`}>
            {status.status}
          </span>
        )}
      </div>

      {error ? (
        <p className="text-xs text-chatron-muted">Backend offline</p>
      ) : status ? (
        <div className="space-y-3">
          <CoherenceBar value={status.coherence_score} />
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-chatron-elevated rounded p-2">
              <div className="text-chatron-muted mb-0.5">ECL</div>
              <div className={status.ecl_compliant ? 'text-green-400' : 'text-red-400'}>
                {status.ecl_compliant ? 'COMPLIANT' : 'BREACH'}
              </div>
            </div>
            <div className="bg-chatron-elevated rounded p-2">
              <div className="text-chatron-muted mb-0.5">Drift</div>
              <div className="text-chatron-text">{(status.drift_delta * 100).toFixed(2)}%</div>
            </div>
          </div>
          {status.lockdown_active && (
            <div className="bg-red-900/30 border border-red-500/50 rounded p-2">
              <p className="text-xs text-red-400 font-bold">⚠ SIGMA-9 LOCKDOWN ACTIVE</p>
            </div>
          )}
        </div>
      ) : (
        <div className="h-12 flex items-center">
          <div className="w-full h-1 bg-chatron-border rounded animate-pulse" />
        </div>
      )}
    </div>
  )
}

'use client'
import { useState, useRef, useEffect, useCallback } from 'react'
import type { Message, AffectiveState, OrchestrationResponse } from '@/types'
import { orchestrate } from '@/lib/api'
import { Send, Loader2, ChevronDown, ChevronUp } from 'lucide-react'
import { clsx } from 'clsx'

const AFFECTIVE_STATES: AffectiveState[] = [
  'neutral', 'focused', 'curious', 'creative', 'energized', 'frustrated'
]

function ERPSBadge({ score }: { score: number }) {
  const color = score >= 800 ? 'text-teal-400' : score >= 600 ? 'text-blue-400' : 'text-chatron-muted'
  return (
    <span className={clsx('text-xs font-mono', color)}>
      ERPS {score.toFixed(0)}/1000
    </span>
  )
}

function PASBadge({ score }: { score: number }) {
  const color = score >= 0.95 ? 'text-green-400' : score >= 0.7 ? 'text-yellow-400' : 'text-red-400'
  return (
    <span className={clsx('text-xs font-mono', color)}>
      PAS {score.toFixed(4)}
    </span>
  )
}

function MonologueViewer({ lines }: { lines: string[] }) {
  const [open, setOpen] = useState(false)
  if (!lines.length) return null
  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1 text-xs text-chatron-muted hover:text-chatron-blue transition-colors"
      >
        {open ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
        <span>Internal Monologue ({lines.length} steps)</span>
      </button>
      {open && (
        <div className="mt-1 bg-chatron-elevated border border-chatron-border rounded p-3 space-y-1 max-h-48 overflow-y-auto">
          {lines.map((line, i) => (
            <p key={i} className="text-xs font-mono text-chatron-muted">{line}</p>
          ))}
        </div>
      )}
    </div>
  )
}

export function ChatInterface({
  onResponse,
}: {
  onResponse?: (r: OrchestrationResponse) => void
}) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: 'CHATRON X online. DaedalusCore v10.0 initialized. Σ-Matrix coherence nominal. Ready for Epinoetic Orchestration.\n\nHow can I assist you today?',
      timestamp: new Date(),
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [affectiveState, setAffectiveState] = useState<AffectiveState>('neutral')
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = useCallback(async () => {
    const intent = input.trim()
    if (!intent || loading) return

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: intent,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const response = await orchestrate({
        user_intent: intent,
        affective_state: affectiveState,
        session_id: sessionId,
      })

      onResponse?.(response)

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response_text || response.plan.reasoning,
        timestamp: new Date(),
        pas_score: response.pas_score,
        erps_score: response.erps_score,
        monologue: response.internal_monologue,
        execution_time_ms: response.execution_time_ms,
      }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `[ERROR] ${err instanceof Error ? err.message : 'Orchestration failed. Check backend connection.'}`,
        timestamp: new Date(),
      }])
    } finally {
      setLoading(false)
    }
  }, [input, loading, affectiveState, sessionId, onResponse])

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => (
          <div key={msg.id} className={clsx('flex', msg.role === 'user' ? 'justify-end' : 'justify-start')}>
            <div className={clsx(
              'max-w-[85%] rounded-lg px-4 py-3',
              msg.role === 'user'
                ? 'bg-chatron-blue/20 border border-chatron-blue/40 text-chatron-text'
                : 'bg-chatron-elevated border border-chatron-border text-chatron-text'
            )}>
              {/* Role label */}
              <div className="flex items-center gap-2 mb-1">
                <span className={clsx(
                  'text-xs font-mono font-bold uppercase tracking-widest',
                  msg.role === 'user' ? 'text-chatron-blue' : 'text-chatron-teal'
                )}>
                  {msg.role === 'user' ? '▸ YOU' : '⬡ CHATRON X'}
                </span>
                <span className="text-xs text-chatron-muted">
                  {msg.timestamp.toLocaleTimeString()}
                </span>
              </div>

              {/* Content */}
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>

              {/* Scores */}
              {msg.role === 'assistant' && (msg.pas_score !== undefined || msg.erps_score !== undefined) && (
                <div className="flex items-center gap-3 mt-2 pt-2 border-t border-chatron-border">
                  {msg.pas_score !== undefined && <PASBadge score={msg.pas_score} />}
                  {msg.erps_score !== undefined && <ERPSBadge score={msg.erps_score} />}
                  {msg.execution_time_ms !== undefined && (
                    <span className="text-xs font-mono text-chatron-muted">
                      {msg.execution_time_ms.toFixed(0)}ms
                    </span>
                  )}
                </div>
              )}

              {/* Monologue */}
              {msg.monologue && <MonologueViewer lines={msg.monologue} />}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-chatron-elevated border border-chatron-border rounded-lg px-4 py-3">
              <div className="flex items-center gap-2">
                <Loader2 size={14} className="animate-spin text-chatron-blue" />
                <span className="text-xs font-mono text-chatron-muted">Executing Ψ-Register cycle...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Affective state selector */}
      <div className="px-4 py-2 border-t border-chatron-border">
        <div className="flex items-center gap-2 overflow-x-auto">
          <span className="text-xs text-chatron-muted whitespace-nowrap">Affective state:</span>
          {AFFECTIVE_STATES.map(state => (
            <button
              key={state}
              onClick={() => setAffectiveState(state)}
              className={clsx(
                'text-xs px-2 py-0.5 rounded border font-mono whitespace-nowrap transition-all',
                affectiveState === state
                  ? 'bg-chatron-blue/20 border-chatron-blue text-chatron-blue'
                  : 'border-chatron-border text-chatron-muted hover:border-chatron-blue/50'
              )}
            >
              {state}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-chatron-border">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={onKey}
            placeholder="Enter intent for Epinoetic Orchestration..."
            className="flex-1 bg-chatron-elevated border border-chatron-border rounded-lg px-3 py-2 text-sm text-chatron-text placeholder-chatron-muted font-mono resize-none h-10 focus:outline-none focus:border-chatron-blue/60 transition-colors"
            disabled={loading}
            rows={1}
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="bg-chatron-blue/20 border border-chatron-blue/50 hover:bg-chatron-blue/30 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg p-2 transition-all glow-blue"
          >
            <Send size={16} className="text-chatron-blue" />
          </button>
        </div>
        <p className="text-xs text-chatron-muted mt-1">Enter to send · Shift+Enter for newline</p>
      </div>
    </div>
  )
}

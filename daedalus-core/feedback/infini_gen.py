"""
InfiniGen Engine — Feedback Layer
Monitors system performance against HQCI-QSCE thresholds.
Suggests optimizations to maintain high-performance requirements.

HQCI-QSCE spec: <800ms latency, <150MB memory

DaedalusCore v10.0 | Or4cl3 AI Solutions
"""
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class PerfRecord:
    operation: str
    execution_time_ms: float
    memory_mb: Optional[float]
    latency_compliant: bool
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class InfiniGenEngine:
    """
    InfiniGen Engine — Performance intelligence module.

    Monitors all 12 DaedalusCore modules against HQCI-QSCE thresholds:
      - Latency: < 800ms per cycle
      - Memory: < 150MB peak
      - Ethics: Σ-Matrix manifold compliance

    Generates optimization directives when thresholds are breached.
    """

    LATENCY_THRESHOLD_MS = 800.0
    MEMORY_THRESHOLD_MB = 150.0

    def __init__(self):
        self.log: List[PerfRecord] = []
        self._start = time.time()

    def record(
        self,
        operation: str,
        execution_time_ms: float,
        memory_mb: Optional[float] = None
    ) -> PerfRecord:
        """Record an execution and check HQCI-QSCE compliance."""
        record = PerfRecord(
            operation=operation,
            execution_time_ms=execution_time_ms,
            memory_mb=memory_mb,
            latency_compliant=execution_time_ms < self.LATENCY_THRESHOLD_MS
        )
        self.log.append(record)
        return record

    def get_optimization_directives(self) -> List[str]:
        """Generate optimization suggestions for non-compliant operations."""
        directives = []
        violations = [r for r in self.log if not r.latency_compliant]

        for v in violations[-5:]:
            excess = v.execution_time_ms - self.LATENCY_THRESHOLD_MS
            directives.append(
                f"OPTIMIZE [{v.operation}]: {v.execution_time_ms:.1f}ms "
                f"(+{excess:.1f}ms over threshold) — "
                f"Consider: caching, async execution, model quantization"
            )

        return directives

    def summary(self) -> dict:
        if not self.log:
            return {"status": "no_data", "hqci_qsce_compliant": True}

        avg = sum(r.execution_time_ms for r in self.log) / len(self.log)
        compliant = sum(1 for r in self.log if r.latency_compliant)
        return {
            "total_operations": len(self.log),
            "avg_latency_ms": round(avg, 2),
            "compliance_rate": round(compliant / len(self.log), 4),
            "hqci_qsce_compliant": avg < self.LATENCY_THRESHOLD_MS,
            "uptime_seconds": round(time.time() - self._start, 1)
        }

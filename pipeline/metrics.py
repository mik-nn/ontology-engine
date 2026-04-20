"""Pipeline quality metrics — collected during a run, reported at end."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMCallRecord:
    role: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    elapsed_s: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class PipelineMetrics:
    # Classification
    task_type: str = ""
    classification_confidence: float = 0.0
    classification_mode: str = ""
    matched_entities: int = 0

    # SHACL / graph quality
    shacl_violations: int = 0
    shacl_warnings: int = 0
    graph_triples: int = 0

    # Planning
    subtask_count: int = 0
    subtasks_with_entity_match: int = 0

    # Execution
    stubs_total: int = 0
    stubs_resolved: int = 0
    llm_calls: list[LLMCallRecord] = field(default_factory=list)

    # Timing
    stage_times: dict[str, float] = field(default_factory=dict)
    _stage_start: float = field(default=0.0, repr=False)
    _run_start: float = field(default_factory=time.monotonic, repr=False)

    def begin_stage(self, name: str) -> None:
        self._stage_start = time.monotonic()

    def end_stage(self, name: str) -> None:
        self.stage_times[name] = round(time.monotonic() - self._stage_start, 2)

    @property
    def wall_time(self) -> float:
        return round(time.monotonic() - self._run_start, 2)

    @property
    def plan_fidelity(self) -> float:
        if not self.subtask_count:
            return 1.0
        return round(self.subtasks_with_entity_match / self.subtask_count, 3)

    @property
    def stub_resolution_rate(self) -> Optional[float]:
        if not self.stubs_total:
            return None
        return round(self.stubs_resolved / self.stubs_total, 3)

    @property
    def total_tokens(self) -> int:
        return sum(c.total_tokens for c in self.llm_calls)

    @property
    def token_efficiency(self) -> Optional[float]:
        if not self.total_tokens or not self.stubs_resolved:
            return None
        return round(self.total_tokens / self.stubs_resolved, 1)

    def print_report(self) -> None:
        try:
            from rich.console import Console
        except ImportError:
            self._print_plain()
            return
        console = Console()
        console.print()
        console.rule("[bold blue]Pipeline Quality Metrics[/bold blue]")

        if self.task_type:
            c = "green" if self.classification_confidence >= 0.7 else (
                "yellow" if self.classification_confidence >= 0.45 else "red")
            console.print(
                f"  [bold]Classification[/bold]  {self.task_type}  "
                f"conf=[{c}]{self.classification_confidence:.2f}[/{c}]  "
                f"mode={self.classification_mode}  "
                f"entities={self.matched_entities}"
            )

        shacl_ok = self.shacl_violations == 0
        icon = "[green]✓[/green]" if shacl_ok else "[red]✗[/red]"
        console.print(
            f"  [bold]SHACL[/bold]           {icon}  "
            f"violations={self.shacl_violations}  "
            f"warnings={self.shacl_warnings}  "
            f"triples={self.graph_triples}"
        )

        if self.subtask_count:
            fc = "green" if self.plan_fidelity >= 0.8 else (
                "yellow" if self.plan_fidelity >= 0.5 else "red")
            console.print(
                f"  [bold]Plan fidelity[/bold]   [{fc}]"
                f"{self.subtasks_with_entity_match}/{self.subtask_count}[/{fc}] "
                f"subtasks matched to ontology entities  "
                f"({self.plan_fidelity:.0%})"
            )

        if self.stubs_total:
            rate = self.stub_resolution_rate
            rs = f"{rate:.0%}" if rate is not None else "n/a"
            console.print(
                f"  [bold]Stub resolution[/bold]  "
                f"{self.stubs_resolved}/{self.stubs_total} ({rs})"
            )

        for call in self.llm_calls:
            eff = ""
            if self.stubs_resolved and call.total_tokens:
                eff = f"  [{call.total_tokens // self.stubs_resolved} tok/stub]"
            console.print(
                f"  [bold]LLM[/bold] [[dim]{call.role:10}[/dim]]  "
                f"{call.provider}/{call.model}  "
                f"in={call.input_tokens} out={call.output_tokens}{eff}  "
                f"{call.elapsed_s:.1f}s"
            )

        if self.stage_times:
            parts = "  ".join(f"{k}={v}s" for k, v in self.stage_times.items())
            console.print(f"  [bold]Stages[/bold]          {parts}")

        console.print(f"  [bold]Wall time[/bold]       {self.wall_time}s")
        console.rule()

    def _print_plain(self) -> None:
        print("\n── Pipeline Metrics " + "─" * 40)
        print(f"  task        : {self.task_type} (conf={self.classification_confidence:.2f}, mode={self.classification_mode})")
        print(f"  shacl       : violations={self.shacl_violations} warnings={self.shacl_warnings} triples={self.graph_triples}")
        if self.subtask_count:
            print(f"  plan fidelity: {self.subtasks_with_entity_match}/{self.subtask_count} ({self.plan_fidelity:.0%})")
        if self.stubs_total:
            print(f"  stubs       : {self.stubs_resolved}/{self.stubs_total}")
        for c in self.llm_calls:
            print(f"  llm [{c.role}]: {c.provider}/{c.model}  in={c.input_tokens} out={c.output_tokens}  {c.elapsed_s:.1f}s")
        print(f"  wall time   : {self.wall_time}s")
        print("─" * 60)

    def emit_rdf(self, store, logger) -> None:
        """Write metrics summary as an RDF event for historical querying."""
        try:
            logger.log(
                "PipelineMetricsRecorded",
                agent="PipelineOrchestrator",
                status="completed",
                taskType=self.task_type,
                classificationConfidence=f"{self.classification_confidence:.3f}",
                classificationMode=self.classification_mode,
                shaclViolations=str(self.shacl_violations),
                shaclWarnings=str(self.shacl_warnings),
                graphTriples=str(self.graph_triples),
                planFidelity=f"{self.plan_fidelity:.3f}",
                stubsTotal=str(self.stubs_total),
                stubsResolved=str(self.stubs_resolved),
                totalTokens=str(self.total_tokens),
                wallTime=f"{self.wall_time:.2f}",
            )
        except Exception:
            pass

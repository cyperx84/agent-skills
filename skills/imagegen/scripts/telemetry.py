"""Optional telemetry for tracking metrics, costs, and performance.

This module provides infrastructure for collecting usage metrics, tracking
costs, and monitoring performance. All telemetry is optional and disabled
by default to maintain zero overhead when not needed.

Examples:
    >>> collector = TelemetryCollector(enabled=True)
    >>> metric = collector.track_generation(
    ...     provider="google",
    ...     model="gemini-2.5-flash-image",
    ...     operation="generate",
    ...     prompt="a sunset"
    ... )
    >>> summary = collector.get_summary()
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class GenerationMetrics:
    """Metrics for a single image generation operation.

    Attributes:
        provider: Provider name (e.g., "google", "openai")
        model: Model identifier (e.g., "gemini-2.5-flash-image")
        operation: Operation type ("generate" or "edit")
        prompt: Text prompt used for generation
        timestamp: When the operation started
        duration_ms: Operation duration in milliseconds
        success: Whether the operation succeeded
        error: Error message if operation failed
        estimated_cost: Estimated cost in USD (future implementation)
        resolution: Image resolution (e.g., "1024x1024")
        aspect_ratio: Image aspect ratio (e.g., "16:9")
        num_input_images: Number of input images for editing operations
    """

    provider: str
    model: str
    operation: str  # "generate" or "edit"
    prompt: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: Optional[float] = None
    success: bool = True
    error: Optional[str] = None

    # Cost tracking (for future implementation)
    estimated_cost: Optional[float] = None

    # Quality/technical metrics
    resolution: Optional[str] = None
    aspect_ratio: Optional[str] = None
    num_input_images: int = 0

    def to_dict(self) -> dict:
        """Convert metrics to dictionary with JSON-serializable types.

        Returns:
            dict: Metrics as dictionary with ISO format timestamp
        """
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


class TelemetryCollector:
    """Collect and optionally persist telemetry data.

    The collector maintains a list of metrics and can optionally persist
    them to disk. When disabled, all operations are no-ops with minimal
    overhead.

    Args:
        enabled: Whether to collect telemetry (default: False)
        output_path: Optional path to persist metrics as JSON lines

    Examples:
        >>> # Enabled collector with persistence
        >>> collector = TelemetryCollector(
        ...     enabled=True,
        ...     output_path=Path("metrics.jsonl")
        ... )
        >>>
        >>> # Disabled collector (zero overhead)
        >>> collector = TelemetryCollector(enabled=False)
    """

    def __init__(self, enabled: bool = False, output_path: Optional[Path] = None):
        """Initialize telemetry collector.

        Args:
            enabled: Whether to collect telemetry
            output_path: Path to persist metrics (JSON lines format)
        """
        self.enabled = enabled
        self.output_path = output_path
        self.metrics: list[GenerationMetrics] = []

        # Ensure output directory exists if persistence enabled
        if self.output_path and self.enabled:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def track_generation(
        self, provider: str, model: str, operation: str, prompt: str, **kwargs
    ) -> GenerationMetrics:
        """Track an image generation operation.

        Records metrics for a generation or editing operation. If telemetry
        is disabled, creates the metric object but doesn't store or persist it.

        Args:
            provider: Provider name
            model: Model identifier
            operation: "generate" or "edit"
            prompt: Text prompt used
            **kwargs: Additional metric fields (duration_ms, success, error, etc.)

        Returns:
            GenerationMetrics: The recorded metric

        Examples:
            >>> metric = collector.track_generation(
            ...     provider="google",
            ...     model="gemini-2.5-flash-image",
            ...     operation="generate",
            ...     prompt="a cyberpunk robot",
            ...     duration_ms=2340.5,
            ...     success=True,
            ...     resolution="1024x1024",
            ...     aspect_ratio="1:1"
            ... )
        """
        metric = GenerationMetrics(
            provider=provider, model=model, operation=operation, prompt=prompt, **kwargs
        )

        if self.enabled:
            self.metrics.append(metric)

            if self.output_path:
                self._persist(metric)

        return metric

    def _persist(self, metric: GenerationMetrics) -> None:
        """Persist a single metric to disk.

        Appends the metric as a JSON line to the output file.
        Future enhancement: Could support other formats or databases.

        Args:
            metric: Metric to persist
        """
        try:
            with open(self.output_path, "a") as f:
                json.dump(metric.to_dict(), f)
                f.write("\n")
        except Exception as e:
            # Don't fail the main operation if telemetry fails
            print(f"Warning: Failed to persist telemetry: {e}")

    def get_summary(self) -> dict:
        """Get summary statistics of collected metrics.

        Aggregates metrics by provider, operation type, and success/failure.
        Returns empty summary if no metrics collected.

        Returns:
            dict: Summary with keys:
                - total: Total operations
                - successful: Number of successful operations
                - failed: Number of failed operations
                - by_provider: Operations count per provider
                - by_operation: Operations count per operation type
                - total_duration_ms: Total duration across all operations
                - avg_duration_ms: Average duration per operation

        Examples:
            >>> summary = collector.get_summary()
            >>> print(f"Generated {summary['total']} images")
            >>> print(f"Success rate: {summary['successful'] / summary['total']:.1%}")
        """
        if not self.metrics:
            return {"total": 0}

        successful = sum(1 for m in self.metrics if m.success)
        failed = len(self.metrics) - successful

        # Group by provider
        by_provider = {}
        for metric in self.metrics:
            if metric.provider not in by_provider:
                by_provider[metric.provider] = 0
            by_provider[metric.provider] += 1

        # Group by operation
        by_operation = {}
        for metric in self.metrics:
            if metric.operation not in by_operation:
                by_operation[metric.operation] = 0
            by_operation[metric.operation] += 1

        # Calculate durations
        durations = [m.duration_ms for m in self.metrics if m.duration_ms is not None]
        total_duration = sum(durations) if durations else 0
        avg_duration = total_duration / len(durations) if durations else 0

        return {
            "total": len(self.metrics),
            "successful": successful,
            "failed": failed,
            "by_provider": by_provider,
            "by_operation": by_operation,
            "total_duration_ms": total_duration,
            "avg_duration_ms": avg_duration,
        }

    def get_cost_summary(self) -> dict:
        """Get cost summary (future implementation).

        Will aggregate estimated costs by provider and operation type.

        Returns:
            dict: Cost summary with keys:
                - total_cost: Total estimated cost in USD
                - by_provider: Cost breakdown by provider
                - by_operation: Cost breakdown by operation type

        Note:
            Currently returns placeholder data. Cost tracking will be
            implemented when provider-specific pricing is added.
        """
        # Future implementation
        # Will calculate based on GenerationMetrics.estimated_cost
        return {
            "total_cost": 0.0,
            "by_provider": {},
            "by_operation": {},
            "note": "Cost tracking not yet implemented",
        }

    def clear(self) -> None:
        """Clear all collected metrics.

        Useful for resetting between test runs or sessions.
        """
        self.metrics.clear()

    def export_json(self, output_path: Path) -> None:
        """Export all metrics to a JSON file.

        Args:
            output_path: Path to write JSON file

        Examples:
            >>> collector.export_json(Path("metrics_export.json"))
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {"summary": self.get_summary(), "metrics": [m.to_dict() for m in self.metrics]}

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

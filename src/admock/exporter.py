"""Export helpers for bundling AdMock Studio assets."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable

from .models import Project, Storyboard


class Exporter:
    """Serialize project assets to simple JSON and text artifacts."""

    def __init__(self, base_path: str = "exports") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def export_storyboard_pdf(self, storyboard: Storyboard) -> Path:
        # Placeholder export; writes a markdown summary to emulate PDF creation.
        pdf_path = self.base_path / f"{storyboard.id}.md"
        with pdf_path.open("w", encoding="utf-8") as handle:
            handle.write(f"# Storyboard {storyboard.id}\n\n")
            for frame in storyboard.frames:
                handle.write(f"## Frame {frame.id} – {frame.beat}\n")
                handle.write(f"Voice over: {frame.voice_over}\n\n")
                handle.write(f"On-screen text: {frame.on_screen_text}\n\n")
        return pdf_path

    def export_project_json(self, project: Project) -> Path:
        path = self.base_path / f"{project.id}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self._to_serialisable(asdict(project)), handle, indent=2, ensure_ascii=False)
        return path

    def bundle(self, project: Project, storyboards: Iterable[Storyboard]) -> list[Path]:
        paths = [self.export_project_json(project)]
        for storyboard in storyboards:
            paths.append(self.export_storyboard_pdf(storyboard))
        return paths

    def _to_serialisable(self, value: Any) -> Any:
        from datetime import datetime

        if isinstance(value, dict):
            return {key: self._to_serialisable(val) for key, val in value.items()}
        if isinstance(value, list):
            return [self._to_serialisable(item) for item in value]
        if isinstance(value, datetime):
            return value.isoformat()
        if is_dataclass(value):
            return self._to_serialisable(asdict(value))
        return value

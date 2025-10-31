"""Storyboard generation utilities.

The generator produces structured data for both pencil sketches and a
narrative shot list. While image generation is outside the scope of this
prototype, the module returns symbolic file paths that stand in for sketches
and hi-fi renders.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from ..models import BrandTokens, Frame, Storyboard, StoryboardStyle


@dataclass
class ShotList:
    """Intermediate representation for storyboard planning."""

    narrative: str
    frames: List[Frame]
    risks: List[str]
    alt_hooks: List[str]


class StoryboardGenerator:
    """Create storyboard data structures for pencil sketches."""

    def generate_shot_list(self, *, brief_length: int, platform: str, tone: str) -> ShotList:
        """Return a deterministic shot list for testing purposes."""

        beats = ["Hook", "Problem", "Solution", "Proof", "CTA"]
        durations = self._distribute_duration(brief_length, len(beats))
        frames: List[Frame] = []
        for idx, (beat, duration) in enumerate(zip(beats, durations), start=1):
            frame_id = f"f{idx}"
            frames.append(
                Frame(
                    id=frame_id,
                    beat=beat,
                    voice_over=f"{beat} voice over tailored for {platform} with {tone} tone.",
                    on_screen_text=f"{beat} message",
                    camera="push-in" if beat == "Hook" else "cut",
                    duration=duration,
                    sketch_asset=f"assets/pencil/{frame_id}.png",
                    music_cue="warm" if idx > 1 else "",
                )
            )
        return ShotList(
            narrative="Problem → Solution → Proof → CTA",
            frames=frames,
            risks=["Ensure CTA is platform compliant"],
            alt_hooks=["Alternate hook emphasising emotional benefit"],
        )

    def create_storyboard(self, storyboard_id: str, shot_list: ShotList) -> Storyboard:
        return Storyboard(
            id=storyboard_id,
            style=StoryboardStyle.PENCIL,
            frames=shot_list.frames,
            narrative=shot_list.narrative,
            risks=shot_list.risks,
            alt_hooks=shot_list.alt_hooks,
        )

    def apply_global_edit(self, storyboard: Storyboard, description: str) -> None:
        for frame in storyboard.frames:
            frame.apply_edit(description)

    def apply_frame_edit(self, storyboard: Storyboard, frame_id: str, description: str) -> None:
        frame = storyboard.get_frame(frame_id)
        frame.apply_edit(description)

    def _distribute_duration(self, total_length: int, number_of_frames: int) -> Iterable[float]:
        base = total_length / number_of_frames
        return [round(base if i < number_of_frames - 1 else total_length - base * (number_of_frames - 1), 2) for i in range(number_of_frames)]


class HifiStoryboardGenerator:
    """Simulates the Nanobana adapter output."""

    def render(self, storyboard: Storyboard, brand_tokens: BrandTokens) -> Storyboard:
        new_frames: List[Frame] = []
        for frame in storyboard.frames:
            hifi_frame = Frame(
                id=frame.id,
                beat=frame.beat,
                voice_over=frame.voice_over,
                on_screen_text=self._apply_text_guidelines(frame.on_screen_text, brand_tokens),
                camera=frame.camera,
                duration=frame.duration,
                notes=list(frame.notes),
                sketch_asset=frame.sketch_asset,
                hifi_asset=f"assets/hifi/{frame.id}_{brand_tokens.brand}.png",
                music_cue=frame.music_cue or "brand_theme",
            )
            new_frames.append(hifi_frame)
        return Storyboard(
            id=f"{storyboard.id}-hifi",
            style=StoryboardStyle.HIFI,
            frames=new_frames,
            narrative=storyboard.narrative,
            risks=storyboard.risks,
            alt_hooks=storyboard.alt_hooks,
        )

    def _apply_text_guidelines(self, text: str, brand_tokens: BrandTokens) -> str:
        max_words = 7
        words = text.split()
        if len(words) > max_words:
            trimmed = " ".join(words[:max_words]) + "…"
            return f"{trimmed} (trimmed to match {brand_tokens.brand} guidelines)"
        return text

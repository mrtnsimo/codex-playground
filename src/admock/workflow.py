"""High-level orchestration for the AdMock Studio prototype."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, Optional

from .exporter import Exporter
from .models import (
    AudioProfile,
    BrandTokens,
    Brief,
    Frame,
    Project,
    Storyboard,
    StoryboardStyle,
    StoryboardVersion,
    VideoOutput,
)
from .services.brand_extractor import BrandExtractor, BrandExtractionResult
from .services.storyboard_generator import HifiStoryboardGenerator, ShotList, StoryboardGenerator
from .services.video import VideoSynthesizer, VideoSynthesisResult


@dataclass
class WorkflowState:
    """Represents the latest artifacts at a given point in the workflow."""

    brand_tokens: Optional[BrandTokens] = None
    storyboard: Optional[Storyboard] = None
    hifi_storyboard: Optional[Storyboard] = None
    video: Optional[VideoOutput] = None


class AdMockStudioWorkflow:
    """Coordinates the four-step workflow end-to-end."""

    def __init__(self, project: Project) -> None:
        self.project = project
        self.brand_extractor = BrandExtractor()
        self.storyboard_generator = StoryboardGenerator()
        self.hifi_generator = HifiStoryboardGenerator()
        self.video_synthesizer = VideoSynthesizer()
        self.exporter = Exporter()
        self._version_counter = itertools.count(1)
        self.state = WorkflowState()

    # Step 1 -----------------------------------------------------------------
    def ingest_brand(self, brand: str, url: str) -> BrandExtractionResult:
        result = self.brand_extractor.extract(brand, url)
        self.project.brand_tokens = result.tokens
        self.project.log_event("BRAND_EXTRACTED", {"url": url})
        self.state.brand_tokens = result.tokens
        return result

    def capture_brief(self, brief: Brief) -> None:
        self.project.brief = brief
        self.project.log_event("BRIEF_CAPTURED", {"objective": brief.objective})

    def create_concept(self) -> StoryboardVersion:
        if not self.project.brief:
            raise ValueError("Brief must be captured before generating concept")
        shot_list = self.storyboard_generator.generate_shot_list(
            brief_length=self.project.brief.ad_length_seconds,
            platform=self.project.brief.platform,
            tone=self.project.brief.tone,
        )
        storyboard = self.storyboard_generator.create_storyboard(self._next_storyboard_id(), shot_list)
        version = self._register_storyboard(storyboard)
        self.state.storyboard = storyboard
        self.project.log_event("STORYBOARD_CREATED", {"storyboard_id": storyboard.id})
        return version

    # Step 2 -----------------------------------------------------------------
    def apply_global_edit(self, description: str) -> None:
        storyboard = self._require_storyboard(StoryboardStyle.PENCIL)
        self.storyboard_generator.apply_global_edit(storyboard, description)
        self.project.log_event("GLOBAL_EDIT", {"description": description})

    def apply_frame_edit(self, frame_id: str, description: str) -> None:
        storyboard = self._require_storyboard(StoryboardStyle.PENCIL)
        self.storyboard_generator.apply_frame_edit(storyboard, frame_id, description)
        self.project.log_event("FRAME_EDIT", {"frame_id": frame_id, "description": description})

    def lock_storyboard(self) -> StoryboardVersion:
        storyboard_version = self._require_storyboard_version(StoryboardStyle.PENCIL)
        storyboard_version.locked = True
        storyboard_version.version = self._increment_major_version(storyboard_version.version)
        self.project.log_event("STORYBOARD_LOCKED", {"storyboard_id": storyboard_version.storyboard.id})
        return storyboard_version

    # Step 3 -----------------------------------------------------------------
    def render_hifi_storyboard(self) -> StoryboardVersion:
        if not self.project.brand_tokens:
            raise ValueError("Brand tokens required before rendering hi-fi storyboard")
        pencil_version = self._require_storyboard_version(StoryboardStyle.PENCIL)
        if not pencil_version.locked:
            raise ValueError("Storyboard must be locked before hi-fi render")
        hifi_storyboard = self.hifi_generator.render(pencil_version.storyboard, self.project.brand_tokens)
        version = self._register_storyboard(hifi_storyboard)
        self.state.hifi_storyboard = hifi_storyboard
        self.project.log_event("HIFI_RENDERED", {"storyboard_id": hifi_storyboard.id})
        return version

    # Step 4 -----------------------------------------------------------------
    def render_video(self, audio: AudioProfile) -> VideoSynthesisResult:
        hifi_version = self._require_storyboard_version(StoryboardStyle.HIFI)
        result = self.video_synthesizer.render(hifi_version.storyboard, audio)
        self.project.video_outputs.append(result.video)
        self.state.video = result.video
        self.project.log_event("VIDEO_RENDERED", {"storyboard_id": hifi_version.storyboard.id})
        return result

    # Export -----------------------------------------------------------------
    def export(self) -> list[str]:
        storyboards = [version.storyboard for version in self.project.storyboards]
        paths = self.exporter.bundle(self.project, storyboards)
        return [str(path) for path in paths]

    # Helpers ----------------------------------------------------------------
    def _register_storyboard(self, storyboard: Storyboard) -> StoryboardVersion:
        version_label = f"sb_v{next(self._version_counter)}"
        version = StoryboardVersion(storyboard=storyboard, version=version_label, locked=False)
        self.project.storyboards.append(version)
        return version

    def _require_storyboard(self, style: StoryboardStyle) -> Storyboard:
        version = self._require_storyboard_version(style)
        return version.storyboard

    def _require_storyboard_version(self, style: StoryboardStyle) -> StoryboardVersion:
        for version in reversed(self.project.storyboards):
            if version.storyboard.style == style:
                return version
        raise ValueError(f"No storyboard with style {style} available")

    def _increment_major_version(self, version: str) -> str:
        if "_locked" in version:
            prefix, _, suffix = version.partition("_locked")
            major = int(prefix.split("_v")[-1])
            return f"sb_v{major + 1}_locked"
        major = int(version.split("_v")[-1])
        return f"sb_v{major}_locked"

    def _next_storyboard_id(self) -> str:
        return f"sb_{len(self.project.storyboards) + 1}"

    def get_state(self) -> WorkflowState:
        return self.state

"""Core data models used throughout the AdMock Studio workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class StoryboardStyle(str, Enum):
    """Storyboards are rendered either as pencil sketches or hi-fi frames."""

    PENCIL = "pencil"
    HIFI = "hifi"


@dataclass
class BrandTokens:
    """Represents the distilled design language for a brand."""

    brand: str
    url: str
    colors: Dict[str, str]
    typography: Dict[str, str]
    logo: Dict[str, str]
    voice: Dict[str, List[str] | str]


@dataclass
class Brief:
    """User supplied inputs gathered during Step 1 of the workflow."""

    audience: str
    objective: str
    url: str
    ad_length_seconds: int
    platform: str
    tone: str
    constraints: Optional[str] = None
    languages: Optional[List[str]] = None


@dataclass
class Frame:
    """Single storyboard frame shared by both pencil and high-fidelity boards."""

    id: str
    beat: str
    voice_over: str
    on_screen_text: str
    camera: str
    duration: float
    notes: List[str] = field(default_factory=list)
    sketch_asset: Optional[str] = None
    hifi_asset: Optional[str] = None
    music_cue: Optional[str] = None

    def apply_edit(self, description: str) -> None:
        """Record an edit note for the frame."""

        self.notes.append(description)


@dataclass
class Storyboard:
    """Collection of frames representing the ad narrative."""

    id: str
    style: StoryboardStyle
    frames: List[Frame]
    narrative: str
    risks: List[str] = field(default_factory=list)
    alt_hooks: List[str] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        """Total length of the storyboard derived from frame durations."""

        return sum(frame.duration for frame in self.frames)

    def get_frame(self, frame_id: str) -> Frame:
        for frame in self.frames:
            if frame.id == frame_id:
                return frame
        raise KeyError(f"Frame {frame_id} not found")


@dataclass
class StoryboardVersion:
    """Tracks storyboard revisions and lock state."""

    storyboard: Storyboard
    version: str
    locked: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AudioProfile:
    """Details about the desired voiceover and music characteristics."""

    voice_style: str
    music_style: str
    voice_speed: float = 1.0
    voice_pitch: float = 1.0


@dataclass
class VideoOutput:
    """Represents the final render returned by Veo 3."""

    storyboard_id: str
    mp4_url: str
    srt_url: str
    alt_voiceovers: List[str]
    duration: float


@dataclass
class Project:
    """Aggregates all artifacts produced during a workflow run."""

    id: str
    owner: str
    brand_tokens: Optional[BrandTokens] = None
    brief: Optional[Brief] = None
    storyboards: List[StoryboardVersion] = field(default_factory=list)
    video_outputs: List[VideoOutput] = field(default_factory=list)
    audit_log: List[Dict[str, str]] = field(default_factory=list)

    def log_event(self, event: str, payload: Dict[str, str]) -> None:
        self.audit_log.append({"event": event, **payload, "ts": datetime.utcnow().isoformat()})

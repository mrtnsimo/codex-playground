"""Video synthesis simulation for Veo 3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..models import AudioProfile, Storyboard, VideoOutput


@dataclass
class VideoSynthesisResult:
    """Container describing the outcome of a Veo 3 render."""

    video: VideoOutput
    timeline: List[dict]


class VideoSynthesizer:
    """Mimics the Veo 3 adapter by stitching storyboard frames together."""

    def render(self, storyboard: Storyboard, audio: AudioProfile) -> VideoSynthesisResult:
        total_duration = round(sum(frame.duration for frame in storyboard.frames), 2)
        timeline = [
            {
                "frame_id": frame.id,
                "start": round(sum(f.duration for f in storyboard.frames[:idx]), 2),
                "duration": frame.duration,
                "camera": frame.camera,
            }
            for idx, frame in enumerate(storyboard.frames)
        ]
        video = VideoOutput(
            storyboard_id=storyboard.id,
            mp4_url=f"renders/{storyboard.id}.mp4",
            srt_url=f"renders/{storyboard.id}.srt",
            alt_voiceovers=[
                f"{audio.voice_style} voice {variant}"
                for variant in ("neutral", "warm", "energetic")
            ],
            duration=total_duration,
        )
        return VideoSynthesisResult(video=video, timeline=timeline)

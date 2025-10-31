"""Unit tests for the AdMock Studio workflow prototype."""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from admock import AdMockStudioWorkflow, AudioProfile, Brief, Project


class WorkflowTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.project = Project(id="proj_test", owner="user_test")
        self.workflow = AdMockStudioWorkflow(self.project)
        self.workflow.ingest_brand("Eco Brand", "https://eco.example")
        self.workflow.capture_brief(
            Brief(
                audience="Eco conscious adults",
                objective="Consideration",
                url="https://eco.example",
                ad_length_seconds=15,
                platform="Instagram",
                tone="optimistic",
            )
        )

    def test_full_workflow(self) -> None:
        storyboard_version = self.workflow.create_concept()
        self.assertEqual(storyboard_version.storyboard.style.value, "pencil")
        self.assertAlmostEqual(storyboard_version.storyboard.total_duration, 15, places=0)

        self.workflow.apply_global_edit("Increase brightness across frames")
        self.workflow.apply_frame_edit("f2", "Add product close-up")
        locked_version = self.workflow.lock_storyboard()
        self.assertTrue(locked_version.locked)

        hifi_version = self.workflow.render_hifi_storyboard()
        self.assertEqual(hifi_version.storyboard.style.value, "hifi")
        self.assertTrue(all(frame.hifi_asset for frame in hifi_version.storyboard.frames))

        result = self.workflow.render_video(AudioProfile(voice_style="neutral", music_style="ambient"))
        self.assertGreater(result.video.duration, 0)
        self.assertEqual(len(result.timeline), len(hifi_version.storyboard.frames))

        exported = self.workflow.export()
        self.assertTrue(any(path.endswith(".json") for path in exported))
        self.assertTrue(any(path.endswith(".md") for path in exported))

        project_json = next(path for path in exported if path.endswith(".json"))
        with open(project_json, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.assertEqual(payload["id"], "proj_test")

    def tearDown(self) -> None:
        if os.path.isdir("exports"):
            for name in os.listdir("exports"):
                os.remove(os.path.join("exports", name))
            os.rmdir("exports")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

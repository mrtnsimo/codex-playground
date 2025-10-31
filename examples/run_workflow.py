"""Demonstration script for executing the AdMock Studio workflow."""

from __future__ import annotations

from admock import AdMockStudioWorkflow, AudioProfile, Brief, Project


def main() -> None:
    project = Project(id="proj_001", owner="user_123")
    workflow = AdMockStudioWorkflow(project)

    workflow.ingest_brand("Acme", "https://acme.example")
    workflow.capture_brief(
        Brief(
            audience="New parents",
            objective="Awareness",
            url="https://acme.example",
            ad_length_seconds=15,
            platform="YouTube",
            tone="warm",
        )
    )
    workflow.create_concept()
    workflow.apply_frame_edit("f1", "Introduce mascot in the opening shot")
    workflow.lock_storyboard()
    workflow.render_hifi_storyboard()
    workflow.render_video(AudioProfile(voice_style="neutral", music_style="acoustic"))

    exported = workflow.export()
    for path in exported:
        print(f"Exported {path}")


if __name__ == "__main__":
    main()

# AdMock Studio Prototype

This repository contains a Python-based simulation of the AdMock Studio
workflow described in `PRD.md`. The goal is to model the four guided steps for
turning a marketing brief into a video ad mock-up using easily testable
components that run without external dependencies.

## Features

- **Brand grounding** – heuristically generates colour palettes, typography,
  and brand voice guidance from a supplied URL.
- **Storyboard generation** – creates deterministic pencil storyboards with
  edit tracking for both global and per-frame adjustments.
- **High-fidelity rendering** – simulates Nanobana output with brand-aware text
  adjustments and asset placeholders.
- **Video synthesis** – produces a mock Veo 3 render timeline and audio
  variants while collecting audit metadata.
- **Export** – writes project JSON and storyboard summaries to the `exports/`
  directory, representing the PDF/MP4 deliverables in the PRD.

## Running the Example

```
PYTHONPATH=src python examples/run_workflow.py
```

## Running Tests

```
PYTHONPATH=src python -m unittest discover -s tests -t .
```

The test suite covers the complete happy path for the workflow, ensuring the
artefacts described in the PRD are produced and exported successfully.

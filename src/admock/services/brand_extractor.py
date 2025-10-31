"""Brand token extraction service.

The real product would crawl a website and extract design tokens. For the
prototype we emulate the behaviour by transforming the supplied URL and
heuristically inferring colour and typography choices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..models import BrandTokens


@dataclass
class BrandExtractionResult:
    """Return value for :func:`BrandExtractor.extract`."""

    tokens: BrandTokens
    warnings: list[str]


class BrandExtractor:
    """High level interface for brand grounding.

    The implementation does not perform network requests; instead it uses
    simple heuristics to produce deterministic token packs suitable for unit
    tests. This keeps the module self-contained while modelling the real
    workflow's responsibilities.
    """

    DEFAULT_COLORS: Dict[str, str] = {
        "primary": "#0A84FF",
        "secondary": "#111111",
        "accent": "#FFCC00",
    }
    DEFAULT_TYPOGRAPHY: Dict[str, str] = {
        "heading": "Inter Bold",
        "body": "Inter Regular",
    }

    def extract(self, brand: str, url: str) -> BrandExtractionResult:
        """Return a :class:`BrandTokens` instance derived from *url*.

        Args:
            brand: Human readable brand name.
            url: Website used for grounding.
        """

        palette = self._infer_palette(url)
        typography = self._infer_typography(url)
        logo_url = f"{url.rstrip('/')}/assets/logo.svg"
        voice = {
            "tone": "confident, playful" if "play" in url else "modern, helpful",
            "donts": ["no sarcasm", "no slang"],
        }
        tokens = BrandTokens(
            brand=brand,
            url=url,
            colors=palette,
            typography=typography,
            logo={"url": logo_url, "safe_area": "10%"},
            voice=voice,
        )
        warnings: list[str] = []
        if palette == self.DEFAULT_COLORS:
            warnings.append("Using default palette; no colours detected")
        if typography == self.DEFAULT_TYPOGRAPHY:
            warnings.append("Using default typography; no fonts detected")
        return BrandExtractionResult(tokens=tokens, warnings=warnings)

    def _infer_palette(self, url: str) -> Dict[str, str]:
        if "eco" in url:
            return {"primary": "#2E7D32", "secondary": "#1B5E20", "accent": "#A5D6A7"}
        if "lux" in url or "premium" in url:
            return {"primary": "#1A1A1A", "secondary": "#E5C07B", "accent": "#61AFEF"}
        return dict(self.DEFAULT_COLORS)

    def _infer_typography(self, url: str) -> Dict[str, str]:
        if "eco" in url:
            return {"heading": "Work Sans SemiBold", "body": "Work Sans Regular"}
        if "lux" in url or "premium" in url:
            return {"heading": "Playfair Display Bold", "body": "Source Sans Pro"}
        return dict(self.DEFAULT_TYPOGRAPHY)

#!/usr/bin/env python3
"""
SVG Diagram Generation Helper Script
Provides common SVG element generation functions
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorScheme:
    """Unified color scheme - corresponds to design-spec.md"""
    flowchart: str = "#22D3EE"
    flowchart_light: str = "#67E8F9"
    flowchart_bg: str = "#0C2D3E"

    architecture: str = "#A78BFA"
    architecture_light: str = "#B892FA"
    architecture_bg: str = "#2D2150"

    sequence: str = "#FB923C"
    sequence_light: str = "#FDBA74"
    sequence_bg: str = "#3D2510"

    comparison: str = "#4ADE80"
    comparison_light: str = "#86EFAC"
    comparison_bg: str = "#0D3320"

    stats: str = "#F472B6"
    stats_light: str = "#F9A8D4"
    stats_bg: str = "#3D1530"

    bg_dark: str = "#0B0F19"
    bg_card: str = "#181C2A"
    bg_card_alt: str = "#1E283F"

    text_title: str = "#FFFFFF"
    text_subtitle: str = "#A0A5B5"
    text_heading: str = "#E2E8F0"
    text_body: str = "#94A3B8"
    text_muted: str = "#6B7280"

    border: str = "#334155"
    connector: str = "#64748B"
    highlight: str = "#38BDF8"


def escape_xml(text: str) -> str:
    """Escape XML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def card(x: int, y: int, width: int, height: int,
         title: str, body: list[str],
         color: str = "#22D3EE",
         bg: str = "#181C2A") -> str:
    """Generate card component

    Args:
        x, y: Card position
        width, height: Card dimensions
        title: Card title
        body: Description text list
        color: Border and title color (type accent)
        bg: Background color
    """
    body_text = '\n'.join(
        f'<text x="{x + 15}" y="{y + 55 + i * 16}" class="node-b">{escape_xml(line)}</text>'
        for i, line in enumerate(body)
    )

    return f'''
<g transform="translate({x}, {y})">
  <rect width="{width}" height="{height}" rx="12" fill="{bg}" stroke="{color}" stroke-width="1.5"/>
  <text x="15" y="28" class="node-h" fill="{color}">{escape_xml(title)}</text>
  {body_text}
</g>'''


def step_circle(x: int, y: int, number: int, color: str = "#22D3EE") -> str:
    """Generate step number circle

    Args:
        x, y: Circle center position
        number: Step number
        color: Circle fill color (type accent)
    """
    return f'''
<circle cx="{x}" cy="{y}" r="14" fill="{color}"/>
<text x="{x}" y="{y + 5}" text-anchor="middle" class="step-num" fill="#FFFFFF">{number}</text>'''


def arrow_marker(id: str, color: str) -> str:
    """Generate arrow marker definition

    Args:
        id: Marker ID (e.g., arrowBlue, arrowGreen, etc.)
        color: Arrow color
    """
    return f'''
<marker id="{id}" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
  <polygon points="0 0, 9 3, 0 6" fill="{color}"/>
</marker>'''


def connection_line(x1: int, y1: int, x2: int, y2: int,
                    color: str = "#64748B",
                    dashed: bool = False,
                    marker_end: Optional[str] = None) -> str:
    """Generate connection line

    Args:
        x1, y1: Start point coordinates
        x2, y2: End point coordinates
        color: Line color
        dashed: Whether to use dashed line
        marker_end: Arrow marker ID
    """
    dash = ' stroke-dasharray="6,3"' if dashed else ''
    marker = f' marker-end="url(#{marker_end})"' if marker_end else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"{dash}{marker}/>'


def svg_template(width: int, height: int,
                 title: str, subtitle: str,
                 content: str,
                 markers: str = "") -> str:
    """Generate complete SVG template

    Args:
        width, height: SVG dimensions
        title: Chart title
        subtitle: Subtitle
        content: SVG content (cards, connectors, etc.)
        markers: Marker definitions from arrow_marker
    """
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: system-ui, -apple-system, sans-serif; font-weight: 800; font-size: 28px; fill: #FFFFFF; }}
      .subtitle {{ font-family: system-ui, -apple-system, sans-serif; font-size: 14px; fill: #A0A5B5; }}
      .node-h {{ font-family: system-ui, -apple-system, sans-serif; font-weight: 700; font-size: 14px; }}
      .node-b {{ font-family: system-ui, -apple-system, sans-serif; font-size: 12px; fill: #94A3B8; }}
      .step-num {{ font-family: system-ui, -apple-system, sans-serif; font-weight: 900; font-size: 18px; }}
    </style>
    {markers}
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#0B0F19"/>

  <!-- Title Area -->
  <text x="{width // 2}" y="40" text-anchor="middle" class="title">{escape_xml(title)}</text>
  <text x="{width // 2}" y="60" text-anchor="middle" class="subtitle">{escape_xml(subtitle)}</text>

  <!-- Content -->
  {content}
</svg>'''


if __name__ == '__main__':
    colors = ColorScheme()
    print("ColorScheme loaded successfully")
    print(f"  flowchart: {colors.flowchart}")
    print(f"  architecture: {colors.architecture}")
    print(f"  comparison: {colors.comparison}")

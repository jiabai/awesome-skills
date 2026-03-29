#!/usr/bin/env python3
"""
SVG Syntax Validation Script
Checks XML escape issues and basic syntax errors
"""

import sys
import re
from pathlib import Path


def validate_svg(filepath: str) -> list[str]:
    """Validate SVG file, returns list of errors"""
    errors = []

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except FileNotFoundError:
        return [f"File not found: {filepath}"]
    except Exception as e:
        return [f"Failed to read file: {e}"]

    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        matches = re.findall(r'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', line)
        if matches and not line.strip().startswith('<!--'):
            if 'fill=' not in line and 'stroke=' not in line:
                errors.append(f"Line {i}: Found unescaped '&', should be '&amp;'")

    if '<svg' not in content:
        errors.append("Missing <svg> tag")
    if '</svg>' not in content:
        errors.append("Missing </svg> closing tag")

    if 'viewBox=' not in content and 'viewbox=' not in content.lower():
        errors.append("Recommendation: Add viewBox attribute for responsive sizing")

    if 'xmlns=' not in content:
        errors.append("Missing xmlns attribute")

    tags_to_check = ['rect', 'circle', 'line', 'path', 'text', 'g', 'defs', 'marker']
    for tag in tags_to_check:
        self_closing = len(re.findall(f'<{tag}[^>]*/>', content))
        opening = len(re.findall(f'<{tag}[^>]*>(?!</{tag}>)', content))
        closing = len(re.findall(f'</{tag}>', content))

        if opening != closing:
            errors.append(f"<{tag}> tag not closed: {opening} opening tags, {closing} closing tags")

    return errors


def validate_for_jpeg_export(filepath: str) -> list[str]:
    """Validate if SVG is suitable for JPEG export"""
    errors = []

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except Exception as e:
        return [f"Failed to read file: {e}"]

    if 'viewBox=' not in content and 'viewbox=' not in content.lower():
        errors.append("Warning: No viewBox may cause incorrect JPEG export dimensions")

    if '<style' in content:
        errors.append("Warning: Contains <style> tag, some SVG renderers may not support it")

    width_match = re.search(r'width=["\']?(\d+)', content)
    height_match = re.search(r'height=["\']?(\d+)', content)
    if not width_match or not height_match:
        errors.append("Warning: No explicit width/height attributes")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_svg.py <file.svg> [file2.svg ...]")
        sys.exit(1)

    all_passed = True
    for filepath in sys.argv[1:]:
        print(f"\n=== Validating: {filepath} ===")
        errors = validate_svg(filepath)

        if errors:
            all_passed = False
            for err in errors:
                print(f"  ❌ {err}")
        else:
            print("  ✓ Validation passed")

        if '--check-jpeg' in sys.argv or '-j' in sys.argv:
            jpeg_errors = validate_for_jpeg_export(filepath)
            if jpeg_errors:
                for err in jpeg_errors:
                    print(f"  ⚠ {err}")
            else:
                print("  ✓ Suitable for JPEG export")

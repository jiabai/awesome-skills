#!/usr/bin/env python3
"""
SVG 语法验证脚本
检查 XML 转义问题和基本语法错误
"""

import sys
import re
from pathlib import Path


def validate_svg(filepath: str) -> list[str]:
    """验证 SVG 文件，返回错误列表"""
    errors = []

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except FileNotFoundError:
        return [f"文件不存在: {filepath}"]
    except Exception as e:
        return [f"读取文件失败: {e}"]

    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        matches = re.findall(r'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', line)
        if matches and not line.strip().startswith('<!--'):
            if 'fill=' not in line and 'stroke=' not in line:
                errors.append(f"第 {i} 行: 发现未转义的 '&'，应转为 '&amp;'")

    if '<svg' not in content:
        errors.append("缺少 <svg> 标签")
    if '</svg>' not in content:
        errors.append("缺少 </svg> 闭合标签")

    if 'viewBox=' not in content and 'viewbox=' not in content.lower():
        errors.append("建议添加 viewBox 属性以保证响应式")

    if 'xmlns=' not in content:
        errors.append("缺少 xmlns 属性")

    tags_to_check = ['rect', 'circle', 'line', 'path', 'text', 'g', 'defs', 'marker']
    for tag in tags_to_check:
        self_closing = len(re.findall(f'<{tag}[^>]*/>', content))
        opening = len(re.findall(f'<{tag}[^>]*>(?!</{tag}>)', content))
        closing = len(re.findall(f'</{tag}>', content))

        if opening != closing:
            errors.append(f"<{tag}> 标签未闭合: 开标签 {opening} 个, 闭标签 {closing} 个")

    return errors


def validate_for_jpeg_export(filepath: str) -> list[str]:
    """验证 SVG 是否适合导出为 JPEG"""
    errors = []

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except Exception as e:
        return [f"读取文件失败: {e}"]

    if 'viewBox=' not in content and 'viewbox=' not in content.lower():
        errors.append("警告: 没有 viewBox 可能导致 JPEG 导出尺寸不正确")

    if '<style' in content:
        errors.append("警告: 包含 <style> 标签，某些 SVG 渲染器可能不支持")

    width_match = re.search(r'width=["\']?(\d+)', content)
    height_match = re.search(r'height=["\']?(\d+)', content)
    if not width_match or not height_match:
        errors.append("警告: 没有明确的 width/height 属性")

    return errors


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_svg.py <file.svg> [file2.svg ...]")
        sys.exit(1)

    all_passed = True
    for filepath in sys.argv[1:]:
        print(f"\n=== 验证: {filepath} ===")
        errors = validate_svg(filepath)

        if errors:
            all_passed = False
            for err in errors:
                print(f"  ❌ {err}")
        else:
            print("  ✓ 验证通过")

        if '--check-jpeg' in sys.argv or '-j' in sys.argv:
            jpeg_errors = validate_for_jpeg_export(filepath)
            if jpeg_errors:
                for err in jpeg_errors:
                    print(f"  ⚠ {err}")
            else:
                print("  ✓ 适合 JPEG 导出")

    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()

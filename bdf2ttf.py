#!/usr/bin/env fontforge
"""Convert a BDF bitmap font into a scalable TrueType font by tracing each
glyph's pixels into vector rectangle outlines.

macOS (Catalina onward) dropped support for bitmap-only fonts system-wide,
so a BDF or a TTF with only an embedded bitmap strike won't install in Font
Book. Tracing the pixels into real outlines sidesteps that: the result is a
normal scalable TTF Core Text/iTerm2 can render at any point size, and since
the outlines are literally the pixel squares, it keeps the exact blocky look
of the console font.

Usage: fontforge -script bdf2ttf.py in.bdf out.ttf FamilyName
"""
import sys

import fontforge

UNITS_PER_EM = 2048


def parse_bdf(path):
    glyphs = {}
    cell_width = cell_height = descent = None
    code = bbx = None
    bitmap_rows = []
    in_bitmap = False

    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("FONTBOUNDINGBOX"):
            parts = line.split()
            cell_width, cell_height = int(parts[1]), int(parts[2])
        elif line.startswith("FONT_DESCENT"):
            descent = int(line.split()[1])
        elif line.startswith("ENCODING"):
            code = int(line.split()[1])
        elif line.startswith("BBX"):
            bbx = tuple(int(x) for x in line.split()[1:])
        elif line == "BITMAP":
            in_bitmap = True
            bitmap_rows = []
        elif line == "ENDCHAR":
            in_bitmap = False
            glyphs[code] = (bbx, bitmap_rows)
        elif in_bitmap:
            bitmap_rows.append(int(line, 16))

    return glyphs, cell_width, cell_height, descent


def add_glyph_outline(glyph, bbx, rows, cell_width, scale):
    bbx_w, bbx_h, bbx_x, bbx_y = bbx
    pen = glyph.glyphPen()
    for row_idx, row_bits in enumerate(rows):
        y_top = (bbx_y + bbx_h - row_idx) * scale
        y_bot = y_top - scale
        col = 0
        while col < bbx_w:
            if not (row_bits >> (7 - col)) & 1:
                col += 1
                continue
            span_start = col
            while col < bbx_w and (row_bits >> (7 - col)) & 1:
                col += 1
            x0 = (bbx_x + span_start) * scale
            x1 = (bbx_x + col) * scale
            pen.moveTo((x0, y_bot))
            pen.lineTo((x0, y_top))
            pen.lineTo((x1, y_top))
            pen.lineTo((x1, y_bot))
            pen.closePath()
    pen = None
    glyph.width = cell_width * scale
    if len(glyph.foreground) > 0:
        glyph.correctDirection()


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: fontforge -script bdf2ttf.py in.bdf out.ttf FamilyName")
    path_in, path_out, family = sys.argv[1], sys.argv[2], sys.argv[3]

    glyphs, cell_width, cell_height, descent = parse_bdf(path_in)
    ascent = cell_height - descent
    scale = UNITS_PER_EM // cell_height

    font = fontforge.font()
    font.encoding = "UnicodeFull"
    font.em = UNITS_PER_EM
    font.ascent = ascent * scale
    font.descent = descent * scale
    font.familyname = family
    font.fontname = family
    font.fullname = family
    font.copyright = "Derived from Slackware kbd console font (GPL-2.0-or-later)"

    for code, (bbx, rows) in glyphs.items():
        glyph = font.createChar(code)
        add_glyph_outline(glyph, bbx, rows, cell_width, scale)

    font.generate(path_out)
    print(f"{path_in} -> {path_out}: {len(glyphs)} glyphs, family={family}")


if __name__ == "__main__":
    main()

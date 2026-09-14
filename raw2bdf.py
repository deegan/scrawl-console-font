#!/usr/bin/env python3
"""Convert a raw headerless VGA console font (256 glyphs, fixed cell) to BDF.

These Slackware/kbd "consolefonts" .fnt files have no PSF magic: they are
just 256 glyphs back to back, each `height` bytes tall and 8 pixels wide
(1 byte per row). setfont recognizes them by file size alone:
  2048 bytes -> 8x8, 3584 bytes -> 8x14, 4096 bytes -> 8x16.
"""
import sys

SIZE_TO_HEIGHT = {2048: 8, 3584: 14, 4096: 16}


def convert(path_in, path_out, family):
    data = open(path_in, "rb").read()
    height = SIZE_TO_HEIGHT.get(len(data))
    if height is None:
        raise SystemExit(f"{path_in}: unrecognized raw font size {len(data)} bytes")
    width = 8
    n_glyphs = 256
    descent = 2 if height == 16 else 1 if height == 14 else 0
    ascent = height - descent

    lines = []
    lines.append("STARTFONT 2.1")
    lines.append(
        f"FONT -kbd-{family}-medium-r-normal--{height}-{height*10}-75-75-c-80-iso10646-1"
    )
    lines.append(f"SIZE {height} 72 72")
    lines.append(f"FONTBOUNDINGBOX {width} {height} 0 -{descent}")
    lines.append("STARTPROPERTIES 6")
    lines.append(f"FONT_ASCENT {ascent}")
    lines.append(f"FONT_DESCENT {descent}")
    lines.append("DEFAULT_CHAR 0")
    lines.append('FONT_NAME "%s"' % family)
    lines.append('CHARSET_REGISTRY "ISO10646"')
    lines.append('CHARSET_ENCODING "1"')
    lines.append("ENDPROPERTIES")
    lines.append(f"CHARS {n_glyphs}")

    for code in range(n_glyphs):
        glyph = data[code * height:(code + 1) * height]
        lines.append(f"STARTCHAR U+{code:04X}")
        lines.append(f"ENCODING {code}")
        lines.append(f"SWIDTH {int(1000*width/ (width))} 0")
        lines.append(f"DWIDTH {width} 0")
        lines.append(f"BBX {width} {height} 0 -{descent}")
        lines.append("BITMAP")
        for row in glyph:
            lines.append(f"{row:02X}")
        lines.append("ENDCHAR")

    lines.append("ENDFONT")

    with open(path_out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{path_in} ({height}px) -> {path_out}: {n_glyphs} glyphs")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(f"usage: {sys.argv[0]} in.fnt out.bdf family-name")
    convert(sys.argv[1], sys.argv[2], sys.argv[3])

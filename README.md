# scrawl-console-font

The Slackware `scrawl` console font — a hand-scrawled-looking bitmap
typeface from the old Linux `kbd` package — packaged for use in a modern
Wayland terminal instead of just the raw text console.

![scrawl font rendered in foot](screenshot.png)

## Backstory

`scrawl_s.fnt.gz` and `scrawl_w.fnt.gz` are 8x16 pixel bitmap fonts meant
for the Linux virtual console (`setfont`), bundled with Slackware's `kbd`
package. They only work on the raw TTY — GPU terminal emulators can't load
that format at all. This repo converts them to BDF (a format FreeType
understands) and packages the result for Arch/Omarchy, along with a config
fragment for the `foot` terminal.

## Install (Arch / Omarchy)

```sh
git clone <this repo>
cd scrawl-console-font
makepkg -si
```

Then wire it into `foot`:

```sh
scrawl-font-setup-foot           # ScrawlS, the 8x16 "short" variant
scrawl-font-setup-foot ScrawlW   # or the wide variant
```

Open a new `foot` window — existing ones won't pick up the change.

This edits `~/.config/foot/foot.ini` directly (a backup of the previous
version is saved alongside it). If you'd rather do it by hand, see
`foot-scrawl.ini` for the settings and why each one is there.

## What's in this repo

| File | Purpose |
|---|---|
| `PKGBUILD` | Builds and packages everything below |
| `scrawl_s.fnt.gz`, `scrawl_w.fnt.gz` | The original raw Slackware console fonts |
| `raw2bdf.py` | Converts the raw font to BDF at build time |
| `foot-scrawl.ini` | The `foot` settings this font needs, with comments explaining why |
| `scrawl-font-setup-foot` | Installed to `/usr/bin`; patches `foot.ini` for you |
| `scrawl-console-font.install` | pacman hook: refreshes the font cache after install |

## Notes

- It's a fixed-size 16px bitmap font — there is no other size. `pixelsize=16`
  and `dpi-aware=yes` in `foot.ini` are both required, otherwise `foot`
  multiplies the pixel size by your monitor's scale factor and the font
  gets blurrily upscaled.
- Only ASCII (codepoints 0–127) is guaranteed correct. The upper 128 glyphs
  have no embedded Unicode table, so they won't map to their intended
  characters.
- Not tested outside `foot`. Other terminals (Alacritty, Kitty, Ghostty) have
  much weaker bitmap-font support and may not render this well.

## License

The font data comes from Slackware's `kbd` package (GPL-2.0-or-later). The
conversion script and packaging in this repo are released under the same
terms.

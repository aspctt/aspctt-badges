# aspctt's Badges

<p align="center">
	<img alt="SpaceDock" height="56" src="assets/cozy-minimal/available/spacedock_vector.svg">
	<img alt="KSP Forum" height="56" src="assets/cozy-minimal/available/ksp-forum_vector.svg">
</p>

Badges for the places my mods live that [Devin's Badges](https://github.com/intergrav/devins-badges)
does not cover. They follow its design, so the two sets can sit side by side on one mod
page. The repository is public and the badges are free to use, but they are made for my
own projects first, so requests may or may not happen.

## Styles

Both styles are minimal: the icon on its own, with no text.

- **Cozy minimal** is the minimal version of a cozy badge. The recommended height is 48 to
  64px, and the SVG is 56px by default.
- **Compact minimal** is the minimal version of a compact badge. The recommended height is
  32 to 46px, and the SVG is 40px by default.

Every badge comes as an SVG and as a PNG at the top of its range, 64px for cozy and 46px
for compact.

## Badges

| Badge | Cozy minimal | Compact minimal | Path |
|---|---|---|---|
| SpaceDock | <img alt="SpaceDock" src="assets/cozy-minimal/available/spacedock_vector.svg"> | <img alt="SpaceDock" src="assets/compact-minimal/available/spacedock_vector.svg"> | `available/spacedock` |
| KSP Forum | <img alt="KSP Forum" src="assets/cozy-minimal/available/ksp-forum_vector.svg"> | <img alt="KSP Forum" src="assets/compact-minimal/available/ksp-forum_vector.svg"> | `available/ksp-forum` |

## Using them

Link a badge through jsDelivr, putting the style and the path from the table into the URL:

```
https://cdn.jsdelivr.net/gh/aspctt/aspctt-badges@main/assets/<style>/<path>_vector.svg
https://cdn.jsdelivr.net/gh/aspctt/aspctt-badges@main/assets/<style>/<path>_<height>h.png
```

HTML is the better choice, since it can set the height:

```html
<a href="https://spacedock.info/mod/..."><img alt="Available on SpaceDock" height="40" src="https://cdn.jsdelivr.net/gh/aspctt/aspctt-badges@main/assets/compact-minimal/available/spacedock_vector.svg"></a>
```

Markdown works as well, at the badge's default size:

```md
[![Available on SpaceDock](https://cdn.jsdelivr.net/gh/aspctt/aspctt-badges@main/assets/compact-minimal/available/spacedock_vector.svg)](https://spacedock.info/mod/...)
```

Some sites, mod portals among them, do not show SVGs. The PNG is there for those.

## Making badges

[docs/DESIGN.md](docs/DESIGN.md) has the template, the sizes and the steps for adding a
badge. In short, a new badge is drawn once as compact minimal, and `scripts/build.py`
makes the cozy one and renders both PNGs.

## License

The badge designs and the build script are released under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), the same as Devin's
Badges, so they can be used and changed for anything without credit. The logos on them
belong to their owners, see [NOTICE](NOTICE).

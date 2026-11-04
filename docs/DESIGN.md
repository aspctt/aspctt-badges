# aspctt's Badges: Design

How a badge is drawn, so new ones match the old. The template follows Devin's Badges, so
these sit well next to them.

## Styles

Both styles are minimal: a rounded square with the icon and no text.

| Style | Folder | Vector size | PNG height | Recommended height |
|---|---|---|---|---|
| Compact minimal | `assets/compact-minimal/` | 40×40 | 46px | 32 to 46px |
| Cozy minimal | `assets/cozy-minimal/` | 56×56 | 64px | 48 to 64px |

Inside each style, badges go in a category folder, the same ones Devin's Badges uses:
`available`, `built-with`, `documentation`, `donate`, `requires`, `social`, `supported`,
`translate` and `unsupported`. A badge is two files, `<name>_vector.svg` and
`<name>_<height>h.png`, with the name in lowercase and words joined by hyphens.

## Template

A compact minimal badge, with the icon left out:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 40 40">
	<rect width="40" height="40" fill="url(#a)" rx="8"/>
	<rect width="37.9" height="37.9" x="1.05" y="1.05" stroke="#fff" stroke-opacity=".15" stroke-width="2.1" rx="6.95"/>
	<g filter="url(#b)">
		<!-- icon -->
	</g>
	<defs>
		<linearGradient id="a" x1="20" x2="20" y1="0" y2="40" gradientUnits="userSpaceOnUse">
			<stop stop-color="#1f1f1f"/>
			<stop offset="1" stop-color="#131313"/>
		</linearGradient>
		<filter id="b" width="36" height="36" x="2" y="2" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse">
			<feFlood flood-opacity="0" result="BackgroundImageFix"/>
			<feColorMatrix in="SourceAlpha" result="hardAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"/>
			<feOffset/>
			<feGaussianBlur stdDeviation="2"/>
			<feComposite in2="hardAlpha" operator="out"/>
			<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"/>
			<feBlend in2="BackgroundImageFix" result="shadow"/>
			<feBlend in="SourceGraphic" in2="shadow" result="shape"/>
		</filter>
	</defs>
</svg>
```

- **Background:** a vertical gradient from a colour to a slightly darker one. Neutral
  `#1f1f1f` to `#131313` by default, or a dark tint of the service's own colour, like
  the KSP Forum badge's `#15253e` to `#0c1628`.
- **Border:** white at 15%, 2.1 units wide, drawn inside the edge.
- **Icon:** fits the 28 unit square from 6 to 34, centred. Anything the icon needs, such
  as its own gradients or clip paths, goes in `defs` after the background gradient with
  ids other than `a` and `b`.
- **Shadow:** a soft black glow at 25% around the icon, no offset.

## Cozy minimal

A cozy minimal badge is the compact one at 1.4286 times the size, except for the frame:
the border stays 2.1 units wide, and the corners are 8.4 and 7.35 rather than scaled.
The icon fills 40 units from 8 to 48, and the shadow's blur grows to 2.857.

`scripts/build.py` makes a cozy badge from every compact one that has none yet. It
wraps the icon in a scaling transform, so a cozy badge drawn by hand is fine too, and
the script leaves an existing one alone.

## Building

```
python scripts/build.py
```

It needs Python 3.9 or later and ImageMagick 7 with librsvg on the PATH. After creating
the missing cozy badges, it renders every vector badge to its PNG: drawn at four times
the size, then scaled down for smooth edges, in 8-bit colour and without a date, so an
unchanged badge renders to an unchanged file.

## Adding a badge

1. Draw the icon into the template and save it as
   `assets/compact-minimal/<category>/<name>_vector.svg`.
2. Run the build script.
3. Look over both PNGs at their real size, since a detail that reads fine at 64px can
   turn to mush at 46.
4. Add the badge to the table in the README.

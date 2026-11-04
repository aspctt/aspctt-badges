"""
Builds the badge assets from their vector sources.

Every compact minimal badge gets a cozy minimal counterpart scaled up from it, unless one
already exists, so a cozy badge drawn by hand is never overwritten. Every vector badge is
then rendered to a PNG at its style's recommended height.

Usage: python scripts/build.py
Needs ImageMagick 7 (`magick`) on the PATH, built with librsvg for SVG support.
"""

# Dependencies

import subprocess
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

# Constants

ASSETS_DIRECTORY = Path(__file__).resolve().parent.parent / "assets"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

# Badge side length in SVG units, and the PNG height it is rendered at
STYLE_SIZES = {
	"compact-minimal": (40, 46),
	"cozy-minimal": (56, 64),
}

# The icon area grows from 28 to 40 units between compact and cozy, around the centre,
# matching how the cozy badges are drawn in Devin's Badges.
COZY_ICON_SCALE = 40 / 28

# ImageMagick renders SVG units as pixels at 96 DPI
DEFAULT_DENSITY = 96

# How many times larger than the PNG a badge is drawn before scaling down, for smoother edges
SUPERSAMPLING = 4

# Private functions

def findChild(parent: ElementTree.Element, tag: str, attributes: dict[str, str]) -> ElementTree.Element:
	"""Returns the direct child with this tag and attributes, failing loudly when the
	badge does not follow the template rather than writing a broken cozy badge."""
	for child in parent:
		if child.tag != f"{{{SVG_NAMESPACE}}}{tag}":
			continue

		if all(child.get(name) == value for name, value in attributes.items()):
			return child

	raise ValueError(f"no <{tag}> with {attributes} found, is the badge built from the template?")


def formatNumber(value: float) -> str:
	# Three decimals is what Figma exports, and enough for a 56 unit badge
	return f"{value:.3f}".rstrip("0").rstrip(".")


def createCozy(compactPath: Path, cozyPath: Path) -> None:
	"""Writes a cozy minimal badge scaled up from a compact minimal one."""
	ElementTree.register_namespace("", SVG_NAMESPACE)
	tree = ElementTree.parse(compactPath)
	root = tree.getroot()

	# Resize the canvas
	root.set("width", "56")
	root.set("height", "56")
	root.set("viewBox", "0 0 56 56")

	# The frame keeps its 2.1 unit border at both sizes, so only its size and corner radius change
	background = findChild(root, "rect", {"fill": "url(#a)"})
	background.set("width", "56")
	background.set("height", "56")
	background.set("rx", "8.4")

	border = findChild(root, "rect", {"stroke": "#fff"})
	border.set("width", "53.9")
	border.set("height", "53.9")
	border.set("rx", "7.35")

	# Scale the icon around the centre. Wrapping it in a transform also carries along any
	# clip paths and gradients it uses, since those resolve in the icon's own user space.
	icon = findChild(root, "g", {"filter": "url(#b)"})
	offset = 28 - 20 * COZY_ICON_SCALE
	# Six decimals here, since three would put the icon's edges a fiftieth of a unit off.
	scale = f"{COZY_ICON_SCALE:.6f}"
	scaled = ElementTree.Element(f"{{{SVG_NAMESPACE}}}g", {
		"transform": f"matrix({scale} 0 0 {scale} {offset:.6f} {offset:.6f})",
	})
	scaled.extend(list(icon))
	for child in list(icon):
		icon.remove(child)
	icon.append(scaled)

	# The background gradient and the shadow filter are in canvas units, so they scale by
	# hand. The shadow region and blur scale with the icon, as in Devin's Badges.
	definitions = findChild(root, "defs", {})
	gradient = findChild(definitions, "linearGradient", {"id": "a"})
	gradient.set("x1", "28")
	gradient.set("x2", "28")
	gradient.set("y2", "56")

	shadow = findChild(definitions, "filter", {"id": "b"})
	shadow.set("x", formatNumber(offset + 2 * COZY_ICON_SCALE))
	shadow.set("y", formatNumber(offset + 2 * COZY_ICON_SCALE))
	shadow.set("width", formatNumber(36 * COZY_ICON_SCALE))
	shadow.set("height", formatNumber(36 * COZY_ICON_SCALE))
	findChild(shadow, "feGaussianBlur", {}).set("stdDeviation", formatNumber(2 * COZY_ICON_SCALE))

	# Write with tabs, tight self-closing tags and a trailing newline, like the hand-written
	# badges. ElementTree puts a space before every "/>", which no other badge has.
	ElementTree.indent(tree, space="\t")
	text = ElementTree.tostring(root, encoding="unicode").replace(" />", "/>")
	cozyPath.parent.mkdir(parents=True, exist_ok=True)
	cozyPath.write_text(text + "\n", encoding="utf-8", newline="\n")


def renderPng(vectorPath: Path, side: int, height: int) -> Path:
	"""Renders a vector badge to a PNG next to it, named after its height."""
	pngPath = vectorPath.with_name(vectorPath.name.replace("_vector.svg", f"_{height}h.png"))

	# Draw the vector at four times the target size, then scale down to exactly the target.
	# Drawing straight at the target density rounds the size down, giving 63px for 64px,
	# and scaling up a bitmap drawn at the SVG's own size would blur it.
	# The date chunks are left out so an unchanged badge renders to an unchanged file,
	# otherwise every build would show every PNG as modified. librsvg hands over 16 bits
	# per channel, which only doubles the file size for nothing.
	subprocess.run([
		"magick",
		"-background", "none",
		"-density", formatNumber(DEFAULT_DENSITY * SUPERSAMPLING * height / side),
		str(vectorPath),
		"-resize", f"{height}x{height}!",
		"-depth", "8",
		"-define", "png:exclude-chunks=date,time",
		str(pngPath),
	], check=True)
	return pngPath

# Public API

def main() -> int:
	# Derive missing cozy badges first, so they are rendered in the same run
	for compactPath in sorted((ASSETS_DIRECTORY / "compact-minimal").rglob("*_vector.svg")):
		cozyPath = ASSETS_DIRECTORY / "cozy-minimal" / compactPath.relative_to(ASSETS_DIRECTORY / "compact-minimal")
		if cozyPath.exists():
			continue

		createCozy(compactPath, cozyPath)
		print(f"Created {cozyPath.relative_to(ASSETS_DIRECTORY)}")

	for style, (side, height) in STYLE_SIZES.items():
		for vectorPath in sorted((ASSETS_DIRECTORY / style).rglob("*_vector.svg")):
			pngPath = renderPng(vectorPath, side, height)
			print(f"Rendered {pngPath.relative_to(ASSETS_DIRECTORY)}")

	return 0

# Exports

if __name__ == "__main__":
	sys.exit(main())

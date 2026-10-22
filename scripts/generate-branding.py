#!/usr/bin/env python3
"""Generate RW Notes native icons from the core SVG using its icon renderer."""
import argparse
import importlib.util
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--core-repo", type=Path, default=Path(__file__).resolve().parents[2] / "rw-notes")
args = parser.parse_args()
core = args.core_repo.resolve()
source = core / "app/src/assets/icon.svg"
generator = core / "app/src/assets/generate_icons.py"
if not source.is_file() or not generator.is_file():
    parser.error("--core-repo must contain the RW Notes SVG and core icon generator")
spec = importlib.util.spec_from_file_location("rw_notes_icons", generator)
icons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icons)
repo = Path(__file__).resolve().parents[1]
master = icons.render_svg(source, 1024)

import xml.etree.ElementTree as ET

res = repo / "app/src/main/res"
svg = ET.parse(source).getroot()
svg_ns = "{http://www.w3.org/2000/svg}"
groups = [g for g in svg.findall(svg_ns + "g") if g.findall(svg_ns + "path")]
if len(groups) != 1 or groups[0].get("transform") != "rotate(180 512 512)" or svg.get("viewBox") != "0 0 1024 1024":
    raise SystemExit("SVG structure changed; update the native vector conversion before regenerating")
paths = groups[0].findall(svg_ns + "path")
android_ns = "http://schemas.android.com/apk/res/android"
ET.register_namespace("android", android_ns)
def attr(**values):
    return {"{" + android_ns + "}" + key: str(value) for key, value in values.items()}
for name, monochrome in [("launcher_foreground.xml", False), ("launcher_monochrome.xml", True)]:
    vector = ET.Element("vector", attr(width="108dp", height="108dp", viewportWidth=1024, viewportHeight=1024))
    group = ET.SubElement(vector, "group", attr(rotation=180, pivotX=512, pivotY=512, scaleX=0.5, scaleY=0.5))
    for path in paths:
        ET.SubElement(group, "path", attr(pathData=path.attrib["d"], fillColor="#FFFFFF" if monochrome else path.attrib["fill"]))
    ET.indent(vector, space="    ")
    ET.ElementTree(vector).write(res / "drawable" / name, encoding="utf-8", xml_declaration=True)
for name in ["icon.png", "shorthand_icon.png"]:
    icons.save_png(icons.square_canvas(master, 512, 0.825), res / "drawable" / name)
print("Generated Android launcher, monochrome, boot, and shortcut icons from", source)

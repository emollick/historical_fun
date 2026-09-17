#!/usr/bin/env python3
"""Re-draw the elevation profiles with the legend under the axis (data/profiles_report.svg); uses figures.profiles_svg."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figures
with open(os.path.join(figures.DATA, "routes.json")) as f: routes = json.load(f)
with open(os.path.join(figures.DATA, "profiles.json")) as f: profiles = json.load(f)
figures.profiles_svg(routes, profiles, out_name="profiles_report.svg", legend_below=True)
print("profiles_report.svg written")

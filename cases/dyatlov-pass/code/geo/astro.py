#!/usr/bin/env python3
"""astro.py - sun and moon at the Dyatlov tent site for 1-2 Feb, 26 Feb and 5 Mar 1959.

Method: PyEphem 4.x (ephem) - self-contained VSOP87/ELP-based ephemerides (no downloads), USNO
conventions: rise/set = upper limb at -34' refraction (ephem default horizon '-0:34' with pressure=0),
civil / nautical / astronomical twilight = sun centre at -6/-12/-18 deg. Independent cross-check of
the sun altitude with a from-scratch NOAA (Meeus) solar position algorithm implemented below.
Time zone: Sverdlovsk oblast 1959 = UTC+5 (tzdata Asia/Yekaterinburg: '+05' from 1930-06-21 to 1991).
Output: out/astro_tables.md, out/astro_tables.json
"""
import json, math, os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import ephem
from geo_common import OUT, load_coordinates

C = load_coordinates()
tent = C["tent_dyatlovpass_map"]
LAT, LON, ELEV = tent["lat"], tent["lon"], 898.0   # elevation from Copernicus GLO-30 (dem_slope.py)
TZ = ZoneInfo("Asia/Yekaterinburg")
assert datetime(1959, 2, 1, 12, tzinfo=TZ).utcoffset() == timedelta(hours=5)
UTC5 = timezone(timedelta(hours=5))

def obs(elev=ELEV):
    o = ephem.Observer(); o.lat, o.lon, o.elevation = str(LAT), str(LON), elev
    o.pressure = 0; o.horizon = "-0:34"; return o

def loc(dt_utc):
    return ephem.Date(dt_utc).datetime().replace(tzinfo=timezone.utc).astimezone(UTC5)

def fmt(d):
    return d.strftime("%Y-%m-%d %H:%M") if d else "-"

def sun_events(date):
    """Events for the local civil date `date` (UTC+5)."""
    o = obs(); sun = ephem.Sun()
    start = datetime(date.year, date.month, date.day, 0, 0, tzinfo=UTC5).astimezone(timezone.utc)
    o.date = ephem.Date(start.replace(tzinfo=None))
    ev = {}
    o.horizon = "-0:34"
    ev["sunrise"] = loc(o.next_rising(sun)); ev["sunset"] = loc(o.next_setting(sun))
    for name, h in [("civil", "-6"), ("nautical", "-12"), ("astronomical", "-18")]:
        o.date = ephem.Date(start.replace(tzinfo=None)); o.horizon = h
        ev[f"{name}_dawn"] = loc(o.next_rising(sun, use_center=True)); ev[f"{name}_dusk"] = loc(o.next_setting(sun, use_center=True))
    o.horizon = "-0:34"; o.date = ephem.Date(start.replace(tzinfo=None))
    ev["solar_noon"] = loc(o.next_transit(sun))
    return ev

def moon_events(date):
    o = obs(); moon = ephem.Moon()
    start = datetime(date.year, date.month, date.day, 0, 0, tzinfo=UTC5).astimezone(timezone.utc)
    o.date = ephem.Date(start.replace(tzinfo=None)); o.horizon = "-0:34"
    ev = {}
    for key, fn in [("moonrise", o.next_rising), ("moonset", o.next_setting)]:
        o.date = ephem.Date(start.replace(tzinfo=None))
        try:
            t = fn(moon)
            tl = loc(t)
            ev[key] = tl if tl.date() == date else None   # only if it happens on that civil date
            if ev[key] is None:  # maybe the event is later that same day after a first event -> check next
                pass
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            ev[key] = None
    noon = datetime(date.year, date.month, date.day, 12, tzinfo=UTC5).astimezone(timezone.utc).replace(tzinfo=None)
    moon.compute(ephem.Date(noon)); ev["illum_pct_at_noon"] = round(moon.phase, 1)
    ev["prev_new_moon"] = loc(ephem.previous_new_moon(ephem.Date(noon))); ev["next_new_moon"] = loc(ephem.next_new_moon(ephem.Date(noon)))
    ev["prev_full_moon"] = loc(ephem.previous_full_moon(ephem.Date(noon))); ev["next_full_moon"] = loc(ephem.next_full_moon(ephem.Date(noon)))
    return ev

def altitudes(dt_local):
    o = obs(); o.date = ephem.Date(dt_local.astimezone(timezone.utc).replace(tzinfo=None)); o.horizon = "0"
    s = ephem.Sun(o); m = ephem.Moon(o)
    return {"sun_alt_deg": round(math.degrees(s.alt), 1), "sun_az_deg": round(math.degrees(s.az), 0),
            "moon_alt_deg": round(math.degrees(m.alt), 1), "moon_az_deg": round(math.degrees(m.az), 0), "moon_illum_pct": round(m.phase, 1)}

def noaa_sun_alt(dt_local):
    """Independent solar altitude (deg, no refraction) - NOAA Solar Calculator equations (Meeus)."""
    d = dt_local.astimezone(timezone.utc)
    jd = 367 * d.year - int(7 * (d.year + int((d.month + 9) / 12)) / 4) + int(275 * d.month / 9) + d.day + 1721013.5 + (d.hour + d.minute / 60 + d.second / 3600) / 24
    T = (jd - 2451545.0) / 36525
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360
    M = 357.52911 + T * (35999.05029 - 0.0001537 * T)
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    Cc = math.sin(math.radians(M)) * (1.914602 - T * (0.004817 + 0.000014 * T)) + math.sin(math.radians(2 * M)) * (0.019993 - 0.000101 * T) + math.sin(math.radians(3 * M)) * 0.000289
    true_long = L0 + Cc
    omega = 125.04 - 1934.136 * T
    app_long = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    eps0 = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60
    eps = eps0 + 0.00256 * math.cos(math.radians(omega))
    decl = math.degrees(math.asin(math.sin(math.radians(eps)) * math.sin(math.radians(app_long))))
    y = math.tan(math.radians(eps / 2)) ** 2
    eqt = 4 * math.degrees(y * math.sin(2 * math.radians(L0)) - 2 * e * math.sin(math.radians(M)) + 4 * e * y * math.sin(math.radians(M)) * math.cos(2 * math.radians(L0)) - 0.5 * y * y * math.sin(4 * math.radians(L0)) - 1.25 * e * e * math.sin(2 * math.radians(M)))
    minutes_utc = d.hour * 60 + d.minute + d.second / 60
    tst = (minutes_utc + eqt + 4 * LON) % 1440
    ha = tst / 4 - 180
    if ha < -180: ha += 360
    cosz = math.sin(math.radians(LAT)) * math.sin(math.radians(decl)) + math.cos(math.radians(LAT)) * math.cos(math.radians(decl)) * math.cos(math.radians(ha))
    return round(90 - math.degrees(math.acos(max(-1, min(1, cosz)))), 1)

dates = [datetime(1959, 2, 1).date(), datetime(1959, 2, 2).date(), datetime(1959, 2, 26).date(), datetime(1959, 3, 5).date()]
res = {"site": {"lat": LAT, "lon": LON, "elev_m": ELEV, "tz": "UTC+5 (Sverdlovsk 1959; tzdata Asia/Yekaterinburg)"}, "days": {}}
md = ["# Sun and moon at the tent site (generated by astro.py; PyEphem %s)" % ephem.__version__, "",
      f"Site {LAT:.5f} N {LON:.5f} E, {ELEV:.0f} m; all times local UTC+5 (Sverdlovsk decree time 1959, tzdata Asia/Yekaterinburg).", "",
      "| date | astr. dawn | naut. dawn | civil dawn | sunrise | solar noon | sunset | civil dusk | naut. dusk | astr. dusk | day length |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for dt in dates:
    s = sun_events(dt); m = moon_events(dt)
    daylen = s["sunset"] - s["sunrise"]
    res["days"][str(dt)] = {"sun": {k: fmt(v) for k, v in s.items()}, "moon": {k: (fmt(v) if isinstance(v, datetime) else v) for k, v in m.items()},
                            "day_length_h": round(daylen.total_seconds() / 3600, 2)}
    md.append(f"| {dt} | {s['astronomical_dawn'].strftime('%H:%M')} | {s['nautical_dawn'].strftime('%H:%M')} | {s['civil_dawn'].strftime('%H:%M')} | {s['sunrise'].strftime('%H:%M')} | {s['solar_noon'].strftime('%H:%M')} | {s['sunset'].strftime('%H:%M')} | {s['civil_dusk'].strftime('%H:%M')} | {s['nautical_dusk'].strftime('%H:%M')} | {s['astronomical_dusk'].strftime('%H:%M')} | {daylen.total_seconds()/3600:.2f} h |")
md += ["", "| date | moonrise | moonset | illuminated at local noon | previous new moon | next new moon | previous full moon |", "|---|---|---|---|---|---|---|"]
for dt in dates:
    m = res["days"][str(dt)]["moon"]
    md.append(f"| {dt} | {m['moonrise']} | {m['moonset']} | {m['illum_pct_at_noon']} % | {m['prev_new_moon']} | {m['next_new_moon']} | {m['prev_full_moon']} |")
md += ["", "## Sun and moon altitude at selected hours (local UTC+5)", "", "| local time | sun alt (ephem) | sun alt (NOAA check) | sun az | moon alt | moon az | moon illum |", "|---|---|---|---|---|---|---|"]
res["hours"] = {}
for day, hrs in [((1959, 2, 1), [15, 17, 18, 19, 21, 23]), ((1959, 2, 2), [0, 1, 3, 5, 6, 7, 8, 9]), ((1959, 2, 26), [12, 18]), ((1959, 3, 5), [12, 18])]:
    for h in hrs:
        t = datetime(*day, h, 0, tzinfo=UTC5)
        a = altitudes(t); a["sun_alt_noaa_deg"] = noaa_sun_alt(t)
        res["hours"][t.strftime("%Y-%m-%d %H:%M")] = a
        md.append(f"| {t.strftime('%Y-%m-%d %H:%M')} | {a['sun_alt_deg']} | {a['sun_alt_noaa_deg']} | {a['sun_az_deg']:.0f} | {a['moon_alt_deg']} | {a['moon_az_deg']:.0f} | {a['moon_illum_pct']} % |")
# darkness classification for the night of 1-2 Feb
def darkness(a):
    s = a["sun_alt_deg"]
    if s > -0.833: return "daylight"
    if s > -6: return "civil twilight"
    if s > -12: return "nautical twilight"
    if s > -18: return "astronomical twilight"
    return "night"
md += ["", "## Darkness on the night of 1-2 Feb 1959 (sun/moon geometry only; cloud not included)", ""]
for key in ["1959-02-01 17:00", "1959-02-01 18:00", "1959-02-01 21:00", "1959-02-02 01:00", "1959-02-02 06:00", "1959-02-02 08:00", "1959-02-02 09:00"]:
    a = res["hours"][key]
    moon = "moon above horizon (alt %.0f deg, %.0f %% lit)" % (a["moon_alt_deg"], a["moon_illum_pct"]) if a["moon_alt_deg"] > 0 else "moon below horizon"
    md.append(f"- {key}: {darkness(a)} (sun alt {a['sun_alt_deg']} deg); {moon}")
open(os.path.join(OUT, "astro_tables.md"), "w").write("\n".join(md))
json.dump(res, open(os.path.join(OUT, "astro_tables.json"), "w"), indent=1, default=str)
print("\n".join(md))

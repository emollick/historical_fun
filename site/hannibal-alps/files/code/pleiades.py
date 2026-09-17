#!/usr/bin/env python3
"""Dates of the Pleiades' phases in 218 BC (astronomical year -217) at 45 N.

Polybius 3.54.1 puts Hannibal's arrival at the summit of the pass "near the
setting of the Pleiades" (synaptein ten tes Pleiados dysin); Livy 21.35.6
"iam cadente sidere Vergiliarum".  The phrase is a calendar date in the Greek
parapegma tradition: the *morning (cosmical) setting* of the Pleiades, the
season when the cluster is seen for the first time setting in the west at
dawn (Hesiod, Works and Days 383-4, 615-6 ties ploughing and the end of
sailing to it).

Method
  * Star: Alcyone (eta Tau, HIP 17702), Hipparcos J2000 position and proper
    motion; precessed and nutated to the date by Skyfield (IAU 2006 precession,
    IAU 2000A nutation), with aberration, observed from a topocentric observer.
  * Sun: JPL DE406 ephemeris (valid -3000..+3000) through Skyfield.  DE421,
    which the task suggested, stops at 1900; it is unusable for 218 BC.
  * Time: TT from Skyfield's built-in Delta-T tables (Morrison-Stephenson
    long-term parabola before 1600; Delta-T ~ 3.5 h in 218 BC).  Delta-T only
    shifts the local clock time of an event, not its calendar day, by more
    than 0.15 day, and all results are reported to the day.
  * Calendar: proleptic Julian calendar (the calendar Polybius' dates are
    conventionally converted to); JD from the Julian-calendar branch of Meeus,
    Astronomical Algorithms ch. 7.
  * Criterion (the classical "arcus visionis" convention of Ptolemy, Phaseis,
    and Schoch 1924 / Neugebauer HAMA II p. 926ff): the phase falls on the
    day on which the star is on the mathematical horizon (true altitude 0,
    no refraction) at the moment the sun's true altitude equals -h, where h
    is the arcus visionis.  We report h = 6, 7.5, 9 deg (the range the task
    asked for; Schoch's value for the Pleiades' morning setting is about
    11 deg, which we also give), and the "true" phase with the sun's centre
    at -0.833 deg (upper limb on the horizon).
      - morning (cosmical) setting: first morning on which Alcyone sets while
        the sun is still >= h below the horizon (before that day the cluster
        sets in daylight/twilight and is lost).
      - evening (heliacal) setting: last evening on which Alcyone sets after
        the sun is >= h below the horizon (in spring).
      - acronychal (evening) rising: last evening on which Alcyone is seen
        rising with the sun >= h below the horizon (autumn; after that it
        rises in daylight).  Given for completeness.
  * Cross-check: the same events with PyEphem (independent precession code and
    its own analytic Sun).  Agreement to <= 1 day is reported.

Observer: latitude 45.0 N, longitude 7.0 E, at sea level for the geometric
horizon (a real observer at a col sees a raised western horizon, so the
*observed* setting behind a ridge is a day or two later than these dates;
the ancient phrase, however, is calendrical, not an observation from the pass).

Output: data/pleiades_output.json and a printed table.
Usage:  python3 pleiades.py [path/to/de406.bsp]
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
YEAR = -217  # 218 BC
LAT, LON = 45.0, 7.0
DEFAULT_EPH = os.environ.get(
    "HANNIBAL_EPHEMERIS",
    os.path.join(HERE, "de406.bsp"),
)
THRESHOLDS = {"true (sun -0.833)": -0.833, "h=6": -6.0, "h=7.5": -7.5, "h=9": -9.0, "h=11 (Schoch)": -11.0}

# Alcyone, Hipparcos (van Leeuwen 2007) via SIMBAD: HIP 17702
ALCYONE = dict(ra_hours=(3, 47, 29.077), dec_degrees=(24, 6, 18.49), ra_mas_per_year=19.34,
               dec_mas_per_year=-43.67, parallax_mas=8.09)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def jd_julian(Y, M, D):
    """JD at 0h of a proleptic Julian calendar date (Meeus ch. 7, Julian branch)."""
    if M <= 2:
        Y -= 1
        M += 12
    return math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D - 1524.5


def julian_from_jd(jd):
    """Inverse of jd_julian for the Julian calendar (Meeus ch. 7)."""
    jd = jd + 0.5
    Z = math.floor(jd)
    F = jd - Z
    A = Z
    B = A + 1524
    C = math.floor((B - 122.1) / 365.25)
    D = math.floor(365.25 * C)
    E = math.floor((B - D) / 30.6001)
    day = B - D - math.floor(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    return year, month, day


def fmt(jd):
    y, m, d = julian_from_jd(jd)
    return "%d %s %d BC" % (int(d), MONTHS[m - 1], -y + 1)


# ---------------------------------------------------------------- Skyfield
def skyfield_events(eph_path):
    from skyfield.api import Star, load, wgs84
    import numpy as np

    eph = load(eph_path)
    ts = load.timescale()
    earth, sun = eph["earth"], eph["sun"]
    obs = earth + wgs84.latlon(LAT, LON, elevation_m=0)
    star = Star(**ALCYONE)

    def alts(jd_tt):
        t = ts.tt_jd(jd_tt)
        a_star = obs.at(t).observe(star).apparent().altaz()[0].degrees
        a_sun = obs.at(t).observe(sun).apparent().altaz()[0].degrees
        return a_star, a_sun

    def crossing(jd0, jd1, rising):
        """time in [jd0, jd1] where the star's altitude crosses 0 (bisection)."""
        a0, _ = alts(jd0)
        for _ in range(40):
            m = 0.5 * (jd0 + jd1)
            am, _ = alts(m)
            if (am > 0) == (a0 > 0):
                jd0, a0 = m, am
            else:
                jd1 = m
        return 0.5 * (jd0 + jd1)

    def star_horizon_times(jd_day, kind):
        """all star horizon crossings of the given kind in the 24 h from jd_day (local mean midnight)."""
        # local mean midnight in TT ~ UT midnight - LON/360 d (+ Delta T, irrelevant for the day label)
        start = jd_day - LON / 360.0
        grid = np.linspace(start, start + 1.0, 145)  # 10-minute steps
        out = []
        prev = alts(grid[0])[0]
        for i in range(1, len(grid)):
            cur = alts(grid[i])[0]
            if kind == "set" and prev > 0 >= cur:
                out.append(crossing(grid[i - 1], grid[i], False))
            if kind == "rise" and prev <= 0 < cur:
                out.append(crossing(grid[i - 1], grid[i], True))
            prev = cur
        return out

    def daily_sun_alt(jd_day, kind, sun_side):
        """sun altitude at the star's horizon crossing of `kind` nearest sunrise/sunset side"""
        best = None
        for tcross in star_horizon_times(jd_day, kind):
            a_star, a_sun = alts(tcross)
            # choose the crossing where the sun is on the requested side of the sky
            t = ts.tt_jd(tcross)
            az_sun = obs.at(t).observe(sun).apparent().altaz()[1].degrees
            if sun_side == "east" and az_sun < 180 or sun_side == "west" and az_sun >= 180:
                best = (tcross, a_sun)
        return best

    results = {}
    # 1. morning (cosmical) setting: star sets in the west while the sun is in the east below horizon
    days = [jd_julian(YEAR, 9, 1) + i for i in range(0, 122)]
    series = []
    for jd in days:
        r = daily_sun_alt(jd, "set", "east")
        series.append((jd, r[1] if r else float("nan"), r[0] if r else None))
    results["morning_setting"] = first_day_sun_below(series)
    # 2. evening (heliacal) setting: star sets in the west after sunset; last day sun is <= -h at star set
    days = [jd_julian(YEAR, 2, 1) + i for i in range(0, 150)]
    series = []
    for jd in days:
        r = daily_sun_alt(jd, "set", "west")
        series.append((jd, r[1] if r else float("nan"), r[0] if r else None))
    results["evening_setting"] = last_day_sun_below(series)
    # 3. acronychal rising: star rises in the east after sunset (sun in west); first day sun <= -h
    days = [jd_julian(YEAR, 8, 1) + i for i in range(0, 122)]
    series = []
    for jd in days:
        r = daily_sun_alt(jd, "rise", "west")
        series.append((jd, r[1] if r else float("nan"), r[0] if r else None))
    # the star rises ever closer to sunset as autumn advances: LAST evening it is seen rising
    results["acronychal_rising"] = last_day_sun_below(series)
    # 4. heliacal rising: star rises in the east before sunrise; first day sun <= -h at star rise
    days = [jd_julian(YEAR, 4, 15) + i for i in range(0, 90)]
    series = []
    for jd in days:
        r = daily_sun_alt(jd, "rise", "east")
        series.append((jd, r[1] if r else float("nan"), r[0] if r else None))
    results["heliacal_rising"] = first_day_sun_below(series)
    # star position in 218 BC for the record
    t = ts.tt_jd(jd_julian(YEAR, 11, 1))
    ra, dec, _ = earth.at(t).observe(star).apparent().radec(epoch="date")
    results["alcyone_apparent_218BC"] = {"ra_hours": ra.hours, "dec_deg": dec.degrees}
    return results


def first_day_sun_below(series):
    """for each threshold, the first calendar day on which the sun's altitude at the star's
    horizon crossing is <= threshold (sun altitude decreases day by day in this branch)."""
    out = {}
    for name, thr in THRESHOLDS.items():
        found = None
        for jd, a, _ in series:
            if a == a and a <= thr:  # not nan
                found = jd
                break
        out[name] = {"jd": found, "date": fmt(found) if found else None}
    out["_series"] = [(fmt(jd), round(a, 2)) for jd, a, _ in series if a == a][::5]
    return out


def last_day_sun_below(series):
    out = {}
    for name, thr in THRESHOLDS.items():
        found = None
        for jd, a, _ in series:
            if a == a and a <= thr:
                found = jd
        out[name] = {"jd": found, "date": fmt(found) if found else None}
    out["_series"] = [(fmt(jd), round(a, 2)) for jd, a, _ in series if a == a][::5]
    return out


# ---------------------------------------------------------------- PyEphem cross-check
def ephem_events():
    import ephem

    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(LAT), str(LON), 0
    obs.pressure = 0  # no refraction: geometric horizon
    obs.horizon = "0"
    alc = ephem.FixedBody()
    alc._ra = ephem.hours("3:47:29.077")
    alc._dec = ephem.degrees("24:06:18.49")
    alc._epoch = ephem.J2000
    alc._pmra, alc._pmdec = 19.34, -43.67
    sun = ephem.Sun()

    def sun_alt_at(d):
        obs.date = d
        sun.compute(obs)
        return math.degrees(sun.alt), math.degrees(sun.az)

    def scan(m0, ndays, kind, side):
        series = []
        for i in range(ndays):
            # ephem uses the Julian calendar before 1582
            jd0 = jd_julian(YEAR, m0[0], m0[1]) + i
            d0 = ephem.Date(jd0 - 2415020.0 - LON / 360.0)  # ephem's epoch is 1899 Dec 31 12h = JD 2415020
            obs.date = d0
            try:
                if kind == "set":
                    ev = obs.next_setting(alc, start=d0)
                else:
                    ev = obs.next_rising(alc, start=d0)
            except Exception:  # noqa: BLE001
                series.append((jd0, float("nan"), None))
                continue
            a, az = sun_alt_at(ev)
            ok = (side == "east" and az < 180) or (side == "west" and az >= 180)
            if not ok:
                # take the following crossing of the same kind
                try:
                    ev = obs.next_setting(alc, start=ev + 0.01) if kind == "set" else obs.next_rising(alc, start=ev + 0.01)
                    a, az = sun_alt_at(ev)
                except Exception:  # noqa: BLE001
                    series.append((jd0, float("nan"), None))
                    continue
            series.append((jd0, a, ev))
        return series

    res = {
        "morning_setting": first_day_sun_below(scan((9, 1), 122, "set", "east")),
        "evening_setting": last_day_sun_below(scan((2, 1), 150, "set", "west")),
        "acronychal_rising": last_day_sun_below(scan((8, 1), 122, "rise", "west")),
        "heliacal_rising": first_day_sun_below(scan((4, 15), 90, "rise", "east")),
    }
    obs.date = ephem.Date(jd_julian(YEAR, 11, 1) - 2415020.0)
    alc.compute(obs)
    res["alcyone_apparent_218BC"] = {"ra_hours": float(alc.ra) * 12 / math.pi, "dec_deg": math.degrees(float(alc.dec))}
    return res


def main():
    eph_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EPH
    out = {"year": "218 BC (astronomical -217)", "observer": {"lat": LAT, "lon": LON}, "calendar": "proleptic Julian",
           "criterion": "star true altitude 0 (mathematical horizon, no refraction) when the sun's true altitude = -h",
           "thresholds_deg": THRESHOLDS}
    if os.path.exists(eph_path):
        out["skyfield"] = skyfield_events(eph_path)
        out["skyfield"]["ephemeris"] = os.path.basename(eph_path)
    else:
        out["skyfield"] = {"error": "ephemeris not found: %s" % eph_path}
    try:
        out["pyephem"] = ephem_events()
    except Exception as e:  # noqa: BLE001
        out["pyephem"] = {"error": str(e)}
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "pleiades_output.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("Pleiades (Alcyone) phases, 218 BC, lat 45N lon 7E, Julian calendar")
    for ev in ["morning_setting", "evening_setting", "acronychal_rising", "heliacal_rising"]:
        print("\n%s" % ev)
        for name in THRESHOLDS:
            s = out["skyfield"].get(ev, {}).get(name, {}).get("date") if "error" not in out["skyfield"] else "n/a"
            p = out["pyephem"].get(ev, {}).get(name, {}).get("date") if "error" not in out["pyephem"] else "n/a"
            print("  %-20s skyfield/DE406: %-16s pyephem: %-16s" % (name, s, p))
    for k in ("skyfield", "pyephem"):
        if "alcyone_apparent_218BC" in out[k]:
            a = out[k]["alcyone_apparent_218BC"]
            print("%s Alcyone apparent RA %.3f h, Dec %+.2f deg (1 Nov 218 BC)" % (k, a["ra_hours"], a["dec_deg"]))
    print("\nwrote", os.path.join(DATA, "pleiades_output.json"))


if __name__ == "__main__":
    main()

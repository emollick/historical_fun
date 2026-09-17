#!/usr/bin/env python3
"""Sun and moon at Grinder's Stand on the night of 10-11 October 1809.

Site: Meriwether Lewis grave and Grinder's Stand site, Natchez Trace Parkway, Lewis County, Tennessee.
Coordinates used: 35.5215 N, 87.4569 W (the monument; the stand stood a few tens of metres from it).
Times are given in UTC and in local mean solar time (LMT = UTC - 5h 49m 50s for 87.4569 W).
Nobody at the stand had a clock set to a standard; "about three o'clock" in the accounts means a
guess at local time, so LMT (or apparent solar time, which on 10 October runs about 13 minutes
ahead of mean time) is the right frame.
Requires: pip install ephem (PyEphem, VSOP87/ELP-based; accuracy far better than needed).
"""
import ephem, datetime as dt

lat, lon = 35.5215, -87.4569
obs = ephem.Observer()
obs.lat, obs.lon = str(lat), str(lon)
obs.elevation = 280
obs.pressure = 0          # no refraction fudge beyond ephem's default horizon handling
obs.horizon = '-0:34'     # standard refraction at the horizon for rise/set

def lmt(d):
    """convert an ephem.Date (UTC) to local mean time string"""
    t = ephem.Date(d).datetime() + dt.timedelta(hours=lon/15.0)
    return t.strftime('%Y-%m-%d %H:%M')

sun, moon = ephem.Sun(), ephem.Moon()
print("Site lat/lon:", lat, lon, "; LMT offset (h):", round(lon/15.0, 3))
print()
# phases around the date
d0 = ephem.Date('1809/10/01')
print("New moon before:", ephem.previous_new_moon('1809/10/11'), "UTC ->", lmt(ephem.previous_new_moon('1809/10/11')), "LMT")
print("First quarter:  ", ephem.next_first_quarter_moon('1809/10/01'), "UTC ->", lmt(ephem.next_first_quarter_moon('1809/10/01')), "LMT")
print("Full moon:      ", ephem.next_full_moon('1809/10/01'), "UTC ->", lmt(ephem.next_full_moon('1809/10/01')), "LMT")
print("Last quarter:   ", ephem.next_last_quarter_moon('1809/10/01'), "UTC ->", lmt(ephem.next_last_quarter_moon('1809/10/01')), "LMT")
print()
# evening of 10 Oct: sunset; moonrise/moonset; moon phase & altitude at 03:00 LMT 11 Oct
obs.date = ephem.Date('1809/10/10 12:00')  # noon UTC ~ 06:10 LMT on the 10th
ss = obs.next_setting(sun)
print("Sunset 10 Oct:", ss, "UTC ->", lmt(ss), "LMT")
obs.date = ss
sr = obs.next_rising(sun)
print("Sunrise 11 Oct:", sr, "UTC ->", lmt(sr), "LMT")
# civil twilight
obs.horizon = '-6'
obs.date = ephem.Date('1809/10/10 12:00')
ct_e = obs.next_setting(sun, use_center=True)
obs.date = ct_e
ct_m = obs.next_rising(sun, use_center=True)
print("End of civil twilight 10 Oct:", lmt(ct_e), "LMT; start of civil twilight 11 Oct:", lmt(ct_m), "LMT")
obs.horizon = '-0:34'
# moon
obs.date = ephem.Date('1809/10/10 12:00')
mr = obs.next_rising(moon)
obs.date = ephem.Date('1809/10/10 12:00')
ms = obs.next_setting(moon)
print("Moonrise (next after 06 LMT 10 Oct):", lmt(mr), "LMT")
print("Moonset  (next after 06 LMT 10 Oct):", lmt(ms), "LMT")
obs.date = ms
mr2 = obs.next_rising(moon)
print("Following moonrise:", lmt(mr2), "LMT")
for hh in ['1809/10/11 01:00','1809/10/11 03:00','1809/10/11 05:00','1809/10/11 07:00','1809/10/11 08:50','1809/10/11 11:00']:
    # these strings are UTC; convert LMT wanted -> UTC: LMT 19:10 on 10th = 01:00 UTC 11th etc.
    obs.date = ephem.Date(hh)
    moon.compute(obs); sun.compute(obs)
    print(f"{hh} UTC = {lmt(obs.date)} LMT: moon alt {float(moon.alt)*57.2958:6.1f} deg, az {float(moon.az)*57.2958:6.1f}, illuminated {moon.phase:5.1f}% ; sun alt {float(sun.alt)*57.2958:6.1f}")

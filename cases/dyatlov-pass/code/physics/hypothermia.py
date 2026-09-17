"""
hypothermia.py -- Part B.4: time to incapacitation / unconsciousness / death for
lightly clothed people at -25 to -30 C in 5-20 m/s wind.

Two independent estimates are produced:

 1. Wind-chill equivalent temperature (Osczevski & Bluestein 2005, BAMS 86:1453,
    the Environment Canada / NWS JAG/TI formula; also used, via GOST R ISO 15743, by
    Pigol'tsyna 2020):
        T_wc = 13.12 + 0.6215 T - 11.37 V^0.16 + 0.3965 T V^0.16   (T in C, V in km/h at 10 m)
    with the standard frostbite-time bands (Environment Canada): -28..-40 C 10-30 min,
    -40..-48 C 5-10 min, -48..-55 C 2-5 min for exposed skin.

 2. A single-compartment heat-balance model of the Tikuisis (1995) type
    (Int J Biometeorol 39:94-102): core -> tissue shell -> clothing -> boundary
    layer, resting metabolism + shivering driven by core and skin temperature,
    end points at core temperature 34 C (incapacitation: loss of dexterity,
    confusion), 30 C (unconsciousness; Tikuisis' survival end point), 28 C (high
    risk of cardiac arrest; WMS 2019 'severe' < 28 C).
    This is NOT the Tikuisis model itself (whose code is not public); the
    published anchor points of that model are used to check the implementation:
      nude, calm air (1 km/h): 1.8 h @ -30 C, 2.5 h @ -20 C, 4.1 h @ -10 C
      two loose 1-mm layers, 5 km/h wind: 8.6 h @ -30 C, 15.4 h @ -20 C.

Outputs: fig_B4_survival.png, hypothermia_results.txt
Run:  python3 hypothermia.py
"""
from __future__ import annotations

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "hypothermia_results.txt"), "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


# ------------------------------------------------------------------ wind chill
def wind_chill(T_c, V_ms):
    V = max(V_ms * 3.6, 4.8)          # formula valid for V >= 4.8 km/h
    return 13.12 + 0.6215 * T_c - 11.37 * V ** 0.16 + 0.3965 * T_c * V ** 0.16


def frostbite_band(twc):
    if twc > -28:
        return "low risk (>30 min)"
    if twc > -40:
        return "exposed skin freezes in 10-30 min"
    if twc > -48:
        return "5-10 min"
    if twc > -55:
        return "2-5 min"
    return "< 2 min"


log("== 1. Wind chill (Osczevski & Bluestein 2005) ==")
log(" T(C)  V(m/s)   T_wc(C)   frostbite of exposed skin")
for T in (-20, -25, -30):
    for V in (2.5, 5, 10, 15, 20):
        twc = wind_chill(T, V)
        log(f" {T:4d}   {V:4.1f}    {twc:6.1f}    {frostbite_band(twc)}")
log("Pigol'tsyna (2020, Trudy GGO 597, Table 3) computed for the tent site: -30.3 C at 19 h, -36.5 at 23 h, "
    "-45.9 at 03 h, -50.5 at 07 h on 2 Feb 1959 (air -17.9 / -22.5 / -28.7 / -31.7 C, wind 9.2 / 9.4 / 11.3 / 12.4 m/s).")

# ------------------------------------------------------------------ heat-balance model
CLO = 0.155                # m2 K / W per clo
SIGMA_SB = 5.67e-8


def h_conv(V, dT=40.0):
    """Convection coefficient W/m2K: max(natural convection 2.4 dT^0.25, forced 8.3 sqrt(V))."""
    return max(2.4 * dT ** 0.25, 8.3 * math.sqrt(max(V, 0.1)))


def clothing_eff(I_cl_clo, V):
    """Effective intrinsic clothing insulation reduced by wind penetration/compression
    (Havenith / ISO 9920: roughly 30 % loss at 3.5 m/s for permeable clothing; extrapolated
    and capped at 65 % loss for strong wind). Returns m2K/W."""
    loss = min(0.65, 0.28 * math.log1p(V))
    return I_cl_clo * CLO * (1.0 - loss)


def survival_times(T_a, V, I_cl_clo, mass=70.0, area=1.85, activity_W=0.0, activity_h=1.5,
                   wet=False, shiver_sustained_Wm2=150.0, shiver_endurance_h=6.0,
                   dt=10.0, t_max_h=30.0):
    """Integrate a single-compartment body until core temperature reaches 34 / 30 / 28 C.
    Tissue (vasoconstricted) insulation 0.09 m2K/W; boundary layer 1/(h_c + h_r).
    Shivering: Hayward-type drive from core and skin temperature, capped at a sustainable
    ~2.5 x resting level, fading linearly to zero over shiver_endurance_h (shivering
    fatigue -- Tikuisis 1995 notes survival is governed by shivering endurance when heat
    balance is reached), and ceasing below ~31 C core.  Activity heat (walking) is only
    available for activity_h hours.  'wet' removes 60 % of clothing insulation."""
    c_body = 3470.0 * mass                       # J/K
    I_t = 0.09                                   # m2K/W tissue (vasoconstricted)
    I_cl = clothing_eff(I_cl_clo, V) * (0.4 if wet else 1.0)
    T_core = 37.0
    t = 0.0
    hits = {}
    M_rest = 58.0 * area                         # 1 met = 58 W/m2
    while t < t_max_h * 3600:
        h_r = 4.0
        I_a = 1.0 / (h_conv(V, max(5.0, 30.0 - T_a)) + h_r)
        R_tot = I_t + I_cl + I_a                 # m2K/W, core to air
        T_sk = T_core - (T_core - T_a) * I_t / R_tot
        M_sh = 155.5 * (37.0 - T_core) + 47.0 * (33.0 - T_sk) - 1.57 * (33.0 - T_sk) ** 2
        M_sh = max(0.0, min(shiver_sustained_Wm2, M_sh))
        M_sh *= max(0.0, 1.0 - t / (shiver_endurance_h * 3600.0))
        if T_core < 31.0:
            M_sh *= max(0.0, (T_core - 29.0) / 2.0)
        act = activity_W if t < activity_h * 3600.0 else 0.0
        M = M_rest + M_sh * area + act
        H_resp = 0.0014 * M * (34.0 - T_a) + 0.0173 * M * 5.0
        H_skin = area * (T_core - T_a) / R_tot
        dT = (M - H_skin - H_resp) / c_body * dt
        T_core += dT
        t += dt
        for thr in (34.0, 30.0, 28.0):
            if thr not in hits and T_core <= thr:
                hits[thr] = t / 3600.0
        if 28.0 in hits:
            break
    return hits


def fmt(h, k):
    return f"{h[k]:5.1f}" if k in h else " >30 "


log("\n== 2. Heat-balance model: anchor check against Tikuisis (1995) published points ==")
log("   (his end point is core 30 C; sedentary; 'nude, 1 km/h' and 'two loose 1-mm layers, 5 km/h')")
log("   The sketch model is tuned only through sustained shivering (150 W/m2, 6 h endurance) and tissue insulation 0.09 m2K/W.")
for T in (-30, -20, -10):
    h = survival_times(T, 0.3, 0.0)
    log(f"   nude, calm, {T:4d} C: model t(30 C) = {fmt(h, 30.0)} h   (Tikuisis: {dict([(-30,1.8),(-20,2.5),(-10,4.1)])[T]} h)")
for T in (-30, -20):
    h = survival_times(T, 1.4, 0.9)
    log(f"   2 loose layers (taken as 0.9 clo), 5 km/h, {T:4d} C: model t(30 C) = {fmt(h, 30.0)} h   (Tikuisis: {dict([(-30,8.6),(-20,15.4)])[T]} h)")

log("\n== 3. Dyatlov scenarios: time (h) to core 34 C (incapacitation) / 30 C (unconscious) / 28 C ==")
log("   clothing: 0.5 clo = shirt+trousers+socks (Dyatlov, Kolmogorova, Slobodin-type), "
    "1.0 clo = plus sweater/jacket (Thibeaux, Zolotaryov-type); no boots, hands bare.")
log(" T(C)  V(m/s)  clo  wet  activity |  t34   t30   t28   (h)")
rows = []
for T in (-25, -30):
    for V in (5, 10, 15, 20):
        for clo in (0.5, 1.0):
            for wet in (False, True):
                for act in (0.0, 150.0):
                    h = survival_times(T, V, clo, wet=wet, activity_W=act)
                    rows.append((T, V, clo, wet, act, h))
                    if act == 0.0 or (V in (5, 15) and clo == 0.5):
                        log(f" {T:4d}   {V:4d}   {clo:3.1f}  {'y' if wet else 'n'}   {act:4.0f} W  | "
                            f"{fmt(h,34.0)} {fmt(h,30.0)} {fmt(h,28.0)}")

# figure: time to 30 C vs wind for the scenarios
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
Vgrid = np.linspace(2, 20, 19)
for ax, T in zip(axes, (-25, -30)):
    for clo, col in ((0.5, "tab:red"), (1.0, "tab:blue")):
        for wet, ls in ((False, "-"), (True, "--")):
            t30 = [survival_times(T, V, clo, wet=wet).get(30.0, np.nan) for V in Vgrid]
            t34 = [survival_times(T, V, clo, wet=wet).get(34.0, np.nan) for V in Vgrid]
            ax.plot(Vgrid, t30, color=col, ls=ls, label=f"{clo} clo{' wet' if wet else ''}: core 30 C")
            ax.plot(Vgrid, t34, color=col, ls=ls, lw=0.8, alpha=0.6)
    ax.axhspan(2, 3, color="grey", alpha=0.15)
    ax.text(2.2, 2.35, "1959 rescuers' estimate 2-3 h", fontsize=8)
    ax.set_title(f"air temperature {T} C (thin lines: core 34 C = incapacitation)")
    ax.set_xlabel("wind speed (m/s)")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("hours after leaving the tent")
axes[0].set_ylim(0, 12)
axes[0].legend(fontsize=7)
fig.suptitle("Single-compartment heat-balance model (Tikuisis-type), resting, 70 kg, shivering endurance 6 h; not a substitute for a validated model", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B4_survival.png"), dpi=150)

log("\nWhat the estimate cannot capture: individual variation (body fat, sex, size: Dubinina 20 y, small; "
    "Zolotaryov 38 y), exercise-induced heat then exhaustion, wet clothing from snow, paradoxical "
    "undressing, frostbite-caused loss of hand function (which ends the ability to build shelter or a fire "
    "long before core hypothermia), huddling (the Cedar pair), the snow den's shelter, injuries and shock. "
    "Shivering endurance and vasoconstriction are modelled crudely; the model is only good to a factor ~2.")
OUT.close()
print("done")

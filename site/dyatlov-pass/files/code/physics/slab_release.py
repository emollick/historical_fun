"""
slab_release.py -- Part B.1 / B.3: replication and stress-testing of the delayed
slab-release model of Gaume & Puzrin (2021), doi:10.1038/s43247-020-00081-8.

Outputs (written next to this script):
  fig_B1_delay_vs_slope.png       time-to-release vs weak-layer slope for several
                                  wind deposition fluxes Q (paper's other parameters)
  fig_B1_regime_map.png           regime map in (slope, friction angle) space
  fig_B1_delay_vs_Q.png           delay vs Q with the Sturm & Stuefer (2013) flux envelope
  fig_B1_sensitivity.png          one-at-a-time sensitivity (tornado) of dt_max
  fig_B3_lowslope_window.png      (phi, c) window allowing a 9-13 h delayed release at
                                  22, 23, 25, 28, 30 deg
  slab_release_results.txt        all printed numbers

Run:  python3 slab_release.py
"""
from __future__ import annotations

import math
import os
from dataclasses import replace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gp_model import (Params, delay_bounds_h, hw0_max, hw0_min, regime,
                      slab_dimensions, tan_phi_max, tan_phi_min,
                      time_to_release_h, critical_crack_length)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "slab_release_results.txt"), "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


# --------------------------------------------------------------------------
# 0. Replication of the paper's Dyatlov numbers
# --------------------------------------------------------------------------
base = Params()
a, b, ta, tb = delay_bounds_h(base)
log("== 0. Replication of Gaume & Puzrin (2021) 'The Dyatlov case' ==")
log(f"L0={base.L0:.3f} m  lambda0={base.lambda0:.2f}  r1={base.r1:.3f}")
log(f"phi_min={math.degrees(math.atan(tan_phi_min(base))):.2f} deg  "
    f"phi_max(lambda0)={math.degrees(math.atan(tan_phi_max(base, base.lambda0))):.2f} deg")
log(f"hw0_min={a:.3f} m (paper 0.24)   hw0_max={b:.3f} m (paper 0.44)")
log(f"dt_min={ta:.2f} h (paper 7.2)     dt_max={tb:.2f} h (paper 13.5)")
sd = slab_dimensions(base)
log(f"tension crack at lcw={sd['lcw']:.2f} m (paper 4.95); width B={sd['B']:.2f} m (paper 8.8); "
    f"line mass={sd['line_mass']:.0f} kg/m; slab mass={sd['mass']/1000:.1f} t; volume={sd['volume']:.1f} m^3")
# cohesion limit for which a finite hw0_max still exists (paper: c ~ 440 Pa at phi=20)
for c in (300, 400, 440, 450, 500, 600):
    p = replace(base, c=c)
    log(f"   c={c:4d} Pa: hw0_min={hw0_min(p):.3f}  hw0_max={hw0_max(p):.3f}  -> {regime(p)}")

# --------------------------------------------------------------------------
# 1. Time-to-release vs slope angle for several deposition fluxes
# --------------------------------------------------------------------------
log("\n== 1. Delay vs weak-layer slope angle (all other parameters as in the paper) ==")
alphas = np.arange(18.0, 36.01, 0.25)
Qs = [0.002, 0.004, 0.008, 0.016, 0.032, 0.064]
fig, ax = plt.subplots(figsize=(8.5, 5.5))
colors = plt.cm.viridis(np.linspace(0.05, 0.95, len(Qs)))
for Q, col in zip(Qs, colors):
    tmin = []
    tmax = []
    for al in alphas:
        p = replace(base, alpha_deg=float(al), Q=Q)
        _, _, t1, t2 = delay_bounds_h(p)
        tmin.append(t1 if t1 > 0 else np.nan)
        tmax.append(t2 if t2 > 0 else np.nan)
    tmin, tmax = np.array(tmin), np.array(tmax)
    ax.fill_between(alphas, tmin, np.where(np.isfinite(tmax), tmax, 1e3), color=col, alpha=0.18)
    ax.plot(alphas, tmin, color=col, lw=1.8, label=f"Q = {Q} kg/m/s")
    ax.plot(alphas, tmax, color=col, lw=1.8, ls="--")
ax.axhspan(9.5, 13.5, color="red", alpha=0.10)
ax.text(18.3, 11.0, "forensic window 9.5-13.5 h", color="darkred", fontsize=9)
ax.set_yscale("log")
ax.set_ylim(0.3, 300)
ax.set_xlim(18, 36)
ax.set_xlabel("weak-layer inclination alpha (deg)")
ax.set_ylabel("time to release after the cut (h)")
ax.set_title("Gaume-Puzrin model: delay bounds vs slope (solid: no sintering; dashed: full sintering)\n"
             "phi = 20 deg, c = 440 Pa, h0 = 0.5 m, hc = 0.1 m, lc = 4 m, le0 = 1 m, K0 = 0.5")
ax.legend(fontsize=8, loc="upper right")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B1_delay_vs_slope.png"), dpi=150)

for al in (22, 23, 25, 28, 30):
    p = replace(base, alpha_deg=al)
    hmin, hmax, t1, t2 = delay_bounds_h(p)
    log(f"alpha={al:2d} deg: phi_min={math.degrees(math.atan(tan_phi_min(p))):5.2f}  "
        f"phi_max(l0)={math.degrees(math.atan(tan_phi_max(p, p.lambda0))):5.2f}  "
        f"hw0=[{hmin:.3f},{hmax:.3f}] m  dt=[{t1:.2f},{t2:.2f}] h  -> {regime(p)}")

# --------------------------------------------------------------------------
# 2. Regime map in (alpha, phi) space, paper's other parameters
# --------------------------------------------------------------------------
log("\n== 2. Regime map ==")
al_grid = np.linspace(15, 40, 126)
ph_grid = np.linspace(5, 40, 141)
Z = np.zeros((len(ph_grid), len(al_grid)))
T = np.full_like(Z, np.nan)
for i, ph in enumerate(ph_grid):
    for j, al in enumerate(al_grid):
        p = replace(base, alpha_deg=float(al), phi_deg=float(ph))
        r = regime(p)
        Z[i, j] = {"immediate failure at cut": 0, "delayed release": 2,
                   "delayed release only if wind snow does not sinter": 1,
                   "no release (wind load never reaches peak strength)": 3}[r]
        if Z[i, j] == 2:
            T[i, j] = delay_bounds_h(p)[3]
fig, ax = plt.subplots(figsize=(8.5, 5.5))
cmap = matplotlib.colors.ListedColormap(["#d9534f", "#f0ad4e", "#5cb85c", "#9e9e9e"])
ax.pcolormesh(al_grid, ph_grid, Z, cmap=cmap, vmin=-0.5, vmax=3.5, shading="auto")
cs = ax.contour(al_grid, ph_grid, T, levels=[2, 5, 9.5, 13.5, 24, 48], colors="k", linewidths=0.8)
ax.clabel(cs, fmt="%g h", fontsize=8)
ax.plot([28], [20], "k*", ms=14, label="paper's Dyatlov point (28 deg, 20 deg)")
ax.axvline(23, color="k", ls=":", lw=1)
ax.text(23.2, 36, "23 deg (commonly cited)", fontsize=8)
ax.axvline(21, color="k", ls=":", lw=1)
ax.text(15.3, 36, "21 deg (Popovnin 2019)", fontsize=8)
ax.set_xlabel("weak-layer inclination alpha (deg)")
ax.set_ylabel("weak-layer friction angle phi (deg)")
ax.set_title("Regimes (c = 440 Pa, Q = 0.008 kg/m/s): red = fails at the cut, green = delayed release\n"
             "(contours: upper-bound delay dt_max), orange = only without sintering, grey = never releases")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B1_regime_map.png"), dpi=150)

# --------------------------------------------------------------------------
# 3. Delay vs Q, with the Sturm & Stuefer (2013) flux envelope
#    Q_upper = 1.3e-3 w^2.5, Q_lower = 3.3e-9 w^6.5 (kg/m/s, w in m/s, w > 5 m/s)
# --------------------------------------------------------------------------
log("\n== 3. Delay vs deposition flux Q ==")
Qgrid = np.logspace(-3.3, -0.3, 200)
fig, ax = plt.subplots(figsize=(8.5, 5.5))
for al, col in zip((23, 25, 28, 30), ("tab:red", "tab:orange", "tab:green", "tab:blue")):
    p = replace(base, alpha_deg=al)
    hmin, hmax, _, _ = delay_bounds_h(p)
    if hmin <= 0 or not math.isfinite(hmin):
        log(f"alpha={al}: no delayed release with paper parameters ({regime(p)})")
        continue
    t1 = np.array([time_to_release_h(replace(p, Q=q), hmin) for q in Qgrid])
    t2 = np.array([time_to_release_h(replace(p, Q=q), hmax) for q in Qgrid])
    ax.fill_between(Qgrid, t1, t2 if np.all(np.isfinite(t2)) else t1 * 10, color=col, alpha=0.2)
    ax.plot(Qgrid, t1, color=col, label=f"alpha = {al} deg")
ax.axhspan(9.5, 13.5, color="red", alpha=0.1)
for w, ls in ((5, ":"), (8, "--"), (10, "-."), (12, "-")):
    qu, ql = 1.3e-3 * w ** 2.5, 3.3e-9 * w ** 6.5
    ax.axvspan(ql, qu, color="grey", alpha=0.06)
    ax.axvline(ql, color="grey", ls=ls, lw=0.8)
    ax.axvline(qu, color="grey", ls=ls, lw=0.8)
    ax.text(ql, 0.4, f"{w} m/s", fontsize=7, rotation=90, va="bottom", color="grey")
    ax.text(qu, 0.4, f"{w} m/s", fontsize=7, rotation=90, va="bottom", color="grey")
    log(f"Sturm&Stuefer envelope at w={w} m/s: Q_lower={ql:.2e}, Q_upper={qu:.2e} kg/m/s")
ax.axvline(0.008, color="k", lw=1.2)
ax.text(0.0085, 100, "paper's Q = 0.008", fontsize=8)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("wind deposition flux Q (kg m$^{-1}$ s$^{-1}$)")
ax.set_ylabel("time to release (h)")
ax.set_ylim(0.3, 1000)
ax.set_title("Delay is inversely proportional to Q; grey bands = Sturm & Stuefer (2013)\n"
             "lower/upper fence-flux bounds for 5, 8, 10, 12 m/s winds")
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B1_delay_vs_Q.png"), dpi=150)
for w in (5, 8, 9, 10, 12, 15):
    qu, ql = 1.3e-3 * w ** 2.5, 3.3e-9 * w ** 6.5
    log(f"  w={w:2d} m/s: dt_max = {time_to_release_h(replace(base, Q=qu), b):8.2f} h (upper-bound flux) ... "
        f"{time_to_release_h(replace(base, Q=ql), b):8.2f} h (lower-bound flux)")

# --------------------------------------------------------------------------
# 4. One-at-a-time sensitivity of dt_max and dt_min (paper's point)
# --------------------------------------------------------------------------
log("\n== 4. Sensitivity (one-at-a-time, +/-10 % or +/-1 deg) around the paper's point ==")
pert = {"alpha_deg": 1.0, "phi_deg": 1.0, "c": 44.0, "h0": 0.05, "hc": 0.01, "lc": 0.4,
        "le0": 0.1, "rho": 30.0, "rho_w": 40.0, "K0": 0.05, "Q": 0.0008}
rows = []
for k, dv in pert.items():
    v0 = getattr(base, k)
    res = []
    for sgn in (-1, +1):
        p = replace(base, **{k: v0 + sgn * dv})
        _, _, t1, t2 = delay_bounds_h(p)
        res.append((t1, t2, regime(p)))
    lo, hi = res
    rows.append((k, v0, dv, lo, hi))
    log(f"{k:9s} {v0:8.3f} -{dv:g}: dt=[{lo[0]:6.2f},{lo[1]:6.2f}] ({lo[2]});  "
        f"+{dv:g}: dt=[{hi[0]:6.2f},{hi[1]:6.2f}] ({hi[2]})")
fig, ax = plt.subplots(figsize=(8.5, 5.5))
names = [f"{r[0]} ({r[1]:g} +/- {r[2]:g})" for r in rows]
lo_vals = [r[3][1] if math.isfinite(r[3][1]) and r[3][1] > 0 else np.nan for r in rows]
hi_vals = [r[4][1] if math.isfinite(r[4][1]) and r[4][1] > 0 else np.nan for r in rows]
y = np.arange(len(rows))
ax.barh(y, np.nan_to_num(np.array(lo_vals) - tb, nan=0), left=tb, color="tab:blue", alpha=0.7, label="parameter - delta")
ax.barh(y, np.nan_to_num(np.array(hi_vals) - tb, nan=0), left=tb, color="tab:orange", alpha=0.7, label="parameter + delta")
for i, (lv, hv, r) in enumerate(zip(lo_vals, hi_vals, rows)):
    if np.isnan(lv):
        ax.text(tb + 0.3, i, f"-: {r[3][2]}", fontsize=7, va="center")
    if np.isnan(hv):
        ax.text(tb + 0.3, i - 0.3, f"+: {r[4][2]}", fontsize=7, va="center")
ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=8)
ax.axvline(tb, color="k")
ax.set_xlabel("upper-bound delay dt_max (h)")
ax.set_title("One-at-a-time sensitivity of the upper-bound delay (paper point: 13.5 h)")
ax.legend(fontsize=8)
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B1_sensitivity.png"), dpi=150)

# --------------------------------------------------------------------------
# 5. Part B.3: what (phi, c) allow a 9-13 h delayed release on low slopes?
# --------------------------------------------------------------------------
log("\n== 5. Low-slope window: (phi, c) combinations giving a 9.5-13.5 h release (Q = 0.008) ==")
ph_grid = np.linspace(5, 32, 109)
c_grid = np.linspace(0, 1500, 121)
fig, axes = plt.subplots(1, 5, figsize=(16, 4.2), sharey=True)
for ax, al in zip(axes, (22, 23, 25, 28, 30)):
    W = np.full((len(c_grid), len(ph_grid)), np.nan)
    D = np.zeros_like(W)
    for i, c in enumerate(c_grid):
        for j, ph in enumerate(ph_grid):
            p = replace(base, alpha_deg=al, phi_deg=float(ph), c=float(c))
            if regime(p) != "delayed release":
                continue
            _, _, t1, t2 = delay_bounds_h(p)
            D[i, j] = 1
            if t1 <= 13.5 and t2 >= 9.5:          # bounds overlap the forensic window
                W[i, j] = t2
    ax.pcolormesh(ph_grid, c_grid, D, cmap="Greys", vmin=0, vmax=3, shading="auto")
    m = ax.pcolormesh(ph_grid, c_grid, W, cmap="viridis", vmin=5, vmax=40, shading="auto")
    ax.set_title(f"alpha = {al} deg")
    ax.set_xlabel("phi (deg)")
    ax.axvspan(12, 28, color="tab:red", alpha=0.07)
    ax.axhspan(100, 1500, color="tab:blue", alpha=0.05)
    ax.axhline(170, color="tab:blue", ls=":", lw=0.8)
    ax.axhline(440, color="k", ls="--", lw=0.8)
    if al == 28:
        ax.plot([20], [440], "k*", ms=12)
    n_ok = np.isfinite(W).sum()
    frac = n_ok / D.sum() if D.sum() else 0
    log(f"alpha={al}: delayed-release cells={int(D.sum())}, cells overlapping 9.5-13.5 h={n_ok}; "
        f"phi range with any delayed release: "
        f"{ph_grid[np.any(D > 0, axis=0)].min() if D.sum() else float('nan'):.1f}-"
        f"{ph_grid[np.any(D > 0, axis=0)].max() if D.sum() else float('nan'):.1f} deg")
    if n_ok:
        ii, jj = np.where(np.isfinite(W))
        log(f"          window: phi {ph_grid[jj].min():.1f}-{ph_grid[jj].max():.1f} deg, "
            f"c {c_grid[ii].min():.0f}-{c_grid[ii].max():.0f} Pa")
axes[0].set_ylabel("weak-layer cohesion c (Pa)")
fig.suptitle("Grey: delayed release possible; colour: upper-bound delay when the bounds overlap 9.5-13.5 h. "
             "Red band: Reiweger et al. (2015) friction 12-28 deg; dotted: their c = 170 Pa; dashed: paper c = 440 Pa",
             fontsize=9)
fig.colorbar(m, ax=axes, label="dt_max (h)", shrink=0.8)
fig.savefig(os.path.join(HERE, "fig_B3_lowslope_window.png"), dpi=150)

# --------------------------------------------------------------------------
# 6. Anticrack critical crack length as an independent scale check
# --------------------------------------------------------------------------
log("\n== 6. Critical crack length (Gaume et al. 2017 form) for comparison ==")
for al in (21, 23, 25, 28, 30):
    for D in (0.5, 1.0):
        tau_p = 300 * 9.81 * D * math.cos(math.radians(al)) * math.tan(math.radians(20)) + 440
        ac = critical_crack_length(D, 300, al, tau_p)
        log(f"alpha={al} D={D} m: tau_p={tau_p:.0f} Pa, a_c={ac:.2f} m")
log("(a_c of order 0.2-0.45 m -- far shorter than the ~6.5 m cut and the ~5 m wind-loaded zone -- means that once the weak layer "
    "yields over the cut, self-sustained propagation is plausible; a_c = 0 marks cases where the slab is already at failure; "
    "this is a scale check with the anticrack formula, not a replication of the paper.)")
OUT.close()
print("done")

"""
slab_impact.py -- Part B.2: slab-on-body impact estimates (independent of the MPM
simulation used by Gaume & Puzrin 2021; this is a lumped-parameter cross-check).

Three pieces:
  A. Impact velocity of a released slab by energy balance with basal friction
        v^2 = 2 g s (sin(alpha) - mu cos(alpha)),  mu = tan(phi_bed)
     (paper: bed friction angle 22 deg, MPM impact velocity <= 2 m/s, sliding
      distance of order the slab length ~5 m).
  B. Thorax impact: 1-DOF sternum/thorax model against a FIXED back (the hikers
     lay on skis on a compacted floor; Kroell et al. 1974 'fixed-back' tests),
     with the impactor being a crushable snow block: the contact force cannot
     exceed  F_cap = sigma_c * A_contact  (snow crushes at ~its compressive
     strength), the rest of the block's kinetic energy is dissipated in crushing.
     The chest model is calibrated exactly as in the paper: a 10 kg rigid mass
     at 7 m/s must give a maximum normalized deflection C = 0.49 (paper Methods,
     citing Kroell et al. 1974, SAE 741187). Injury mapping (AIS vs C) from the
     Kroell/Nahum data as reported by the automotive-biomechanics literature:
        C ~ 0.30 -> AIS 2,  C ~ 0.40 -> AIS 4 (linear fit AIS = 20 C - 4),
        >20 % compression regularly produces rib fractures at 5-7 m/s,
        50 % probability of >= 7 rib fractures (males) at C = 0.34 (Kimpara et al.,
        IRCOBI 2003, pooled Nahum 1970 / Kroell 1971, 1974 / Stalnaker 1972 data).
  C. Quasi-static burial ("den collapse" hypothesis of the 2019-2020 prosecutor's
     re-investigation): chest load under H metres of snow.

Outputs: fig_B2_velocity.png, fig_B2_chest_deflection.png, slab_impact_results.txt
Run:  python3 slab_impact.py
"""
from __future__ import annotations

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "slab_impact_results.txt"), "w")
G = 9.81


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


# ------------------------------------------------------------------ A. velocity
def impact_velocity(alpha_deg, s, phi_bed_deg=22.0):
    al, mu = math.radians(alpha_deg), math.tan(math.radians(phi_bed_deg))
    acc = G * (math.sin(al) - mu * math.cos(al))
    return math.sqrt(2 * acc * s) if acc > 0 else 0.0


log("== A. Slab impact velocity, v = sqrt(2 g s (sin a - tan(phi_bed) cos a)) ==")
fig, ax = plt.subplots(figsize=(7.5, 5))
s_grid = np.linspace(0, 6, 121)
for al in (21, 23, 25, 28, 30):
    for phib, ls in ((22.0, "-"), (17.0, "--")):
        v = [impact_velocity(al, s, phib) for s in s_grid]
        ax.plot(s_grid, v, ls=ls, label=f"alpha={al}, phi_bed={phib:.0f}")
        log(f"alpha={al:2d} phi_bed={phib:4.1f}: v(s=1 m)={impact_velocity(al, 1, phib):.2f}  "
            f"v(2 m)={impact_velocity(al, 2, phib):.2f}  v(5 m)={impact_velocity(al, 5, phib):.2f} m/s")
ax.axhline(2.0, color="k", ls=":")
ax.text(0.1, 2.05, "paper MPM: <= 2 m/s", fontsize=8)
ax.set_xlabel("sliding distance before impact s (m)")
ax.set_ylabel("impact velocity (m/s)")
ax.set_title("Slab velocity from energy balance (solid: bed friction 22 deg as in the paper's MPM;\n"
             "dashed: 17 deg). Below ~24 deg with 22 deg friction the slab barely moves.")
ax.legend(fontsize=7, ncol=2)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B2_velocity.png"), dpi=150)


# ------------------------------------------------------------------ B. thorax
CHEST_DEPTH = 0.20          # m, the paper normalizes deflection by 20 cm
M_STERNUM = 0.45            # kg (Lobdell-type lumped model, effective sternal mass)


X_STOP = 0.12               # m: 'bottoming' of the thorax at C ~ 0.6 (sternum approaching the spine)
K_STOP = 5.0e5              # N/m beyond X_STOP


def chest_force(x, xdot, k1, c1, k3):
    """Nonlinear Kelvin-Voigt thorax against a fixed back.
    F = k1 x + k3 x^3 + c1 xdot  (k3 gives the stiffening beyond ~35 % compression
    seen in the Kroell corridors) plus a stiff stop beyond 60 % compression (the
    thorax cannot be compressed much further; any surplus energy then goes into
    the spine/floor and into crushing the snow)."""
    return k1 * x + k3 * x ** 3 + c1 * xdot + K_STOP * max(0.0, x - X_STOP)


def simulate(M, v0, k1, c1, k3, F_cap=math.inf, k_snow=5e6, dt=5e-6, t_end=0.15):
    """Impactor mass M at v0 hits the sternum. Contact through an elastic-perfectly-
    plastic snow element (stiffness k_snow, yield F_cap); a rigid impactor is F_cap=inf.
    Returns max normalized deflection, peak force, crushed snow length, energy split."""
    x = xdot = 0.0            # sternum
    y = 0.0                   # impactor front face position (same origin), starts in contact
    ydot = v0
    plastic = 0.0             # permanent crushing of the snow element
    xmax = fmax = 0.0
    t = 0.0
    e_crush = 0.0
    while t < t_end:
        pen = (y - x) - plastic
        if pen <= 0:
            Fc = 0.0
        else:
            Fc = k_snow * pen
            if Fc > F_cap:               # snow crushes: force capped, plastic length grows
                extra = pen - F_cap / k_snow
                plastic += extra
                e_crush += F_cap * extra
                Fc = F_cap
        Fch = chest_force(x, xdot, k1, c1, k3)
        xdd = (Fc - Fch) / M_STERNUM
        ydd = -Fc / M
        xdot += xdd * dt
        x += xdot * dt
        ydot += ydd * dt
        y += ydot * dt
        t += dt
        xmax = max(xmax, x)
        fmax = max(fmax, Fc)
        if t > 0.005 and ydot < 0 and Fc == 0.0 and xdot < 0:
            break
    return dict(C=xmax / CHEST_DEPTH, F=fmax, crush=plastic, e_crush=e_crush,
                e_kin=0.5 * M * v0 ** 2)


def calibrate(target_C=0.49, M=10.0, v0=7.0, c1=300.0, k3=1.0e6):
    """Find k1 such that a rigid mass M at v0 gives C = target.
    Default = the paper's calibration point (10 kg, 7 m/s -> 0.49).  c1 and k3 are fixed a priori
    (c1 = 300 Ns/m is of the order of the Lobdell damper; k3 = 1e6 N/m^3 adds ~1 kN at 10 cm),
    so that the single calibration point is carried by k1 alone."""
    lo, hi = 1e2, 5e6
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        C = simulate(M, v0, mid, c1, k3)["C"]
        if C > target_C:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def ais_from_C(C):
    """Linear Kroell-type mapping AIS = 20 C - 4 (AIS 2 at 30 %, AIS 4 at 40 %), clipped."""
    return max(0.0, min(6.0, 20.0 * C - 4.0))


log("\n== B. Thorax impact (fixed back), lumped model calibrated to the paper's 10 kg @ 7 m/s -> C = 0.49 ==")
c1, k3 = 300.0, 1.0e6
k1 = calibrate(c1=c1, k3=k3)
chk = simulate(10.0, 7.0, k1, c1, k3)
log(f"calibrated k1 = {k1:.0f} N/m (c1 = {c1} Ns/m, k3 = {k3:.1e} N/m^3): "
    f"10 kg @ 7 m/s -> C = {chk['C']:.3f}, peak force {chk['F']/1000:.2f} kN")
log("   NOTE: the paper (Methods, 'Impact simulations') calibrates its body modulus so that a 10 kg rigid block at 7 m/s")
log("   gives C = 0.49 'in line with' Kroell et al. 1974.  The Kroell fixed-back series used 19.5-23.1 kg pendulums at")
log("   4.9-7.2 m/s (secondary sources; the SAE report itself is paywalled and was not read), i.e. 2-2.5 x more energy.")
log("   With the paper's calibration point those real Kroell energies over-compress the model thorax:")
for M, v in ((23.1, 7.2), (19.5, 4.9), (23.1, 4.9), (1.6, 14.0)):
    r = simulate(M, v, k1, c1, k3)
    log(f"   rigid {M:5.1f} kg @ {v:4.1f} m/s -> C = {r['C']:.2f}, F = {r['F']/1000:.1f} kN, AIS~{ais_from_C(r['C']):.1f}")
# alternative, stiffer calibration: Kroell's own 23.1 kg @ 7.2 m/s pendulum -> C = 0.49
k1_alt = calibrate(M=23.1, v0=7.2, c1=c1, k3=k3)
chk2 = simulate(23.1, 7.2, k1_alt, c1, k3)
log(f"   ALTERNATIVE calibration 23.1 kg @ 7.2 m/s -> C = 0.49: k1 = {k1_alt:.0f} N/m "
    f"(check C = {chk2['C']:.3f}, F = {chk2['F']/1e3:.1f} kN); 10 kg @ 7 m/s then gives C = {simulate(10.0, 7.0, k1_alt, c1, k3)['C']:.2f}")

# snow blocks: paper's 0.125 / 0.25 / 0.5 m^3 at 400 kg/m^3 and 2 m/s (MPM: C = 0.28-0.34)
A_contact = 0.12     # m^2 chest contact area (~0.3 x 0.4 m)
log(f"\nSnow blocks against the chest (contact area {A_contact} m^2). F_cap = sigma_c * A:")
log(" volume  rho   v    sigma_c |   C    AIS  Fpeak  crushed  E_kin  E_crush   | C with the stiffer (23.1 kg) calibration")
results = {}
for sigma_c in (30e3, 100e3, 300e3, math.inf):
    for V in (0.125, 0.25, 0.5, 1.0):
        for rho in (300, 400):
            for v in (1.0, 2.0, 3.0, 4.0):
                M = rho * V
                r = simulate(M, v, k1, c1, k3, F_cap=sigma_c * A_contact)
                results[(sigma_c, V, rho, v)] = r
                if rho == 400 and v in (2.0, 3.0) or (V == 0.5 and rho == 400):
                    r2 = simulate(M, v, k1_alt, c1, k3, F_cap=sigma_c * A_contact)
                    log(f" {V:5.3f} {rho:4d} {v:4.1f} {sigma_c/1e3 if math.isfinite(sigma_c) else float('inf'):7.0f} | "
                        f"{r['C']:.2f}  {ais_from_C(r['C']):3.1f}  {r['F']/1e3:5.1f}  {r['crush']*100:5.1f}cm  "
                        f"{r['e_kin']:6.0f}J {r['e_crush']:6.0f}J   | C_alt = {r2['C']:.2f}")

fig, axes = plt.subplots(2, 3, figsize=(15, 8.6), sharey=True, sharex=True)
vgrid = np.linspace(0.5, 4.0, 15)
for row, (kk, cal) in enumerate(((k1, "paper calib. 10 kg @ 7 m/s -> C=0.49 (k1 = %.0f kN/m)" % (k1 / 1e3)),
                                 (k1_alt, "Kroell 23.1 kg @ 7.2 m/s -> C=0.49 (k1 = %.0f kN/m)" % (k1_alt / 1e3)))):
    for ax, sigma_c in zip(axes[row], (30e3, 100e3, 300e3)):
        for V, col in zip((0.125, 0.25, 0.5, 1.0), ("tab:blue", "tab:orange", "tab:green", "tab:red")):
            for rho, ls in ((300, "--"), (400, "-")):
                C = [simulate(rho * V, v, kk, c1, k3, F_cap=sigma_c * A_contact)["C"] for v in vgrid]
                ax.plot(vgrid, C, ls=ls, color=col, label=f"{V} m3, {rho} kg/m3")
        ax.axhspan(0.20, 0.30, color="yellow", alpha=0.15)
        ax.axhspan(0.30, 0.40, color="orange", alpha=0.15)
        ax.axhspan(0.40, 0.60, color="red", alpha=0.12)
        ax.axhline(0.34, color="k", ls=":", lw=0.8)
        ax.text(0.55, 0.345, "50 % prob. of >= 7 rib fractures (C=0.34)", fontsize=7)
        ax.axvline(2.0, color="grey", lw=0.8)
        ax.set_title(f"snow crushing strength {sigma_c/1e3:.0f} kPa (F_cap = {sigma_c*A_contact/1e3:.1f} kN)\n{cal}", fontsize=8)
        ax.grid(alpha=0.3)
        if row == 1:
            ax.set_xlabel("impact velocity (m/s)")
    axes[row][0].set_ylabel("max normalized chest deflection C")
axes[0][0].set_ylim(0, 0.7)
axes[0][0].legend(fontsize=6, ncol=2)
fig.suptitle("Lumped fixed-back thorax model hit by crushable snow blocks. Bands: 20-30 % rib fractures/AIS 1-2, "
             "30-40 % AIS 2-4, >40 % AIS 4+. Paper's MPM: 0.125-0.5 m3 @ 2 m/s -> C = 0.28-0.34 (vertical line: 2 m/s)", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_B2_chest_deflection.png"), dpi=150)

# what velocity does a 400 kg/m3 block need for C >= 0.20 (rib fractures) / 0.34 / 0.40 / 0.49?
for Mblk, label in ((50.0, "0.125 m^3, 400 kg/m^3 block (50 kg)"), (200.0, "0.5 m^3, 400 kg/m^3 block (200 kg)")):
    for kk, cal in ((k1, "paper calibration 10 kg@7 m/s"), (k1_alt, "stiffer calibration 23.1 kg@7.2 m/s")):
        log(f"\nThreshold velocities for a {label}, {cal}:")
        for sigma_c in (30e3, 100e3, 300e3, math.inf):
            out = []
            for target in (0.20, 0.30, 0.34, 0.40, 0.49):
                vv = None
                for v in np.linspace(0.2, 8.0, 79):
                    if simulate(Mblk, v, kk, c1, k3, F_cap=sigma_c * A_contact)["C"] >= target:
                        vv = v
                        break
                out.append(f"C>={target}: {vv:.1f} m/s" if vv else f"C>={target}: never (<8 m/s)")
            log(f"  sigma_c={sigma_c/1e3 if math.isfinite(sigma_c) else float('inf'):5.0f} kPa: " + "; ".join(out))
log("\nContact pressure at the chest = F / A_contact: a 3-6 kN chest force spread over 0.12 m^2 is 25-50 kPa, "
    "i.e. of the order of the snow's own crushing strength and two to three orders of magnitude below skin-laceration "
    "pressures -- the classic 'fractures without external wounds' signature of a broad, soft, heavy impactor.")

# ------------------------------------------------------------------ C. static burial
log("\n== C. Quasi-static burial: chest load under H m of snow ==")
log(" H(m)  rho   pressure(kPa)  force on 0.12 m^2 (kN)   static C (paper calib.)   static C (stiffer calib.)")


def static_C(F, kk):
    x = 0.0
    for _ in range(200):
        x -= (kk * x + k3 * x ** 3 - F) / (kk + 3 * k3 * x ** 2)
    return x / CHEST_DEPTH


for H in (1.0, 2.0, 3.0, 4.0):
    for rho in (300, 400, 500):
        p = rho * G * H
        F = p * A_contact
        log(f" {H:4.1f}  {rho:4d}  {p/1e3:8.1f}       {F/1e3:6.2f}                  {static_C(F, k1):.2f}                    {static_C(F, k1_alt):.2f}")
log("Quasi-static chest stiffness in vivo is ~5-25 kN/m at 3-6 cm compression (CPR studies: ~400-500 N for 5 cm), and "
    "5-6 cm CPR compressions fracture ribs in roughly a third of (mostly elderly) patients; young adults tolerate more. "
    "3-4 m of 400 kg/m3 snow gives ~1.4-1.9 kN on a 0.12 m^2 chest: enough for 20-40 % quasi-static compression on the "
    "soft (paper) calibration, only ~10 % on the stiff one -- so a static burial of that depth can, but need not, "
    "break ribs, and does so more easily if the load is concentrated (rock or ledge under the back).")

# ------------------------------------------------------------------ D. skull
log("\n== D. Skull: force available from a snow block vs. fracture tolerance ==")
log("Temporo-parietal fracture forces (Allsop et al. 1991, flat 5x10 cm plate / 2.54 cm disc, 10.6-12 kg drop): "
    "2.5-10 kN, mean 5.2 kN; Yoganandan et al. 2004 review: 5.6-9.9 kN, mean 7.7 kN.")
for sigma_c in (30e3, 100e3, 300e3):
    for A in (0.002, 0.005, 0.01):   # contact area on a hard object under the head (camera, rock): 2-10 cm^2 ... 100 cm^2
        log(f"  crushing {sigma_c/1e3:4.0f} kPa over {A*1e4:5.0f} cm^2 -> max force {sigma_c*A/1e3:5.2f} kN")
log("A snow block cannot transmit more than sigma_c * A_contact; to reach 2.5-5 kN on a temporal bone the load must be "
    "concentrated (head on a hard object, e.g. a camera used as a pillow as Buyanov suggests) or the snow must be very hard.")
OUT.close()
print("done")

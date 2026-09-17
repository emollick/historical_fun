"""
gp_model.py -- Re-implementation of the analytical delayed-slab-release model of
Gaume & Puzrin (2021), "Mechanisms of slab avalanche release and impact in the
Dyatlov Pass incident in 1959", Communications Earth & Environment 2:10,
https://doi.org/10.1038/s43247-020-00081-8  (open access, CC-BY 4.0).

Equation numbers below refer to that paper (Methods section, pp. 7-9).

Geometry (paper Fig. 3a):
  * weak layer of thickness d, inclined at alpha, buried under a slab whose
    depth decreases parabolically from h0 at the cut (x = 0) to hc at x >= lc:
        h(x) = h0 (1 - x/L0)^2,   L0 = lc / (1 - sqrt(hc/h0))          (Eq. 7-8)
  * after the cut, wind-transported snow (density rho_w) of thickness
    hw(x) = hw0 (1 - x/L0)^2 accumulates above the cut                  (Eq. 9)
  * slab: plane-strain modulus E', weak layer: shear modulus G, thickness d,
    elastic length le0 = sqrt(E' h0 d / G), lambda0 = L0^2 / le0^2       (Eq. 19)

Failure criterion at the cut (Eq. 1 / Eq. 33):
    tau0 = tau_g0 + r1 Pg0/L0 + r3/(r3+2) Pw0/L0  >=  tau_p = tau_p0 + tau_pw
with
    Pg0 = 1/2 K0 rho g h0^2 cos(alpha)           (lateral force released by cut)
    Pw0 = rho_w g hw0 L0 sin(alpha)              (wind-load shear resultant)
    tau_g0 = rho g h0 sin(alpha)
    tau_p0 = rho g h0 cos(alpha) tan(phi) + c
    tau_pw = rho_w g hw0 cos(alpha) tan(phi)
    r1 = (1 + sqrt(1 + 4 lambda0))/2 ;  r3 = (1 + sqrt(1 + 4 lambda_s))/2
    lambda_s = lambda0 h0/(h0 + hs0)   (hs0 = sintered part of the wind snow)

Closed-form results (Eq. 37-41):
    tan(phi_min) = tan(alpha) - c/(rho g h0) sqrt(1+tan^2 alpha) + r1 K0 h0/(2 L0)
    tan(phi_max(lam)) = r/(r+2) tan(alpha),  r = (1+sqrt(1+4 lam))/2
    hw0_min = h0 (rho/rho_w) (tan phi - tan phi_min)/(tan phi_max(lambda0) - tan phi)   [no sintering]
    hw0_max = h0 (rho/rho_w) (tan phi - tan phi_min)/(tan phi_max(lambda_s) - tan phi)  [full sintering, implicit]
    dt = rho_w hw0 L0 / (3 Q) * (1 - (1 - lc/L0)^3)                                    (Eq. 6 / 35-36)

Delayed release is possible only if  tan(phi_min) < tan(phi) < tan(phi_max(lambda_s)) (Eq. 43):
  * phi <= phi_min  -> the slab fails immediately when the cut is made
  * phi >= phi_max  -> wind loading can never bring the weak layer to peak strength

Paper's Dyatlov parameter set (Methods, "The Dyatlov case", and SI Note 6):
  alpha = 28 deg, h0 = 0.5 m, hc = 0.1 m, lc = 4 m, le0 = 1.0 m
  (E = 8 MPa, G = 1 MPa, d = 0.20 m), rho = 300, rho_w = 400 kg/m^3,
  K0 = 0.5, phi = 20 deg, c = 440 Pa, Q = 0.008 kg/m/s
  -> hw0_min = 0.24 m, hw0_max = 0.44 m, dt_min = 7.2 h, dt_max = 13.5 h
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy.optimize import brentq

G_ACC = 9.81


@dataclass
class Params:
    alpha_deg: float = 28.0   # weak-layer inclination [deg]
    h0: float = 0.5           # slab depth at the cut [m]
    hc: float = 0.1           # slab depth on the straight upper slope [m]
    lc: float = 4.0           # distance from cut to constant-depth slope [m]
    le0: float = 1.0          # elastic length sqrt(E' h0 d / G) [m]
    rho: float = 300.0        # original slab density [kg/m^3]
    rho_w: float = 400.0      # wind-transported snow density [kg/m^3]
    K0: float = 0.5           # at-rest lateral pressure coefficient
    phi_deg: float = 20.0     # weak-layer internal friction [deg]
    c: float = 440.0          # weak-layer cohesion [Pa]
    Q: float = 0.008          # wind deposition flux [kg/m/s]

    # ---- derived quantities -------------------------------------------------
    @property
    def alpha(self) -> float:
        return math.radians(self.alpha_deg)

    @property
    def phi(self) -> float:
        return math.radians(self.phi_deg)

    @property
    def L0(self) -> float:                                   # Eq. 8
        return self.lc / (1.0 - math.sqrt(self.hc / self.h0))

    @property
    def lambda0(self) -> float:                              # Eq. 19
        return (self.L0 / self.le0) ** 2

    @property
    def r1(self) -> float:                                   # Eq. 20
        return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 * self.lambda0))

    @property
    def geom_factor(self) -> float:
        """(1 - (1 - lc/L0)^3): area factor of the parabolic wind wedge, Eq. 35."""
        return 1.0 - (1.0 - self.lc / self.L0) ** 3


def r_of_lambda(lam: float) -> float:
    return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 * lam))


def tan_phi_max(p: Params, lam: float) -> float:            # Eq. 38 / 40
    r = r_of_lambda(lam)
    return r / (r + 2.0) * math.tan(p.alpha)


def tan_phi_min(p: Params) -> float:                        # Eq. 38 / 40
    ta = math.tan(p.alpha)
    return (ta
            - p.c / (p.rho * G_ACC * p.h0) * math.sqrt(1.0 + ta * ta)
            + p.r1 * p.K0 * p.h0 / (2.0 * p.L0))


def hw0_min(p: Params) -> float:
    """Critical wind-snow height at the cut if none of it sinters (Eq. 39).
    Returns inf when phi >= phi_max(lambda0), and 0 when phi <= phi_min."""
    tp, tmin, tmax = math.tan(p.phi), tan_phi_min(p), tan_phi_max(p, p.lambda0)
    if tp <= tmin:
        return 0.0
    if tp >= tmax:
        return math.inf
    return p.h0 * (p.rho / p.rho_w) * (tp - tmin) / (tmax - tp)


def hw0_max(p: Params) -> float:
    """Critical height if all wind snow sinters instantly (Eq. 37, implicit in hs0).
    Solves hs0 = h0 (rho/rho_w)(tan phi - tan phi_min)/(tan phi_max(lambda_s(hs0)) - tan phi).
    Returns inf if no finite root exists."""
    tp, tmin = math.tan(p.phi), tan_phi_min(p)
    if tp <= tmin:
        return 0.0

    def f(hs0):
        lam_s = p.lambda0 * p.h0 / (p.h0 + hs0)
        den = tan_phi_max(p, lam_s) - tp
        if den <= 0:
            return math.inf
        return p.h0 * (p.rho / p.rho_w) * (tp - tmin) / den - hs0

    # scan for a sign change on a geometric grid (the root, if any, is the smallest one)
    grid = np.geomspace(1e-4, 5.0, 160)
    prev_h, prev_v = grid[0], f(grid[0])
    if not math.isfinite(prev_v):
        return math.inf
    if prev_v <= 0:                      # root essentially at zero thickness
        return prev_h
    for h in grid[1:]:
        v = f(h)
        if not math.isfinite(v):
            return math.inf
        if v <= 0:
            return brentq(f, prev_h, h)
        prev_h, prev_v = h, v
    return math.inf


def time_to_release_h(p: Params, hw0: float) -> float:      # Eq. 6 / 35
    if not math.isfinite(hw0):
        return math.inf
    return p.rho_w * hw0 * p.L0 / (3.0 * p.Q) * p.geom_factor / 3600.0


def delay_bounds_h(p: Params) -> tuple[float, float, float, float]:
    """(hw0_min, hw0_max, dt_min [h], dt_max [h])."""
    a, b = hw0_min(p), hw0_max(p)
    return a, b, time_to_release_h(p, a), time_to_release_h(p, b)


def regime(p: Params) -> str:
    tp = math.tan(p.phi)
    if tp <= tan_phi_min(p):
        return "immediate failure at cut"
    if tp >= tan_phi_max(p, p.lambda0):
        return "no release (wind load never reaches peak strength)"
    if not math.isfinite(hw0_max(p)):
        return "delayed release only if wind snow does not sinter"
    return "delayed release"


# ---- released slab size (Eq. 44-46) ------------------------------------------
def slab_dimensions(p: Params, hw0: float = 0.5, sigma_t: float = 6000.0,
                    sigma_s: float = 5200.0) -> dict:
    """Length (tension crack position) lcw, width B, cross-section areas, mass.
    Paper: phi=20 deg, sigma_t=6.0 kPa, sigma_s=5.2 kPa, hw0=0.5 m -> lcw=4.95 m, B=8.8 m."""
    L0, h0, hc, lc = p.L0, p.h0, p.hc, p.lc
    lcw = L0 * (1.0 - math.sqrt(hc / (h0 + hw0)))
    A0 = h0 * L0 / 3.0 * (1.0 - (1.0 - lc / L0) ** 3) + hc * (lcw - lc)
    As = (h0 + hw0) * L0 / 3.0 * (1.0 - (1.0 - lcw / L0) ** 3)
    line_mass = A0 * p.rho + (As - A0) * p.rho_w                     # kg per m of width
    drive = line_mass * G_ACC * math.cos(p.alpha) * (math.tan(p.alpha) - math.tan(p.phi))
    den = drive - hc * sigma_t
    B = 2.0 * lcw * hc * sigma_s / den if den > 0 else math.inf
    return dict(lcw=lcw, A0=A0, As=As, line_mass=line_mass, B=B,
                mass=line_mass * B if math.isfinite(B) else math.inf,
                volume=As * B if math.isfinite(B) else math.inf)


# ---- critical crack length (anticrack model, Gaume et al. 2017) --------------
def critical_crack_length(D: float, rho_slab: float, psi_deg: float, tau_p: float,
                          E_prime: float = 8e6 / (1 - 0.3 ** 2), d_wl: float = 0.2,
                          G_wl: float = 1e6) -> float:
    """Critical length of a basal (weak-layer) crack for self-sustained propagation,
    Gaume, van Herwijnen, Chambon, Wever & Schweizer (2017), The Cryosphere 11:217-228,
    https://doi.org/10.5194/tc-11-217-2017, Eq. (8):
        a_c = Lambda * (-tau + sqrt(tau^2 + 2 sigma (tau_p - tau))) / sigma
        Lambda = sqrt(E' D d_wl / G_wl),  sigma = rho g D cos psi,  tau = rho g D sin psi.
    NOT used by Gaume & Puzrin (2021) -- provided as an independent cross-check of the
    scale over which a softened zone near the cut becomes self-propagating."""
    psi = math.radians(psi_deg)
    sigma = rho_slab * G_ACC * D * math.cos(psi)
    tau = rho_slab * G_ACC * D * math.sin(psi)
    if tau_p <= tau:
        return 0.0
    lam = math.sqrt(E_prime * D * d_wl / G_wl)
    return lam * (-tau + math.sqrt(tau * tau + 2.0 * sigma * (tau_p - tau))) / sigma


if __name__ == "__main__":
    p = Params()
    a, b, ta, tb = delay_bounds_h(p)
    print(f"L0 = {p.L0:.3f} m, lambda0 = {p.lambda0:.2f}, r1 = {p.r1:.3f}")
    print(f"phi_min = {math.degrees(math.atan(tan_phi_min(p))):.2f} deg, "
          f"phi_max(lambda0) = {math.degrees(math.atan(tan_phi_max(p, p.lambda0))):.2f} deg")
    print(f"hw0_min = {a:.3f} m, hw0_max = {b:.3f} m  (paper: 0.24, 0.44)")
    print(f"dt_min = {ta:.2f} h, dt_max = {tb:.2f} h  (paper: 7.2, 13.5)")
    print("regime:", regime(p))
    print("slab:", {k: round(v, 3) for k, v in slab_dimensions(p).items()})

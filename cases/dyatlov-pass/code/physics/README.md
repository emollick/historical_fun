# Dyatlov Pass -- physics replication scripts

Independent re-implementation and stress-testing of the slab-avalanche physics in
Gaume & Puzrin (2021), *Communications Earth & Environment* 2:10,
<https://doi.org/10.1038/s43247-020-00081-8>, plus impact and hypothermia estimates.
Written for the historical investigation in `../../research/physics-assessment.md`.

Everything is plain Python 3 + numpy/scipy/matplotlib (`pip install numpy scipy matplotlib`).
Each script writes its figures (PNG) and a `*_results.txt` log next to itself.

| script | what it does | outputs |
|---|---|---|
| `gp_model.py` | The paper's analytical delayed-release model, equation by equation (Eq. 1-9, 33-46). Run it alone to print the replication of the paper's numbers. | stdout |
| `slab_release.py` | Part B.1/B.3. (0) replication; (1) time-to-release vs weak-layer slope for several wind fluxes Q; (2) regime map in (slope, friction) space; (3) delay vs Q against the Sturm & Stuefer (2013) flux envelope; (4) one-at-a-time sensitivity; (5) the (friction, cohesion) window that still gives a 9.5-13.5 h release at 22/23/25/28/30 deg; (6) anticrack critical-crack-length scale check | `fig_B1_delay_vs_slope.png`, `fig_B1_regime_map.png`, `fig_B1_delay_vs_Q.png`, `fig_B1_sensitivity.png`, `fig_B3_lowslope_window.png`, `slab_release_results.txt` |
| `slab_impact.py` | Part B.2. Slab velocity by energy balance; a lumped fixed-back thorax model (nonlinear spring + damper + bottoming stop at 60 % compression) hit by *crushable* snow blocks (force capped by snow crushing strength x contact area). Two calibrations are carried through: the paper's (10 kg rigid mass at 7 m/s -> 49 % deflection) and a stiffer one using Kroell's actual 23.1 kg pendulum at 7.2 m/s; AIS mapping; threshold velocities; quasi-static burial loads (the 2020 prosecutor's 'den collapse'); skull-fracture force comparison | `fig_B2_velocity.png`, `fig_B2_chest_deflection.png`, `slab_impact_results.txt` |
| `hypothermia.py` | Part B.4. Wind chill (Osczevski & Bluestein 2005) and a Tikuisis-type single-compartment heat-balance model giving time to core 34/30/28 C for 0.5-1.0 clo, dry/wet, resting/walking, at -25/-30 C and 5-20 m/s; checked against Tikuisis' published anchor points | `fig_B4_survival.png`, `hypothermia_results.txt` |

Run order does not matter; `slab_release.py` takes a few minutes (parameter grids).

```
cd code/physics
python3 gp_model.py
python3 slab_release.py
python3 slab_impact.py
python3 hypothermia.py
```

## Notes on fidelity

* `gp_model.py` reproduces the paper's published values to the quoted precision
  (hw0 = 0.24/0.44 m, delay 7.2/13.5 h, tension crack at 4.95 m, width 8.8 m). The
  paper's own code (Zenodo 10.5281/zenodo.4088052) could not be downloaded (Zenodo
  returned 504 through the proxy on three attempts), so the equations were taken
  from the Methods section directly.
* The MPM (material point method) impact simulation of the paper is **not**
  replicated; `slab_impact.py` is a deliberately simple lumped model. Its purpose is
  to show which variables control the chest deflection (block mass and velocity,
  the assumed chest stiffness, and -- only for a stiff chest -- the snow's crushing
  strength), not to reproduce the MPM numbers. The paper's calibration point (a 10 kg
  rigid mass at 7 m/s giving 49 % deflection, attributed to Kroell et al. 1974) is
  carried through as published, but note that the Kroell fixed-back series used
  19.5-23.1 kg pendulums (per secondary sources; the SAE report is paywalled), i.e.
  2-2.5 x the impact energy, so a second, stiffer calibration is reported alongside.
  The whole block momentum is assumed to go into the chest (contact area 0.12 m^2);
  in reality part of a wide slab face is carried by the pelvis, shoulders, head and
  the tent floor, so the chest deflections are upper estimates for a given block.
* The hypothermia model is a heat-balance sketch checked against the five anchor
  points Tikuisis (1995) published in his abstract: it is 25-30 % pessimistic for
  nude subjects and 3-4 x pessimistic for lightly clothed subjects in light wind, so
  its clothed survival times should be read as lower bounds (factor 2-4).

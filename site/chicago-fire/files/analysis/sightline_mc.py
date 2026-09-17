#!/usr/bin/env python3
"""Sightline test for Daniel Sullivan's claimed view of the O'Leary barn, 8 October 1871.

Method
------
The block is modelled as a height field h(x, y): every building is a box with a gable roof
(ridge along the N-S or E-W axis), fences are thin walls, everything else is at grade.
A ray from the observer's eye E to a target T is clear if, at every sampled point along the
horizontal path between them, the ray's height exceeds h(x, y).  Because the obstacles are a
height field, visibility of a vertical column above any plan point is monotone in height, so
the lowest visible height at that column is found by bisection.

For each Monte Carlo draw, every uncertain input in plan_inputs.json is sampled from its range
(uniform), the observer is placed at a random point of the chosen position box with a random
eye height, and we record:
  body_visible : whether any point of the barn's south or east wall below the eaves is visible
  z_body_min   : lowest visible height on those walls (NaN if none)
  ridge_visible: whether any point of the ridge line is visible
  H_min        : lowest visible height on vertical columns above the barn (min over the barn's
                 four corners and centre) -- the height flames or lit smoke had to reach to be seen
  above_ridge  : H_min minus the sampled ridge height

Outputs: results_<position>_<eye>.csv and summary.csv / summary.md in the same folder.
"""
import json, math, sys, csv
import numpy as np

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
INP = json.load(open(f'{HERE}/plan_inputs.json'))
rng = np.random.default_rng(20261008)

def U(r):
    return rng.uniform(r[0], r[1]) if isinstance(r, (list, tuple)) else float(r)

class Box:
    """Building with gable roof. Heights absolute above grade."""
    def __init__(self, x0, x1, y0, y1, eaves, ridge, axis, name):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.eaves, self.ridge, self.axis, self.name = eaves, ridge, axis, name
    def h(self, x, y):
        inside = (x >= self.x0) & (x <= self.x1) & (y >= self.y0) & (y <= self.y1)
        if self.axis == 'N-S':
            xm = 0.5 * (self.x0 + self.x1); half = 0.5 * (self.x1 - self.x0)
            f = 1 - np.abs(x - xm) / max(half, 1e-6)
        else:
            ym = 0.5 * (self.y0 + self.y1); half = 0.5 * (self.y1 - self.y0)
            f = 1 - np.abs(y - ym) / max(half, 1e-6)
        z = self.eaves + (self.ridge - self.eaves) * np.clip(f, 0, 1)
        return np.where(inside, z, 0.0)

class Wall:
    """Thin fence along x=const (vertical) or y=const (horizontal)."""
    def __init__(self, axis, c, a0, a1, height, name, thick=0.5):
        self.axis, self.c, self.a0, self.a1, self.height, self.name, self.t = axis, c, a0, a1, height, name, thick
    def h(self, x, y):
        if self.axis == 'x':   # fence runs N-S at x=c
            inside = (np.abs(x - self.c) <= self.t / 2) & (y >= self.a0) & (y <= self.a1)
        else:                  # fence runs E-W at y=c
            inside = (np.abs(y - self.c) <= self.t / 2) & (x >= self.a0) & (x <= self.a1)
        return np.where(inside, self.height, 0.0)

def sample_block():
    B = INP['buildings']; F = INP['fences']
    obs = []
    def bld(key, name):
        b = B[key]
        x0 = U(b['x0']); w = U(b['width']); y0 = U(b['y0']); d = U(b['depth'])
        fl = U(b['floor']); e = fl + U(b['eaves_above_floor']); r = fl + U(b['ridge_above_floor'])
        r = max(r, e + 0.5)
        return Box(x0, x0 + w, y0, y0 + d, e, r, b['ridge_axis'], name)
    ole = bld('oleary_cottages', 'O\'Leary cottages'); obs.append(ole)
    dal = bld('dalton_house', 'Dalton house')
    dal_depth = dal.y1 - dal.y0; dal.y0 = ole.y1 - rng.uniform(1, 3); dal.y1 = dal.y0 + dal_depth
    obs.append(dal)
    fob = bld('forbes_cottages_133', '133 cottages'); obs.append(fob)
    obs.append(bld('barn_133', '133 barn'))
    shd = bld('dalton_shed', 'Dalton shed'); obs.append(shd)
    # O'Leary barn
    b = B['oleary_barn']
    v = b['variants'][0] if rng.uniform() < b['variants'][0]['p'] else b['variants'][1]
    bx0 = U(b['x0']); bw = v['width']; bd = v['depth']; by1 = b['y1']; by0 = by1 - bd
    ridge = U(b['ridge']); eaves = ridge - U(b['eaves_below_ridge'])
    axis = 'N-S' if rng.uniform() < b['ridge_axis_p_NS'] else 'E-W'
    barn = Box(bx0, bx0 + bw, by0, by1, eaves, ridge, axis, 'O\'Leary barn')
    # fences
    obs.append(Wall('x', 158.4, dal.y1, shd.y0, F['dalton_west_fence_house_to_shed']['height'], 'Dalton 8-ft fence'))
    f = F['oleary_dalton_front_fence']
    if rng.uniform() < f['p']:
        obs.append(Wall('x', 158.4, 0, dal.y0, U(f['height']), 'O\'Leary/Dalton front fence'))
    f = F['dalton_133_fence']
    if rng.uniform() < f['p']:
        obs.append(Wall('x', 183.4, f['y0'], f['y1'], U(f['height']), 'Dalton/133 fence'))
    obs.append(Wall('y', 0.0, 130, 260, U(F['street_pickets']['height']), 'street pickets'))
    f = F['oleary_shed']
    if rng.uniform() < f['p']:
        obs.append(Box(f['x0'], f['x1'], f['y0'], f['y1'], U(f['height']), U(f['height']), 'E-W', 'O\'Leary shed'))
    return obs, barn, dict(dalton=dal, forbes=fob, oleary=ole)

def hfield(obs, x, y):
    h = np.zeros_like(x)
    for o in obs:
        h = np.maximum(h, o.h(x, y))
    return h

def ray_clear(E, T, obs, n=900):
    """True if the segment E->T (3-D) stays above the height field, endpoints excluded."""
    s = np.linspace(0.0, 1.0, n)[1:-1]
    x = E[0] + (T[0] - E[0]) * s; y = E[1] + (T[1] - E[1]) * s; z = E[2] + (T[2] - E[2]) * s
    # exclude the target's own footprint (the barn) from blocking: handled by caller via barn walls only
    return bool(np.all(z > hfield(obs, x, y)))

def lowest_visible_on_column(E, x, y, obs, zlo=0.0, zhi=80.0, tol=0.25):
    """Bisection for the lowest visible height at plan point (x, y). Returns NaN if not visible at zhi."""
    if not ray_clear(E, (x, y, zhi), obs):
        return float('nan')
    if ray_clear(E, (x, y, zlo), obs):
        return zlo
    lo, hi = zlo, zhi
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if ray_clear(E, (x, y, mid), obs):
            hi = mid
        else:
            lo = mid
    return hi

def run(position, eye_key, ndraw=400, out=None):
    P = INP['observer']['positions'][position]; EH = INP['observer']['eye_heights'][eye_key]
    rows = []
    for i in range(ndraw):
        obs, barn, named = sample_block()
        ex = U(P['x']); ey = U(P['y']); ez = U(EH)
        E = (ex, ey, ez)
        # barn body: south wall (y=barn.y0) and east wall (x=barn.x1), points below the eaves
        z_body = float('nan'); body_vis = False
        xs = np.linspace(barn.x0 + 0.5, barn.x1 - 0.5, 5)
        cols = [(x, barn.y0 - 0.01) for x in xs] + [(barn.x1 + 0.01, y) for y in np.linspace(barn.y0 + 0.5, barn.y1 - 0.5, 5)]
        zmins = []
        for (cx, cy) in cols:
            zm = lowest_visible_on_column(E, cx, cy, obs, 0.0, 80.0)
            zmins.append(zm)
        zmins = np.array(zmins)
        # walls: visible if lowest visible height on a wall column is below the eaves
        wall_vis = zmins[~np.isnan(zmins)]
        wall_vis = wall_vis[wall_vis < barn.eaves]
        if wall_vis.size:
            body_vis = True; z_body = float(wall_vis.min())
        # column above the barn: corners and centre (the barn itself does not block its own column: we
        # evaluate columns at the barn's plan points but the barn is not in obs)
        pts = [(barn.x0 + 0.5, barn.y0 + 0.5), (barn.x1 - 0.5, barn.y0 + 0.5), (barn.x0 + 0.5, barn.y1 - 0.5),
               (barn.x1 - 0.5, barn.y1 - 0.5), (0.5 * (barn.x0 + barn.x1), 0.5 * (barn.y0 + barn.y1))]
        H = np.array([lowest_visible_on_column(E, px, py, obs, 0.0, 120.0) for (px, py) in pts])
        Hmin = float(np.nanmin(H)) if np.any(~np.isnan(H)) else float('nan')
        ridge_vis = bool(np.any(H[~np.isnan(H)] <= barn.ridge)) if np.any(~np.isnan(H)) else False
        dal = named['dalton']; fob = named['forbes']
        rows.append(dict(draw=i, obs_x=round(ex, 1), obs_y=round(ey, 1), eye_z=round(ez, 2),
                         barn_w=round(barn.x1 - barn.x0, 1), barn_d=round(barn.y1 - barn.y0, 1),
                         barn_eaves=round(barn.eaves, 1), barn_ridge=round(barn.ridge, 1), barn_axis=barn.axis,
                         dalton_w=round(dal.x1 - dal.x0, 1), dalton_y0=round(dal.y0, 1), dalton_eaves=round(dal.eaves, 1), dalton_ridge=round(dal.ridge, 1),
                         forbes_x0=round(fob.x0, 1), forbes_w=round(fob.x1 - fob.x0, 1), forbes_depth=round(fob.y1 - fob.y0, 1), forbes_eaves=round(fob.eaves, 1), forbes_ridge=round(fob.ridge, 1),
                         body_visible=int(body_vis), z_body_min=round(z_body, 2) if not math.isnan(z_body) else '',
                         ridge_visible=int(ridge_vis), H_min=round(Hmin, 2) if not math.isnan(Hmin) else '',
                         above_ridge=round(Hmin - barn.ridge, 2) if not math.isnan(Hmin) else ''))
    if out:
        with open(out, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return rows

def summarize(rows):
    n = len(rows)
    bv = np.array([r['body_visible'] for r in rows]); rv = np.array([r['ridge_visible'] for r in rows])
    ab = np.array([r['above_ridge'] for r in rows if r['above_ridge'] != ''], dtype=float)
    Hm = np.array([r['H_min'] for r in rows if r['H_min'] != ''], dtype=float)
    q = lambda a, p: float(np.percentile(a, p)) if a.size else float('nan')
    ab_all = np.array([float(r['above_ridge']) if r['above_ridge'] != '' else np.inf for r in rows])
    return dict(n=n, p_body=bv.mean(), p_ridge=rv.mean(), p_above5=float((ab_all <= 5).mean()), p_above10=float((ab_all <= 10).mean()), p_above20=float((ab_all <= 20).mean()),
                H_med=q(Hm, 50), H_p10=q(Hm, 10), H_p90=q(Hm, 90), above_med=q(ab, 50), above_p10=q(ab, 10), above_p90=q(ab, 90))

if __name__ == '__main__':
    ndraw = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    summary = []
    for pos in INP['observer']['positions']:
        for eye in INP['observer']['eye_heights']:
            rows = run(pos, eye, ndraw, out=f'{HERE}/results_{pos}_{eye}.csv')
            s = summarize(rows); s.update(position=pos, eye=eye); summary.append(s)
            print(f"{pos:28s} {eye:22s} n={s['n']} P(barn walls visible)={s['p_body']:.2f} P(ridge visible)={s['p_ridge']:.2f} "
                  f"P(<=5ft above ridge)={s['p_above5']:.2f} P(<=10)={s['p_above10']:.2f} P(<=20)={s['p_above20']:.2f} H_min median={s['H_med']:.1f} ft (p10-p90 {s['H_p10']:.1f}-{s['H_p90']:.1f}); above ridge median={s['above_med']:.1f} ft (p10-p90 {s['above_p10']:.1f}-{s['above_p90']:.1f})", flush=True)
    with open(f'{HERE}/summary.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)

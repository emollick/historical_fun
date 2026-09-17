#!/usr/bin/env python3
"""Figures for the Chicago fire sightline report.

fig_plan.png      block plan (central values of every range in plan_inputs.json) with the
                  six observer boxes and the straight lines from Bales's seat (P1b) and from
                  the front of Sullivan's own house (P3) to the O'Leary barn.
fig_profile.png   vertical section along the line of sight from P1b and from P3 to the
                  barn: ground, the silhouette of everything the ray crosses, the ray to the
                  barn's ridge, and the lowest point on the barn's south wall that the eye
                  can see (bisection, as in sightline_mc.py).
Central configuration = midpoint of every uniform range; Andreas barn variant (16 ft E-W by
20 ft N-S); the two optional fences with p = 0.7 are drawn at their mid height; the optional
O'Leary shed (p = 0.4) is left out.
"""
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import sightline_mc as S

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
INP = S.INP
B = INP['buildings']; F = INP['fences']; P = INP['observer']['positions']; EH = INP['observer']['eye_heights']

def mid(r):
    return 0.5 * (r[0] + r[1]) if isinstance(r, (list, tuple)) else float(r)

def central_block(variant=0):
    obs = []
    def bld(key, name):
        b = B[key]
        x0 = mid(b['x0']); w = mid(b['width']); y0 = mid(b['y0']); d = mid(b['depth'])
        fl = mid(b['floor']); e = fl + mid(b['eaves_above_floor']); r = fl + mid(b['ridge_above_floor'])
        return S.Box(x0, x0 + w, y0, y0 + d, e, r, b['ridge_axis'], name)
    ole = bld('oleary_cottages', "O'Leary cottages"); obs.append(ole)
    dal = bld('dalton_house', 'Dalton house')
    dd = dal.y1 - dal.y0; dal.y0 = ole.y1 - 2.0; dal.y1 = dal.y0 + dd
    obs.append(dal)
    fob = bld('forbes_cottages_133', '133 cottages'); obs.append(fob)
    obs.append(bld('barn_133', '133 barn'))
    shd = bld('dalton_shed', 'Dalton shed'); obs.append(shd)
    b = B['oleary_barn']; v = b['variants'][variant]
    bx0 = mid(b['x0']); by1 = b['y1']; by0 = by1 - v['depth']
    ridge = mid(b['ridge']); eaves = ridge - mid(b['eaves_below_ridge'])
    barn = S.Box(bx0, bx0 + v['width'], by0, by1, eaves, ridge, 'N-S', "O'Leary barn")
    obs.append(S.Wall('x', 158.4, dal.y1, shd.y0, F['dalton_west_fence_house_to_shed']['height'], 'Dalton 8-ft fence'))
    obs.append(S.Wall('x', 158.4, 0, dal.y0, mid(F['oleary_dalton_front_fence']['height']), "O'Leary/Dalton front fence"))
    f = F['dalton_133_fence']; obs.append(S.Wall('x', 183.4, f['y0'], f['y1'], mid(f['height']), 'Dalton/133 fence'))
    obs.append(S.Wall('y', 0.0, 130, 260, mid(F['street_pickets']['height']), 'street pickets'))
    return obs, barn, dict(dalton=dal, forbes=fob, oleary=ole, shed=shd)

def draw_plan():
    obs, barn, d = central_block(0)
    fig, ax = plt.subplots(figsize=(11, 8.2))
    # street and alley bands
    ax.add_patch(Rectangle((95, -60), 215, 60, facecolor='#e9e4d8', edgecolor='none', zorder=0))
    ax.add_patch(Rectangle((95, 100.75), 215, 15, facecolor='#e9e4d8', edgecolor='none', zorder=0))
    ax.text(102, -32, 'DeKoven Street (60 ft)', fontsize=9, color='#555', va='center')
    ax.text(102, 108, 'alley (15 ft)', fontsize=9, color='#555', va='center')
    # lot lines north side
    for x in [108.4, 133.4, 158.4, 183.4, 208.4, 233.4, 258.4, 283.4, 308.4]:
        ax.plot([x, x], [0, 100.75], color='#b0a89a', lw=0.8, zorder=1)
    for x in [108.5, 133.5, 158.5, 183.5, 208.5, 233.5, 258.5, 283.5, 308.5]:
        ax.plot([x, x], [-60, -160], color='#b0a89a', lw=0.8, zorder=1)
    ax.plot([95, 310], [0, 0], color='#7a7266', lw=1); ax.plot([95, 310], [-60, -60], color='#7a7266', lw=1)
    ax.plot([95, 310], [100.75, 100.75], color='#7a7266', lw=1); ax.plot([95, 310], [115.75, 115.75], color='#7a7266', lw=1)
    # house numbers
    for x, n in [(120.9, '139'), (145.9, '137'), (170.9, '135'), (195.9, '133'), (220.9, '131'), (245.9, '129'), (270.9, '127')]:
        ax.text(x, -5.5, n, ha='center', va='top', fontsize=8, color='#555')
    for x, n in [(121, '138'), (146, '136'), (171, '136'), (196, '134'), (221, '132'), (246, '130'), (271, '128')]:
        pass
    ax.text(146, -66, 'H lot 1', ha='center', va='top', fontsize=7, color='#555'); ax.text(171, -66, 'W 1/2 lot 18', ha='center', va='top', fontsize=7, color='#555')
    ax.text(196, -66, 'E 1/2 lot 18\n(134 by 1891\nnumbering)', ha='center', va='top', fontsize=7, color='#555'); ax.text(221, -66, 'W 1/2 lot 19\nSullivan\n(deeds)', ha='center', va='top', fontsize=7, color='#555')
    ax.text(246, -66, 'E 1/2 lot 19\nWhite, west parcel\n(deeds; No. 130)', ha='center', va='top', fontsize=7, color='#555')
    ax.text(271, -66, 'W 1/2 lot 20\nWhite, east\nparcel (1870)', ha='center', va='top', fontsize=7, color='#555')
    # buildings
    cols = {"O'Leary cottages": '#c9a96e', 'Dalton house': '#a3b18a', '133 cottages': '#a3b18a', '133 barn': '#9c8c7a', 'Dalton shed': '#9c8c7a'}
    for o in obs:
        if isinstance(o, S.Box):
            ax.add_patch(Rectangle((o.x0, o.y0), o.x1 - o.x0, o.y1 - o.y0, facecolor=cols.get(o.name, '#bbb'), edgecolor='#444', lw=0.8, zorder=2))
        else:
            if o.axis == 'x':
                ax.plot([o.c, o.c], [o.a0, o.a1], color='#7b3f00', lw=2.2, zorder=3)
            else:
                ax.plot([o.a0, o.a1], [o.c, o.c], color='#7b3f00', lw=1.2, ls=':', zorder=3)
    # barn, both variants
    ax.add_patch(Rectangle((barn.x0, barn.y0), barn.x1 - barn.x0, barn.y1 - barn.y0, facecolor='#d9534f', edgecolor='#7a1f1b', lw=1.2, zorder=4, alpha=0.85))
    v = B['oleary_barn']['variants'][1]
    ax.add_patch(Rectangle((barn.x0, 100.75 - v['depth']), v['width'], v['depth'], facecolor='none', edgecolor='#7a1f1b', lw=1.0, ls='--', zorder=4))
    ax.text(barn.x0 + 8, 90.5, "O'Leary\nbarn", ha='center', va='center', fontsize=8, color='white', zorder=5, weight='bold')
    ax.text(d['oleary'].x0 + 8, 20, "O'Leary\ncottages", ha='center', va='center', fontsize=8, zorder=5)
    ax.text(d['dalton'].x0 + 9.5, 56, 'Dalton\n(on 4-ft posts)', ha='center', va='center', fontsize=8, zorder=5)
    ax.text(d['forbes'].x0 + 9, 36, 'Forbes /\nLee /\nConnovan', ha='center', va='center', fontsize=7.5, zorder=5)
    ax.text(195.9, 90.75, '133 barn\n(2 storey)', ha='center', va='center', fontsize=7.5, zorder=5)
    ax.text(168.4, 94.75, 'shed', ha='center', va='center', fontsize=7.5, zorder=5)
    ax.text(156.6, 18, 'front fence / 8-ft fence', rotation=90, fontsize=6.5, color='#7b3f00', va='center', ha='right')
    # observer boxes
    labels = {'P1_white_west_fence_Bales': 'P1', 'P1b_white_west_midpoint_Bales': 'P1b', 'P2_white_east_130': 'P2', 'P3_own_house_134': 'P3', 'P4_vacant_lot_136': 'P4', 'P5_opposite_oleary': 'P5'}
    for k, p in P.items():
        ax.add_patch(Rectangle((p['x'][0], p['y'][0]), p['x'][1] - p['x'][0], p['y'][1] - p['y'][0], facecolor='#4a6fa5', alpha=0.25 if k != 'P1b_white_west_midpoint_Bales' else 0.9, edgecolor='#1f3b63', lw=0.8, zorder=6))
        ax.text(0.5 * (p['x'][0] + p['x'][1]), p['y'][0] - 3.5 if k != 'P1b_white_west_midpoint_Bales' else p['y'][1] + 3.5, labels[k], ha='center', va='top' if k != 'P1b_white_west_midpoint_Bales' else 'bottom', fontsize=8, color='#1f3b63', weight='bold', zorder=7)
    # rays
    E1 = (221.0, -59.0); E3 = (196.0, -55.5); E2 = (246.0, -59.0)
    for E, col, lab in [(E2, '#7a1f1b', 'from P2 (Bales seat)'), (E1, '#1f3b63', 'from P1b'), (E3, '#2a7f62', 'from P3')]:
        for T in [(barn.x0, barn.y0), (barn.x1, barn.y0), (barn.x1, barn.y1)]:
            ax.plot([E[0], T[0]], [E[1], T[1]], color=col, lw=1.0, alpha=0.9, zorder=8)
        ax.plot([E[0]], [E[1]], marker='o', color=col, ms=5, zorder=9)
    ax.plot([], [], color='#7a1f1b', label="from P2: Bales's seat, midpoint of White's west parcel (E 1/2 lot 19 by the deeds)")
    ax.plot([], [], color='#1f3b63', label="from P1b: midpoint of the parcel west of it (Sullivan's house by the deeds)")
    ax.plot([], [], color='#2a7f62', label="from P3: the next half-lot west (No. 134 by the 1891 numbering)")
    ax.legend(loc='upper right', fontsize=8, frameon=True)
    ax.set_xlim(95, 310); ax.set_ylim(-84, 118); ax.set_aspect('equal')
    ax.set_xlabel('feet east of the 1871 east line of Jefferson Street'); ax.set_ylabel('feet north of the DeKoven Street building line')
    ax.set_title('Block 38 north of DeKoven Street, 8 October 1871: central values of the model (not a survey)', fontsize=10)
    fig.tight_layout(); fig.savefig(f'{HERE}/fig_plan.png', dpi=150); plt.close(fig)

def profile(E, ax, title, variant=0):
    obs, barn, d = central_block(variant)
    # target: centre of the barn's south wall at the ridge, and the lowest visible point on that column
    tx = 0.5 * (barn.x0 + barn.x1); ty = barn.y0 - 0.01
    z_low = S.lowest_visible_on_column(E, tx, ty, obs, zlo=0.0, zhi=120.0, tol=0.1)
    L = math.hypot(tx - E[0], ty - E[1])
    s = np.linspace(0, 1, 1200)
    xs = E[0] + s * (tx - E[0]); ys = E[1] + s * (ty - E[1])
    h = S.hfield(obs, xs, ys)
    dist = s * L
    ax.fill_between(dist, 0, h, color='#b8b0a4', step=None, label='silhouette of what the ray crosses')
    # barn
    bz = np.linspace(0, 1, 50)
    ax.add_patch(Rectangle((L, 0), 4, barn.ridge, facecolor='#d9534f', edgecolor='#7a1f1b', label="O'Leary barn (south wall to ridge)"))
    # rays
    ax.plot([0, L], [E[2], barn.ridge], color='#1f3b63', lw=1.2, label=f'ray to the ridge ({barn.ridge:.0f} ft)')
    if not np.isnan(z_low):
        ax.plot([0, L], [E[2], z_low], color='#c0392b', lw=1.2, ls='--', label=f'lowest visible point on the south wall: {z_low:.1f} ft')
    ax.plot([0], [E[2]], marker='o', color='#1f3b63')
    ax.text(0, E[2] + 1, f'eye {E[2]:.1f} ft', fontsize=8, color='#1f3b63')
    # annotate obstacles crossed
    for o in obs:
        if isinstance(o, S.Box):
            hh = o.h(xs, ys); m = hh > 0
            if m.any():
                i0 = np.argmax(m); i1 = len(m) - 1 - np.argmax(m[::-1])
                ax.text(0.5 * (dist[i0] + dist[i1]), hh[m].max() + 0.6, o.name, ha='center', fontsize=7.5)
    ax.set_xlim(0, L + 8); ax.set_ylim(0, 36); ax.set_xlabel('distance along the line of sight (ft)'); ax.set_ylabel('height above lot grade (ft)')
    ax.set_title(title, fontsize=9); ax.legend(loc='upper left', fontsize=7.5)
    return z_low, barn

def draw_profiles():
    fig, axes = plt.subplots(3, 1, figsize=(11, 12.5))
    z2, b2 = profile((246.0, -59.0, 4.4), axes[0], "From P2, Bales's seat: seated on the raised walk at the midpoint of White's west parcel (x 246, y -59, eye 4.4 ft) to the middle of the barn's south wall")
    z1, b1 = profile((221.0, -59.0, 4.4), axes[1], "From P1b, the midpoint of the parcel west of it, Sullivan's own house by the deeds (x 221, y -59, eye 4.4 ft)")
    z3, b3 = profile((196.0, -55.5, 4.4), axes[2], "From P3, the next half-lot west, No. 134 by the 1891 numbering (x 196, y -55.5, eye 4.4 ft)")
    print('P2  lowest visible on south wall (central config):', z2, 'ridge', b2.ridge)
    fig.tight_layout(); fig.savefig(f'{HERE}/fig_profile.png', dpi=150); plt.close(fig)
    print('P1b lowest visible on south wall (central config):', z1, 'ridge', b1.ridge)
    print('P3  lowest visible on south wall (central config):', z3, 'ridge', b3.ridge)

if __name__ == '__main__':
    draw_plan(); draw_profiles()
    print('figures written')

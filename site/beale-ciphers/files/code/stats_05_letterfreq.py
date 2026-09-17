"""Task 5: letter frequencies of B1 and B3 decoded with the Declaration key.

Decodes with (i) the straight count of the pamphlet's Declaration and (ii) the pamphlet's
own numbering as resolved by cipher 2 ('resolved', results/stats_key_check.json).  Compares
the decoded letter distribution with (a) English (Norvig's Google-books counts) and the
pamphlet's own prose, (b) the distribution of initial letters of the key, and (c) what the
same decode gives for cipher 2.  The null 'numbers unrelated to the key' is made concrete by
re-decoding each cipher with locally shuffled keys (initials permuted within blocks of 20
consecutive words: this keeps each number's neighbourhood but destroys the identity of the
word) - the decoded letter distribution should then look like the key's initial distribution
re-weighted by where the cipher's numbers fall.  Per-letter standardised residuals identify
any letter in excess.  Writes results/stats_letterfreq.json.
"""
import os, json
from collections import Counter
import numpy as np
from scipy import stats
from stats_common import *

SEED = 20260914
NSH = 4000
rng = np.random.default_rng(SEED)
C = load_ciphers()
with open(os.path.join(RESULTS, "stats_key_check.json")) as f:
    KC = json.load(f)
keys = {"straight": [word_initial(w) for w in load_key_words()], "resolved": KC["best_initials"]}
eng = english_probs()
prose_letters = load_pamphlet_prose_letters()
prose_p = freq_vector(prose_letters); prose_p /= prose_p.sum()
b2_letters = KC["plaintext_763"]
b2_p = freq_vector(b2_letters); b2_p /= b2_p.sum()


def letter_counts(dec):
    return freq_vector([c for c in dec if c != "?"])


def local_shuffle(initials, block, rng):
    ini = list(initials)
    for s in range(0, len(ini), block):
        seg = ini[s:s + block]
        rng.shuffle(seg)
        ini[s:s + block] = seg
    return ini


out = {"seed": SEED, "n_shuffles": NSH, "english_probs": eng.tolist(), "pamphlet_prose_probs": prose_p.tolist(),
       "b2_plaintext_probs": b2_p.tolist(), "keys": {}}
for kname, ini in keys.items():
    key_ini_p = freq_vector([c for c in ini if c]); key_ini_p /= key_ini_p.sum()
    kres = {"key_initial_probs": key_ini_p.tolist(), "ciphers": {}}
    for k in (1, 2, 3):
        x = C[k]
        dec = decode(x, ini)
        n_oob = dec.count("?")
        obs = letter_counts(dec); n = obs.sum()
        obs_p = obs / n
        # distances to references
        def comp(ref):
            st, dof, p = chi2_gof(obs, ref, min_expected=5)
            return {"chi2": st, "dof": dof, "p": p, "kl_obs_ref": kl_div(obs_p, ref), "js": js_div(obs_p, ref)}
        r = {"n_decoded": int(n), "n_out_of_range": n_oob, "counts": obs.astype(int).tolist(),
             "probs": obs_p.tolist(), "decoded_text": dec,
             "vs_english": comp(eng), "vs_pamphlet_prose": comp(prose_p), "vs_key_initials": comp(key_ini_p),
             "vs_b2_plaintext": comp(b2_p)}
        # null: locally shuffled keys (block 20) -> expected letter distribution given the numbers
        sims = np.zeros((NSH, 26)); kls = np.zeros(NSH); kl_eng = np.zeros(NSH); top_e = np.zeros(NSH)
        for i in range(NSH):
            ini_s = local_shuffle(ini, 20, rng)
            cs = letter_counts(decode(x, ini_s)); sims[i] = cs
            ps = cs / cs.sum()
            kls[i] = kl_div(ps, key_ini_p); kl_eng[i] = kl_div(ps, eng)
        exp_p = sims.mean(axis=0) / sims.mean(axis=0).sum()
        st, dof, p = chi2_gof(obs, exp_p, min_expected=5)
        # Monte-Carlo p for chi2 vs the reweighted expectation (statistic under the shuffles)
        chi_sims = np.array([chi2_gof(s, exp_p, min_expected=5)[0] for s in sims])
        p_mc = perm_pvalue(int((chi_sims >= st - 1e-12).sum()), NSH)
        # is the decode closer to English than shuffled keys would make it?
        kl_obs_eng = kl_div(obs_p, eng)
        p_eng = perm_pvalue(int((kl_eng <= kl_obs_eng + 1e-12).sum()), NSH)
        # per-letter standardised residuals
        sd = sims.std(axis=0); z = (obs - sims.mean(axis=0)) / np.where(sd > 0, sd, np.nan)
        r["vs_local_shuffle_null"] = {"expected_probs": exp_p.tolist(), "chi2": st, "dof": dof,
                                      "p_asymptotic": p, "p_mc": p_mc, "kl_obs_vs_english": kl_obs_eng,
                                      "kl_null_vs_english_mean": float(kl_eng.mean()),
                                      "kl_null_vs_english_p2.5": float(np.percentile(kl_eng, 2.5)),
                                      "p_closer_to_english_than_null": p_eng,
                                      "z_by_letter": dict(zip(ALPHA, [None if np.isnan(v) else float(v) for v in z])),
                                      "expected_counts": sims.mean(axis=0).tolist()}
        # letters in excess (z > 3) / deficit
        r["letters_z_gt_3"] = [c for c, v in zip(ALPHA, z) if not np.isnan(v) and v > 3]
        r["letters_z_lt_m3"] = [c for c, v in zip(ALPHA, z) if not np.isnan(v) and v < -3]
        kres["ciphers"][f"B{k}"] = r
        print(f"key={kname} B{k}: decoded {n} (+{n_oob} out of range); chi2 vs English {r['vs_english']['chi2']:.0f} "
              f"(KL {r['vs_english']['kl_obs_ref']:.3f}); vs key initials KL {r['vs_key_initials']['kl_obs_ref']:.3f}; "
              f"vs local-shuffle expectation chi2={st:.1f} p_mc={p_mc:.3f}; KL to English {kl_obs_eng:.3f} vs null {kl_eng.mean():.3f} "
              f"(p closer={p_eng:.3f}); excess letters {r['letters_z_gt_3']} deficit {r['letters_z_lt_m3']}")
        top = sorted(zip(ALPHA, obs_p), key=lambda t: -t[1])[:8]
        print("     top letters: " + ", ".join(f"{c}={p:.3f}" for c, p in top))
    out["keys"][kname] = kres
save_json(out, "stats_letterfreq.json")

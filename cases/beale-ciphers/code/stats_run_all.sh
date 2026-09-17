#!/bin/sh
# Re-run every statistics script in order (Python 3.11, numpy, scipy, matplotlib).
# Total run time about 60-90 minutes (the scan-forward grid, stats_10, is the slow part; set NSIM
# to a smaller value for a quick pass). All Monte Carlo uses fixed seeds (given in each script).
set -e
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"
python3 stats_00_key_check.py
python3 stats_01_descriptive.py
python3 stats_02_digits.py
python3 stats_03_sequential.py
python3 stats_08_serial_extras.py
python3 stats_06_capacity.py      # needs the census files in data/census/, not included here (see script)
NSIM=${NSIM:-1000} python3 stats_04_homophone_sim.py
NSIM=${NSIM:-1000} python3 stats_09_calibrated_reuse.py
NSIM=${NSIM:-300} python3 stats_10_scan_forward.py
NSIM=${NSIM:-300} python3 stats_11_acf.py
python3 stats_05_letterfreq.py
python3 stats_07_figures.py
python3 stats_summary_tables.py

The blind rerun's own code (independent-rerun/code/ngt.py and run_tests.py, unchanged) run on this
report's Lincoln and Hay pools for the 2019 design (designs.get('grieve')['candidates'], written to
data/pools.json in the rerun's format: {"lincoln_pre1860": [[id, text], ...], "hay_all": [[id, text], ...]}),
with the rerun's copies of register.json and specials.json as the questioned texts.
Command: python3 run_tests.py letter --nseq 50 --workers 1 --tag _minepool; python3 run_tests.py summary --tag _minepool
Result: 26 of the 63 Lincoln register pieces to Hay by the character 4-10 vote (the rerun's own pool: 19; this report's code on this pool: 28 to 30).

# implementing-fuzz-testing-in-cicd-with-aflplusplus — 详细参考（由 SKILL.md 拆分）

# Build a CmpLog binary for better coverage
$CC -o fuzz_harness_cmplog fuzz_harness.c -ltarget_parser \
  -fsanitize=address -DCMPLOG
```

### Step 3 --- Prepare Seed Corpus

```bash
mkdir -p corpus/
# Add valid input samples
cp test_inputs/* corpus/
# Minimize the corpus
afl-cmin -i corpus/ -o corpus_min/ -- ./fuzz_harness @@
# Further minimize individual inputs
mkdir -p corpus_tmin/
for f in corpus_min/*; do
    afl-tmin -i "$f" -o "corpus_tmin/$(basename $f)" -- ./fuzz_harness @@
done
```

### Step 4 --- Configure CI/CD Integration

**GitHub Actions:**

```yaml
name: Fuzz Testing
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Nightly fuzzing

jobs:
  fuzz:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4

      - name: Install AFL++
        run: |
          sudo apt-get update
          sudo apt-get install -y aflplusplus

      - name: Restore corpus cache
        uses: actions/cache@v4
        with:
          path: corpus/
          key: fuzz-corpus-${{ github.sha }}
          restore-keys: fuzz-corpus-

      - name: Build fuzzing harness
        run: |
          export CC=afl-clang-fast
          export AFL_USE_ASAN=1
          make fuzz_harness

      - name: Run AFL++ fuzzing (CI mode)
        env:
          AFL_CMPLOG_ONLY_NEW: 1
          AFL_FAST_CAL: 1
          AFL_NO_STARTUP_CALIBRATION: 1
        run: |
          mkdir -p findings/
          timeout 7200 afl-fuzz \
            -S ci_fuzzer \
            -i corpus/ \
            -o findings/ \
            -t 5000 \
            -- ./fuzz_harness @@ || true

      - name: Check for crashes
        run: |
          CRASHES=$(find findings/ -path "*/crashes/*" -not -name "README.txt" | wc -l)
          echo "Found $CRASHES unique crashes"
          if [ "$CRASHES" -gt 0 ]; then
            echo "::error::AFL++ found $CRASHES crashes"
            for crash in findings/*/crashes/*; do
              [ -f "$crash" ] && echo "Crash: $crash ($(wc -c < $crash) bytes)"
            done
            exit 1
          fi

      - name: Update corpus cache
        if: always()
        run: |
          afl-cmin -i findings/ci_fuzzer/queue/ -o corpus/ -- ./fuzz_harness @@
```

### Step 5 --- Parallel Fuzzing for Nightly Runs

```bash
# Launch multiple secondary instances for better coverage
for i in $(seq 1 $(nproc)); do
    afl-fuzz -S fuzzer_$i \
      -i corpus/ \
      -o findings/ \
      -- ./fuzz_harness @@ &
done

# Wait for all fuzzers
wait

# Merge and minimize corpus
afl-cmin -i findings/*/queue/ -o corpus_merged/ -- ./fuzz_harness @@
```

### Step 6 --- Crash Triage

```bash
# Reproduce and categorize crashes
for crash in findings/*/crashes/*; do
    echo "=== Testing: $crash ==="
    timeout 5 ./fuzz_harness_asan "$crash" 2>&1 | head -20
    echo "---"
done

# Deduplicate crashes by stack trace
afl-collect findings/ crashes_deduped/ -- ./fuzz_harness @@
```

## CI/CD Best Practices for AFL++

| Setting | CI Short Run | Nightly Long Run |
|---------|-------------|-----------------|
| Duration | 30-60 min | 4-24 hours |
| Mode | `-S` (secondary only) | `-S` (no `-M` for CI) |
| `AFL_CMPLOG_ONLY_NEW` | 1 | 1 |
| `AFL_FAST_CAL` | 1 | 0 |
| `AFL_NO_STARTUP_CALIBRATION` | 1 | 0 |
| Corpus caching | Required | Required |
| Parallel instances | 1-2 | nproc |

## Monitoring Fuzzing Campaigns

```bash
# View fuzzing statistics
afl-whatsup findings/

# Key metrics to track:
# - Total paths found (code coverage indicator)
# - Unique crashes / unique hangs
# - Stability percentage (should be >90%)
# - Exec speed (execs/sec)
# - Cycles done (full corpus cycles completed)
```

## References

- [AFL++ Documentation](https://aflplus.plus/docs/)
- [AFL++ GitHub Repository](https://github.com/AFLplusplus/AFLplusplus)
- [AFL++ Fuzzing in Depth Guide](https://aflplus.plus/docs/fuzzing_in_depth/)
- [Google Testing Handbook - AFL++](https://appsec.guide/docs/fuzzing/c-cpp/aflpp/)
- [OWASP Fuzzing Guide](https://owasp.org/www-community/Fuzzing)

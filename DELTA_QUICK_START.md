# Δ-Audit Quick Start Guide
**For: Rapid framework validation**
**Time: 1-hour audit → decision**

---

## The 1-Hour Audit Protocol

### Setup (5 minutes)

1. **State your claim in ONE sentence**:
   - ❌ Bad: "Our system is better"
   - ✅ Good: "TrueSkill ranking reduces memory entrenchment by ≥20% vs recency baseline"

2. **Define the null** (what's boring/random):
   - Example: Random memory selection

3. **Pick your metric**:
   - What measures success? (conversion rate, recall accuracy, speed, etc.)

4. **Set corridor** (safe operating range):
   - K_min: Minimum acceptable performance
   - K_max: Maximum before diminishing returns

---

### The 5-Question Audit (10 min each)

#### Q1: E0 - Does Random Give Zero? (Calibration)

**Test**: Run your metric on randomized/shuffled data
**Pass**: Result ≈ 0 or baseline (p > 0.05)
**Fail**: Your measurement is broken

**Example**:
```python
# Claim: "JIT Memory improves recall"
baseline_success = random_memory_selection(trials=100)
# Should be ≈50% (chance)

if baseline_success < 0.45 or baseline_success > 0.55:
    print("❌ E0 FAIL: Metric is biased")
else:
    print("✅ E0 PASS: Metric is calibrated")
```

---

#### Q2: E1 - Does It Survive Amplitude Mute? (Real Signal)

**Test**: Flatten/normalize magnitudes, keep structure
**Pass**: Pattern persists
**Fail**: Effect disappears (was amplitude artifact)

**Example**:
```python
# Claim: "Concept relationships are phase-based"
normalized_concepts = normalize_amplitudes(concepts)
relationships_after = measure_relationships(normalized_concepts)

if relationships_after ~= relationships_before:  # within CI
    print("✅ E1 PASS: Real structure")
else:
    print("❌ E1 FAIL: Amplitude artifact")
```

---

#### Q3: E2 - Does Relabeling Change Results? (Invariance)

**Test**: Shuffle labels, reindex, permute
**Pass**: Same results (within CI)
**Fail**: Results depend on arbitrary choices

**Example**:
```python
# Claim: "Hazard score measures action validity"
original_scores = [hazard(a) for a in actions]
shuffled_actions = shuffle(actions)
shuffled_scores = [hazard(a) for a in shuffled_actions]

if sorted(original_scores) == sorted(shuffled_scores):
    print("✅ E2 PASS: Permutation invariant")
else:
    print("❌ E2 FAIL: Depends on indexing")
```

---

#### Q4: E3 - Does Nudging Change Things? (Causality)

**Test**: Small intervention, measure response
**Pass**: Predicted change > sham/control
**Fail**: No effect or wrong direction

**Example**:
```python
# Claim: "Humanisms improve naturalness"
# Test: Add fillers to 120 calls, remove from 120 calls
group_with = add_humanisms(calls[:120])
group_without = baseline(calls[120:])

lift = mean(naturalness(group_with)) - mean(naturalness(group_without))
p_value = t_test(group_with, group_without)

if lift > 0 and p_value < 0.01:
    print(f"✅ E3 PASS: Lift = {lift:.2f}, p = {p_value:.4f}")
else:
    print(f"❌ E3 FAIL: No causal effect")
```

---

#### Q5: E4 - Does It Scale? (Persistence)

**Test**: 2x the data/complexity, remeasure
**Pass**: Effect persists or improves
**Fail**: Effect degrades or inverts

**Example**:
```python
# Claim: "TrueSkill prevents entrenchment"
entrenchment_1x = measure_entrenchment(memories=1000)
entrenchment_2x = measure_entrenchment(memories=2000)

if entrenchment_2x <= entrenchment_1x * 1.2:  # allow 20% slack
    print(f"✅ E4 PASS: Scales well ({entrenchment_2x:.3f})")
else:
    print(f"❌ E4 FAIL: Degrades at scale ({entrenchment_2x:.3f})")
```

---

### Decision (5 minutes)

Count your passes:

| Passes | Label | What It Means |
|--------|-------|---------------|
| 0-1 | ❌ **Broken** | Fix measurement or claim |
| 2 | 🔬 **Probe** | Interesting, keep exploring |
| 3 | ⚠️ **Primitive** | Real pattern, no causality |
| 4 | ⚠️ **Primitive+** | Causal, doesn't scale |
| 5 | ✅ **Law** | Ship it! |

---

## Common Failure Patterns

### Pattern 1: "Amazing Results, But..."

**Symptom**: Claims look great in demos, fail in audit
**Cause**: Overfitting, cherry-picking, or amplitude artifacts
**Fix**: Run E1 (amplitude mute) immediately

**Example**:
- "Our AI remembers perfectly!" → but only recalls recent items (amplitude: recency bias)
- Fix: Normalize by time, test again

---

### Pattern 2: "It Works, But We Don't Know Why"

**Symptom**: E0-E2 pass, E3 fails
**Cause**: Correlation without causation
**Fix**: You have a **Primitive**, not a **Law**. Can report, but can't predict interventions.

**Example**:
- "High engagement correlates with sales" → but increasing engagement doesn't increase sales
- Label: Primitive (observational, not causal)

---

### Pattern 3: "Works in Lab, Breaks in Production"

**Symptom**: E0-E3 pass, E4 fails
**Cause**: Doesn't scale, overfitted to small regime
**Fix**: Simplify or restrict scope

**Example**:
- "Complex ensemble wins on 1000 samples" → but degrades at 10k samples
- Solution: Use simpler model that scales

---

### Pattern 4: "Different Every Time"

**Symptom**: E2 fails (not invariant)
**Cause**: Results depend on arbitrary choices (seed, ordering, labels)
**Fix**: Find root cause of variation, fix it

**Example**:
- "Performance depends on random seed" → not a robust method
- Solution: Average over seeds or make deterministic

---

## Mini-Audit Templates

### For AI Memory Systems

```python
def audit_memory(system):
    # E0: Random baseline
    random_recall = system.recall(random_memories())
    assert random_recall < 0.55, "E0 FAIL: Random isn't random"

    # E1: Semantic structure survives normalization
    normalized = normalize_strengths(system.memories)
    assert system.recall(normalized) > baseline * 0.9, "E1 FAIL: Amplitude artifact"

    # E2: Conversation reordering doesn't change recall
    shuffled = shuffle_conversations(system.history)
    assert abs(system.recall(shuffled) - system.recall(original)) < 0.05, "E2 FAIL: Order dependent"

    # E3: Marking memories as useful increases recall
    mark_useful(system, sample_memories)
    assert system.recall(sample_memories) > baseline + 0.1, "E3 FAIL: No causal effect"

    # E4: 10x memories doesn't degrade performance
    system_10x = system.scale(10)
    assert system_10x.recall() > system.recall() * 0.8, "E4 FAIL: Doesn't scale"

    return "LAW" if all_pass else "PRIMITIVE"
```

---

### For Business Metrics

```python
def audit_business_claim(intervention, metric):
    # E0: Baseline measurement
    control = measure_metric(no_intervention, n=100)
    assert 0.4 < control < 0.6, "E0 FAIL: Baseline isn't baseline"

    # E1: Effect persists in A/B test (not demo artifact)
    ab_test = run_ab_test(intervention, control, n=200)
    assert ab_test.treatment > ab_test.control, "E1 FAIL: No A/B lift"

    # E2: Effect holds across customer segments
    segments = ['enterprise', 'smb', 'consumer']
    for seg in segments:
        lift = measure_lift(intervention, segment=seg)
        assert lift > 0, f"E2 FAIL: Doesn't work for {seg}"

    # E3: Intervention causes lift (not confounded)
    causal = intervene_randomly(sample, intervention)
    assert causal.treatment_effect > 0 and causal.p < 0.01, "E3 FAIL: Not causal"

    # E4: Effect scales to 2x volume
    scale_test = measure_metric(intervention, n=400)
    assert scale_test.lift > ab_test.lift * 0.8, "E4 FAIL: Doesn't scale"

    return "LAW" if all_pass else "PRIMITIVE"
```

---

### For Speed Claims

```python
def audit_speed_claim(system, baseline):
    # E0: Apples-to-apples comparison
    task = "Summarize 100k chars to 500 words"
    system_time = benchmark(system, task, trials=10)
    baseline_time = benchmark(baseline, task, trials=10)
    assert system_time < baseline_time, "E0 FAIL: Not actually faster"

    # E1: Speed comes from architecture, not shortcuts
    equal_quality = verify_output_quality(system, baseline)
    assert equal_quality, "E1 FAIL: Quality sacrificed for speed"

    # E2: Speed holds across different tasks
    tasks = [summarize, qa, reasoning, code_gen]
    for t in tasks:
        assert benchmark(system, t) < benchmark(baseline, t), f"E2 FAIL: {t}"

    # E3: Adding parallelism increases speed linearly
    modules = [1, 2, 4, 8]
    speeds = [benchmark(system, modules=m) for m in modules]
    assert is_linear(speeds, modules), "E3 FAIL: Doesn't parallelize"

    # E4: Speed scales to 10x task size
    large_task = scale_task(task, 10)
    assert benchmark(system, large_task) < baseline(large_task), "E4 FAIL: Breaks at scale"

    speedup = baseline_time / system_time
    return f"LAW: {speedup:.1f}x faster" if all_pass else "PRIMITIVE"
```

---

## Red Flags (Abort Audit)

### 🚩 Red Flag #1: Can't Define the Null
If you can't articulate "what would boring/random look like?", you can't audit.
**Action**: Stop. Define null first.

### 🚩 Red Flag #2: Metric Changes During Testing
If you're tweaking the metric as you go, you're p-hacking.
**Action**: Pre-register metric, stick to it.

### 🚩 Red Flag #3: "Trust Me, It's Good"
If explanation involves intuition, philosophy, or hand-waving without numbers:
**Action**: Demand operational definition.

### 🚩 Red Flag #4: Results Too Good
If your system is 100x better, something's probably wrong (measurement, comparison, or overfitting).
**Action**: Check E0 very carefully.

### 🚩 Red Flag #5: Can't Reproduce
If results change every run (and E2 passes), something's non-deterministic that shouldn't be.
**Action**: Fix randomness or document variance.

---

## The 10-Minute Audit (Ultra-Fast)

When you need a verdict NOW:

1. **E0 (2 min)**: Random gives ~50%? → ✅ or ❌
2. **E3 (5 min)**: Intervention lifts metric? → ✅ or ❌
3. **E4 (3 min)**: 2x data, same effect? → ✅ or ❌

**Decision**:
- 3/3 → Ship it (Law)
- 2/3 → Investigate (Primitive)
- 1/3 or 0/3 → Don't ship (Probe or Broken)

---

## Audit Notebook Template

Copy this into your notes when auditing:

```markdown
# Δ-Audit: [Framework Name]

## Claim (one sentence)
[Your claim here]

## Null Hypothesis
[What's random/boring?]

## Metric
[How do you measure success?]

## E0: Calibration
- [ ] Test: [Describe test]
- [ ] Result: [Pass/Fail + numbers]
- [ ] Notes: [Any issues?]

## E1: Vibration
- [ ] Test: [Describe test]
- [ ] Result: [Pass/Fail + numbers]
- [ ] Notes: [Any issues?]

## E2: Symmetry
- [ ] Test: [Describe test]
- [ ] Result: [Pass/Fail + numbers]
- [ ] Notes: [Any issues?]

## E3: Causal
- [ ] Test: [Describe test]
- [ ] Result: [Pass/Fail + numbers]
- [ ] Notes: [Any issues?]

## E4: RG Persistence
- [ ] Test: [Describe test]
- [ ] Result: [Pass/Fail + numbers]
- [ ] Notes: [Any issues?]

## Decision
- Audits passed: [#]/5
- Label: [Probe/Primitive/Law]
- Confidence: [Low/Medium/High]
- Next steps: [What needs to happen?]

## Kill Switches
- [ ] None activated
- [ ] [List any that triggered]

## PCO
- Data: [hash or source]
- Code: [hash or version]
- Seeds: [RNG seeds used]
- Config: [parameters]
```

---

## Integration with Existing Workflow

### Before Starting Work
1. Write claim (one sentence)
2. Define null
3. Run E0 (2 minutes)
4. **If E0 fails, stop. Fix measurement.**

### During Development
- Run E1/E2 as sanity checks
- Track metrics over time
- Document anomalies immediately

### Before Shipping
- Run full E0-E4 audit (1 hour)
- Get peer review on audit
- Archive PCO (hashes, seeds, configs)
- Label appropriately (Probe/Primitive/Law)

### Post-Launch
- Monitor E4 in production (does it scale?)
- Track degradation over time
- Re-audit quarterly if Law, annually if Primitive

---

## Audit Budgets (Time)

| Task | Time | When |
|------|------|------|
| Quick check (E0 only) | 2 min | Every commit |
| Sanity audit (E0-E2) | 10 min | Daily |
| Causal audit (E0-E3) | 30 min | Before feature |
| Full audit (E0-E4) | 1 hour | Before launch |
| Scale test (E4 deep) | 1 day | After 10x growth |
| Research audit (comprehensive) | 1 week | Major claims |

---

## FAQ (Rapid Fire)

**Q: My system is too complex to audit in 1 hour.**
A: Break it into components. Audit each separately.

**Q: I don't have 240 trials for E3.**
A: Start with 30. Get directional signal. Scale later.

**Q: E0 fails. Now what?**
A: Fix measurement system. Everything downstream is meaningless.

**Q: Can I skip E4?**
A: Yes, if you label as Primitive (not Law). But test it eventually.

**Q: What if E2 fails?**
A: Your result is an artifact. Find the source of variance and fix it.

**Q: My metric is perfect, audit is wrong.**
A: Audit doesn't lie. If E0 fails, your metric is miscalibrated.

**Q: How do I audit qualitative claims?**
A: Make them quantitative. "Better UX" → "Task completion time <30s"

**Q: Can I adjust thresholds?**
A: Yes, but pre-register them. Don't tweak after seeing results.

---

## Real-World Example (Start to Finish)

### Scenario: Auditing "Humanisms Database"

**Claim**: "Adding 'um' and 'uh' to AI speech increases perceived naturalness by 20%."

**Time budget**: 1 hour

---

#### Minute 0-5: Setup

**Null**: Random noise insertion (not semantic fillers)
**Metric**: Human rating of naturalness (1-10 scale)
**Corridor**: Baseline = 3.2/10 (synthetic), Target ≥ 4.0/10

---

#### Minute 5-15: E0

**Test**: Ask 20 people to rate:
- Synthetic voice (no fillers)
- Synthetic voice + random beeps
- Human voice (ground truth)

**Results**:
- Synthetic: 3.1/10 (σ=0.8)
- Random beeps: 3.3/10 (σ=0.9)
- Human: 7.8/10 (σ=1.2)

**Verdict**: ✅ E0 PASS (random is ~baseline, not inflated)

---

#### Minute 15-25: E1

**Test**: Does timing matter, or just filler presence?
- Condition A: Fillers with natural timing (delays before "um")
- Condition B: Fillers with random timing (immediate "um")

**Results**:
- A: 4.6/10 (σ=1.1)
- B: 3.5/10 (σ=0.9)

**Verdict**: ✅ E1 PASS (timing matters → phase structure, not amplitude)

---

#### Minute 25-35: E2

**Test**: Permutation invariance across listener demographics
- Age: 20s, 30s, 40s, 50s+
- Gender: M, F, Other
- Native English: Yes, No

**Results**: All segments show lift (4.2-4.9 range), p<0.05 for each

**Verdict**: ✅ E2 PASS (effect is robust across segments)

---

#### Minute 35-50: E3

**Test**: A/B test on 240 calls (120 with, 120 without)
- Measure: Naturalness rating + conversion rate

**Results**:
- With fillers: 4.7/10 naturalness, 18% conversion
- Without: 3.2/10 naturalness, 15% conversion
- Lift: +1.5 points naturalness (p<0.001), +3% conversion (p=0.04)

**Verdict**: ⚠️ E3 PARTIAL PASS
- Naturalness lift: ✅ Clear causal effect
- Conversion lift: ⚠️ Marginal (3%, not 20% claimed)
- **Claim overstated but directionally correct**

---

#### Minute 50-60: E4

**Test**: Scale to 480 calls (2x), remeasure
**Results**:
- Naturalness lift holds: +1.4 points (stable)
- Conversion lift: +2.8% (stable, but still not 20%)

**Verdict**: ✅ E4 PASS (scales consistently)

---

#### Decision (Minute 60)

**Audits**: E0✅ E1✅ E2✅ E3⚠️ E4✅

**Label**: **PRIMITIVE+** (approaching Law, but claim needs revision)

**S***: 3.1 (just above Primitive threshold)

**Recommendation**:
- ✅ **Ship** with revised claim: "Increases naturalness by ~45% (3.2→4.7/10) with 3% conversion lift"
- ❌ Don't claim 20% conversion lift (not supported by data)
- 🔬 Investigate: Why is conversion lift smaller than expected? (Maybe naturalness ≠ trust?)

**Next steps**:
- A/B test other factors (voice tone, script, timing)
- Longer-term study (does effect persist after 1000+ calls?)
- Cross-industry validation (real estate vs B2B vs retail)

---

## Conclusion

**Δ-Audit in 3 Rules**:

1. **Define null, measure it** (E0)
2. **Nudge system, measure response** (E3)
3. **Scale 2x, measure again** (E4)

Everything else is detail.

**When in doubt**: Run E0 and E3. If both pass, you're 80% there.

**Remember**:
- ❌ No audit = no ship
- ⚠️ Partial audit = ship with caveats
- ✅ Full audit = ship with confidence

---

## Appendix: One-Liners

**E0**: "Does random give zero?"
**E1**: "Does it survive amplitude mute?"
**E2**: "Does relabeling change results?"
**E3**: "Does nudging change things?"
**E4**: "Does it scale?"

**Probe**: Interesting, keep exploring (0-2 passes)
**Primitive**: Real, but not causal (3 passes)
**Law**: Causal and persistent (4-5 passes)

**Kill switches**:
- ❌ Force phase outside capture
- ❌ Amplitude-only gains
- ❌ Symmetry violations
- ❌ No causal lift
- ❌ RG inversion

**Golden rule**: Low-order wins. Simple beats complex if both work.

---

**Ready to audit? Go.**

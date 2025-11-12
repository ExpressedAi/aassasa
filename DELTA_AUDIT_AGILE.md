# Δ-Audit: Agile Primitives System
**Version 2.0 - Operational**
*Compact audit framework for novel systems*

---

## Quick Reference

**Purpose**: Rapidly audit novel frameworks, architectures, and claims with rigorous discipline.

**Core Principle**: **Low-order wins**. Simple explanations that survive testing beat complex ones that don't.

**Audit Levels**: E0 → E1 → E2 → E3 → E4 (fail any = demote)

**Labels**:
- **Probe** (E0-E1): Exploring, no claims
- **Primitive** (E0-E2): Reproducible structure, no causality proven
- **Law** (E0-E4): Causal, persistent, predictive

---

## The Five Audits (Gate Model)

### E0: CALIBRATION (Is this measurement trustworthy?)
**Question**: Does your measurement system work under null conditions?

**Requirements**:
- [ ] Define the **null hypothesis** (what does "nothing interesting" look like?)
- [ ] Run null test: shuffle, scramble, or randomize your data
- [ ] Your metric should be ~0 or ~baseline under null
- [ ] P-values, confidence intervals work as expected
- [ ] Measurement is gauge-invariant (doesn't depend on arbitrary choices)

**Example**:
- Claim: "JIT Memory improves recall"
- Null: Random memory selection
- Test: Does your scoring system give ~0 advantage to random selection?

**Fail → Can't trust ANY downstream results. Fix optics.**

---

### E1: VIBRATION (Is there genuine signal?)
**Question**: Is there real structure, or are you measuring noise/artifacts?

**Requirements**:
- [ ] **Amplitude mute test**: If you flatten/normalize the data, does the pattern survive?
- [ ] **Narrowband signature**: Is the signal localized, not broadband noise?
- [ ] **Time-reversal sanity**: Directed effects flip sign; symmetric effects don't

**Example**:
- Claim: "Bloch Array shows concept relationships"
- Test: If you randomize concept amplitudes but keep phases, do relationships persist?

**Fail → You're measuring amplitude artifacts, not real structure. Demote to Probe.**

---

### E2: SYMMETRY (Is this invariant or arbitrary?)
**Question**: Does your claim depend on arbitrary choices?

**Requirements**:
- [ ] **Permutation invariant**: Relabeling/reordering doesn't change results
- [ ] **Gauge invariant**: Coordinate system choices don't matter
- [ ] **Declared symmetries hold**: If you claim translation/rotation invariance, prove it

**Example**:
- Claim: "Hazard Law measures action validity"
- Test: Does hazard score change if you reindex your action space? (It shouldn't)

**Fail → Your result is an artifact of labeling/framing. Void claim.**

---

### E3: CAUSAL (Does intervention work?)
**Question**: If you nudge the system, does it respond as predicted?

**Requirements**:
- [ ] **Micro-nudge protocol**: ±5° phase / ±2% parameter, ≥240 trials
- [ ] **On-manifold**: Nudge within valid operating range
- [ ] **Positive lift vs sham**: Real nudges > fake nudges, correct sign
- [ ] **Lag consistency**: Effect appears at predicted time, not instantly

**Example**:
- Claim: "Maritime's humanisms database improves perceived naturalness"
- Test: Add/remove fillers in A/B test, measure human ratings. Does it lift?

**Fail → No causal link. Correlation only. Demote to Primitive.**

---

### E4: RG PERSISTENCE (Does it survive coarse-graining?)
**Question**: Does your structure persist when you zoom out / pool data?

**Requirements**:
- [ ] **×2 pooling test**: Double your window/granularity, retest
- [ ] **Integer-thinning**: Simple explanations survive; complex ones die
- [ ] **Hierarchy stable**: Low-order structure persists; high-order degrades
- [ ] **Brittleness doesn't inflate**: System doesn't become more fragile at scale

**Example**:
- Claim: "TrueSkill ranking prevents memory entrenchment"
- Test: With 2x more memories, does entrenchment stay low or worsen?

**Fail → Doesn't scale. Works only in narrow regime. Demote.**

---

## Decision Matrix

| Audits Passed | Label | Rights | Requirements |
|--------------|-------|---------|--------------|
| E0-E1 | **Probe** | Explore freely | No public claims; provisional |
| E0-E2 | **Primitive** | Report findings | Include caveats; no causality |
| E0-E4 | **Law** | Make predictions | Ship with steer plan + PCO |

**PCO** = Provenance (data sources) + Configuration (settings) + Outcome (results). Must be reproducible.

---

## Operational Checklist (Use This)

### Phase 1: Setup (Before Testing)
1. [ ] **Define claim precisely** (one sentence)
2. [ ] **Specify null hypothesis** (what's random/boring?)
3. [ ] **Declare metrics** (how do you measure success?)
4. [ ] **Fix optics** (windows, gauges, tolerances - don't change mid-test)
5. [ ] **Set corridor** (safe operating range: [K_min, K_max])

### Phase 2: Audit Sequence
6. [ ] **E0**: Run null test, verify calibration
7. [ ] **E1**: Amplitude mute + narrowband checks
8. [ ] **E2**: Permutation/gauge invariance tests
9. [ ] **E3**: Micro-nudge trials (≥240, FDR p<0.01)
10. [ ] **E4**: ×2 pooling, thinning check

### Phase 3: Decision
11. [ ] **Promote or Demote** based on failures
12. [ ] **Document** in Δ-Report (see template below)
13. [ ] **Archive PCO** (hashes, seeds, configs)

---

## Core Metrics

### Lock Strength (K)
Measures "pull" between related components:
```
K ∝ |⟨e^(i·phase_error)⟩| × √(Q_a × Q_b) × gain(A_a, A_b)
```
- High K = strong relationship
- Must be phase-aligned, not just correlated amplitudes

### Capture (ε_cap)
Operating window where control is possible:
```
ε_cap = [2π·K - (Γ_a + Γ_b)]₊
```
- If ε_cap = 0, you can't steer the system
- Never force actions outside capture

### Brittleness (ζ)
How fragile is the system?
```
ζ = (Γ_a·p² + Γ_b·q²) / max(ε_cap, K)
```
- Low ζ = robust
- High ζ = fragile, will break under stress

### Evidence Score (S*)
Unified metric (gated by audits):
```
S* = w_Z·|Z| + w_χ·χ² + w_KL·D_KL + w_K·|K|
```
- Z: How many sigmas above null?
- χ²: Phase distribution mismatch
- D_KL: Information divergence
- K: Lock strength

**Only report S* if E0-E2 pass. Otherwise it's meaningless.**

---

## Anti-Patterns (Don't Do This)

1. ❌ **Forcing phase outside capture** (|s_f| > 1 or ε_cap = 0)
2. ❌ **Optimizing amplitude before eligibility** (get frequency/phase right first)
3. ❌ **Elevating high-order without RG** (complex claims need E4)
4. ❌ **Switching explanations on correlation** (need E3 causal proof)
5. ❌ **Skipping null tests** (E0 is non-negotiable)
6. ❌ **Accepting surrogate-matched effects** (if null reproduces it, it's null)
7. ❌ **Amplitude-only gains** (must survive amplitude mute, E1)

---

## Controller Discipline (F → P → A → S)

When intervening on a system, follow this priority:

### F: Frequency (Eligibility)
- **Goal**: Ensure you CAN control the system
- **Check**: ε_cap > 0 and |s_f| ≤ 0.2
- **Action**: Retune ≤2% or widen operating window
- **Never**: Force phase when |s_f| > 1

### P: Phase (Timing)
- **Goal**: Align phases on the manifold
- **Action**: Low-gain loop, max one ±5-15° snap
- **Release**: When |phase_error| ≤ 10°

### A: Amplitude (Harmony)
- **Goal**: Reweight contributions for coherence
- **Action**: Multiplicative weights, β ∈ [0, 0.05]
- **Stop**: When max|contribution| ≤ 0.02 for 3 windows
- **Guard**: Must survive amplitude mute

### S: Space (Topology)
- **Goal**: Add bridges, prune brittle edges
- **Add**: Edges that reduce complexity AND brittleness
- **Prune**: Edges with negative marginal value
- **Require**: E2 symmetry checks after edits

**One action per axis per window. Re-measure between axes.**

---

## Δ-Report Template

```json
{
  "claim": "One sentence description",
  "null": "What's the boring/random baseline?",
  "optics": {
    "window": "Time/space resolution",
    "gauges": "Coordinate systems used",
    "corridor": [K_min, K_max]
  },
  "audits": {
    "E0": {"pass": true, "notes": "Null is ~0 ± CI"},
    "E1": {"pass": true, "notes": "Survives amplitude mute"},
    "E2": {"pass": true, "notes": "Permutation invariant"},
    "E3": {"pass": true, "notes": "Lifts ΔK=+0.14 vs sham"},
    "E4": {"pass": true, "notes": "Persists under ×2 pooling"}
  },
  "metrics": {
    "S_star": 3.2,
    "K": 0.18,
    "epsilon_cap": 0.05,
    "zeta": 0.12
  },
  "label": "Law | Primitive | Probe",
  "PCO": {
    "data_hash": "sha256:...",
    "code_hash": "sha256:...",
    "seeds": {"detect": 123, "nudge": 456}
  }
}
```

---

## Domain-Specific Quick Audits

### For AI Memory Systems (like JIT)
**E0**: Random selection baseline
**E1**: Does semantic structure persist after amplitude normalization?
**E2**: Invariant to conversation reordering?
**E3**: Injecting/removing memories changes recall as predicted?
**E4**: Scales to 2x memory size without entrenchment?

### For Relationship Models (like Bloch Array)
**E0**: Null = random concept pairs
**E1**: Relationships survive if you normalize concept strengths?
**E2**: Invariant to concept relabeling?
**E3**: Nudging concept A affects concept B as predicted?
**E4**: Relationships persist when you coarse-grain the concept space?

### For Metrics/Scores (like Hazard Law)
**E0**: Null = random action selection
**E1**: Score based on phase/structure, not just magnitude?
**E2**: Invariant to action indexing?
**E3**: High-hazard actions produce predicted bad outcomes?
**E4**: Hazard predictions stable across different scales?

### For Business Claims (like Maritime)
**E0**: Random baseline (untrained model / coin flip)
**E1**: Effect persists in controlled A/B test?
**E2**: Invariant to customer segment permutations?
**E3**: Intervention (adding feature) lifts conversion?
**E4**: Effect scales to 2x volume?

---

## Axioms (Foundation)

**A0: Ground-State**
The default is boring. Claim must beat law-of-large-numbers null.

**A1: Vibration**
Phase-coherent structure is primitive. Amplitude artifacts are not.

**A2: Closure**
Only use admissible transforms. No peeking, no cheating.

**A3: Observer Discipline**
Results must be gauge-invariant. Arbitrary choices can't matter.

**A4: Quality Identity (MDL)**
Prefer simpler explanations with fewer parameters.

**A5: Contrast Restoration**
Work inside safe corridors. Abort if you leave the regime.

**Core Law: Low-Order Wins**
Simple integer relationships persist under coarse-graining. Complex ones die.

---

## Promotion Ladder

### L0: Calibration
- Fix optics, gauges, windows
- Run E0, publish null curves
- **Exit**: Null sanity achieved

### L1: Vibration Sighting
- Phase-only evidence exists
- **Operators**: Frequency (eligibility check)
- **Exit**: ε_cap > 0, phase survives mute

### L2: Symmetry-Qualified
- Invariance proven
- **Operators**: F, P, A (to lock)
- **Exit**: Amplitude-lock + invariances pass

### L3: Causal-Certified
- Tiny nudges lift metrics
- **Operators**: F, P, A, S (prudent)
- **Exit**: ΔK, Δε_cap, ΔT > 0 vs sham

### L4: RG-Persistent Law
- Survives pooling
- **Operators**: F, P, A, S (full)
- **Exit**: Integer-thinning holds, survivors stable

**One level at a time. Fail → retreat.**

---

## Integer-Thinning (RG Signature)

Simple explanations should dominate after you zoom out:

```
log(K) ≈ α - β·(complexity)
```

Where complexity = p + q (for integer ratios) or parameter count.

**After ×2 pooling**:
- β should stay negative (slope down-right)
- Low-order survivors should persist
- High-order should die first

**If this inverts (high-order beats low-order after pooling), you fail E4.**

---

## One-Page SOP (Tape This To Your Wall)

### BEFORE YOU START
1. Write claim as one sentence
2. Define null (boring baseline)
3. Fix all parameters (no tweaking mid-test)
4. Declare safe corridor [K_min, K_max]

### AUDIT SEQUENCE
5. E0: Null test → verify metric ~0 under null
6. E1: Amplitude mute → does structure survive?
7. E2: Permutation test → is it invariant?
8. E3: Nudge trials → does intervention lift metrics?
9. E4: Pool ×2 → does it scale?

### DECISION
10. Count passes: 0-1=Probe, 2-3=Primitive, 4-5=Law
11. Write Δ-Report with PCO
12. If any audit fails, demote and document why

### NEVER
- ❌ Force phase outside capture
- ❌ Skip null tests
- ❌ Change parameters mid-test
- ❌ Accept amplitude-only gains
- ❌ Promote high-order without E4

### ALWAYS
- ✅ One action per axis per window
- ✅ Re-measure between interventions
- ✅ Document all kill-switches
- ✅ Archive seeds and hashes (PCO)

---

## Kill-Switches (Automatic Demote)

1. **Eligibility breach**: Phase action with |s_f| > 1 or ε_cap = 0
2. **Amplitude illusion**: Phase evidence vanishes under mute
3. **Gauge drift**: Results change under declared symmetries
4. **Causal null**: Nudges don't lift vs sham
5. **RG inversion**: High-order beats low-order after pooling
6. **Brittleness surge**: ζ increases without performance gain

**Any of these → immediate demotion. No partial credit.**

---

## Defaults (Safe Starting Values)

```json
{
  "ratios": ["1:1", "2:1", "3:2", "1:2", "2:3"],
  "τf": 0.2,
  "φ_tol_deg": 10,
  "φ_snap_deg": 25,
  "W_windows": 3,
  "β_MWU": 0.02,
  "E3_nudge_deg": 5,
  "E3_nudge_pct": 2,
  "E3_trials_min": 240,
  "FDR": 0.01,
  "Z_min": 3
}
```

---

## Usage Examples

### Example 1: Auditing JIT Memory

**Claim**: "TrueSkill ranking prevents memory entrenchment better than recency."

**Null**: Random memory selection baseline

**E0**: ✅ Random selection gives ~0 advantage (p=0.52)
**E1**: ✅ After normalizing memory strengths (amplitude mute), semantic relationships persist
**E2**: ✅ Results identical after conversation reordering
**E3**: ✅ Manually marking memories as useful increases their TrueSkill score and recall probability (Δμ = +0.3 ± 0.1, p<0.001, Z=3.8)
**E4**: ✅ With 2x memories, entrenchment coefficient stays <0.15 (vs 0.42 for recency baseline)

**Label**: **Law**
**S***: 4.2
**Brittleness**: ζ = 0.11 (robust)

---

### Example 2: Auditing Maritime Humanisms

**Claim**: "Adding verbal fillers ('um', 'uh') increases perceived naturalness by 15%."

**Null**: Synthetic voice with no fillers vs random noise injection

**E0**: ✅ Listeners rate random noise as baseline natural (μ=3.2/10)
**E1**: ✅ Removing all prosody (amplitude flatten) destroys naturalness gains → structure is in timing
**E2**: ✅ Effect holds across age/gender permutations of listeners
**E3**: ⚠️ Adding fillers lifts perceived naturalness by only 7% (±3%), not 15%. Significant vs noise (p<0.01, Z=2.9) but weaker than claimed.
**E4**: ❓ Pending scale test with 2x sample size

**Label**: **Primitive** (needs E4)
**S***: 2.8
**Note**: Original claim overstated effect size. Causal link proven, but magnitude half of initial estimate.

---

## Integration Notes

### For Financial Applications
- E0 null = random/no-feature baseline
- E3 requires A/B test with ≥240 customers
- E4 checks if effect scales to 2x volume
- Report conversion lifts with CIs

### For Consciousness Claims
- E0 requires explicit definition of "consciousness indicators"
- E1 checks if behaviors persist without anthropomorphic framing
- E2 tests if claims hold across different AI architectures
- E3 requires intervention showing predicted change in consciousness metric
- E4 verifies that consciousness indicators scale (don't degrade with more complexity)

### For Novel Architectures
- E0 benchmarks against standard baselines (transformer, RAG, etc.)
- E1 verifies architectural advantage isn't just parameter count
- E2 ensures results generalize across datasets
- E3 validates that architectural choices have causal impact
- E4 confirms architecture scales efficiently

---

## FAQ

**Q: Do I need all five audits for every claim?**
A: No. For exploration (Probe), E0-E1 sufficient. For publication (Primitive), need E0-E2. For causal claims (Law), need all five.

**Q: What if I fail E3 but pass E0-E2?**
A: You have a reproducible pattern (Primitive) but no causal mechanism. Can't make intervention predictions. Must demote from Law to Primitive.

**Q: Can I skip E0?**
A: **Never**. E0 failure means all downstream results are uninterpretable. Fix your measurement system first.

**Q: What's the difference between E1 and E2?**
A: E1 asks "is the signal real?" (vs amplitude artifacts). E2 asks "is it fundamental?" (vs arbitrary framing).

**Q: How do I choose the null hypothesis?**
A: Ask: "What's the boring explanation?" Then test if your claim beats it.

**Q: What does "integer-thinning" mean practically?**
A: Simpler explanations should win after you zoom out. If complex explanations are required at every scale, something's wrong.

**Q: What's ε_cap and why does it matter?**
A: It's your operating window. If ε_cap = 0, you can't control the system. Like trying to steer a car with no steering wheel.

**Q: When do I use S* vs individual metrics?**
A: S* is an aggregate for ranking. Use individual metrics (K, ε_cap, ζ) for operational decisions. Both matter.

**Q: What if my system is too complex for these metrics?**
A: That's a red flag. If you can't define simple metrics, your system might be overfitted or ill-defined. Simplify first.

---

## Versioning

**v2.0 Agile** (This Document)
- Streamlined from 200KB formalism to <30KB operational guide
- Preserved E0-E4 audit rigor
- Added domain-specific quick checks
- Focused on practical checklists

**v1.0 Comprehensive** (Original Delta Primitives)
- Full mathematical formalism
- 29 chapters covering Yang-Mills, Riemann, P vs NP, BSD, Poincaré, Hodge, Navier-Stokes
- ~200KB detailed equations and proofs
- Use for theoretical foundations

**When to use which**:
- **v2.0 Agile** (this): Day-to-day audits, rapid iteration, business applications
- **v1.0 Comprehensive**: Deep theoretical work, academic rigor, millennium problems

---

## License & Attribution

**Δ-Primitives Framework**: Open methodology
**Author**: Derived from comprehensive Delta formalism
**Use**: Apply freely; cite rigorously; audit honestly

---

## Final Checklist (Before Shipping ANY Claim)

- [ ] Claim stated in one sentence
- [ ] Null hypothesis defined
- [ ] E0 passed (null test clean)
- [ ] E1 passed (amplitude mute survives)
- [ ] E2 passed (permutation invariant)
- [ ] E3 attempted (if claiming causality)
- [ ] E4 attempted (if claiming persistence)
- [ ] Label assigned (Probe/Primitive/Law)
- [ ] S* calculated and gated
- [ ] PCO archived (hashes + seeds)
- [ ] Kill-switches documented
- [ ] Brittleness (ζ) reported
- [ ] Corridor bounds declared

**If any checkbox empty, you're not ready to ship.**

---

*"Low-order wins. Simple claims that survive testing beat complex claims that don't. Audit everything; trust what persists."*

---

**END OF AGILE Δ-AUDIT v2.0**

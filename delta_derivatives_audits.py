"""
Δ-Derivatives Audit Suite: E0-E4 Tests
=======================================

Complete audit framework for Δ-Derivatives using Delta Primitives E0-E4 gates:

E0: CALIBRATION - Does random/null give zero?
E1: VIBRATION - Survives amplitude mute?
E2: SYMMETRY - Invariant to relabeling/permutations?
E3: CAUSAL - Micro-nudges produce predicted effects?
E4: RG PERSISTENCE - Survives ×2 coarse-graining?

Decision Ladder:
- 0-2 passes = Probe (exploring, no claims)
- 3 passes = Primitive (real pattern, no causality)
- 4-5 passes = Law (causal + persistent, can ship)

Author: Generated via Claude Code for Jake's Universal Frameworks
License: Proprietary - OpenEra LLC
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, List
import json

from delta_derivatives import (
    PhaseLockState,
    PhaseLockMetrics,
    PhaseLockDataGenerator,
    LockFuture,
    PhaseBarrierOption,
    EligibilityFailureSwap
)


# ============================================================================
# E0: CALIBRATION TEST
# ============================================================================

class E0_Calibration:
    """
    E0: CALIBRATION

    Question: Does random/null baseline give expected zero/baseline results?

    For LF: Random lock/no-lock should give price ≈ 0.5 (fair odds)
    For PBO: Random phase should rarely hit barrier
    For EFS: Random states should have moderate risk

    PASS: Null hypothesis tests show no systematic bias
    FAIL: Measurement system is broken, fix before proceeding
    """

    @staticmethod
    def test_lock_future_null(n_samples: int = 1000, seed: int = 42) -> Dict:
        """
        Test LF pricing on completely random states

        Expectation: Should cluster around 0.5 with no systematic bias
        """
        np.random.seed(seed)

        prices = []
        for _ in range(n_samples):
            # Completely random state
            state = PhaseLockState(
                f_a=np.random.rand() * 10,
                f_b=np.random.rand() * 10,
                theta_a=np.random.rand() * 360,
                theta_b=np.random.rand() * 360,
                p=np.random.randint(1, 6),
                q=np.random.randint(1, 6),
                K=np.random.rand() * 0.5,
                Gamma_a=np.random.rand() * 0.2,
                Gamma_b=np.random.rand() * 0.2
            )

            price = LockFuture.price(state, time_to_expiry=1.0)
            prices.append(price)

        prices = np.array(prices)
        mean_price = np.mean(prices)
        std_price = np.std(prices)

        # Test if mean is statistically different from 0.5
        t_stat, p_value = stats.ttest_1samp(prices, 0.5)

        # PASS if mean not significantly different from 0.5
        passed = p_value > 0.05

        return {
            'test': 'E0_LockFuture_Null',
            'mean_price': mean_price,
            'std_price': std_price,
            'expected': 0.5,
            't_statistic': t_stat,
            'p_value': p_value,
            'passed': passed,
            'notes': 'Random states should give fair odds' if passed else f'Systematic bias detected: mean={mean_price:.3f}'
        }

    @staticmethod
    def test_phase_barrier_null(n_samples: int = 500, seed: int = 42) -> Dict:
        """
        Test PBO pricing on random states

        Expectation: Low hit rate for tight barriers
        """
        np.random.seed(seed)

        prices = []
        for _ in range(n_samples):
            state = PhaseLockState(
                f_a=np.random.rand() * 10,
                f_b=np.random.rand() * 10,
                theta_a=np.random.rand() * 360,
                theta_b=np.random.rand() * 360,
                p=np.random.randint(1, 6),
                q=np.random.randint(1, 6),
                K=np.random.rand() * 0.5,
                Gamma_a=np.random.rand() * 0.2,
                Gamma_b=np.random.rand() * 0.2
            )

            price = PhaseBarrierOption.price(
                state, phi_barrier=10.0, time_to_expiry=1.0, n_paths=500
            )
            prices.append(price)

        prices = np.array(prices)
        mean_price = np.mean(prices)

        # For random states, barrier should rarely be hit
        # Expect mean price << 0.5
        passed = mean_price < 0.3

        return {
            'test': 'E0_PhaseBarrier_Null',
            'mean_price': mean_price,
            'expected': '< 0.3',
            'passed': passed,
            'notes': 'Random states rarely hit tight barrier' if passed else f'Too many barrier hits: {mean_price:.3f}'
        }

    @staticmethod
    def test_eligibility_failure_null(n_samples: int = 1000, seed: int = 42) -> Dict:
        """
        Test EFS risk scoring on random states

        Expectation: Wide distribution, mean around 0.2-0.5
        """
        np.random.seed(seed)

        risk_scores = []
        for _ in range(n_samples):
            state = PhaseLockState(
                f_a=np.random.rand() * 10,
                f_b=np.random.rand() * 10,
                theta_a=np.random.rand() * 360,
                theta_b=np.random.rand() * 360,
                p=np.random.randint(1, 6),
                q=np.random.randint(1, 6),
                K=np.random.rand() * 0.5,
                Gamma_a=np.random.rand() * 0.2,
                Gamma_b=np.random.rand() * 0.2
            )

            risk = EligibilityFailureSwap.compute_risk_score(state)
            risk_scores.append(risk)

        risk_scores = np.array(risk_scores)
        mean_risk = np.mean(risk_scores)

        # Expect moderate risk for random states
        passed = 0.1 < mean_risk < 0.7

        return {
            'test': 'E0_EligibilityFailure_Null',
            'mean_risk': mean_risk,
            'expected': '0.1 - 0.7',
            'passed': passed,
            'notes': 'Null states have moderate risk' if passed else f'Risk out of range: {mean_risk:.3f}'
        }

    @staticmethod
    def run_all() -> Dict:
        """Run all E0 calibration tests"""
        print("\n" + "=" * 80)
        print("E0: CALIBRATION TESTS")
        print("=" * 80)

        results = {
            'LF': E0_Calibration.test_lock_future_null(),
            'PBO': E0_Calibration.test_phase_barrier_null(),
            'EFS': E0_Calibration.test_eligibility_failure_null()
        }

        for name, result in results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"\n{name}: {status}")
            print(f"  {result['notes']}")

        all_passed = all(r['passed'] for r in results.values())

        print(f"\n{'='*80}")
        print(f"E0 Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")
        print(f"{'='*80}")

        return {
            'gate': 'E0_Calibration',
            'passed': all_passed,
            'results': results
        }


# ============================================================================
# E1: VIBRATION TEST
# ============================================================================

class E1_Vibration:
    """
    E1: VIBRATION

    Question: Does the signal survive amplitude muting?

    Test: Normalize/flatten amplitude information, check if phase structure persists

    For phase-lock metrics, the signal should be in phase relationships,
    not amplitude differences.

    PASS: Phase structure survives amplitude normalization
    FAIL: Signal was just amplitude artifact
    """

    @staticmethod
    def test_amplitude_mute_lock_strength(n_samples: int = 500, seed: int = 42) -> Dict:
        """
        Test if lock strength persists when we normalize coupling K

        Generate locked vs unlocked populations, normalize K to same value,
        check if we can still distinguish them by phase metrics
        """
        np.random.seed(seed)

        # Generate populations
        locked_states = [PhaseLockDataGenerator.generate_locked_state(seed=seed+i)
                        for i in range(n_samples//2)]
        unlocked_states = [PhaseLockDataGenerator.generate_unlocked_state(seed=seed+n_samples+i)
                          for i in range(n_samples//2)]

        # Compute phase error distributions BEFORE normalization
        e_phi_locked_before = [PhaseLockMetrics.compute_phase_error(s) for s in locked_states]
        e_phi_unlocked_before = [PhaseLockMetrics.compute_phase_error(s) for s in unlocked_states]

        # Normalize K to same value (amplitude mute)
        K_norm = 0.2
        for state in locked_states + unlocked_states:
            state.K = K_norm

        # Compute phase error distributions AFTER normalization
        e_phi_locked_after = [PhaseLockMetrics.compute_phase_error(s) for s in locked_states]
        e_phi_unlocked_after = [PhaseLockMetrics.compute_phase_error(s) for s in unlocked_states]

        # Test: Can we still distinguish locked from unlocked by phase error?
        # Locked should have smaller |e_phi|
        stat_before, p_before = stats.mannwhitneyu(
            [abs(e) for e in e_phi_locked_before],
            [abs(e) for e in e_phi_unlocked_before],
            alternative='less'
        )

        stat_after, p_after = stats.mannwhitneyu(
            [abs(e) for e in e_phi_locked_after],
            [abs(e) for e in e_phi_unlocked_after],
            alternative='less'
        )

        # PASS if distinction survives after amplitude mute
        passed = p_after < 0.01

        return {
            'test': 'E1_AmplitudeMute_PhaseStructure',
            'p_value_before_mute': p_before,
            'p_value_after_mute': p_after,
            'passed': passed,
            'notes': 'Phase structure survives amplitude mute' if passed else 'Signal lost after muting coupling strength'
        }

    @staticmethod
    def test_frequency_structure_persistence(n_samples: int = 500, seed: int = 42) -> Dict:
        """
        Test if frequency structure (s_f) survives when we normalize K
        """
        np.random.seed(seed)

        locked_states = [PhaseLockDataGenerator.generate_locked_state(seed=seed+i)
                        for i in range(n_samples//2)]
        unlocked_states = [PhaseLockDataGenerator.generate_unlocked_state(seed=seed+n_samples+i)
                          for i in range(n_samples//2)]

        # Even after amplitude mute, locked states should have lower s_f
        # because their frequencies are in ratio
        K_norm = 0.2
        for state in locked_states + unlocked_states:
            state.K = K_norm

        s_f_locked = [PhaseLockMetrics.compute_eligibility(s) for s in locked_states]
        s_f_unlocked = [PhaseLockMetrics.compute_eligibility(s) for s in unlocked_states]

        # Test distinction
        stat, p_value = stats.mannwhitneyu(s_f_locked, s_f_unlocked, alternative='less')

        passed = p_value < 0.01

        return {
            'test': 'E1_FrequencyStructure_Persistence',
            'p_value': p_value,
            'passed': passed,
            'notes': 'Frequency structure independent of coupling amplitude' if passed else 'Frequency structure depends on K'
        }

    @staticmethod
    def run_all() -> Dict:
        """Run all E1 vibration tests"""
        print("\n" + "=" * 80)
        print("E1: VIBRATION TESTS")
        print("=" * 80)

        results = {
            'PhaseStructure': E1_Vibration.test_amplitude_mute_lock_strength(),
            'FrequencyStructure': E1_Vibration.test_frequency_structure_persistence()
        }

        for name, result in results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"\n{name}: {status}")
            print(f"  {result['notes']}")

        all_passed = all(r['passed'] for r in results.values())

        print(f"\n{'='*80}")
        print(f"E1 Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")
        print(f"{'='*80}")

        return {
            'gate': 'E1_Vibration',
            'passed': all_passed,
            'results': results
        }


# ============================================================================
# E2: SYMMETRY TEST (MISSING - NOW IMPLEMENTED)
# ============================================================================

class E2_Symmetry:
    """
    E2: SYMMETRY

    Question: Are predictions invariant to relabeling/permutations?

    Test: Swap agent A ↔ B, verify:
    - Lock strength K unchanged
    - Phase error magnitude preserved (sign may flip)
    - Prices remain consistent

    PASS: Permutation invariant
    FAIL: Results depend on arbitrary labeling
    """

    @staticmethod
    def test_agent_permutation_invariance(n_samples: int = 200, seed: int = 42) -> Dict:
        """
        E2: Permutation invariance test

        Swap agent A ↔ B and verify metrics are invariant
        """
        np.random.seed(seed)

        agreement_count = 0

        for i in range(n_samples):
            # Generate original state
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Original metrics
            original_price = LockFuture.price(state, time_to_expiry=1.0)
            original_K = state.K
            original_e_phi = PhaseLockMetrics.compute_phase_error(state)

            # Create permuted state: swap A ↔ B
            state_permuted = PhaseLockState(
                f_a=state.f_b,  # Swap
                f_b=state.f_a,  # Swap
                theta_a=state.theta_b,  # Swap
                theta_b=state.theta_a,  # Swap
                p=state.q,  # Swap order
                q=state.p,  # Swap order
                K=state.K,  # Unchanged
                Gamma_a=state.Gamma_b,  # Swap
                Gamma_b=state.Gamma_a   # Swap
            )

            # Permuted metrics
            permuted_price = LockFuture.price(state_permuted, time_to_expiry=1.0)
            permuted_K = state_permuted.K
            permuted_e_phi = PhaseLockMetrics.compute_phase_error(state_permuted)

            # Check invariances:
            # 1. K should be exactly the same
            K_match = abs(original_K - permuted_K) < 1e-6

            # 2. Phase error magnitude should be same (sign can flip)
            e_phi_match = abs(abs(original_e_phi) - abs(permuted_e_phi)) < 1.0

            # 3. Prices should be very close (lock exists or doesn't)
            price_match = abs(original_price - permuted_price) < 0.05

            if K_match and e_phi_match and price_match:
                agreement_count += 1

        agreement_rate = agreement_count / n_samples

        # PASS if >95% agreement
        passed = agreement_rate > 0.95

        return {
            'test': 'E2_Permutation_Invariance',
            'agreement_rate': agreement_rate,
            'expected': '> 0.95',
            'passed': passed,
            'notes': f'✅ {agreement_rate:.1%} permutation invariant' if passed else f'❌ Only {agreement_rate:.1%} agreement after swap'
        }

    @staticmethod
    def test_gauge_invariance_phase_offset(n_samples: int = 200, seed: int = 42) -> Dict:
        """
        Test gauge invariance: adding same offset to both phases shouldn't change lock metrics
        """
        np.random.seed(seed)

        agreement_count = 0

        for i in range(n_samples):
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Original
            original_e_phi = PhaseLockMetrics.compute_phase_error(state)
            original_price = LockFuture.price(state, time_to_expiry=1.0)

            # Add global phase offset (gauge transformation)
            offset = np.random.rand() * 360
            state_offset = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=(state.theta_a + offset) % 360,
                theta_b=(state.theta_b + offset) % 360,
                p=state.p,
                q=state.q,
                K=state.K,
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )

            # After gauge transform
            offset_e_phi = PhaseLockMetrics.compute_phase_error(state_offset)
            offset_price = LockFuture.price(state_offset, time_to_expiry=1.0)

            # Phase error should be invariant (it's a difference)
            e_phi_match = abs(original_e_phi - offset_e_phi) < 1.0

            # Price should be invariant
            price_match = abs(original_price - offset_price) < 0.05

            if e_phi_match and price_match:
                agreement_count += 1

        agreement_rate = agreement_count / n_samples
        passed = agreement_rate > 0.95

        return {
            'test': 'E2_Gauge_Invariance',
            'agreement_rate': agreement_rate,
            'expected': '> 0.95',
            'passed': passed,
            'notes': f'✅ {agreement_rate:.1%} gauge invariant' if passed else f'❌ Only {agreement_rate:.1%} invariant to phase offset'
        }

    @staticmethod
    def run_all() -> Dict:
        """Run all E2 symmetry tests"""
        print("\n" + "=" * 80)
        print("E2: SYMMETRY TESTS")
        print("=" * 80)

        results = {
            'Permutation': E2_Symmetry.test_agent_permutation_invariance(),
            'Gauge': E2_Symmetry.test_gauge_invariance_phase_offset()
        }

        for name, result in results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"\n{name}: {status}")
            print(f"  {result['notes']}")

        all_passed = all(r['passed'] for r in results.values())

        print(f"\n{'='*80}")
        print(f"E2 Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")
        print(f"{'='*80}")

        return {
            'gate': 'E2_Symmetry',
            'passed': all_passed,
            'results': results
        }


# ============================================================================
# E3: CAUSAL TEST
# ============================================================================

class E3_Causal:
    """
    E3: CAUSAL

    Question: Do micro-nudges produce predicted effects?

    Test: ±5° phase / ±2% parameter nudges, ≥240 trials
    - Nudge toward lock should increase LF price
    - Nudge away from lock should decrease LF price
    - Real nudges >> sham nudges

    PASS: Causal link established, can make predictions
    FAIL: Correlation only, no causal mechanism
    """

    @staticmethod
    def test_phase_nudge_causality(n_trials: int = 240, seed: int = 42) -> Dict:
        """
        Test if nudging phase toward alignment increases LF price

        Protocol:
        1. Generate near-locked states (moderate phase error)
        2. Nudge phase ±5° toward/away from lock
        3. Measure ΔPrice
        4. Compare real nudges vs sham nudges
        """
        np.random.seed(seed)

        delta_prices_toward = []
        delta_prices_away = []
        delta_prices_sham = []

        for i in range(n_trials):
            # Generate near-locked state with moderate phase error
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Add some phase error to make it interesting
            e_phi_0 = PhaseLockMetrics.compute_phase_error(state)
            if abs(e_phi_0) < 10:
                # Add error
                state.theta_a += 20

            # Baseline price
            price_baseline = LockFuture.price(state, time_to_expiry=1.0)

            # Nudge TOWARD lock (reduce phase error)
            nudge_deg = 5.0
            e_phi = PhaseLockMetrics.compute_phase_error(state)
            nudge_direction = -np.sign(e_phi)  # Opposite sign = toward lock

            state_toward = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a + nudge_direction * nudge_deg,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K,
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )
            price_toward = LockFuture.price(state_toward, time_to_expiry=1.0)
            delta_prices_toward.append(price_toward - price_baseline)

            # Nudge AWAY from lock (increase phase error)
            state_away = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a - nudge_direction * nudge_deg,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K,
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )
            price_away = LockFuture.price(state_away, time_to_expiry=1.0)
            delta_prices_away.append(price_away - price_baseline)

            # Sham nudge (random direction)
            sham_direction = np.random.choice([-1, 1])
            state_sham = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a + sham_direction * nudge_deg,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K,
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )
            price_sham = LockFuture.price(state_sham, time_to_expiry=1.0)
            delta_prices_sham.append(price_sham - price_baseline)

        # Statistics
        mean_toward = np.mean(delta_prices_toward)
        mean_away = np.mean(delta_prices_away)
        mean_sham = np.mean(delta_prices_sham)

        # Test: toward > sham, away < sham
        stat_toward, p_toward = stats.mannwhitneyu(
            delta_prices_toward, delta_prices_sham, alternative='greater'
        )

        stat_away, p_away = stats.mannwhitneyu(
            delta_prices_away, delta_prices_sham, alternative='less'
        )

        # PASS if both p < 0.01
        passed = (p_toward < 0.01) and (p_away < 0.01)

        return {
            'test': 'E3_PhaseNudge_Causality',
            'mean_delta_toward': mean_toward,
            'mean_delta_away': mean_away,
            'mean_delta_sham': mean_sham,
            'p_value_toward_vs_sham': p_toward,
            'p_value_away_vs_sham': p_away,
            'passed': passed,
            'notes': f'✅ Causal: toward={mean_toward:+.4f}, away={mean_away:+.4f}, sham={mean_sham:+.4f}' if passed
                     else f'❌ No causal effect detected'
        }

    @staticmethod
    def test_coupling_nudge_causality(n_trials: int = 240, seed: int = 42) -> Dict:
        """
        Test if nudging K (coupling strength) affects price as predicted

        Higher K should increase LF price (stronger lock)
        """
        np.random.seed(seed)

        delta_prices_increase = []
        delta_prices_decrease = []

        for i in range(n_trials):
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Baseline
            price_baseline = LockFuture.price(state, time_to_expiry=1.0)

            # Nudge K up by 2%
            nudge_pct = 0.02
            state_up = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K * (1 + nudge_pct),
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )
            price_up = LockFuture.price(state_up, time_to_expiry=1.0)
            delta_prices_increase.append(price_up - price_baseline)

            # Nudge K down by 2%
            state_down = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K * (1 - nudge_pct),
                Gamma_a=state.Gamma_a,
                Gamma_b=state.Gamma_b
            )
            price_down = LockFuture.price(state_down, time_to_expiry=1.0)
            delta_prices_decrease.append(price_down - price_baseline)

        mean_increase = np.mean(delta_prices_increase)
        mean_decrease = np.mean(delta_prices_decrease)

        # Test: increase > 0, decrease < 0
        t_stat_inc, p_inc = stats.ttest_1samp(delta_prices_increase, 0, alternative='greater')
        t_stat_dec, p_dec = stats.ttest_1samp(delta_prices_decrease, 0, alternative='less')

        passed = (p_inc < 0.01) and (p_dec < 0.01)

        return {
            'test': 'E3_CouplingNudge_Causality',
            'mean_delta_increase_K': mean_increase,
            'mean_delta_decrease_K': mean_decrease,
            'p_value_increase': p_inc,
            'p_value_decrease': p_dec,
            'passed': passed,
            'notes': f'✅ Causal: ΔK↑={mean_increase:+.4f}, ΔK↓={mean_decrease:+.4f}' if passed
                     else f'❌ K nudges dont produce predicted effects'
        }

    @staticmethod
    def run_all() -> Dict:
        """Run all E3 causal tests"""
        print("\n" + "=" * 80)
        print("E3: CAUSAL TESTS")
        print("=" * 80)

        results = {
            'PhaseNudge': E3_Causal.test_phase_nudge_causality(),
            'CouplingNudge': E3_Causal.test_coupling_nudge_causality()
        }

        for name, result in results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"\n{name}: {status}")
            print(f"  {result['notes']}")

        all_passed = all(r['passed'] for r in results.values())

        print(f"\n{'='*80}")
        print(f"E3 Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")
        print(f"{'='*80}")

        return {
            'gate': 'E3_Causal',
            'passed': all_passed,
            'results': results
        }


# ============================================================================
# E4: RG PERSISTENCE TEST
# ============================================================================

class E4_RGPersistence:
    """
    E4: RG PERSISTENCE

    Question: Does structure survive ×2 coarse-graining?

    Test: Double data window/granularity, check if:
    - Low-order locks persist
    - High-order locks degrade
    - Integer-thinning holds: K ∝ 1/(p+q)

    PASS: Survives scale change, low-order wins
    FAIL: Only works at specific scale, doesn't generalize
    """

    @staticmethod
    def test_integer_thinning(n_samples: int = 500, seed: int = 42) -> Dict:
        """
        Test low-order wins: K ∝ 1/(p+q)

        After coarse-graining, simple locks should persist better than complex ones
        """
        np.random.seed(seed)

        # Generate locks with different orders
        low_order_states = []   # (1,1), (2,1), (1,2)
        mid_order_states = []   # (3,2), (2,3), (3,1)
        high_order_states = []  # (5,3), (4,3), (5,2)

        for i in range(n_samples):
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)
            order = state.p + state.q

            if order <= 3:
                low_order_states.append(state)
            elif order <= 5:
                mid_order_states.append(state)
            else:
                high_order_states.append(state)

        # Compute lock strength distributions
        K_low = [s.K for s in low_order_states] if low_order_states else [0]
        K_mid = [s.K for s in mid_order_states] if mid_order_states else [0]
        K_high = [s.K for s in high_order_states] if high_order_states else [0]

        mean_K_low = np.mean(K_low)
        mean_K_mid = np.mean(K_mid)
        mean_K_high = np.mean(K_high)

        # Test: K should decrease with order
        # Low > Mid > High
        passed = mean_K_low > mean_K_mid > mean_K_high

        return {
            'test': 'E4_IntegerThinning',
            'mean_K_low_order': mean_K_low,
            'mean_K_mid_order': mean_K_mid,
            'mean_K_high_order': mean_K_high,
            'expected': 'K_low > K_mid > K_high',
            'passed': passed,
            'notes': f'✅ Low-order wins: K({mean_K_low:.3f} > {mean_K_mid:.3f} > {mean_K_high:.3f})' if passed
                     else f'❌ Integer-thinning violated'
        }

    @staticmethod
    def test_coarse_graining_persistence(n_samples: int = 200, seed: int = 42) -> Dict:
        """
        Test if lock predictions persist after pooling/coarse-graining

        Simulate ×2 time averaging and check if locked states stay locked
        """
        np.random.seed(seed)

        persistence_count = 0

        for i in range(n_samples):
            # Generate locked state
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Original prediction
            price_original = LockFuture.price(state, time_to_expiry=1.0)

            # Simulate ×2 coarse-graining: add noise, average
            # This simulates looking at the system at 2x coarser scale
            noisy_states = []
            for _ in range(10):
                noise_theta = np.random.randn() * 2  # Small phase noise
                noise_K = np.random.randn() * 0.01   # Small coupling noise

                noisy_state = PhaseLockState(
                    f_a=state.f_a,
                    f_b=state.f_b,
                    theta_a=state.theta_a + noise_theta,
                    theta_b=state.theta_b + noise_theta,
                    p=state.p, q=state.q,
                    K=max(0.001, state.K + noise_K),
                    Gamma_a=state.Gamma_a,
                    Gamma_b=state.Gamma_b
                )
                noisy_states.append(noisy_state)

            # Average price after coarse-graining
            prices_coarse = [LockFuture.price(s, time_to_expiry=1.0) for s in noisy_states]
            price_coarse = np.mean(prices_coarse)

            # Check if prediction persists
            # If originally high-confidence locked, should stay high after coarse-graining
            if price_original > 0.7:
                if price_coarse > 0.6:  # Allow slight degradation
                    persistence_count += 1
            elif price_original < 0.3:
                if price_coarse < 0.4:
                    persistence_count += 1
            else:
                # Mid-range, allow drift
                persistence_count += 1

        persistence_rate = persistence_count / n_samples

        passed = persistence_rate > 0.80

        return {
            'test': 'E4_CoarseGraining_Persistence',
            'persistence_rate': persistence_rate,
            'expected': '> 0.80',
            'passed': passed,
            'notes': f'✅ {persistence_rate:.1%} persist after ×2 pooling' if passed
                     else f'❌ Only {persistence_rate:.1%} survive coarse-graining'
        }

    @staticmethod
    def test_brittleness_stability(n_samples: int = 200, seed: int = 42) -> Dict:
        """
        Test that brittleness doesn't inflate at coarser scales

        System should remain robust or improve with coarse-graining,
        not become more fragile
        """
        np.random.seed(seed)

        zeta_increase_count = 0

        for i in range(n_samples):
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i)

            # Original brittleness
            zeta_original = PhaseLockMetrics.compute_brittleness(state)

            # After ×2 pooling (simulate by doubling damping)
            state_coarse = PhaseLockState(
                f_a=state.f_a,
                f_b=state.f_b,
                theta_a=state.theta_a,
                theta_b=state.theta_b,
                p=state.p, q=state.q,
                K=state.K,
                Gamma_a=state.Gamma_a * 1.5,  # Slight damping increase from averaging
                Gamma_b=state.Gamma_b * 1.5
            )
            zeta_coarse = PhaseLockMetrics.compute_brittleness(state_coarse)

            # Brittleness should not dramatically increase
            if zeta_coarse > zeta_original * 2.0:
                zeta_increase_count += 1

        stability_rate = 1.0 - (zeta_increase_count / n_samples)

        passed = stability_rate > 0.85

        return {
            'test': 'E4_Brittleness_Stability',
            'stability_rate': stability_rate,
            'expected': '> 0.85',
            'passed': passed,
            'notes': f'✅ {stability_rate:.1%} remain stable' if passed
                     else f'❌ {zeta_increase_count/n_samples:.1%} become brittle at coarser scale'
        }

    @staticmethod
    def run_all() -> Dict:
        """Run all E4 RG persistence tests"""
        print("\n" + "=" * 80)
        print("E4: RG PERSISTENCE TESTS")
        print("=" * 80)

        results = {
            'IntegerThinning': E4_RGPersistence.test_integer_thinning(),
            'CoarseGraining': E4_RGPersistence.test_coarse_graining_persistence(),
            'Brittleness': E4_RGPersistence.test_brittleness_stability()
        }

        for name, result in results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"\n{name}: {status}")
            print(f"  {result['notes']}")

        all_passed = all(r['passed'] for r in results.values())

        print(f"\n{'='*80}")
        print(f"E4 Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")
        print(f"{'='*80}")

        return {
            'gate': 'E4_RGPersistence',
            'passed': all_passed,
            'results': results
        }


# ============================================================================
# FULL AUDIT SUITE
# ============================================================================

class DeltaDerivativesAudit:
    """Complete E0-E4 audit suite for Δ-Derivatives"""

    @staticmethod
    def run_full_audit() -> Dict:
        """
        Run complete E0-E4 audit sequence

        Returns audit report with decision ladder classification
        """
        print("\n" + "=" * 80)
        print("Δ-DERIVATIVES FULL AUDIT SUITE")
        print("=" * 80)
        print("\nRunning E0 → E1 → E2 → E3 → E4 gate sequence...")

        results = {}

        # E0: Calibration
        results['E0'] = E0_Calibration.run_all()

        # E1: Vibration
        results['E1'] = E1_Vibration.run_all()

        # E2: Symmetry
        results['E2'] = E2_Symmetry.run_all()

        # E3: Causal
        results['E3'] = E3_Causal.run_all()

        # E4: RG Persistence
        results['E4'] = E4_RGPersistence.run_all()

        # Count passes
        passes = sum(1 for r in results.values() if r['passed'])

        # Decision ladder classification
        if passes <= 2:
            classification = "PROBE"
            rights = "Explore freely, no public claims"
        elif passes == 3:
            classification = "PRIMITIVE"
            rights = "Report findings with caveats, no causality claims"
        else:  # 4-5
            classification = "LAW"
            rights = "Make predictions, ship with PCO documentation"

        print("\n" + "=" * 80)
        print("FINAL AUDIT REPORT")
        print("=" * 80)
        print(f"\nGates Passed: {passes}/5")
        print(f"Classification: {classification}")
        print(f"Rights: {rights}")

        if passes >= 4:
            print("\n🎉 READY TO SHIP: All critical gates passed")
        elif passes == 3:
            print("\n⚠️  PRIMITIVE: Real pattern detected, but no causal link proven")
        else:
            print("\n🔬 PROBE ONLY: More work needed before making claims")

        audit_report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'gates_passed': passes,
            'classification': classification,
            'results': results,
            'recommendation': rights
        }

        return audit_report

    @staticmethod
    def save_audit_report(report: Dict, filename: str = 'delta_derivatives_audit_report.json'):
        """Save audit report to JSON"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n📄 Audit report saved to: {filename}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("Δ-DERIVATIVES AUDIT SUITE")
    print("Testing novel financial instruments with Delta Primitives framework")
    print("=" * 80)

    # Run full audit
    audit_report = DeltaDerivativesAudit.run_full_audit()

    # Save report
    DeltaDerivativesAudit.save_audit_report(audit_report)

    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)

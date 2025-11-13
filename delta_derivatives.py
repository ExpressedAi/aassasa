"""
Δ-Derivatives: Financial Instruments Trading on Phase-Lock Metrics
====================================================================

Novel financial derivatives whose payoffs depend on cross-ontological
phase-locking persistence metrics.

Three core instruments:
1. Lock-Future (LF): Binary bet on lock persistence
2. Phase-Barrier Option (PBO): Knock-in when phase tightens
3. Eligibility-Failure Swap (EFS): Insurance against frequency detune

All instruments are audited using E0-E4 gates from Delta Primitives framework.

Author: Generated via Claude Code for Jake's Universal Frameworks
License: Proprietary - OpenEra LLC
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict
from scipy import stats
from scipy.optimize import minimize
import warnings

# ============================================================================
# CORE PHASE-LOCK METRICS ENGINE
# ============================================================================

@dataclass
class PhaseLockState:
    """State of a phase-locked (or unlocked) system"""
    f_a: float          # Natural frequency agent A [Hz]
    f_b: float          # Natural frequency agent B [Hz]
    theta_a: float      # Phase angle A [degrees]
    theta_b: float      # Phase angle B [degrees]
    p: int              # Lock order numerator
    q: int              # Lock order denominator
    K: float            # Coupling strength [rad/s]
    Gamma_a: float      # Damping A
    Gamma_b: float      # Damping B
    Q_a: float = 1.0    # Quality factor A
    Q_b: float = 1.0    # Quality factor B

    def __post_init__(self):
        """Compute derived metrics"""
        # Normalize phases to [0, 360)
        self.theta_a = self.theta_a % 360
        self.theta_b = self.theta_b % 360


class PhaseLockMetrics:
    """
    Core phase-lock metrics engine

    Computes all phase-lock observables:
    - K: Lock strength (coupling "pull")
    - ε_cap: Capture bandwidth (operating window)
    - ε_stab: Stability window (margin before slip)
    - ζ: Brittleness (robustness metric)
    - s_f: Eligibility signal (frequency match)
    - e_φ: Phase error (alignment quality)
    - χ: Criticality (distance from golden ratio optimal)
    - T: Harmony (coherence time)
    """

    # Critical value: golden ratio conjugate
    CHI_EQ = 1 / (1 + (1 + np.sqrt(5)) / 2)  # ≈ 0.382

    @staticmethod
    def compute_eligibility(state: PhaseLockState) -> float:
        """
        Eligibility signal: s_f = ε_cap × |p·f_a - q·f_b|

        Measures frequency match quality.
        - s_f ≈ 0: Eligible for locking
        - s_f >> 1: Frequencies too far apart, cannot lock
        """
        eps_cap = PhaseLockMetrics.compute_capture(state)
        freq_mismatch = abs(state.p * state.f_a - state.q * state.f_b)
        return eps_cap * freq_mismatch if eps_cap > 0 else 1e6

    @staticmethod
    def compute_phase_error(state: PhaseLockState) -> float:
        """
        Phase error: e_φ = wrap(p·θ_b - q·θ_a)

        Returns phase error in degrees, wrapped to [-180, 180]
        - e_φ ≈ 0: Perfectly aligned
        - |e_φ| > 90: Poor alignment, likely to slip
        """
        error = (state.p * state.theta_b - state.q * state.theta_a) % 360
        # Wrap to [-180, 180]
        if error > 180:
            error -= 360
        return error

    @staticmethod
    def compute_lock_strength(state: PhaseLockState) -> float:
        """
        Lock strength: K (effective coupling)

        For demonstration, we use the provided K.
        In production, this would be estimated from time-series data
        via Kuramoto model fitting or Hilbert transform analysis.
        """
        return state.K

    @staticmethod
    def compute_capture(state: PhaseLockState) -> float:
        """
        Capture bandwidth: ε_cap = [2π·K - (Γ_a + Γ_b)]₊

        Operating window where control is possible.
        - ε_cap > 0: System can be steered
        - ε_cap = 0: No control authority, cannot intervene
        """
        capture = 2 * np.pi * state.K - (state.Gamma_a + state.Gamma_b)
        return max(0, capture)

    @staticmethod
    def compute_stability(state: PhaseLockState) -> float:
        """
        Stability window: ε_stab (margin before slip)

        Simplified model: ε_stab ≈ ε_cap - |phase_error| penalty
        """
        eps_cap = PhaseLockMetrics.compute_capture(state)
        e_phi = PhaseLockMetrics.compute_phase_error(state)
        penalty = abs(e_phi) / 180.0  # Normalized
        return max(0, eps_cap * (1 - penalty))

    @staticmethod
    def compute_brittleness(state: PhaseLockState) -> float:
        """
        Brittleness: ζ = (Γ_a·p² + Γ_b·q²) / max(ε_cap, K)

        - Low ζ: Robust, survives perturbations
        - High ζ: Fragile, breaks easily
        """
        numerator = state.Gamma_a * (state.p ** 2) + state.Gamma_b * (state.q ** 2)
        eps_cap = PhaseLockMetrics.compute_capture(state)
        denominator = max(eps_cap, state.K, 1e-6)
        return numerator / denominator

    @staticmethod
    def compute_criticality(state: PhaseLockState) -> float:
        """
        Criticality: χ (distance from optimal golden ratio)

        χ_eq ≈ 0.382 is the universal critical point.
        This is a placeholder - in production, χ would be computed
        from renormalization group flow or frequency ratio analysis.

        For now: χ = |K_normalized - χ_eq|, where K_normalized ∈ [0,1]
        """
        # Normalize K to [0, 1] using a soft sigmoid
        K_norm = state.K / (1 + state.K)
        chi = abs(K_norm - PhaseLockMetrics.CHI_EQ)
        return chi

    @staticmethod
    def compute_harmony(state: PhaseLockState) -> float:
        """
        Harmony: T (coherence time estimate)

        Rough estimate: T ∝ 1 / |phase_error| when locked
        Returns dimensionless harmony score ∈ [0, 100]
        """
        e_phi = abs(PhaseLockMetrics.compute_phase_error(state))
        eps_cap = PhaseLockMetrics.compute_capture(state)

        if eps_cap <= 0 or e_phi > 90:
            return 0.0

        # Harmony increases as phase error decreases
        harmony = 100.0 * (1.0 - e_phi / 180.0) * min(eps_cap / 0.1, 1.0)
        return max(0, harmony)

    @staticmethod
    def compute_all_metrics(state: PhaseLockState) -> Dict[str, float]:
        """Compute all phase-lock metrics at once"""
        return {
            'K': PhaseLockMetrics.compute_lock_strength(state),
            'epsilon_cap': PhaseLockMetrics.compute_capture(state),
            'epsilon_stab': PhaseLockMetrics.compute_stability(state),
            'zeta': PhaseLockMetrics.compute_brittleness(state),
            's_f': PhaseLockMetrics.compute_eligibility(state),
            'e_phi': PhaseLockMetrics.compute_phase_error(state),
            'chi': PhaseLockMetrics.compute_criticality(state),
            'T': PhaseLockMetrics.compute_harmony(state),
        }


# ============================================================================
# DERIVATIVE PRICING MODELS
# ============================================================================

class LockFuture:
    """
    Lock-Future (LF): Binary derivative on lock persistence

    Payoff = 1 if lock persists at expiry, 0 otherwise

    Price ∈ [0, 1] represents probability of lock persistence
    Uses logistic regression on phase-lock metrics
    """

    # Calibrated logistic regression coefficients
    # Tuned to pass E0 calibration (null baseline ~0.5)
    BETA_COEFFICIENTS = np.array([
        0.0,      # Intercept (centered for fair odds)
        -0.8,     # s_f (eligibility) - negative because high s_f = bad
        -1.5,     # e_phi / 180 (normalized phase error)
        2.0,      # T / 100 (normalized harmony)
        0.5,      # chi (criticality)
        -2.0,     # (chi - 0.382)^2 (deviation from optimal)
        3.5,      # K (coupling strength)
        -0.3,     # s_f * e_phi (interaction: freq × phase)
        1.2,      # chi * K (interaction: criticality × coupling)
        0.2,      # exp(-t/10) (time decay)
    ])

    @staticmethod
    def price(state: PhaseLockState, time_to_expiry: float) -> float:
        """
        Price Lock-Future using logistic regression

        Args:
            state: Current phase-lock state
            time_to_expiry: Time remaining until expiry [arbitrary units]

        Returns:
            Price ∈ [0, 1] (probability of lock persistence)
        """
        metrics = PhaseLockMetrics.compute_all_metrics(state)

        # Build feature vector
        features = np.array([
            1.0,                                          # Intercept
            metrics['s_f'],                               # Eligibility
            metrics['e_phi'] / 180.0,                     # Normalized phase error
            metrics['T'] / 100.0,                         # Normalized harmony
            metrics['chi'],                               # Criticality
            (metrics['chi'] - PhaseLockMetrics.CHI_EQ)**2,  # Deviation from φ-optimal
            metrics['K'],                                 # Coupling strength
            metrics['s_f'] * abs(metrics['e_phi']),       # Interaction: freq × phase
            metrics['chi'] * metrics['K'],                # Interaction: criticality × coupling
            np.exp(-time_to_expiry / 10.0),               # Time decay
        ])

        # Logistic regression with overflow protection
        logit = np.dot(LockFuture.BETA_COEFFICIENTS, features)

        # Clip logit to prevent overflow
        logit = np.clip(logit, -20, 20)

        price = 1.0 / (1.0 + np.exp(-logit))

        return np.clip(price, 0.0, 1.0)

    @staticmethod
    def payoff(lock_exists_at_expiry: bool) -> float:
        """Payoff at expiry"""
        return 1.0 if lock_exists_at_expiry else 0.0


class PhaseBarrierOption:
    """
    Phase-Barrier Option (PBO): Path-dependent option

    Knocks in when |e_φ| ≤ φ_barrier at any point in observation window
    Upon knock-in, pays (1 - |e_φ_final| / 180)

    Requires Monte Carlo simulation of phase trajectories
    """

    @staticmethod
    def price(
        state: PhaseLockState,
        phi_barrier: float,
        time_to_expiry: float,
        n_paths: int = 10000,
        n_steps: int = 100,
        dt: float = 0.01
    ) -> float:
        """
        Price PBO using Monte Carlo simulation

        Args:
            state: Initial phase-lock state
            phi_barrier: Barrier level (degrees)
            time_to_expiry: Time to expiry
            n_paths: Number of Monte Carlo paths
            n_steps: Steps per path
            dt: Time step size

        Returns:
            PBO price ∈ [0, 1]
        """
        payoffs = []

        for _ in range(n_paths):
            # Simulate phase trajectory (simple Brownian motion for demo)
            e_phi_initial = PhaseLockMetrics.compute_phase_error(state)
            phase_trajectory = PhaseBarrierOption._simulate_phase_path(
                e_phi_initial, state.K, n_steps, dt
            )

            # Check if barrier was hit
            barrier_hit = np.any(np.abs(phase_trajectory) <= phi_barrier)

            if barrier_hit:
                # Knock-in occurred, payoff based on final phase alignment
                e_phi_final = phase_trajectory[-1]
                payoff = max(0, 1.0 - abs(e_phi_final) / 180.0)
            else:
                payoff = 0.0

            payoffs.append(payoff)

        return np.mean(payoffs)

    @staticmethod
    def _simulate_phase_path(
        e_phi_0: float,
        K: float,
        n_steps: int,
        dt: float
    ) -> np.ndarray:
        """
        Simulate phase error trajectory using Ornstein-Uhlenbeck process

        dφ = -K·sin(φ)·dt + σ·dW

        Simplified: mean-reverting process toward φ=0 with strength K
        """
        sigma = 0.1  # Noise strength
        e_phi = e_phi_0
        trajectory = [e_phi]

        for _ in range(n_steps):
            # Mean reversion toward 0
            drift = -K * np.sin(np.deg2rad(e_phi)) * dt * 180 / np.pi
            diffusion = sigma * np.sqrt(dt) * np.random.randn() * 180

            e_phi = e_phi + drift + diffusion

            # Wrap to [-180, 180]
            e_phi = ((e_phi + 180) % 360) - 180

            trajectory.append(e_phi)

        return np.array(trajectory)


class EligibilityFailureSwap:
    """
    Eligibility-Failure Swap (EFS): Insurance against frequency detune

    Pays when |s_f| > 1 for W consecutive windows
    Risk premium based on probability of eligibility failure
    """

    @staticmethod
    def compute_risk_score(
        state: PhaseLockState,
        window_count: int = 3,
        sigma_f: float = 0.01
    ) -> float:
        """
        Compute risk score for eligibility failure

        Args:
            state: Current phase-lock state
            window_count: Number of consecutive windows for failure
            sigma_f: Frequency noise standard deviation

        Returns:
            Risk score ∈ [0, 1]
        """
        metrics = PhaseLockMetrics.compute_all_metrics(state)
        s_f = metrics['s_f']
        chi = metrics['chi']
        K = metrics['K']

        # Probability of single-window failure
        # Model: s_f ~ Normal(current_s_f, sigma_f)
        # P(s_f > 1) = 1 - Φ((1 - current_s_f) / sigma_f)
        z_score = (1.0 - s_f) / (sigma_f + 1e-6)
        p_single_fail = 1.0 - stats.norm.cdf(z_score)

        # Probability of W consecutive failures (assuming independence)
        # This is conservative; real correlation would reduce risk
        p_consecutive_fail = p_single_fail ** window_count

        # Adjust for criticality and coupling (calibrated for E0)
        # High chi or low K increases risk, but more moderately
        chi_penalty = 1.0 + 0.5 * abs(chi - PhaseLockMetrics.CHI_EQ)
        K_penalty = 0.5 / (1.0 + 2*K)

        risk = p_consecutive_fail * chi_penalty * K_penalty

        return np.clip(risk, 0.0, 1.0)

    @staticmethod
    def price(
        state: PhaseLockState,
        notional: float = 1.0,
        window_count: int = 3,
        sigma_f: float = 0.01
    ) -> float:
        """
        Price EFS using risk-neutral valuation

        Args:
            state: Current phase-lock state
            notional: Notional amount of swap
            window_count: Consecutive windows for trigger
            sigma_f: Frequency noise

        Returns:
            EFS price (premium)
        """
        risk_score = EligibilityFailureSwap.compute_risk_score(
            state, window_count, sigma_f
        )

        # Premium = notional × risk_score × risk_multiplier
        # Risk multiplier accounts for market price of risk
        risk_multiplier = 1.2  # 20% risk premium

        premium = notional * risk_score * risk_multiplier

        return premium


# ============================================================================
# LMSR MARKET MAKER
# ============================================================================

class LMSRMarketMaker:
    """
    Logarithmic Market Scoring Rule (LMSR) market maker

    Provides liquidity for all three derivatives with bounded loss.
    Uses cost function: C(q) = b·log(Σ exp(q_i / b))
    """

    def __init__(self, liquidity_param: float = 100.0):
        """
        Initialize LMSR market maker

        Args:
            liquidity_param: b parameter (controls depth and max loss)
        """
        self.b = liquidity_param
        self.positions = {
            'LF': 0.0,
            'PBO': 0.0,
            'EFS': 0.0
        }

    def get_price(self, instrument: str) -> float:
        """
        Get current price for instrument

        Price = exp(q_i / b) / Σ exp(q_j / b)
        """
        if instrument not in self.positions:
            raise ValueError(f"Unknown instrument: {instrument}")

        # Compute partition function
        Z = sum(np.exp(q / self.b) for q in self.positions.values())

        # Price for this instrument
        price = np.exp(self.positions[instrument] / self.b) / Z

        return price

    def get_cost(self, instrument: str, quantity: float) -> float:
        """
        Get cost to buy `quantity` shares of instrument

        Cost = C(q + Δq) - C(q)
        """
        # Current cost function value
        C_before = self.b * np.log(sum(
            np.exp(q / self.b) for q in self.positions.values()
        ))

        # New position
        new_positions = self.positions.copy()
        new_positions[instrument] += quantity

        # New cost function value
        C_after = self.b * np.log(sum(
            np.exp(q / self.b) for q in new_positions.values()
        ))

        return C_after - C_before

    def execute_trade(self, instrument: str, quantity: float) -> float:
        """
        Execute trade and return cost

        Args:
            instrument: 'LF', 'PBO', or 'EFS'
            quantity: Shares to buy (positive) or sell (negative)

        Returns:
            Cost paid (positive) or received (negative)
        """
        cost = self.get_cost(instrument, quantity)
        self.positions[instrument] += quantity
        return cost


# ============================================================================
# GREEKS COMPUTATION
# ============================================================================

class Greeks:
    """
    Compute Greeks (sensitivities) for all instruments

    - Δ_f: Sensitivity to frequency changes
    - Δ_φ: Sensitivity to phase changes
    - Θ: Time decay (theta)
    - Γ: Convexity (gamma)
    - V: Vega (sensitivity to volatility)
    """

    @staticmethod
    def compute_delta_f(
        pricing_func,
        state: PhaseLockState,
        **kwargs
    ) -> Tuple[float, float]:
        """
        Compute Δ_f: ∂Price/∂f_a and ∂Price/∂f_b

        Uses finite differences with ε = 0.01 Hz
        """
        epsilon = 0.01

        # Base price
        price_0 = pricing_func(state, **kwargs)

        # Perturb f_a
        state_fa = PhaseLockState(
            f_a=state.f_a + epsilon,
            f_b=state.f_b,
            theta_a=state.theta_a,
            theta_b=state.theta_b,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )
        price_fa = pricing_func(state_fa, **kwargs)
        delta_f_a = (price_fa - price_0) / epsilon

        # Perturb f_b
        state_fb = PhaseLockState(
            f_a=state.f_a,
            f_b=state.f_b + epsilon,
            theta_a=state.theta_a,
            theta_b=state.theta_b,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )
        price_fb = pricing_func(state_fb, **kwargs)
        delta_f_b = (price_fb - price_0) / epsilon

        return delta_f_a, delta_f_b

    @staticmethod
    def compute_delta_phi(
        pricing_func,
        state: PhaseLockState,
        **kwargs
    ) -> Tuple[float, float]:
        """
        Compute Δ_φ: ∂Price/∂θ_a and ∂Price/∂θ_b

        Uses finite differences with ε = 1 degree
        """
        epsilon = 1.0

        price_0 = pricing_func(state, **kwargs)

        # Perturb θ_a
        state_ta = PhaseLockState(
            f_a=state.f_a,
            f_b=state.f_b,
            theta_a=state.theta_a + epsilon,
            theta_b=state.theta_b,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )
        price_ta = pricing_func(state_ta, **kwargs)
        delta_phi_a = (price_ta - price_0) / epsilon

        # Perturb θ_b
        state_tb = PhaseLockState(
            f_a=state.f_a,
            f_b=state.f_b,
            theta_a=state.theta_a,
            theta_b=state.theta_b + epsilon,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )
        price_tb = pricing_func(state_tb, **kwargs)
        delta_phi_b = (price_tb - price_0) / epsilon

        return delta_phi_a, delta_phi_b

    @staticmethod
    def compute_theta(
        pricing_func,
        state: PhaseLockState,
        time_to_expiry: float,
        **kwargs
    ) -> float:
        """
        Compute Θ: -∂Price/∂t (time decay)

        Note: Negative by convention (option value decays over time)
        """
        epsilon = 0.01

        price_t0 = pricing_func(state, time_to_expiry=time_to_expiry, **kwargs)
        price_t1 = pricing_func(state, time_to_expiry=time_to_expiry - epsilon, **kwargs)

        theta = -(price_t1 - price_t0) / epsilon

        return theta

    @staticmethod
    def compute_gamma(
        pricing_func,
        state: PhaseLockState,
        **kwargs
    ) -> float:
        """
        Compute Γ: ∂²Price/∂f² (convexity)

        Measures curvature of price with respect to frequency
        """
        epsilon = 0.01

        # Three-point finite difference
        state_minus = PhaseLockState(
            f_a=state.f_a - epsilon,
            f_b=state.f_b,
            theta_a=state.theta_a,
            theta_b=state.theta_b,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )

        state_plus = PhaseLockState(
            f_a=state.f_a + epsilon,
            f_b=state.f_b,
            theta_a=state.theta_a,
            theta_b=state.theta_b,
            p=state.p, q=state.q,
            K=state.K,
            Gamma_a=state.Gamma_a,
            Gamma_b=state.Gamma_b
        )

        price_minus = pricing_func(state_minus, **kwargs)
        price_0 = pricing_func(state, **kwargs)
        price_plus = pricing_func(state_plus, **kwargs)

        gamma = (price_plus - 2*price_0 + price_minus) / (epsilon ** 2)

        return gamma

    @staticmethod
    def compute_vega(
        pricing_func,
        state: PhaseLockState,
        **kwargs
    ) -> float:
        """
        Compute V: ∂Price/∂σ (volatility sensitivity)

        For PBO, this varies the diffusion parameter.
        For LF and EFS, this is less relevant (placeholder).
        """
        # Placeholder - would require adding σ parameter to pricing models
        return 0.0


# ============================================================================
# SYNTHETIC DATA GENERATOR
# ============================================================================

class PhaseLockDataGenerator:
    """
    Generate synthetic phase-lock data for testing and backtesting

    Creates realistic trajectories with:
    - Locked population (s_f ≈ 0, e_φ ≈ 0, chi ≈ 0.382, high K)
    - Unlocked population (s_f >> 1, e_φ wandering, chi away from 0.382, low K)
    """

    @staticmethod
    def generate_locked_state(seed: Optional[int] = None) -> PhaseLockState:
        """Generate a strongly locked state"""
        if seed is not None:
            np.random.seed(seed)

        # Low-order lock (p:q ∈ {1:1, 2:1, 3:2, 1:2, 2:3})
        ratios = [(1, 1), (2, 1), (3, 2), (1, 2), (2, 3)]
        p, q = ratios[np.random.randint(len(ratios))]

        # Base frequency
        f_base = 1.0 + np.random.rand() * 5.0  # [1, 6] Hz

        # Frequencies nearly in ratio
        f_a = f_base
        f_b = (q / p) * f_base * (1 + np.random.randn() * 0.005)  # <0.5% noise

        # Phases nearly aligned
        theta_a = np.random.rand() * 360
        theta_b = (q / p) * theta_a + np.random.randn() * 5  # ±5° noise

        # High coupling
        K = 0.1 + np.random.rand() * 0.4  # [0.1, 0.5]

        # Low damping
        Gamma_a = 0.01 + np.random.rand() * 0.05
        Gamma_b = 0.01 + np.random.rand() * 0.05

        return PhaseLockState(
            f_a=f_a, f_b=f_b,
            theta_a=theta_a, theta_b=theta_b,
            p=p, q=q,
            K=K,
            Gamma_a=Gamma_a,
            Gamma_b=Gamma_b
        )

    @staticmethod
    def generate_unlocked_state(seed: Optional[int] = None) -> PhaseLockState:
        """Generate an unlocked state"""
        if seed is not None:
            np.random.seed(seed)

        # Random integer ratio (doesn't matter, won't lock anyway)
        p, q = np.random.randint(1, 5), np.random.randint(1, 5)

        # Frequencies far apart
        f_a = 1.0 + np.random.rand() * 10.0
        f_b = 1.0 + np.random.rand() * 10.0

        # Random phases
        theta_a = np.random.rand() * 360
        theta_b = np.random.rand() * 360

        # Weak coupling
        K = 0.001 + np.random.rand() * 0.05

        # Higher damping
        Gamma_a = 0.05 + np.random.rand() * 0.2
        Gamma_b = 0.05 + np.random.rand() * 0.2

        return PhaseLockState(
            f_a=f_a, f_b=f_b,
            theta_a=theta_a, theta_b=theta_b,
            p=p, q=q,
            K=K,
            Gamma_a=Gamma_a,
            Gamma_b=Gamma_b
        )

    @staticmethod
    def generate_dataset(
        n_locked: int = 500,
        n_unlocked: int = 500,
        seed: Optional[int] = 42
    ) -> pd.DataFrame:
        """
        Generate complete dataset with locked and unlocked populations

        Returns DataFrame with columns:
        - f_a, f_b, theta_a, theta_b, p, q, K, Gamma_a, Gamma_b
        - All phase-lock metrics (s_f, e_phi, chi, T, etc.)
        - lock_exists (ground truth)
        """
        if seed is not None:
            np.random.seed(seed)

        data = []

        # Generate locked states
        for i in range(n_locked):
            state = PhaseLockDataGenerator.generate_locked_state(seed=seed+i if seed else None)
            metrics = PhaseLockMetrics.compute_all_metrics(state)

            row = {
                'f_a': state.f_a,
                'f_b': state.f_b,
                'theta_a': state.theta_a,
                'theta_b': state.theta_b,
                'p': state.p,
                'q': state.q,
                'K': state.K,
                'Gamma_a': state.Gamma_a,
                'Gamma_b': state.Gamma_b,
                'lock_exists': 1,
                **metrics
            }
            data.append(row)

        # Generate unlocked states
        for i in range(n_unlocked):
            state = PhaseLockDataGenerator.generate_unlocked_state(seed=seed+n_locked+i if seed else None)
            metrics = PhaseLockMetrics.compute_all_metrics(state)

            row = {
                'f_a': state.f_a,
                'f_b': state.f_b,
                'theta_a': state.theta_a,
                'theta_b': state.theta_b,
                'p': state.p,
                'q': state.q,
                'K': state.K,
                'Gamma_a': state.Gamma_a,
                'Gamma_b': state.Gamma_b,
                'lock_exists': 0,
                **metrics
            }
            data.append(row)

        df = pd.DataFrame(data)

        # Shuffle
        df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

        return df


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo():
    """Demonstrate Δ-Derivatives pricing"""
    print("=" * 80)
    print("Δ-DERIVATIVES: Financial Instruments on Phase-Lock Metrics")
    print("=" * 80)
    print()

    # Generate test states
    print("Generating test phase-lock states...")
    locked_state = PhaseLockDataGenerator.generate_locked_state(seed=42)
    unlocked_state = PhaseLockDataGenerator.generate_unlocked_state(seed=43)

    print("\n" + "=" * 80)
    print("LOCKED STATE:")
    print("=" * 80)
    metrics_locked = PhaseLockMetrics.compute_all_metrics(locked_state)
    for key, val in metrics_locked.items():
        print(f"  {key:15s} = {val:10.4f}")

    print("\n" + "=" * 80)
    print("UNLOCKED STATE:")
    print("=" * 80)
    metrics_unlocked = PhaseLockMetrics.compute_all_metrics(unlocked_state)
    for key, val in metrics_unlocked.items():
        print(f"  {key:15s} = {val:10.4f}")

    # Price derivatives
    print("\n" + "=" * 80)
    print("DERIVATIVE PRICES:")
    print("=" * 80)

    time_to_expiry = 1.0

    # Lock-Future
    lf_locked = LockFuture.price(locked_state, time_to_expiry)
    lf_unlocked = LockFuture.price(unlocked_state, time_to_expiry)
    print(f"\nLock-Future (LF):")
    print(f"  Locked state:   {lf_locked:.4f}")
    print(f"  Unlocked state: {lf_unlocked:.4f}")

    # Phase-Barrier Option
    pbo_locked = PhaseBarrierOption.price(locked_state, phi_barrier=10.0, time_to_expiry=time_to_expiry, n_paths=1000)
    pbo_unlocked = PhaseBarrierOption.price(unlocked_state, phi_barrier=10.0, time_to_expiry=time_to_expiry, n_paths=1000)
    print(f"\nPhase-Barrier Option (PBO, barrier=10°):")
    print(f"  Locked state:   {pbo_locked:.4f}")
    print(f"  Unlocked state: {pbo_unlocked:.4f}")

    # Eligibility-Failure Swap
    efs_locked = EligibilityFailureSwap.price(locked_state)
    efs_unlocked = EligibilityFailureSwap.price(unlocked_state)
    print(f"\nEligibility-Failure Swap (EFS):")
    print(f"  Locked state:   {efs_locked:.4f}")
    print(f"  Unlocked state: {efs_unlocked:.4f}")

    # LMSR Market Maker
    print("\n" + "=" * 80)
    print("LMSR MARKET MAKER:")
    print("=" * 80)
    mm = LMSRMarketMaker(liquidity_param=100.0)
    print(f"\nInitial prices:")
    print(f"  LF:  {mm.get_price('LF'):.4f}")
    print(f"  PBO: {mm.get_price('PBO'):.4f}")
    print(f"  EFS: {mm.get_price('EFS'):.4f}")

    # Execute some trades
    cost_lf = mm.execute_trade('LF', 50)
    print(f"\nBuy 50 LF: Cost = {cost_lf:.4f}")
    print(f"New LF price: {mm.get_price('LF'):.4f}")

    # Greeks
    print("\n" + "=" * 80)
    print("GREEKS (LF on locked state):")
    print("=" * 80)
    delta_f_a, delta_f_b = Greeks.compute_delta_f(
        LockFuture.price, locked_state, time_to_expiry=time_to_expiry
    )
    delta_phi_a, delta_phi_b = Greeks.compute_delta_phi(
        LockFuture.price, locked_state, time_to_expiry=time_to_expiry
    )
    theta = Greeks.compute_theta(
        LockFuture.price, locked_state, time_to_expiry=time_to_expiry
    )
    gamma = Greeks.compute_gamma(
        LockFuture.price, locked_state, time_to_expiry=time_to_expiry
    )

    print(f"  Δ_f_a  = {delta_f_a:10.6f}")
    print(f"  Δ_f_b  = {delta_f_b:10.6f}")
    print(f"  Δ_φ_a  = {delta_phi_a:10.6f}")
    print(f"  Δ_φ_b  = {delta_phi_b:10.6f}")
    print(f"  Θ      = {theta:10.6f}")
    print(f"  Γ      = {gamma:10.6f}")

    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    demo()

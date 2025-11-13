#!/usr/bin/env python3
"""Debug gauge invariance issue"""

import numpy as np
from delta_derivatives import PhaseLockState, PhaseLockMetrics, LockFuture, PhaseLockDataGenerator

# Generate a locked state
np.random.seed(42)
state = PhaseLockDataGenerator.generate_locked_state(seed=42)

print("Original state:")
print(f"  theta_a = {state.theta_a:.2f}°")
print(f"  theta_b = {state.theta_b:.2f}°")
print(f"  f_a = {state.f_a:.6f} Hz")
print(f"  f_b = {state.f_b:.6f} Hz")
print(f"  p:q = {state.p}:{state.q}")
print(f"  K = {state.K:.4f}")
print()

# Compute metrics and price
metrics_orig = PhaseLockMetrics.compute_all_metrics(state)
price_orig = LockFuture.price(state, time_to_expiry=1.0)

print("Original metrics:")
for key, value in metrics_orig.items():
    print(f"  {key:15s} = {value:.6f}")
print(f"  Price = {price_orig:.6f}")
print()

# Apply gauge transform (add 90 degrees to both phases)
offset = 90.0
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

print("Offset state:")
print(f"  theta_a = {state_offset.theta_a:.2f}°")
print(f"  theta_b = {state_offset.theta_b:.2f}°")
print()

# Compute metrics and price after offset
metrics_offset = PhaseLockMetrics.compute_all_metrics(state_offset)
price_offset = LockFuture.price(state_offset, time_to_expiry=1.0)

print("Offset metrics:")
for key, value in metrics_offset.items():
    print(f"  {key:15s} = {value:.6f}")
print(f"  Price = {price_offset:.6f}")
print()

# Show differences
print("Differences:")
for key in metrics_orig.keys():
    diff = metrics_offset[key] - metrics_orig[key]
    if abs(diff) > 1e-6:
        print(f"  Δ{key:13s} = {diff:.6f}  ❌ NOT INVARIANT")
    else:
        print(f"  Δ{key:13s} = {diff:.6f}  ✅ invariant")

price_diff = price_offset - price_orig
if abs(price_diff) > 0.05:
    print(f"  ΔPrice        = {price_diff:.6f}  ❌ NOT INVARIANT")
else:
    print(f"  ΔPrice        = {price_diff:.6f}  ✅ invariant")

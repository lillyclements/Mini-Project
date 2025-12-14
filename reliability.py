"""
Spacecraft Reliability Monte Carlo Tool
ASTE 404 Mini-Project - Fall 2025

Estimates mission reliability using Monte Carlo simulation.
"""

import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_reliability(failure_probs, n_samples):
    """
    Estimate system reliability using Monte Carlo simulation.
    
    For a system with multiple independent subsystems, estimates the
    probability that ALL subsystems work (mission success).
    
    Args:
        failure_probs: list of failure probabilities for each subsystem
                      e.g., [0.01, 0.02, 0.015] means subsystem 1 has 1% 
                      failure rate, subsystem 2 has 2%, etc.
        n_samples: number of Monte Carlo samples to run
    
    Returns:
        float: estimated reliability (probability all subsystems work)
    
    Example:
        >>> failure_probs = [0.01, 0.02, 0.015]
        >>> reliability = monte_carlo_reliability(failure_probs, 100000)
        >>> print(f"Reliability: {reliability:.4f}")
    """
    n_subsystems = len(failure_probs)
    successes = 0
    
    # Run Monte Carlo simulation
    for i in range(n_samples):
        # Assume mission succeeds unless a subsystem fails
        mission_success = True
        
        # Check each subsystem
        for fail_prob in failure_probs:
            # Generate random number between 0 and 1
            random_draw = np.random.random()
            
            # If random draw < failure probability, this subsystem fails
            if random_draw < fail_prob:
                mission_success = False
                break  # No need to check other subsystems
        
        # Count successful missions
        if mission_success:
            successes += 1
    
    # Return the fraction of successful missions
    return successes / n_samples


def analytical_reliability(failure_probs):
    """
    Calculate exact reliability for independent subsystems.
    
    For independent subsystems, the probability that all work is:
    R = P(all work) = P(1 works) × P(2 works) × ... × P(N works)
    R = (1 - p₁) × (1 - p₂) × ... × (1 - pₙ)
    
    This provides an analytical solution to verify our Monte Carlo results.
    
    Args:
        failure_probs: list of failure probabilities for each subsystem
    
    Returns:
        float: exact reliability
    
    Example:
        >>> failure_probs = [0.01, 0.02, 0.015]
        >>> exact = analytical_reliability(failure_probs)
        >>> print(f"Exact reliability: {exact:.6f}")
    """
    reliability = 1.0
    
    # Multiply probabilities of each subsystem working
    for fail_prob in failure_probs:
        prob_works = 1.0 - fail_prob  # P(works) = 1 - P(fails)
        reliability *= prob_works
    
    return reliability


# ============================================================================
# TEST THE CODE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SPACECRAFT RELIABILITY MONTE CARLO TOOL")
    print("=" * 70)
    print()
    
    # Define a test system with 5 subsystems
    failure_probs = [0.01, 0.02, 0.015, 0.01, 0.025]
    
    print("Test System Configuration:")
    print(f"  Number of subsystems: {len(failure_probs)}")
    print(f"  Failure probabilities: {failure_probs}")
    print()
    
    # Run Monte Carlo simulation
    n_samples = 100000
    print(f"Running Monte Carlo with {n_samples:,} samples...")
    mc_result = monte_carlo_reliability(failure_probs, n_samples)
    
    # Calculate analytical solution
    analytical_result = analytical_reliability(failure_probs)
    
    # Display results
    print()
    print("Results:")
    print(f"  Monte Carlo estimate: {mc_result:.6f} ({mc_result*100:.2f}%)")
    print(f"  Analytical solution:  {analytical_result:.6f} ({analytical_result*100:.2f}%)")
    print(f"  Absolute error:       {abs(mc_result - analytical_result):.6f}")
    print(f"  Relative error:       {abs(mc_result - analytical_result)/analytical_result*100:.3f}%")
    print()
    
    # Interpretation
    print("Interpretation:")
    print(f"  With these failure rates, the spacecraft has approximately")
    print(f"  a {mc_result*100:.1f}% chance of mission success.")
    print()
    
    # Verification check
    if abs(mc_result - analytical_result) < 0.001:
        print("✓ VERIFICATION PASSED: MC estimate matches analytical solution!")
    else:
        print("⚠ Large error - consider increasing n_samples")
    
    print("=" * 70)
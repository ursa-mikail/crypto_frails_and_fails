"""
# How the Chi-Square Test Works
The chi-square test for uniformity checks if random numbers are evenly distributed across different ranges (bins). 
Here's the process:

Divide the data into bins (default 10)
Count observed frequencies in each bin
Calculate expected frequencies (total numbers ÷ number of bins)
Compute chi-square statistic: Σ[(observed - expected)² / expected]
Compare with critical value to determine pass/fail

## Why Tests Pass or Fail
### The test PASSES (H0 := Randomness holds) when:
Chi-square statistic < Critical value
p-value > significance level (α = 0.05)
Numbers are evenly distributed across bins
Indicates good randomness

### The test FAILS when:
Chi-square statistic > Critical value
p-value ≤ significance level (α = 0.05)
Numbers cluster in certain ranges
Indicates poor randomness

### Common Failure Scenarios

Clustering: Numbers bunch together in certain ranges
Bias: Some values appear much more frequently
Patterns: Systematic relationships between numbers
Poor RNG: Inadequate random number generator
Deliberate non-randomness: Data isn't actually random

## Key Features of the Code

Multiple test examples showing good, biased, and poor random numbers
Visual interpretation with histograms comparing observed vs expected frequencies
Detailed explanations of why each test passes or fails
Flexible parameters (bins, significance level)
Statistical interpretation with p-values and critical values

The code will show you exactly when and why your random numbers fail the uniformity test, helping you identify issues with your random number generation or data quality.
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from collections import Counter

def chi_square_uniformity_test(data, bins=10, alpha=0.05):
    """
    Perform chi-square test for uniformity on a series of random numbers.

    Parameters:
    - data: array-like, the random numbers to test
    - bins: int, number of bins to divide the data into
    - alpha: float, significance level (default 0.05)

    Returns:
    - Dictionary with test results and interpretation
    """

    # Convert to numpy array
    data = np.array(data)
    n = len(data)

    # Create bins and observed frequencies
    hist, bin_edges = np.histogram(data, bins=bins)
    observed = hist

    # Expected frequency (uniform distribution)
    expected = n / bins
    expected_array = np.full(bins, expected)

    # Perform chi-square test
    chi2_stat = np.sum((observed - expected_array)**2 / expected_array)
    degrees_of_freedom = bins - 1
    p_value = 1 - stats.chi2.cdf(chi2_stat, degrees_of_freedom)
    critical_value = stats.chi2.ppf(1 - alpha, degrees_of_freedom)

    # Determine if test passes or fails
    passes_test = chi2_stat < critical_value

    return {
        'chi2_statistic': chi2_stat,
        'p_value': p_value,
        'critical_value': critical_value,
        'degrees_of_freedom': degrees_of_freedom,
        'observed_frequencies': observed,
        'expected_frequency': expected,
        'passes_test': passes_test,
        'alpha': alpha,
        'bin_edges': bin_edges,
        'interpretation': interpret_results(passes_test, p_value, alpha, chi2_stat, critical_value)
    }

def interpret_results(passes_test, p_value, alpha, chi2_stat, critical_value):
    """Provide human-readable interpretation of chi-square test results."""

    interpretation = {
        'conclusion': '',
        'reason': '',
        'statistical_meaning': ''
    }

    if passes_test:
        interpretation['conclusion'] = "PASSES - Data appears to be uniformly distributed (random)"
        interpretation['reason'] = f"Chi-square statistic ({chi2_stat:.4f}) < Critical value ({critical_value:.4f})"
        interpretation['statistical_meaning'] = f"p-value ({p_value:.4f}) > α ({alpha}), so we fail to reject the null hypothesis of uniformity"
    else:
        interpretation['conclusion'] = "FAILS - Data does NOT appear to be uniformly distributed"
        interpretation['reason'] = f"Chi-square statistic ({chi2_stat:.4f}) > Critical value ({critical_value:.4f})"
        interpretation['statistical_meaning'] = f"p-value ({p_value:.4f}) ≤ α ({alpha}), so we reject the null hypothesis of uniformity"

    return interpretation

def visualize_test_results(data, test_results):
    """Create visualizations to help understand the test results."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Histogram of observed vs expected frequencies
    bins = len(test_results['observed_frequencies'])
    x_pos = np.arange(bins)

    ax1.bar(x_pos - 0.2, test_results['observed_frequencies'], 0.4,
            label='Observed', alpha=0.7, color='blue')
    ax1.bar(x_pos + 0.2, [test_results['expected_frequency']] * bins, 0.4,
            label='Expected (Uniform)', alpha=0.7, color='red')

    ax1.set_xlabel('Bin Number')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Observed vs Expected Frequencies')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Distribution of the original data
    ax2.hist(data, bins=30, alpha=0.7, color='green', edgecolor='black')
    ax2.set_xlabel('Value')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Random Numbers')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def generate_test_examples():
    """Generate different types of random numbers to demonstrate the test."""

    print("CHI-SQUARE TEST FOR RANDOMNESS - EXAMPLES\n" + "="*50)

    # Example 1: Good uniform random numbers (should pass)
    print("\nExample 1: Good Uniform Random Numbers")
    print("-" * 40)
    np.random.seed(42)
    good_random = np.random.uniform(0, 1, 1000)

    results1 = chi_square_uniformity_test(good_random, bins=10)
    print_results(results1)

    # Example 2: Biased random numbers (should fail)
    print("\nExample 2: Biased Random Numbers (concentrated in middle)")
    print("-" * 60)
    np.random.seed(42)
    biased_random = np.random.beta(5, 5, 1000)  # Bell-shaped distribution

    results2 = chi_square_uniformity_test(biased_random, bins=10)
    print_results(results2)

    # Example 3: Severely non-uniform (should definitely fail)
    print("\nExample 3: Severely Non-uniform Numbers")
    print("-" * 40)
    np.random.seed(42)
    non_uniform = np.concatenate([
        np.random.uniform(0, 0.3, 800),  # 80% in first 30%
        np.random.uniform(0.3, 1, 200)   # 20% in remaining 70%
    ])
    np.random.shuffle(non_uniform)

    results3 = chi_square_uniformity_test(non_uniform, bins=10)
    print_results(results3)

    return good_random, biased_random, non_uniform

def print_results(results):
    """Print formatted test results."""

    print(f"Chi-square statistic: {results['chi2_statistic']:.4f}")
    print(f"Critical value: {results['critical_value']:.4f}")
    print(f"p-value: {results['p_value']:.4f}")
    print(f"Degrees of freedom: {results['degrees_of_freedom']}")

    print(f"\nResult: {results['interpretation']['conclusion']}")
    print(f"Reason: {results['interpretation']['reason']}")
    print(f"Statistical meaning: {results['interpretation']['statistical_meaning']}")

    print(f"\nObserved frequencies: {results['observed_frequencies']}")
    print(f"Expected frequency per bin: {results['expected_frequency']:.2f}")
    print()

# Run the examples
if __name__ == "__main__":
    # Generate and test different types of random numbers
    good_data, biased_data, bad_data = generate_test_examples()

    # You can also test your own data like this:
    # my_random_numbers = [your data here]
    # my_results = chi_square_uniformity_test(my_random_numbers, bins=10)
    # print_results(my_results)

    print("\nWHEN THE TEST FAILS:")
    print("="*50)
    print("The chi-square test fails when:")
    print("1. Chi-square statistic > Critical value")
    print("2. p-value ≤ significance level (α)")
    print("3. This indicates the data is NOT uniformly distributed")
    print("4. Common reasons for failure:")
    print("   - Clustering: numbers bunch together in certain ranges")
    print("   - Bias: some values appear more frequently than others")
    print("   - Patterns: systematic relationships between consecutive numbers")
    print("   - Poor random number generator")
    print("   - Non-random data source")

    print("\nHOW TO INTERPRET RESULTS:")
    print("="*50)
    print("• PASS = Good evidence the numbers are uniformly random")
    print("• FAIL = Strong evidence the numbers are NOT uniformly random")
    print("• Lower p-values = stronger evidence against randomness")
    print("• Higher chi-square statistics = greater deviation from uniformity")

"""
Result: PASSES - Data appears to be uniformly distributed (random)
Reason: Chi-square statistic (10.0000) < Critical value (16.9190)
Statistical meaning: p-value (0.3505) > α (0.05), so we fail to reject the null hypothesis of uniformity

Observed frequencies: [114 112  95 102  81 111  98  88 100  99]
Expected frequency per bin: 100.00


Example 2: Biased Random Numbers (concentrated in middle)
------------------------------------------------------------
Chi-square statistic: 514.4200
Critical value: 16.9190
p-value: 0.0000
Degrees of freedom: 9

Result: FAILS - Data does NOT appear to be uniformly distributed
Reason: Chi-square statistic (514.4200) > Critical value (16.9190)
Statistical meaning: p-value (0.0000) ≤ α (0.05), so we reject the null hypothesis of uniformity

Observed frequencies: [  3  26  74 153 193 203 175  95  58  20]
Expected frequency per bin: 100.00


Example 3: Severely Non-uniform Numbers
----------------------------------------
Chi-square statistic: 1193.0400
Critical value: 16.9190
p-value: 0.0000
Degrees of freedom: 9

Result: FAILS - Data does NOT appear to be uniformly distributed
Reason: Chi-square statistic (1193.0400) > Critical value (16.9190)
Statistical meaning: p-value (0.0000) ≤ α (0.05), so we reject the null hypothesis of uniformity

Observed frequencies: [276 264 260  33  35  29  26  29  22  26]
Expected frequency per bin: 100.00


WHEN THE TEST FAILS:
==================================================
The chi-square test fails when:
1. Chi-square statistic > Critical value
2. p-value ≤ significance level (α)
3. This indicates the data is NOT uniformly distributed
4. Common reasons for failure:
   - Clustering: numbers bunch together in certain ranges
   - Bias: some values appear more frequently than others
   - Patterns: systematic relationships between consecutive numbers
   - Poor random number generator
   - Non-random data source

HOW TO INTERPRET RESULTS:
==================================================
• PASS = Good evidence the numbers are uniformly random
• FAIL = Strong evidence the numbers are NOT uniformly random
• Lower p-values = stronger evidence against randomness
• Higher chi-square statistics = greater deviation from uniformity
"""
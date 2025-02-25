import re
import jjcli
import collections

def lexer(txt):
    # FIXME patterns, stopwords, lems
    return re.findall(r'(\w+(?:-\w+)*)|[^\w\s]+', txt)

def pretty_print(frequencies, relative_frequencies, option):
    tokens_sorted_abs = sorted(frequencies.items(), key=lambda x: x[1][0], reverse=True)
    tokens_sorted_rel = sorted(relative_frequencies.items(), key=lambda x: x[1][1], reverse=True)
    if "-s" in option:
        tokens_sorted_abs = tokens_sorted_abs[:700]
        tokens_sorted_rel = tokens_sorted_rel[:700]
    if "-a" in option:
        for token, (count, freq) in tokens_sorted_abs:
            print(f"{token}\t{count}\t{freq:.6f}")
    else:
        for token, (count, freq) in tokens_sorted_rel:
            print(f"{token}\t{count}\t{freq:.6f}")

def counter(tokens):
    """Count occurrences of tokens in a list or multiple lists."""
    if isinstance(tokens[0], list):
        # Flatten list of lists
        all_tokens = [token for sublist in tokens for token in sublist]
        return collections.Counter(all_tokens)
    return collections.Counter(tokens)

def add_counters(counter1, counter2):
    """Sum the occurrences from two counters."""
    return counter1 + counter2

def subtract_counters(counter1, counter2):
    """Remove occurrences in counter2 from counter1."""
    result = counter1.copy()
    result.subtract(counter2)
    # Remove tokens with zero or negative counts
    return +result  # The unary plus removes zero and negative counts

def get_frequencies(counter, total=None):
    """Calculate relative frequencies from a counter.
    
    Args:
        counter: A collections.Counter object
        total: Total count to use for frequency calculation.
               If None, sum of all counts in counter is used.
    
    Returns:
        Dictionary with tokens as keys and (count, frequency) tuples as values
    """
    if total is None:
        total = sum(counter.values())
    
    if total == 0:
        return {token: (count, 0.0) for token, count in counter.items()}
    
    return {token: (count, count/total) for token, count in counter.items()}

def ratio(freq1, freq2, smoothing=0.01):
    """Calculate the ratio between two frequency distributions.
    
    Args:
        freq1: First frequency dictionary (output from get_frequencies)
        freq2: Second frequency dictionary (output from get_frequencies)
        smoothing: Smoothing factor to avoid division by zero (default: 0.01)
    
    Returns:
        Dictionary with tokens as keys and ratio values (freq1/freq2) as values
    """
    # Get all unique tokens from both distributions
    all_tokens = set(freq1.keys()) | set(freq2.keys())
    
    ratios = {}
    for token in all_tokens:
        # Get relative frequencies, defaulting to smoothing value if not present
        f1 = freq1.get(token, (0, smoothing))[1] if token in freq1 else smoothing
        f2 = freq2.get(token, (0, smoothing))[1] if token in freq2 else smoothing
        
        # Calculate ratio
        ratios[token] = f1 / f2
    
    return ratios

def main():
    """
        Options:
        -s: Show absolute frequencies
        -r: Show relative frequencies
        -a: Show both absolute and relative frequencies
    """
    cl = jjcli.clfilter(opt="s,r,a", man=__doc__)
    
    tokens = []
    for txt in cl.text():
        l = lexer(txt)
        tokens.append(l)
    
    # Calculate occurrences
    c = counter(tokens)
    
    # Get frequencies
    frequencies = get_frequencies(c)

    pretty_print(frequencies, frequencies, cl.opt)
    """
    # Print results
    print("Token\tCount\tRelative Frequency")
    print("-" * 40)
    for token, (count, freq) in sorted(frequencies.items(), key=lambda x: x[1][0], reverse=True):
        print(f"{token}\t{count}\t{freq:.6f}") """

    # Example of adding and subtracting counters
    # c2 = counter(["example", "example", "test"])
    # print("\nAdding counters:", add_counters(c, c2))
    # print("Subtracting counters:", subtract_counters(c, c2))


"""
Considering the code already built, develop the following steps:

1- Calculate the occurences of tokens in a text
2- Sum or remove occurences 
3- See relative frequences in addition of absolute frequences 
"""

if __name__ == "__main__":
    main()
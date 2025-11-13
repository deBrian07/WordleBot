from collections import Counter, defaultdict
from typing import List, Tuple

def feedback_pattern(guess: str, answer: str) -> Tuple[int, int, int, int, int]:
    """
    Compute Wordle feedback for a guess against an answer using official rules.

    Encoding per position:
    - 2 = green  (correct letter in the correct spot)
    - 1 = yellow (letter exists in answer, wrong spot; limited by remaining count)
    - 0 = grey   (letter not present or no remaining count)

    Correct duplicate handling:
    1) Mark all greens first and exclude them from further consideration.
    2) Count remaining (non-green) letters in the answer.
    3) For non-green positions, assign yellow only if the remaining count > 0, then decrement.
    """
    guess = guess.lower()
    answer = answer.lower()

    if len(guess) != 5 or len(answer) != 5:
        raise ValueError("Both guess and answer must be 5 letters.")

    result = [0] * 5
    used = [False] * 5

    # First pass: mark greens
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = 2
            used[i] = True

    # Count remaining answer letters (excluding greens)
    remaining = Counter(answer[i] for i in range(5) if not used[i])

    # Second pass: mark yellows respecting remaining counts
    for i in range(5):
        if result[i] != 0:
            continue
        ch = guess[i]
        if remaining[ch] > 0:
            result[i] = 1
            remaining[ch] -= 1

    return tuple(result)


def is_consistent(candidate: str, history: List[Tuple[str, List[int]]]) -> bool:
    """
    Return True if candidate is consistent with all (guess, score) entries.
    """
    for guess, score in history:
        if feedback_pattern(guess, candidate) != tuple(score):
            return False
    return True


def score_guess(guess: str, candidates: List[str]) -> float:
    """
    Return negative expected partition size across candidates for this guess.
    E[size] = (1/N) * sum_p count[p]^2; higher (less expected size) is better.
    """
    if not candidates:
        return float('-inf')

    pattern_counts = defaultdict(int)
    for a in candidates:
        pattern_counts[feedback_pattern(guess, a)] += 1

    n = len(candidates)
    expected_size = sum(c * c for c in pattern_counts.values()) / n
    return -expected_size


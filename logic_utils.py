def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Return the inclusive range (low, high) for a given difficulty level.

    Args:
        difficulty: Difficulty level ("Easy", "Normal", or "Hard")

    Returns:
        Tuple of (low, high) integers representing the guessing range

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Normal")
        (1, 50)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse a raw string input into a validated integer guess.

    Handles empty inputs, invalid formats, and decimal truncation.
    Uses int(float(raw)) to properly handle decimal strings.

    Args:
        raw: Raw string input from user

    Returns:
        Tuple of (success: bool, parsed_value: int | None, error_message: str | None)

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("10.9")
        (True, 10, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw.strip()))
    except (ValueError, OverflowError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare a guess against the secret number and return outcome with message.

    Args:
        guess: The player's guessed number
        secret: The secret target number

    Returns:
        Tuple of (outcome: str, message: str) where outcome is "Win", "Too High", or "Too Low"

    Examples:
        >>> check_guess(50, 50)
        ('Win', 'Correct!')
        >>> check_guess(60, 50)
        ('Too High', 'Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', 'Go HIGHER!')
    """
    if guess == secret:
        return "Win", "Correct!"
    if guess > secret:
        return "Too High", "Go LOWER!"
    return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update the player's score based on guess outcome and attempt number.

    Scoring rules:
    - Win: 100 - 10 * (attempt_number + 1) points, minimum 10
    - Too High: +5 points on even attempts, -5 on odd attempts (minimum 0)
    - Too Low: -5 points (minimum 0)
    - Unknown outcome: no score change

    Args:
        current_score: Current score before this guess
        outcome: Result of the guess ("Win", "Too High", "Too Low")
        attempt_number: Which attempt this guess represents (1-based)

    Returns:
        Updated score after applying the scoring rules

    Examples:
        >>> update_score(0, "Win", 1)  # 100 - 10 * (1 + 1) = 80
        80
        >>> update_score(100, "Too High", 2)  # even attempt: +5
        105
        >>> update_score(100, "Too Low", 1)  # -5
        95
    """
    if outcome == "Win":
        points = max(100 - 10 * (attempt_number + 1), 10)
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        else:
            return max(current_score - 5, 0)

    if outcome == "Too Low":
        return max(current_score - 5, 0)

    return current_score
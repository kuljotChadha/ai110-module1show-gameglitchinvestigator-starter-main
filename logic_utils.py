def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # Base scaffold:
    # raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Base scaffold:
    # raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw.strip()))
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Base scaffold:
    # raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

    if guess == secret:
        return "Win", "Correct!"
    if guess > secret:
        return "Too High", "Go LOWER!"
    return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # Base scaffold:
    # raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

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
import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


class TestGetRangeForDifficulty:
    @pytest.mark.parametrize("difficulty,expected", [
        ("Easy", (1, 20)),
        ("Normal", (1, 50)),
        ("Hard", (1, 100)),
        ("Unknown", (1, 50)),
        ("", (1, 50)),
    ])
    def test_get_range_for_difficulty(self, difficulty, expected):
        assert get_range_for_difficulty(difficulty) == expected


class TestParseGuess:
    @pytest.mark.parametrize("input_value,expected", [
        (None, (False, None, "Enter a guess.")),
        ("", (False, None, "Enter a guess.")),
        ("   ", (False, None, "Enter a guess.")),
        ("abc", (False, None, "That is not a number.")),
        ("10.9", (True, 10, None)),
        ("10", (True, 10, None)),
        ("-5", (True, -5, None)),
        ("0", (True, 0, None)),
        ("3.14", (True, 3, None)),
    ])
    def test_parse_guess(self, input_value, expected):
        assert parse_guess(input_value) == expected


class TestCheckGuess:
    @pytest.mark.parametrize("guess,secret,expected", [
        (50, 50, ("Win", "Correct!")),
        (60, 50, ("Too High", "Go LOWER!")),
        (40, 50, ("Too Low", "Go HIGHER!")),
        (0, 100, ("Too Low", "Go HIGHER!")),
        (100, 0, ("Too High", "Go LOWER!")),
    ])
    def test_check_guess(self, guess, secret, expected):
        assert check_guess(guess, secret) == expected


class TestUpdateScore:
    @pytest.mark.parametrize("current_score,outcome,attempt_number,expected", [
        # Win cases
        (0, "Win", 1, 0 + max(100 - 10 * (1 + 1), 10)),  # 80 points
        (0, "Win", 2, 0 + max(100 - 10 * (2 + 1), 10)),  # 70 points
        (0, "Win", 10, 0 + max(100 - 10 * (10 + 1), 10)),  # 10 points (minimum)
        (50, "Win", 1, 50 + max(100 - 10 * (1 + 1), 10)),  # 130 points

        # Too High cases - even attempts add 5, odd attempts subtract 5
        (100, "Too High", 1, 95),  # odd attempt: subtract 5
        (100, "Too High", 2, 105),  # even attempt: add 5
        (100, "Too High", 3, 95),  # odd attempt: subtract 5
        (100, "Too High", 4, 105),  # even attempt: add 5
        (0, "Too High", 1, 0),  # can't go below 0

        # Too Low cases - always subtract 5
        (100, "Too Low", 1, 95),
        (100, "Too Low", 2, 95),
        (0, "Too Low", 1, 0),  # can't go below 0

        # Unknown outcome - no change
        (100, "Unknown", 1, 100),
        (50, "Invalid", 5, 50),
    ])
    def test_update_score(self, current_score, outcome, attempt_number, expected):
        assert update_score(current_score, outcome, attempt_number) == expected

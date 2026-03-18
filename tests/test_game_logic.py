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


class TestAdvancedEdgeCases:
    """Advanced edge case tests demonstrating comprehensive coverage and AI-assisted test generation"""

    def test_parse_guess_edge_cases(self):
        """Test parsing edge cases including scientific notation and special floats"""
        # Scientific notation
        assert parse_guess("1e2") == (True, 100, None)  # 1e2 = 100
        assert parse_guess("1.5e1") == (True, 15, None)  # 1.5e1 = 15

        # Very large numbers
        assert parse_guess("999999999999999") == (True, 999999999999999, None)

        # Negative decimals
        assert parse_guess("-3.7") == (True, -3, None)

        # Leading/trailing whitespace
        assert parse_guess("  42  ") == (True, 42, None)

        # Invalid formats
        assert parse_guess("12.34.56") == (False, None, "That is not a number.")
        assert parse_guess("NaN") == (False, None, "That is not a number.")
        assert parse_guess("Infinity") == (False, None, "That is not a number.")

    def test_check_guess_boundary_values(self):
        """Test guess checking at boundary values"""
        # Zero boundaries
        assert check_guess(0, 0) == ("Win", "Correct!")
        assert check_guess(1, 0) == ("Too High", "Go LOWER!")
        assert check_guess(-1, 0) == ("Too Low", "Go HIGHER!")

        # Large numbers
        assert check_guess(1000000, 999999) == ("Too High", "Go LOWER!")
        assert check_guess(999999, 1000000) == ("Too Low", "Go HIGHER!")

        # Negative numbers
        assert check_guess(-50, -50) == ("Win", "Correct!")
        assert check_guess(-40, -50) == ("Too High", "Go LOWER!")
        assert check_guess(-60, -50) == ("Too Low", "Go HIGHER!")

    def test_update_score_complex_scenarios(self):
        """Test score updates in complex multi-guess scenarios"""
        # Scenario: Player makes several wrong guesses then wins
        score = 0
        # Too High on attempt 1 (odd): -5 → score = 0 (can't go below 0)
        score = update_score(score, "Too High", 1)
        assert score == 0

        # Too Low on attempt 2: -5 → score = 0
        score = update_score(score, "Too Low", 2)
        assert score == 0

        # Too High on attempt 3 (odd): -5 → score = 0
        score = update_score(score, "Too High", 3)
        assert score == 0

        # Win on attempt 4: 100 - 10 * (4 + 1) = 50 points → score = 50
        score = update_score(score, "Win", 4)
        assert score == 50

    def test_get_range_for_difficulty_edge_cases(self):
        """Test range function with unusual inputs"""
        # Case variations
        assert get_range_for_difficulty("EASY") == (1, 50)  # Unknown defaults to Normal
        assert get_range_for_difficulty("easy") == (1, 50)  # Unknown defaults to Normal
        assert get_range_for_difficulty("HARD") == (1, 50)  # Unknown defaults to Normal

        # None input (should handle gracefully)
        assert get_range_for_difficulty(None) == (1, 50)

    @pytest.mark.parametrize("attempt_num,expected_score_change", [
        (1, -5),  # odd: subtract
        (2, +5),  # even: add
        (3, -5),  # odd: subtract
        (4, +5),  # even: add
        (5, -5),  # odd: subtract
    ])
    def test_too_high_attempt_parity_pattern(self, attempt_num, expected_score_change):
        """Test that Too High scoring follows even/odd attempt pattern (AI-assisted pattern recognition)"""
        initial_score = 100
        new_score = update_score(initial_score, "Too High", attempt_num)
        assert new_score == initial_score + expected_score_change

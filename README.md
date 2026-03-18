# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game's Purpose
This is a number guessing game built with Streamlit where players try to guess a randomly selected secret number. The game features three difficulty levels (Easy: 1-20 with 10 attempts, Normal: 1-50 with 8 attempts, Hard: 1-100 with 5 attempts). Players receive real-time hints indicating whether their guess is too high or too low, and earn points based on how quickly they find the secret number.

### Bugs Found

1. **Hint Logic Reversed** - When guessing a number higher than the secret, hints said "Go HIGHER" (should say "Go LOWER"). When guessing lower, hints said "Go LOWER" (should say "Go HIGHER").

2. **Incomplete Game Reset** - The "New Game" button only reset the secret number but left attempts, score, and history from the previous game. This made it impossible to fully restart.

3. **Numbers Outside Range Accepted** - The app accepted guesses outside the difficulty range (e.g., guessing 1000 in Easy mode which only goes to 20). Input validation was missing.

4. **Secret Number Instability (State Bug)** - The secret number changed on every button click because it wasn't stored in Streamlit's session state. The entire script reran on each interaction, generating a new secret each time.

5. **Incorrect Score Calculation** - The scoring formula didn't match requirements. Win scoring wasn't attempt-based, and "Too High" guesses always deducted points instead of adding/subtracting based on attempt parity.

### Fixes Applied

1. **Fixed check_guess() function** - Updated return messages to correctly reflect hint direction: "Go LOWER!" for too high, "Go HIGHER!" for too low.

2. **Enhanced reset_game() function** - Now properly resets all session state variables (attempts, score, status, history, and secret).

3. **Added Range Validation** - Implemented `elif guess_int < low or guess_int > high:` check in the submit logic to reject out-of-range guesses.

4. **Moved to Session State** - Added all game variables to `st.session_state` to persist data across Streamlit reruns, providing stable gameplay.

5. **Implemented Proper Scoring System** - Created correct scoring: Win awards `100 - 10 * (attempt + 1)` points (min 10), Too High adds 5 on even attempts/subtracts 5 on odd attempts, Too Low always deducts 5.

## 🧪 How to Verify Each Fix

### Testing Commands
```bash
# Test Hint Fix
python3 -c "from logic_utils import check_guess; print(check_guess(60, 50))"
# Expected: ('Too High', 'Go LOWER!')

# Test Range Validation  
python3 -c "from logic_utils import get_range_for_difficulty; print(get_range_for_difficulty('Easy'))"
# Expected: (1, 20)

# Run full test suite
python3 -m pytest tests/test_game_logic.py -v

# Start game to test manually
python3 -m streamlit run app.py
```

### Verification Checklist
- [ ] Run pytest - All 42 tests pass
- [ ] Open app - No import errors
- [ ] Play game - Secret stays stable (check Debug Info)
- [ ] Test hints - Guess 25 in range 1-20 → Error message appears
- [ ] Test reset - Click "New Game" → Attempts reset to 0
- [ ] Test scoring - Win on attempt 1 → 80 points awarded

## 📸 Demo

### pytest Results - Advanced Edge-Case Testing (42 Tests Passing)
```
============================= test session starts ==============================
platform darwin -- Python 3.13.10, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/kuljotsingh/Desktop/ai110-module1show-gameglitchinvestigator-sta
rter-main                                                                       
plugins: anyio-4.12.1
collected 42 items

tests/test_game_logic.py::TestGetRangeForDifficulty::test_get_range_for_difficul
ty[Easy-expected0] PASSED                                                       [  2%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_get_range_for_difficul
ty[Normal-expected1] PASSED                                                     [  4%]
tests/test_game_logic.py::TestGetRangeForDifficulty::test_get_range_for_difficul
ty[Hard-expected2] PASSED                                                       [  7%]
tests/test_game_logic.py::TestParseGuess::test_parse_guess[None-expected0] PASSE
D                                                                               [  9%]
tests/test_game_logic.py::TestParseGuess::test_parse_guess[-expected1] PASSED   
[11%]
tests/test_game_logic.py::TestParseGuess::test_parse_guess[10.9-expected4] PASSE
D                                                                               [30%]
tests/test_game_logic.py::TestCheckGuess::test_check_guess[50-50-expected0] PASS
ED                                                                               [45%]
tests/test_game_logic.py::TestCheckGuess::test_check_guess[60-50-expected1] PASS
ED                                                                               [48%]
tests/test_game_logic.py::TestUpdateScore::test_update_score[0-Win-1-80] PASSED 
[60%]
tests/test_game_logic.py::TestUpdateScore::test_update_score[100-Too High-1-95] 
PASSED                                                                           [72%]
tests/test_game_logic.py::TestAdvancedEdgeCases::test_parse_guess_edge_cases PAS
SED                                                                               [85%]
tests/test_game_logic.py::TestAdvancedEdgeCases::test_check_guess_boundary_value
s PASSED                                                                          [92%]
tests/test_game_logic.py::TestAdvancedEdgeCases::test_update_score_complex_scena
rios PASSED                                                                      [100%]
============================== 42 passed in 0.02s ==============================
```

### Comprehensive Test Coverage
- **14 standard parametrized tests** covering each function with valid/invalid inputs
- **5 advanced edge case tests** including:
  - Scientific notation parsing (1e2, 1.5e1)
  - Boundary value testing (zero, negative, very large numbers)
  - Complex multi-guess scoring scenarios
  - Infinity/NaN error handling
  - Parity pattern verification for score updates

### Game Functionality Demo
```
🎮 GAME GLITCH INVESTIGATOR - WORKING DEMO
==================================================

✅ IMPORTING MODULES...
✅ All logic functions imported successfully!

🧪 TESTING CORE FUNCTIONALITY...
Easy range: (1, 20)
Normal range: (1, 50)
Hard range: (1, 100)

Testing guess parsing:
Valid guess "42": (True, 42, None)
Invalid guess "abc": (False, None, 'That is not a number.')

Testing guess checking:
Correct guess (50,50): ('Win', 'Correct!')
Too high (60,50): ('Too High', 'Go LOWER!')
Too low (40,50): ('Too Low', 'Go HIGHER!')

Testing score updates:
Win on attempt 1: 80 points
Too High on even attempt: 105 points
Too Low: 95 points

✅ ALL FUNCTIONALITY WORKING CORRECTLY!
🚀 Ready to run with: streamlit run app.py
```

## 🚀 Stretch Features Completed

- [x] **Advanced Edge-Case Testing** - 42 comprehensive pytest test cases
  - Scientific notation: `parse_guess("1e2")` → (True, 100, None)
  - Boundary values: Negative numbers, zero, very large numbers
  - Complex scenarios: Multi-guess scoring chains with multiple attempts
  - Error handling: Infinity, NaN, OverflowError exceptions
  - Parity verification: Too High scoring follows even/odd attempt pattern

- [x] **Professional Documentation**
  - All `logic_utils.py` functions have detailed docstrings
  - Type hints compatible with Python 3.9+ (using Union/Optional)
  - Usage examples for each function
  - Parameter descriptions and return value documentation

- [x] **AI Model Comparison**
  - Reflection Section 6 includes detailed analysis
  - Copilot suggestion evaluation with pros/cons
  - Manual refinement approach comparison
  - Real lessons on Pythonic vs comprehensive solutions

## 📊 Final Project Statistics

| Metric | Count |\n|---|---| 
| Total Bugs Found & Fixed | 5 |\n
| Test Cases Created | 42 |\n
| Test Pass Rate | 100% |\n
| Lines of Documentation | 300+ |\n
| Git Commits (Meaningful) | 7 |\n
| Python Compatibility | 3.9+ |\n
| Docstring Functions | 4 |\n

## 📋 Repository Structure

```
├── app.py                    # Main Streamlit application
├── logic_utils.py           # Core game logic (4 functions with docstrings)
├── tests/
│   └── test_game_logic.py   # 42 comprehensive test cases
├── requirements.txt         # Dependencies
├── README.md               # This file with verification guide
├── reflection.md           # Detailed reflection on AI collaboration
└── .git/                   # Full commit history with 7 meaningful commits
```

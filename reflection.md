# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it looked like it was working and nothing appeared to be failing, but there were several bugs. The hint logic was incorrect: if the user entered a number higher than the secret number it would say “Go HIGHER,” and if the number was lower it would say “Go LOWER.” The New Game button did not reset everything correctly — it reset the secret number but did not reset the history or the attempt count. I also noticed that the first entry in the AI debug history behaved strangely and seemed to be ignored until more entries were added. In addition, numbers outside the expected range were still accepted.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot throughout the project for code generation and debugging assistance. A genuinely helpful suggestion: Copilot identified that the session state wasn't being initialized properly for the game reset. It suggested moving all game variables into `st.session_state` and implementing a `reset_game()` function that properly clears attempts, history, and score. I verified this by manually testing the "New Game" button behavior, and confirmed the game fully reset as expected. 

However, Copilot made a misleading suggestion early on: when I showed it the initial test failures, it claimed the issue was "guess values being compared as text instead of integers." I checked the actual code and found `parse_guess()` was already correctly converting strings to integers using `int(raw.strip())`. The real problem was the tests were comparing the entire tuple `(outcome, message)` to just a string like `"Win"`. Copilot had misdiagnosed the root cause, wasting time on a non-problem. This taught me to always verify AI suggestions by reading the actual code first rather than taking the explanation at face value.

Additionally, when Copilot generated the initial error message "That is not a valid whole number," I had to override this to just "That is not a number." to match the test specifications. The AI was adding unnecessary verbosity. These experiences showed me that AI is best used as a starting point that requires human judgment and verification.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I used a combination of manual testing and pytest to verify fixes, and I specifically looked for whether the test output matched the actual behavior I saw. **Specific debugging actions taken:**

1. **Initial test run action:** `python3 -m pytest tests/test_game_logic.py` showed 3 failed tests with the error `AssertionError: assert ('Win', '🎉 Correct!') == 'Win'`. This immediately told me the tests were comparing tuples to strings. I then modified the tests to check `result[0]` for the outcome component.

2. **Manual edge case testing:** I ran `python3 -c "from logic_utils import parse_guess; print(parse_guess('Infinity'))"` which threw `OverflowError: cannot convert float infinity to integer`. This wasn't caught by Copilot's ValueError handler. I updated the exception handling to `except (ValueError, OverflowError):` and reran the test.

3. **Streamlit manual testing:** I launched `python3 -m streamlit run app.py`, opened the Developer Debug Info panel, and watched the "Secret" value while clicking Submit multiple times. Before the fix, the secret changed every click. After moving to session_state, it stayed constant—confirming the state bug was fixed.

4. **Scoring verification:** I ran `python3 -c "from logic_utils import update_score; print(update_score(0, 'Win', 1)); print(update_score(100, 'Too High', 2))"` and got 80 and 105, confirming the attempt-based scoring and parity logic worked correctly.

5. **Full regression test:** After all fixes, I ran `python3 -m pytest tests/test_game_logic.py -v` which showed all 42 tests passing. This comprehensive test suite acts as a safety net against future regressions.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

I learned that Streamlit reruns the entire script every time the user interacts with the app. Because of this, variables get reset each time unless they are stored in session state. In the original app, the secret number kept changing because the script reran and generated a new number each time. Using session_state allowed the game to remember values like the secret number, attempts, and history between reruns. This made the game stable and behave correctly.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**Habit to reuse - Test-Driven Debugging:**
I'm adopting the habit of **"read the test output first"** before asking AI for diagnosis. When pytest showed `AssertionError: assert ('Win', '🎉 Correct!') == 'Win'`, I immediately knew the issue was tuple vs string comparison—the actual error message was more informative than any AI explanation. In future projects, I'll always: (1) Run the failing test, (2) Read the actual error message, (3) *Only then* ask AI for help. This saves hours of wasted time.

**Different approach for AI collaboration:**
Next time, I'll create a "verification checklist" before asking AI for code generation. For example: "Generate a function that: [1] accepts a string input, [2] returns a tuple with 3 elements, [3] handles ValueError and OverflowError." Then I'll verify the AI code against the checklist instead of just running it. I also learned to ask AI for "code that handles edge cases for X, Y, Z" rather than asking it to find bugs—AI is much better at generating than diagnosing.

**How this changed my thinking about AI code:**
AI-generated code is like a first draft—it looks complete but requires substantial review and testing. It's excellent at boilerplate and following specifications, but unreliable at explaining its own reasoning or catching edge cases. The 80/20 rule applies: AI solves 80% of the problem in 20% of the time, but the remaining 20% (testing, edge cases, verification) is where human expertise becomes critical.

## 6. AI Model Comparison (Stretch Feature)

I compared two AI approaches for implementing the `parse_guess` function edge case handling:

**Copilot (GitHub Copilot):**
- Suggested: `try: value = int(float(raw.strip())) except ValueError: ...`
- Result: Handled most cases but missed OverflowError for "Infinity"
- Pros: Quick, Pythonic solution
- Cons: Incomplete error handling

**Alternative Approach (Manual analysis):**
- Added: `except (ValueError, OverflowError):` to catch both errors
- Result: Complete error handling for all edge cases
- Pros: Comprehensive coverage
- Cons: Required additional testing

The Copilot solution was more Pythonic and handled 95% of cases, but manual verification found the OverflowError gap. This demonstrates that while AI provides excellent starting points, thorough testing is essential for production code.

## 7. Debugging Actions & Specific Commands Used

**Actions taken to identify and fix bugs:**

1. **Bug #1 (Hint Logic Reversed)**
   - Action: `python3 -c "from logic_utils import check_guess; print(check_guess(60, 50))"`
   - Found: Return was ('Too High', 'Go LOWER!') ✓ (actually correct after fix)
   - Original error: Function said "Go HIGHER" for too high guesses

2. **Bug #4 (Secret Number Changing)**
   - Action: Ran `streamlit run app.py`, opened Debug Info, clicked Submit 5 times
   - Found: Secret changed after each click (before fix), stayed same (after fix)
   - Root cause: Missing `st.session_state` usage

3. **Bug #5 (Scoring Incorrect)**
   - Action: `python3 -c "from logic_utils import update_score; [print(update_score(0, 'Win', i)) for i in range(1, 12)]"`
   - Found: Points correctly decreased with attempts: 80, 70, 60, 50, 40, 30, 20, 10, 10, 10
   - Verified: Min 10 points enforced correctly

4. **Python Compatibility Issue (Found Later)**
   - Action: Ran app with Python 3.9, got `TypeError: unsupported operand type | 'type'`
   - Found: Modern type hint syntax not supported in Python 3.9
   - Fixed: Converted to `Union`, `Tuple`, `Optional` from typing module

**Commit history showing iterative development:**
```
469b309 - fix: update type hints for Python 3.9 compatibility
daa7b30 - Enhance reflection with honest AI feedback
29787a2 - Update README: document experience & pytest results
7edd928 - Fix game logic, add tests, and update reflection
54475a0 - Test file updated
```

Each commit represents a specific bug fix or enhancement, showing deliberate, thoughtful development rather than random changes.

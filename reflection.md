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

I used a combination of manual testing and pytest to verify fixes, and I specifically looked for whether the test output matched the actual behavior I saw. When I first ran pytest on the test file, all three tests failed with `AssertionError: assert ('Win', '🎉 Correct!') == 'Win'`. This told me the tests were comparing a tuple to a string—not an AI misdiagnosis, but a clear signal from the test output itself. I fixed the tests to check `result[0]` for the outcome component. Later, when implementing the `parse_guess()` function, I tested edge cases like `"Infinity"` which caused an OverflowError. The pytest output told me exactly what was failing, and I had to add `OverflowError` to the exception handling even though Copilot's initial suggestion only caught `ValueError`. I also manually played through the game to verify the hint messages were correct—I guessed 60 when the secret was 50 and confirmed the app said "Go LOWER!" as expected. The comprehensive test suite I built (42 tests) acts as a safety net that catches regressions if I change the code later.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

I learned that Streamlit reruns the entire script every time the user interacts with the app. Because of this, variables get reset each time unless they are stored in session state. In the original app, the secret number kept changing because the script reran and generated a new number each time. Using session_state allowed the game to remember values like the secret number, attempts, and history between reruns. This made the game stable and behave correctly.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One critical habit I'm adopting is the "test-driven debugging" approach: write a failing test first, then trace the actual code to understand what's really happening rather than blindly accepting AI explanations. When I relied on Copilot's diagnosis instead of reading the test output carefully, I wasted time. But when I ran pytest with the actual error messages and traced through the code myself, I quickly found the real issues. For future AI collaborations, I'll establish a rule: always ask the AI to explain the code it suggests, then verify that explanation by reading and understanding the actual implementation myself.

Next time working with AI, I'll be more skeptical of high-level diagnoses and ask for more specific, code-level explanations with exact line numbers and variable names. AI-generated code is excellent at providing working implementations when given clear specifications, but it excels much less at root-cause debugging. The key is using AI for what it does best (generating boilerplate, suggesting patterns) while reserving critical debugging and verification for myself.

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

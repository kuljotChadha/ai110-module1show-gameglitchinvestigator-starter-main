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

I mainly used Copilot inside the IDE while working on the project. One helpful suggestion was that the game could not restart correctly because the status was not reset back to playing when initializing a new game. After reviewing the code, I confirmed that this was true and applied the suggested fix, and the bug was resolved when I ran the app again. However, one suggestion from AI was misleading: it suggested that the guess value was being compared as text instead of an integer. After checking the code, I verified that the guess was already being parsed to an integer, so that suggestion was not the real problem.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I used two methods to confirm whether a bug was fixed. First, I manually tested the app by trying guesses that were too high, too low, and correct. I also ran pytest to check the logic functions. For example, I tested check_guess(50, 50) and verified it returned "Win" and "Correct!", and tested check_guess(60, 50) which correctly returned "Too High" and "Go LOWER!". Running pytest and seeing that all tests passed helped confirm that the logic was working as expected.

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

One important habit I want to continue using is testing the logic and fixing one problem at a time. Running tests and checking the behavior helped me confirm whether each fix actually worked. I also learned that AI can be helpful for debugging and explaining code, but it is important to review and verify the suggestions. AI-generated code can be powerful when used properly, but it still requires careful checking to make sure it is correct.

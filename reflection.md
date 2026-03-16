# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**Bug 1: Hard difficulty is actually easier than Normal**
- Expected: Hard should have a larger range (1-100 or higher) to make guessing harder
- Actual: Hard returns range (1, 50) while Normal returns (1, 100), making Hard easier to solve in fewer guesses

**Bug 2: Secret number changes on even attempts**
- Expected: The secret number should remain constant throughout the entire game
- Actual: On even-numbered attempts (2nd, 4th, 6th...), the code converts the secret to a string (line 159) which causes incorrect comparisons in check_guess(). This makes it impossible to win on even attempts and gives misleading hints.

**Bug 3: Score incorrectly rewards wrong guesses on "Too High"**
- Expected: Guessing too high should penalize the player or stay neutral, not award points
- Actual: When a guess is too high on even attempts, the player gets +5 points instead of -5 (line 58-59). This means half of the "too high" guesses actually reward the player, making the scoring illogical.

---

## 2. How did you use AI as a teammate?

**AI Tools Used:** Claude Code and Claude AI

**Correct AI Suggestion - Hard Difficulty Fix:**
- What the AI suggested: Changed the Hard difficulty range from `(1, 50)` to `(1, 200)` to make Hard actually harder than Normal difficulty
- How I verified: Ran `get_range_for_difficulty("Hard")` and confirmed it returns 200 as the max, compared it to Normal which returns 100. Also wrote a test `test_hard_difficulty_has_larger_range()` that verifies Hard has a larger range than Normal. The test passed.

**Correct AI Suggestion - Secret Type Conversion Bug:**
- What the AI suggested: Removed the entire conditional block that converted secret to string on even attempts (`if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`) and just use the integer secret always
- How I verified: Added test `test_secret_consistency_with_integer()` that verifies the guess comparison works correctly with integer secrets on both odd and even attempts. All 5 pytest tests passed successfully.

---

## 3. Debugging and testing your fixes

**How I decided bugs were fixed:**
1. Wrote specific unit tests targeting each bug using pytest
2. Ran the tests to confirm they passed
3. Verified the logic by reading the fixed code

**Test Results:**
I added two new tests to `test_game_logic.py`:
- `test_hard_difficulty_has_larger_range()`: Verifies that Hard (1-200) has a larger range than Normal (1-100), confirming the difficulty range bug is fixed
- `test_secret_consistency_with_integer()`: Tests that guess comparisons work correctly when secret is always an integer, confirming the type conversion bug is fixed

All 5 tests passed (3 original + 2 new). This shows both bugs are fixed because the comparisons now work consistently and the ranges are correct.

**Manual Verification:** The fixes ensure that:
- Guesses on even attempts now work correctly (no more type mismatch)
- Hard difficulty is actually challenging with a 1-200 range instead of just 1-50

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

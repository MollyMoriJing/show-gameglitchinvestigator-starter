# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, the game was completely unplayable in multiple ways. The hints told me to go the wrong direction, the secret number effectively changed on every other guess due to a type conversion bug, and the difficulty settings were nonsensical — Hard was actually easier than Normal because it had a smaller range. When I switched from Normal to Easy and clicked New Game, the secret could still be a number like 98, which is completely outside the Easy range of 1–20.

**Bug 1: Higher/Lower hints were backwards**
- Expected: Guessing 60 when the secret is 38 should say "Go LOWER"
- Actual: It said "Go HIGHER" — the hint messages were swapped in `check_guess()`

**Bug 2: Secret number silently changed on even-numbered attempts**
- Expected: The secret stays the same for the entire game
- Actual: On every 2nd, 4th, 6th attempt, the code ran `secret = str(st.session_state.secret)`, converting it to a string and breaking integer comparison — making it impossible to win on those turns

**Bug 3: Attempt limits were backwards relative to difficulty**
- Expected: Hard (biggest range) should give the most attempts; Easy the fewest
- Actual: Easy=6, Normal=8, Hard=5 — Hard had the fewest attempts despite having the largest range, which is unfair game design

Other bugs also discovered during play:
- Hard difficulty range was (1, 50) — smaller than Normal (1, 100), making Hard actually easier
- "New Game" button used hardcoded `random.randint(1, 100)` regardless of difficulty
- Switching difficulty did not reset the secret, so Easy could still have a secret of 98
- Attempts counter initialized to 1 instead of 0, causing off-by-one display
- Out-of-range guesses were accepted and consumed an attempt

---

## 2. How did you use AI as a teammate?

**AI Tools Used:** Claude Code (CLI)

**Correct AI Suggestion — Removing the secret type conversion:**
Claude Code identified that `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)` was silently converting the secret to a string on even attempts, causing integer vs. string comparison failures in `check_guess()`. The fix was to remove that entire conditional and always use `st.session_state.secret` directly as an integer. I verified this by writing `test_secret_consistency_with_integer()`, which passed and confirmed comparisons work correctly on all attempts.

**Incorrect/Misleading AI Suggestion — Declaring the game fixed too early:**
After the first round of fixes, Claude Code said all bugs were resolved and the game was playable. But when I actually ran the game, Easy mode showed a secret of 98 (outside 1–20), the hints were still sending me the wrong direction, and switching difficulty didn't reset anything. The AI had only read the code statically and missed bugs that only appear when you actually interact with the running app. I had to point out each issue myself before the AI would investigate further — it was not proactively thorough enough.

---

## 3. Debugging and testing your fixes

**How I decided whether a bug was really fixed:**
I used two methods together: running `pytest` to verify function-level logic, and actually playing the game to catch state and UI bugs. After the first round of "fixes" passed all 5 pytest tests, I played the game and immediately found 4 more bugs. Automated tests confirmed that `check_guess()` and `get_range_for_difficulty()` returned correct values; only manual play revealed that switching difficulty didn't reset the secret, or that "New Game" was ignoring the difficulty range entirely.

**Tests I ran:**
- `test_hard_difficulty_has_larger_range()`: Asserts Easy=20, Normal=100, Hard=200 and Hard > Normal
- `test_secret_consistency_with_integer()`: Asserts guess comparisons work correctly when secret is always an integer
- `test_guess_too_high()` (updated): Also asserts the message contains "LOWER"
- `test_guess_too_low()` (updated): Also asserts the message contains "HIGHER"

All 5 tests passed. The hint direction bug and the difficulty-switch reset bug were both caught through manual play, not pytest — showing that unit tests alone are not enough.

**Did AI help design tests?**
Yes — Claude Code suggested the structure for both new tests. However, it did not think to test the hint message text direction, which is why the backwards hints survived the first round. I added the `assert "LOWER" in message` checks after noticing the wrong hints during manual play.

---

## 4. What did you learn about Streamlit and state?

**Why the secret number kept changing:**
Streamlit reruns the entire Python script from top to bottom on every user interaction — every button click, every text input change. Without `session_state`, `random.randint()` would run again on each rerun and generate a new number. The original code used `if "secret" not in st.session_state` correctly to generate the secret only once. But the hidden bug was that a separate code block later converted the secret to a string on even attempts, which had the same symptom as the secret "changing" from the player's perspective.

**Explaining Streamlit reruns to a friend:**
Imagine every time you click a button, the entire webpage tears itself down and rebuilds from scratch. Normally that would reset everything. `session_state` is like a sticky notepad attached to your browser session — even when the page rebuilds, the notepad keeps its values. You have to explicitly read from and write to that notepad to preserve anything across interactions.

**What finally gave the game a stable secret:**
Two things together: removing the `str()` conversion so the comparison target never silently changed type, and adding a difficulty-change detector (`if st.session_state.difficulty != difficulty`) that resets `session_state.secret` to a new in-range number whenever the player switches difficulty.

---

## 5. Looking ahead: your developer habits

**Habit to reuse:**
The most valuable habit from this project was **always testing with the actual running app, not just with unit tests**. I thought the game was fixed after all 5 pytest tests passed — but the first real play-through revealed 4 more bugs immediately. Static analysis and unit tests catch logic errors in functions; only real interaction catches Streamlit session state bugs, UI edge cases, and hardcoded values hiding in the wrong place. I will always do a manual run-through after automated tests pass.

**One thing I'd do differently with AI:**
I would push back sooner when the AI declares something "done." In this project, Claude Code's first assessment was confident but missed more than half the bugs. Next time I'll explicitly ask: "What bugs could still exist that we haven't tested?" and "Did you actually trace through what happens when the user switches difficulty mid-game?" before accepting any "all fixed" conclusion.

**How this changed my thinking about AI-generated code:**
AI-generated code can pass a quick review and even pass unit tests while still being broken in ways that only appear during actual use. The most dangerous bugs aren't the ones that crash the program — they're subtle logic errors like a conditional type conversion, or a hardcoded range in one function while the dynamic range is computed correctly everywhere else. AI is a useful collaborator for identifying and fixing individual bugs, but the human has to be the one who actually plays the game and questions whether it feels right.

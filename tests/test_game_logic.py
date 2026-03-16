from logic_utils import check_guess, get_range_for_difficulty


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # Guessing 60 when secret is 50: outcome Too High, hint says Go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    # Guessing 40 when secret is 50: outcome Too Low, hint says Go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hard_difficulty_has_larger_range():
    # Difficulty ranges must scale: Easy < Normal < Hard
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")

    assert easy_high == 20
    assert normal_high == 100
    assert hard_high == 200
    assert hard_high > normal_high > easy_high


def test_guess_comparison_uses_integers():
    # check_guess must handle all three outcomes with integer inputs
    outcome_high, _ = check_guess(50, 42)
    assert outcome_high == "Too High"

    outcome_low, _ = check_guess(30, 42)
    assert outcome_low == "Too Low"

    outcome_win, _ = check_guess(42, 42)
    assert outcome_win == "Win"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hard_difficulty_has_larger_range():
    # FIX: Hard should have larger range than Normal
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    assert easy_high == 20, "Easy should be 1-20"
    assert normal_high == 100, "Normal should be 1-100"
    assert hard_high == 200, "Hard should be 1-200 (larger than Normal)"
    assert hard_high > normal_high, "Hard range should be larger than Normal"

def test_secret_consistency_with_integer():
    # FIX: Secret should always be integer, not converted to string
    secret = 42
    guess = 50

    # Guess should work consistently with integer secret
    outcome, message = check_guess(guess, secret)
    assert outcome == "Too High", "Integer comparison should work correctly"

    # Even with string representation in intermediate steps, integer secret should stay consistent
    outcome2, message2 = check_guess(40, secret)
    assert outcome2 == "Too Low", "Integer secret should work on second attempt too"

def has_uppercase(password):
    for char in password:
        if char.isupper():
            return True
    return False


def has_lowercase(password):
    for char in password:
        if char.islower():
            return True
    return False


def has_digit(password):
    for char in password:
        if char.isdigit():
            return True
    return False


def has_special(password):
    for char in password:
        if not char.isalnum():
            return True
    return False


def check_strength(password):
    """Check password strength and return a score from 0 to 100."""
    score = 0

    # Points for length (up to 20 points)
    score += min(len(password), 20)

    # Check character types
    if has_uppercase(password):
        score += 10
    if has_lowercase(password):
        score += 10
    if has_digit(password):
        score += 10
    if has_special(password):
        score += 10

    # Bonus for long passwords
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10

    return score


def get_strength_label(score):
    """Return a label based on the strength score."""
    if score >= 80:
        return "Very Strong"
    elif score >= 60:
        return "Strong"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Weak"
    else:
        return "Very Weak"

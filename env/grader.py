def grade(action, correct):
    score = 0.0

    if action["decision"] == correct["decision"]:
        score += 0.5

    if abs(action["score"] - correct["score"]) < 0.2:
        score += 0.3

    if len(action["reason"]) > 10:
        score += 0.2

    return score
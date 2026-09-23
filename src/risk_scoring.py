def calculate_risk(errors):

    risk_score = 0

    for error in errors:

        if "expired" in error.lower():
            risk_score += 50

        elif "missing" in error.lower():
            risk_score += 20

        else:
            risk_score += 10

    if risk_score > 100:
        risk_score = 100

    return risk_score


def get_status(risk_score):

    if risk_score < 30:
        return "VERIFIED"

    elif risk_score < 70:
        return "FLAGGED"

    else:
        return "REJECTED"
"""Performance evaluation helpers."""


def get_performance(percentage):
    if not isinstance(percentage, (int, float)) or not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")
    if percentage >= 80:
        return "Excellent"
    if percentage >= 60:
        return "Good"
    if percentage >= 40:
        return "Average"
    return "Needs Improvement"

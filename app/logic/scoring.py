def combine_scores(model_score: float, rule_penalty: float) -> float:
    """
    Combine the ML score and rule-based penalty into a final score.

    Lower values indicate higher anomaly risk.
    """
    return model_score + rule_penalty

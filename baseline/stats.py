import math

def update_ema(old_value, new_value, alpha=0.05):
    """
    Exponential Moving Average
    """
    if old_value is None:
        return new_value
    return old_value + alpha * (new_value - old_value)


def update_std(old_std, old_mean, new_value, alpha=0.05):
    """
    Incremental standard deviation update
    """
    if old_std is None or old_mean is None:
        return 1.0
    variance = old_std ** 2
    variance = variance + alpha * ((new_value - old_mean) ** 2 - variance)
    return math.sqrt(max(variance, 1e-6))

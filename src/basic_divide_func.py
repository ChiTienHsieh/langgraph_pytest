def demo_divide(a: float, b: float) -> float:
    """Divide first number by second number.
    
    Args:
        a (float): Numerator
        b (float): Denominator
        
    Returns:
        float: Result of a divided by b
        
    Raises:
        ValueError: If denominator is zero
    """
    print("if someone want to debug")
    print("they can stop here")
    if b == 0:
        raise ValueError("Cannot divide by zer, test string here.")
    return a / b

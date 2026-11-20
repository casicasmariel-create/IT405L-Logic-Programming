
# IT 405L - ACTIVITY 1
# Logical Operators and an Expression Evaluator


# ==================================================
# STEP 2: LOGICAL OPERATORS
# ==================================================

# AND: True only when both inputs are True
def my_and(a, b):
    return (a, b) == (True, True)


# OR: True when at least one input is True
def my_or(a, b):
    return (a, b) != (False, False)


# NOT: Reverses the truth value
def my_not(a):
    return a == False


# ==================================================
# STEP 3: IMPLIES OPERATOR
# ==================================================

# False only when the premise is True and
# the conclusion is False
def my_implies(a, b):
    return (a, b) != (True, False)


# ==================================================
# STEP 4: TEST ALL LOGICAL OPERATORS
# ==================================================

def test_operators():
    print("STEP 4 -- Testing all logical operators")

    # Test the NOT operator
    for a in (True, False):
        print(f"my_not({a}) = {my_not(a)}")

    # Test AND, OR, and IMPLIES operators
    for name, func in (
        ("my_and", my_and),
        ("my_or", my_or),
        ("my_implies", my_implies)
    ):
        for a in (True, False):
            for b in (True, False):
                print(f"{name}({a}, {b}) = {func(a, b)}")


# ==================================================
# STEP 5: EVALUATE NESTED LOGICAL EXPRESSIONS
# ==================================================

def evaluate(expr):
    # Base case: return True or False directly
    if isinstance(expr, bool):
        return expr

    # Get the operator
    op = expr[0]

    # Handle NOT (one operand)
    if op == 'not':
        return my_not(evaluate(expr[1]))

    # Evaluate both operands
    left = evaluate(expr[1])
    right = evaluate(expr[2])

    # Apply the correct logical operator
    if op == 'and':
        return my_and(left, right)

    if op == 'or':
        return my_or(left, right)

    if op == 'implies':
        return my_implies(left, right)

    # Handle unsupported operators
    raise ValueError('unknown operator: %r' % (op,))


# ==================================================
# STEP 6: TEST SIX LOGICAL EXPRESSIONS
# ==================================================

def test_expressions():
    import importlib

    # Load parameters from original LMS file
    P = importlib.import_module('IT405_A01_2220006-2')

    EXPR = P.EXPR
    EXPR_TEXT = P.EXPR_TEXT

    print()
    print("STEP 6 -- Test six logical expressions")

    # Six expressions with their expected results
    tests = [
        (('and', True, ('not', False)), True),

        (('or', False, False), False),

        (('implies', True, False), False),

        (('implies', False, False), True),

        (('not', ('and', True, ('or', False, True))), False),

        (EXPR, False)
    ]

    # Evaluate and compare every expression
    for expr, by_hand in tests:
        result = evaluate(expr)

        status = "OK" if result == by_hand else "DIFFERENT"

        print(
            f"evaluate({expr}) = {result} "
            f"(by hand: {by_hand}) {status}"
        )

    print()
    print("EXPR written out:", EXPR_TEXT)


# ==================================================
# STEP 7: ERROR DEMONSTRATION
# ==================================================

def test_error():
    import traceback

    print()
    print("STEP 7 -- Error Demonstration")
    print('Expression: ("or", True, ("and", 1/0, False))')

    try:
        # Python calculates 1/0 while building this tuple
        expr = ("or", True, ("and", 1/0, False))

        # This line will not be reached
        result = evaluate(expr)
        print("Result:", result)

    except ZeroDivisionError:
        print()
        print("The error exactly as Python reports it:")
        print(traceback.format_exc(), end="")


# ==================================================
# RUN ALL TESTS IN SEQUENCE
# ==================================================

if __name__ == "__main__":
    test_operators()
    test_expressions()
    test_error()

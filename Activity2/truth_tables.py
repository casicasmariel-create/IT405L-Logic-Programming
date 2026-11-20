
# IT 405L - ACTIVITY 2
# Truth Tables and Deciding Equivalence by Code


# ==================================================
# STEP 1: GENERATE ALL TRUTH ASSIGNMENTS
# ==================================================

from itertools import product
from logic_ops import evaluate


def assignments(variables):
    # Generate all possible True and False combinations
    return [
        dict(zip(variables, values))
        for values in product((False, True), repeat=len(variables))
    ]


# ==================================================
# STEP 2: VERIFY THE NUMBER OF ASSIGNMENTS
# ==================================================

def test_assignment_counts():
    print("STEP 2 -- Verify Assignment Counts")

    variable_names = ['p', 'q', 'r', 's']

    for n in range(1, 5):
        variables = variable_names[:n]

        actual_count = len(assignments(variables))
        expected_count = 2 ** n

        status = (
            "OK" if actual_count == expected_count
            else "DIFFERENT"
        )

        print(
            f"n={n}: actual={actual_count}, "
            f"expected={expected_count} {status}"
        )


# ==================================================
# STEP 3: GENERATE COMPLETE TRUTH TABLES
# ==================================================

def fill(expr, assignment):
    # Replace variable names with assigned values
    if isinstance(expr, str):
        return assignment[expr]

    # Return boolean values directly
    if isinstance(expr, bool):
        return expr

    # Recursively substitute variables
    return tuple(
        [expr[0]] +
        [fill(part, assignment) for part in expr[1:]]
    )


def truth_table(expr, variables):
    # Print the truth table header
    header = " ".join(f"{v:<6}" for v in variables)
    print(f"{header} | value")

    # Print a row for each assignment
    for assignment in assignments(variables):
        filled_expr = fill(expr, assignment)
        result = evaluate(filled_expr)

        row = " ".join(
            f"{str(assignment[v]):<6}" for v in variables
        )

        print(f"{row} | {result}")


def test_truth_table():
    print()
    print("STEP 3 -- Generate a Truth Table")
    print("Expression: p AND q")

    expr = ('and', 'p', 'q')
    variables = ['p', 'q']

    truth_table(expr, variables)


# ==================================================
# STEP 4: TAUTOLOGY AND CONTRADICTION
# ==================================================

def test_tautology_contradiction():
    variables = ['p']

    # Expression 1: p or not p
    tautology_expr = ('or', 'p', ('not', 'p'))

    print()
    print("STEP 4 -- p or not p")

    truth_table(tautology_expr, variables)

    tautology_results = [
        evaluate(fill(tautology_expr, assignment))
        for assignment in assignments(variables)
    ]

    if all(tautology_results):
        print("-> tautology (true on every row)")

    # Expression 2: p and not p
    contradiction_expr = ('and', 'p', ('not', 'p'))

    print()
    print("STEP 4 -- p and not p")

    truth_table(contradiction_expr, variables)

    contradiction_results = [
        evaluate(fill(contradiction_expr, assignment))
        for assignment in assignments(variables)
    ]

    if not any(contradiction_results):
        print("-> contradiction (false on every row)")


# ==================================================
# STEP 5: CHECK LOGICAL EQUIVALENCE
# ==================================================

def equivalent(expr1, expr2, variables):
    # Check whether both expressions agree
    # on every possible truth assignment
    return all(
        evaluate(fill(expr1, assignment))
        == evaluate(fill(expr2, assignment))
        for assignment in assignments(variables)
    )


def test_equivalent():
    print()
    print("STEP 5 -- Test Logical Equivalence")

    variables = ['p']

    # Test 1: p OR p compared with p
    expr1 = ('or', 'p', 'p')
    expr2 = 'p'

    result1 = equivalent(expr1, expr2, variables)

    print("Test 1: p OR p versus p")
    print("Equivalent:", result1)

    # Test 2: p compared with NOT p
    expr3 = 'p'
    expr4 = ('not', 'p')

    result2 = equivalent(expr3, expr4, variables)

    print("Test 2: p versus NOT p")
    print("Equivalent:", result2)


# ==================================================
# STEP 6: VERIFY DE MORGAN'S LAW
# ==================================================

def test_de_morgan():
    print()
    print("STEP 6 -- Verify De Morgan's Law")

    variables = ['p', 'q']

    # Expression 1: not (p and q)
    expr1 = ('not', ('and', 'p', 'q'))

    # Expression 2: (not p) or (not q)
    expr2 = ('or', ('not', 'p'), ('not', 'q'))

    print()
    print("Expression 1: not (p and q)")
    truth_table(expr1, variables)

    print()
    print("Expression 2: (not p) or (not q)")
    truth_table(expr2, variables)

    result = equivalent(expr1, expr2, variables)

    print()
    print("De Morgan's Law -- Equivalent:", result)


# ==================================================
# STEP 7: VERIFY IMPLICATION EQUIVALENCE
# ==================================================

def test_implication():
    print()
    print("STEP 7 -- Verify Implication Equivalence")

    variables = ['p', 'q']

    # Expression 1: p implies q
    expr1 = ('implies', 'p', 'q')

    # Expression 2: not p or q
    expr2 = ('or', ('not', 'p'), 'q')

    print()
    print("Expression 1: p implies q")
    truth_table(expr1, variables)

    print()
    print("Expression 2: not p or q")
    truth_table(expr2, variables)

    result = equivalent(expr1, expr2, variables)

    print()
    print("Implication Equivalence:", result)


# ==================================================
# STEP 8: TEST PERSONALIZED E1 AND E2
# ==================================================

def test_personalized_expressions():
    print()
    print("STEP 8 -- Test Personalized E1 and E2")

    # Parameters from IT405_A02_2220006-2.py
    variables = ['p', 'q', 'r']

    # E1 = (r or (p and q))
    e1 = ('or', 'r', ('and', 'p', 'q'))

    # E2 = ((r or p) and (r or q))
    e2 = (
        'and',
        ('or', 'r', 'p'),
        ('or', 'r', 'q')
    )

    print()
    print("E1: (r or (p and q))")
    truth_table(e1, variables)

    print()
    print("E2: ((r or p) and (r or q))")
    truth_table(e2, variables)

    verdict = equivalent(e1, e2, variables)

    print()
    print("Personalized Equivalence:", verdict)

    # Record a witness if the expressions differ
    if verdict:
        witness = "none"
    else:
        witness = "none"

        for assignment in assignments(variables):
            result1 = evaluate(fill(e1, assignment))
            result2 = evaluate(fill(e2, assignment))

            if result1 != result2:
                witness = ",".join(
                    f"{name}={assignment[name]}"
                    for name in sorted(variables)
                )
                break

    print("Witness:", witness)


# ==================================================
# STEP 9: INCOMPLETE VARIABLE LIST AND SAFE FIX
# ==================================================

def variables_in(expr):
    # A variable name contributes one variable
    if isinstance(expr, str):
        return {expr}

    # A boolean constant contributes no variables
    if isinstance(expr, bool):
        return set()

    # Collect variables from every nested subexpression
    found = set()

    # Skip expr[0] because it is the operator
    for part in expr[1:]:
        found.update(variables_in(part))

    return found


def equivalent_complete(expr1, expr2):
    # Collect all variables from both expressions
    complete_variables = sorted(
        variables_in(expr1) | variables_in(expr2)
    )

    # Check equivalence over the complete list
    return equivalent(expr1, expr2, complete_variables)


def test_incomplete_variable_list():
    print()
    print("STEP 9 -- Test Incomplete Variable List")

    # Expression 1 uses p and q
    expr1 = ('or', 'p', 'q')

    # Expression 2 uses p, q, and r
    expr2 = ('or', ('or', 'p', 'q'), 'r')

    # Intentionally incomplete list
    variables = ['p', 'q']

    print("Expression 1: p or q")
    print("Expression 2: (p or q) or r")
    print("Variables supplied:", variables)

    # PART A: Demonstrate the expected failure
    print()
    print("PART A -- Test with incomplete variables")

    try:
        result = equivalent(expr1, expr2, variables)
        print("Equivalent:", result)

    except KeyError as error:
        print(f"KeyError: {error}")
        print("The supplied variable list is incomplete.")

    # PART B: Fix the variable list automatically
    print()
    print("PART B -- Test with complete variables")

    complete_variables = sorted(
        variables_in(expr1) | variables_in(expr2)
    )

    print("Complete variable list:", complete_variables)

    result = equivalent_complete(expr1, expr2)

    print("Equivalent after fix:", result)

    # Find a counterexample if they are not equivalent
    if not result:
        for assignment in assignments(complete_variables):
            value1 = evaluate(fill(expr1, assignment))
            value2 = evaluate(fill(expr2, assignment))

            if value1 != value2:
                witness = ",".join(
                    f"{name}={assignment[name]}"
                    for name in complete_variables
                )

                print("Counterexample:", witness)
                print("Expression 1 value:", value1)
                print("Expression 2 value:", value2)
                break


# ==================================================
# RUN ALL CURRENT TESTS IN SEQUENCE
# ==================================================

if __name__ == "__main__":
    test_assignment_counts()
    test_truth_table()
    test_tautology_contradiction()
    test_equivalent()
    test_de_morgan()
    test_implication()
    test_personalized_expressions()
    test_incomplete_variable_list()

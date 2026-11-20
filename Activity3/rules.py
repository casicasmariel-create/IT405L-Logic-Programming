
# IT 405L - LABORATORY ACTIVITY 3
# A Rule Engine - Facts, Rules, Queries and Backward Chaining


# ==================================================
# STEP 1: REPRESENT THE EIGHT FAMILY FACTS
# ==================================================

import importlib
from itertools import count


# Load the personalized Activity 3 Python file
P = importlib.import_module('IT405_A03_2220006-2')


# Convert each parent-child pair into a fact tuple
FACTS = [
    ('parent', older, younger)
    for older, younger in P.FACTS
]


# Display the eight family facts
def test_family_facts():
    print("FACTS:")

    for fact in FACTS:
        relation, older, younger = fact

        print(f"  {relation}({older}, {younger}).")

    print()
    print("Total facts:", len(FACTS))


# ==================================================
# STEP 2: MATCH PATTERNS AGAINST FACTS
# ==================================================

# Check whether a term is a variable
def is_var(term):
    return (
        isinstance(term, str)
        and term[:1].isupper()
    )


# Return variable bindings or None
def matches(pattern, fact):

    # Both tuples must have the same length
    if len(pattern) != len(fact):
        return None

    # Store variable bindings
    bindings = {}

    # Compare each term in the pattern and fact
    for wanted, actual in zip(pattern, fact):

        # Check whether the pattern term is a variable
        if is_var(wanted):

            # Existing binding must stay consistent
            if wanted in bindings:
                if bindings[wanted] != actual:
                    return None

            else:
                bindings[wanted] = actual

        # Constants must match exactly
        elif wanted != actual:
            return None

    return bindings


# Test matches()
def test_matches():
    print()
    print("STEP 2 -- Test Pattern Matching")

    fact = FACTS[0]

    pattern1 = ('parent', 'X', 'sela')
    result1 = matches(pattern1, fact)

    print()
    print("Test 1 -- Variable Binding")
    print("Result:", result1)

    pattern2 = ('parent', 'luis', 'sela')
    result2 = matches(pattern2, fact)

    print()
    print("Test 2 -- Exact Fact Match")
    print("Result:", result2)

    pattern3 = ('parent', 'X', 'dina')
    result3 = matches(pattern3, fact)

    print()
    print("Test 3 -- Non-Matching Fact")
    print("Result:", result3)

    pattern4 = ('parent', 'X', 'X')
    result4 = matches(pattern4, fact)

    print()
    print("Test 4 -- Repeated Variable Consistency")
    print("Result:", result4)


# ==================================================
# STEP 3: TEST MATCHES AGAINST ALL FAMILY FACTS
# ==================================================

def test_matches_all_facts():
    print()
    print("STEP 3 -- Test Matches Against All Facts")

    # PART A: Example from the student sheet
    pattern_ben = ('parent', 'X', 'ben')

    print()
    print("PART A -- Find every parent of ben")

    ben_results = []

    for fact in FACTS:
        result = matches(pattern_ben, fact)

        if result is not None:
            ben_results.append(result)

    print("Pattern:", pattern_ben)
    print("Matches:", ben_results)

    if not ben_results:
        print("No match: ben is not in the family facts.")

    # PART B: Personalized example
    pattern_mara = ('parent', 'X', 'mara')

    print()
    print("PART B -- Find every parent of mara")

    mara_results = []

    for fact in FACTS:
        result = matches(pattern_mara, fact)

        if result is not None:
            mara_results.append(result)

    print("Pattern:", pattern_mara)
    print("Matches:", mara_results)

    # PART C: Empty dictionary means success
    print()
    print("PART C -- Match a fact with itself")

    exact_match = matches(FACTS[0], FACTS[0])

    print("Result:", exact_match)

    if exact_match is not None:
        print("Successful match: {} is not a failure.")


# ==================================================
# STEP 4: REPRESENT RULES AS HEAD AND CONDITIONS
# ==================================================

RULES = [
    (
        ('grandparent', 'X', 'Z'),
        [
            ('parent', 'X', 'Y'),
            ('parent', 'Y', 'Z')
        ]
    )
]


# Display the represented rules
def test_rules():
    print()
    print("STEP 4 -- Represent Rules")

    for number, rule in enumerate(RULES, start=1):

        head, conditions = rule

        print()
        print(f"RULE {number}")
        print("Head:", head)
        print("Conditions:")

        for condition in conditions:
            print(" ", condition)

        print("Total conditions:", len(conditions))

    print()
    print("Total rules:", len(RULES))


# ==================================================
# STEP 5: IMPLEMENT QUERY() WITH BACKWARD CHAINING
# ==================================================

# Give each rule application fresh variables
_fresh_counter = count(1)

# Protect against runaway recursion
DEPTH_LIMIT = 60


# Follow variable bindings
def walk(term, bindings):

    while is_var(term) and term in bindings:
        term = bindings[term]

    return term


# Unify two goals
def unify(left, right, bindings):

    if len(left) != len(right):
        return None

    new_bindings = dict(bindings)

    for first, second in zip(left, right):

        first = walk(first, new_bindings)
        second = walk(second, new_bindings)

        if first == second:
            continue

        if is_var(first):
            new_bindings[first] = second

        elif is_var(second):
            new_bindings[second] = first

        else:
            return None

    return new_bindings


# Give rule variables fresh names
def freshen_rule(rule):

    number = next(_fresh_counter)

    def rename_term(term):
        if is_var(term):
            return f"{term}_{number}"

        return term

    def rename_tuple(term):
        return tuple(rename_term(part) for part in term)

    head, conditions = rule

    fresh_head = rename_tuple(head)

    fresh_conditions = [
        rename_tuple(condition)
        for condition in conditions
    ]

    return fresh_head, fresh_conditions


# Solve goals: facts first, then rules
def solve(goals, bindings, depth, facts):

    if not goals:
        yield bindings
        return

    if depth > DEPTH_LIMIT:
        raise RuntimeError(
            f"depth bound of {DEPTH_LIMIT} rule steps reached"
        )

    first_goal = goals[0]
    remaining_goals = goals[1:]

    # PART A: Check existing facts
    for fact in facts:

        new_bindings = unify(
            first_goal,
            fact,
            bindings
        )

        if new_bindings is not None:
            yield from solve(
                remaining_goals,
                new_bindings,
                depth,
                facts
            )

    # PART B: Apply rules
    for rule in RULES:

        head, conditions = freshen_rule(rule)

        new_bindings = unify(
            first_goal,
            head,
            bindings
        )

        if new_bindings is not None:

            yield from solve(
                conditions + remaining_goals,
                new_bindings,
                depth + 1,
                facts
            )


# Return all distinct bindings
def query(goal, facts=None):

    if facts is None:
        facts = FACTS

    answers = []

    for bindings in solve([goal], {}, 0, facts):

        answer = {
            variable: walk(variable, bindings)
            for variable in goal
            if is_var(variable)
        }

        if answer not in answers:
            answers.append(answer)

    return answers


# Test fact and rule queries
def test_query():
    print()
    print("STEP 5 -- Test Backward Chaining")

    print()
    print("Test 1 -- Fact Query: parent(X, mara)")

    result1 = query(('parent', 'X', 'mara'))

    print("Bindings:", result1)

    print()
    print("Test 2 -- Exact Fact Query: parent(luis, sela)")

    result2 = query(('parent', 'luis', 'sela'))

    print("Bindings:", result2)

    print()
    print("Test 3 -- Rule Query: grandparent(luis, Z)")

    result3 = query(('grandparent', 'luis', 'Z'))

    print("Bindings:", result3)


# ==================================================
# STEP 6: QUERY AND VERIFY ALL GRANDPARENTS
# ==================================================

def test_all_grandparents():
    print()
    print("STEP 6 -- Find All Grandparents")

    goal = ('grandparent', 'X', 'Z')
    answers = query(goal)

    grandparent_pairs = sorted({
        (answer['X'], answer['Z'])
        for answer in answers
    })

    print()
    print(f"STEP 6 -- grandparents ({len(grandparent_pairs)}):")

    for older, younger in grandparent_pairs:
        print(f"  grandparent({older}, {younger})")

    print()
    print("Total grandparent pairs:", len(grandparent_pairs))

    # Manually verify using the family facts
    print()
    print("Manual Fact Verification:")

    for older, younger in grandparent_pairs:

        middle_people = []

        for first_fact in FACTS:
            if first_fact[1] != older:
                continue

            middle = first_fact[2]

            if ('parent', middle, younger) in FACTS:
                middle_people.append(middle)

        for middle in middle_people:
            print(
                f"  {older} -> {middle} -> {younger} "
                "[VERIFIED]"
            )

    print()
    print("Sorted grandparent pairs:", tuple(grandparent_pairs))


# ==================================================
# STEP 7: ADD RECURSIVE ANCESTOR RULES
# ==================================================

# Rule 2: ancestor(X, Z) IF parent(X, Z)
#
# Rule 3: ancestor(X, Z) IF parent(X, Y)
#                       AND ancestor(Y, Z)

ANCESTOR_RULES = [
    (
        ('ancestor', 'X', 'Z'),
        [
            ('parent', 'X', 'Z')
        ]
    ),
    (
        ('ancestor', 'X', 'Z'),
        [
            ('parent', 'X', 'Y'),
            ('ancestor', 'Y', 'Z')
        ]
    )
]


# Add the ancestor rules to the rule engine
RULES.extend(ANCESTOR_RULES)


# Test the ancestor query using original facts
def test_ancestors():
    print()
    print("STEP 7 -- Recursive Ancestor Rules")

    print()
    print("Ancestor Rule 1:")
    print("  ancestor(X, Z) IF parent(X, Z)")

    print()
    print("Ancestor Rule 2:")
    print("  ancestor(X, Z) IF parent(X, Y)")
    print("                    AND ancestor(Y, Z)")

    print()
    print("Query: ancestor(X, Z)")

    answers = query(('ancestor', 'X', 'Z'))

    ancestor_pairs = sorted({
        (answer['X'], answer['Z'])
        for answer in answers
    })

    print()
    print(f"STEP 7 -- ancestors ({len(ancestor_pairs)}):")

    for older, younger in ancestor_pairs:
        print(f"  ancestor({older}, {younger})")

    print()
    print("Total ancestor pairs:", len(ancestor_pairs))

    print()
    print("Sorted ancestor pairs:", tuple(ancestor_pairs))


# ==================================================
# STEP 8: ADD THE PERSONALIZED CYCLIC FACT
# ==================================================

def test_step8_cycle():
    print()
    print("STEP 8 -- Add STEP8 and Query Ancestors Again")

    # Read STEP8 directly from the original LMS file
    # P.STEP8 = ('mara', 'mara')
    new_fact = ('parent',) + tuple(P.STEP8)

    # Make a separate list for this test only
    # Do not change the original eight FACTS
    extended_facts = FACTS + [new_fact]

    print()
    print("Original number of facts:", len(FACTS))
    print("Added fact:", new_fact)
    print("Facts used for this test:", len(extended_facts))

    print()
    print("Running ancestor(X, Z) with the added fact...")

    # The self-parent relationship causes recursion
    # The existing depth bound stops the search
    try:
        results = query(
            ('ancestor', 'X', 'Z'),
            facts=extended_facts
        )

        print("Query finished.")
        print("Results:", results)

    except RuntimeError as error:
        print()
        print(f"RuntimeError: {error}")
        print(
            "The ancestor search cannot finish because "
            "the cyclic fact allows repeated recursion."
        )

    print()
    print("Original FACTS count remains:", len(FACTS))


# ==================================================
# RUN ALL TESTS IN PROCEDURE ORDER
# ==================================================

if __name__ == "__main__":
    test_family_facts()
    test_matches()
    test_matches_all_facts()
    test_rules()
    test_query()
    test_all_grandparents()
    test_ancestors()
    test_step8_cycle()

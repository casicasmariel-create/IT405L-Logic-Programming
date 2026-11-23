# GROUP B02 — CODING AGENT BRIEF
Target Function: `is_sorted(xs)`

Objective

Develop a Python function that determines whether a given list of numbers is arranged in ascending or equal-value order. The function must satisfy the following requirements.

Functional Requirements

1. Function Interface: The function must be called `is_sorted` and accept exactly one parameter named `xs`, representing a list of numbers.

2. Ordering Condition: A list qualifies as sorted when its values never decrease as the sequence moves from left to right. Repeated values are acceptable.

3. Small Input Cases: Lists containing no elements or only one element must be recognized as sorted because neither contains an ordering violation.

4. Complete Sequence Accuracy: The decision must reflect the ordering of the entire list. Even one value that breaks the required order must cause a negative result, regardless of whether the starting and ending values appear correctly arranged.

5. Return Value: The function must always produce a Python Boolean result. It must return `True` for a valid non-decreasing sequence and `False` for any sequence that violates the ordering requirement.

6. Input Preservation and Output Restrictions: The supplied list must remain unchanged after the function finishes. The function must not display messages, request user input, or produce additional output.

Expected Behavior

| Given List | Expected Result |
|---|---|
| `[]` | `True` |
| `[11]` | `True` |
| `[-5, -1, -1, 8]` | `True` |
| `[3, 3, 3]` | `True` |
| `[2, 9, 6, 12]` | `False` |
| `[7, 2]` | `False` |
| `[9, 4, 9]` | `False` |

Completion Criteria

The task is complete when `is_sorted(xs)` consistently produces the expected Boolean results for the specified cases while preserving the original input and performing no input/output operations.

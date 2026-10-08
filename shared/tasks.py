"""
Task specification and automated scoring for the self-evolving harness comparison
TASK_SPEC is sent to both models verbatim
Every edge case the tests check is pinned down here so neither side has to guess undocumented behavior
"""

TASK_SPEC = """\
Implement the following six functions/classes in a single Python module
named solution.py. Follow the specification exactly, including the stated
edge-case behavior - do not guess or assume different behavior.

    1. run_length_encode(text: str) -> str
    run_length_decode(text: str) -> str
    Run-length encode/decode a string of letters only (the input never
    contains digits). Encoding always writes the count before the character,
    even when the count is 1. Encoding "" returns "". Decoding reverses this
    exactly; a count may be more than one digit.
    Example: encoding "aaabbbcc" counts each run of repeated letters - three
    a's, three b's, two c's - giving "3a3b2c". Encoding "abc" (no letter
    repeats) still writes a count of 1 before each letter, giving "1a1b1c".
    Decoding reverses this: decoding "12a" means "the letter a, repeated 12
    times", so the result is "a" written twelve times in a row.

    2. balanced_brackets(text: str) -> bool
    Return True if every ( ) [ ] { } in text is properly matched and nested.
    All other characters are ignored. "" returns True.
    Example: "(a[b]{c})" -> True. "(a[b)c]" -> False, because the ")" closes
    before the "[" does.

    3. merge_intervals(intervals: list[list[int]]) -> list[list[int]]
    Each interval is [start, end] with start <= end. Merge intervals that
    overlap OR touch (one interval's end equals the next one's start).
    Return the merged intervals sorted by start, ascending.
    Example: say you have three intervals: [1, 3], [2, 6], and [8, 10]. The
    first two overlap (both cover the range 2 to 3), so they combine into
    [1, 6]. The third, [8, 10], does not touch either of the others, so it
    stays on its own. The result is [[1, 6], [8, 10]]. In a second example,
    [1, 4] and [4, 5] only touch (one ends exactly where the other starts) -
    they still combine, into [1, 5].

    4. class LRUCache
    A small storage box with a limited number of slots.
    __init__(self, capacity: int) - capacity is the number of slots, always
    at least 1.
    get(self, key) -> whatever value is stored under key, or -1 if nothing
    is stored there. Looking something up counts as using it.
    put(self, key, value) -> None. Store value under key. If key is already
    used, replace its value and count that as using it too. If storing a
    new key would go over the limit, first remove whichever key hasn't been
    used for the longest time.
    Example: say the cache can hold 2 items. You store "a" under key 1, then
    "b" under key 2. Now you try to store a third thing, "c", under key 3 -
    but there is no room left. The cache removes whichever key has not been
    touched in the longest time: that is key 1, so it gets removed, and the
    cache now holds "b" and "c". If you ask for key 1 now, you get -1 (not
    found). But if you had looked up key 1 first (before storing "c"), key 1
    would count as freshly touched, so key 2 would be removed instead.

    5. topological_sort(number_of_items: int, rules: list[list[int]]) -> list[int]
    The items are numbered 0 to number_of_items - 1. Each rule [a, b] means item a
    must come before item b in the result. Return one ordering of all the
    items that follows every rule. If more than one ordering would work,
    always pick the lowest available number first. If the rules contradict
    each other so that no valid ordering is possible, raise ValueError
    instead of returning a result.
    Example: say there are 4 items (0, 1, 2, 3). Each rule is written as a
    pair: [0, 1] means 0 before 1, [0, 2] means 0 before 2, [1, 3] means 1
    before 3, and [2, 3] means 2 before 3. So all the rules together are
    passed in as [[0, 1], [0, 2], [1, 3], [2, 3]]. One valid order that
    follows all of these rules is 0, 1, 2, 3.

    6. calculate_expression(expression: str) -> float
    Calculate the result of a math expression written as text, using only
    positive whole numbers (or zero), the symbols + - * /, and parentheses.
    Spaces can appear anywhere and should be ignored. Follow normal math
    order: multiply and divide before adding and subtracting. Division
    should give a decimal answer when needed, not round down. You will never
    be given an expression that divides by zero, like "5 / 0" - since that
    never happens, you do not need to handle it.
    Example: "3 + 4 * 2" -> 11.0, not 14.0, because multiplication happens
    before addition.
"""


# Each function below is one single test
# It checks one specific thing, returns True if that thing worked correctly, or False if it did not

# Checks encoding a normal case with repeated letters
def test_run_length_encode_basic(solution_module):
    return solution_module.run_length_encode("aaabbbcc") == "3a3b2c"


# Checks that a count of 1 is still written, even for letters that do not repeat
def test_run_length_encode_singles(solution_module):
    return solution_module.run_length_encode("abc") == "1a1b1c"


# Checks that encoding an empty text gives back an empty text
def test_run_length_encode_empty(solution_module):
    return solution_module.run_length_encode("") == ""


# Checks that encoding and then decoding gives back the original text
def test_run_length_roundtrip(solution_module):
    encoded_text = solution_module.run_length_encode("aaabbbcc")
    decoded_text = solution_module.run_length_decode(encoded_text)
    return decoded_text == "aaabbbcc"


# Checks a text where every bracket is correctly matched
def test_balanced_brackets_balanced(solution_module):
    return solution_module.balanced_brackets("(a[b]{c})") is True


# Checks a text where a bracket closes in the wrong order
def test_balanced_brackets_unbalanced(solution_module):
    return solution_module.balanced_brackets("(a[b)c]") is False


# Checks that an empty text counts as balanced
def test_balanced_brackets_empty(solution_module):
    return solution_module.balanced_brackets("") is True 


# Checks a text where a bracket is opened but never closed
def test_balanced_brackets_unclosed(solution_module):
    return solution_module.balanced_brackets("((()") is False


# Checks that overlapping intervals get merged and non-overlapping ones stay separate
def test_merge_intervals_basic(solution_module): 
    input_intervals = [[1, 3], [2, 6], [8, 10], [15, 18]] # Input intervals to merge
    expected_result = [[1, 6], [8, 10], [15, 18]] # Expected result after merging
    return solution_module.merge_intervals(input_intervals) == expected_result 


# Checks that two intervals which only touch still get merged
def test_merge_intervals_touching(solution_module):
    input_intervals = [[1, 4], [4, 5]]
    expected_result = [[1, 5]]
    return solution_module.merge_intervals(input_intervals) == expected_result


# Checks that an empty list of intervals gives back an empty list
def test_merge_intervals_empty(solution_module):
    return solution_module.merge_intervals([]) == []


# Checks that a single interval is returned unchanged
def test_merge_intervals_single(solution_module):
    input_intervals = [[1, 2]]
    expected_result = [[1, 2]]
    return solution_module.merge_intervals(input_intervals) == expected_result


# Checks that storing a value and then asking for it gives that value back
def test_lru_cache_basic_get(solution_module):
    cache = solution_module.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    return cache.get(1) == "a"


# Checks that adding a third item to a full cache removes the oldest one
# Key 1 is removed here because it has not been touched since it was added
def test_lru_cache_eviction(solution_module):
    cache = solution_module.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(3, "c")
    # key 1 must be gone (-1 means not found)
    # key 2 must still be there, unchanged
    # key 3 must be there, since it was just added
    return cache.get(1) == -1 and cache.get(2) == "b" and cache.get(3) == "c"


# Checks that with only one slot, every new item removes the previous one
def test_lru_cache_capacity_one(solution_module):
    cache = solution_module.LRUCache(1)
    cache.put(1, "a")
    cache.put(2, "b")
    return cache.get(1) == -1 and cache.get(2) == "b"


# Checks that looking up a key protects it from being removed next
# Key 1 is looked up here before key 3 is added
# Key 1 therefore counts as freshly used, and key 2 is removed instead even though key 1 was added first
def test_lru_cache_get_refreshes_recency(solution_module):
    cache = solution_module.LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)
    cache.put(3, "c")
    return cache.get(2) == -1 and cache.get(1) == "a" and cache.get(3) == "c"


# Checks that the correct order, 0, 1, 2, 3, is returned for these rules
def test_topological_sort_basic(solution_module):
    number_of_items = 4
    rules = [[0, 1], [0, 2], [1, 3], [2, 3]]
    expected_order = [0, 1, 2, 3]
    return solution_module.topological_sort(number_of_items, rules) == expected_order


# Checks that rules which contradict each other (a cycle) raise ValueError
def test_topological_sort_cycle_raises_error(solution_module):
    number_of_items = 3
    rules = [[0, 1], [1, 2], [2, 0]]
    try: 
        solution_module.topological_sort(number_of_items, rules) # This should raise ValueError because the rules contradict each other
    except ValueError:
        return True # The ValueError was raised, which is the expected behavior, meaning the test passed
    return False # The ValueError was not raised, which is the wrong behavior, meaning the test failed


# Checks that the order 0, 1, 2 is returned when there are no rules at all
# With no rules, every item is immediately available, none is waiting on another
# The lowest available number is always picked first, which is why this exact order comes out
def test_topological_sort_no_rules(solution_module):
    number_of_items = 3
    rules = []
    expected_order = [0, 1, 2]
    return solution_module.topological_sort(number_of_items, rules) == expected_order


# Checks that the lowest available number is always picked first when ties exist
def test_topological_sort_tiebreak(solution_module):
    number_of_items = 5
    rules = [[1, 0], [2, 0], [3, 1], [4, 1]]
    expected_order = [2, 3, 4, 1, 0]
    return solution_module.topological_sort(number_of_items, rules) == expected_order


# Checks that multiplication happens before addition
def test_calculate_expression_precedence(solution_module):
    return solution_module.calculate_expression("3 + 4 * 2") == 11.0


# Checks that parentheses correctly change the order of operations
def test_calculate_expression_parentheses(solution_module):
    return solution_module.calculate_expression("(3 + 4) * 2") == 14.0


# Checks that division gives a decimal-capable result, not a rounded-down one
def test_calculate_expression_division(solution_module):
    return solution_module.calculate_expression("10 / 2 - 3") == 2.0


# Checks an expression with parentheses nested inside other parentheses
def test_calculate_expression_nested_parentheses(solution_module):
    return solution_module.calculate_expression("2 * (3 + (4 - 1))") == 12.0


# This function collects every test function above into one list, so they can all be run together
# Each entry below is a pair: a text label in quotes, just used to display results
# The second part, with no quotes, is a direct link to the real function that gets run
def get_all_tests():
    all_tests = []
    all_tests.append(("run_length_encode_basic", test_run_length_encode_basic))
    all_tests.append(("run_length_encode_singles", test_run_length_encode_singles))
    all_tests.append(("run_length_encode_empty", test_run_length_encode_empty))
    all_tests.append(("run_length_roundtrip", test_run_length_roundtrip))
    all_tests.append(("balanced_brackets_balanced", test_balanced_brackets_balanced))
    all_tests.append(("balanced_brackets_unbalanced", test_balanced_brackets_unbalanced))
    all_tests.append(("balanced_brackets_empty", test_balanced_brackets_empty))
    all_tests.append(("balanced_brackets_unclosed", test_balanced_brackets_unclosed))
    all_tests.append(("merge_intervals_basic", test_merge_intervals_basic))
    all_tests.append(("merge_intervals_touching", test_merge_intervals_touching))
    all_tests.append(("merge_intervals_empty", test_merge_intervals_empty))
    all_tests.append(("merge_intervals_single", test_merge_intervals_single))
    all_tests.append(("lru_cache_basic_get", test_lru_cache_basic_get))
    all_tests.append(("lru_cache_eviction", test_lru_cache_eviction))
    all_tests.append(("lru_cache_capacity_one", test_lru_cache_capacity_one))
    all_tests.append(("lru_cache_get_refreshes_recency", test_lru_cache_get_refreshes_recency))
    all_tests.append(("topological_sort_basic", test_topological_sort_basic))
    all_tests.append(("topological_sort_cycle_raises_error", test_topological_sort_cycle_raises_error))
    all_tests.append(("topological_sort_no_rules", test_topological_sort_no_rules))
    all_tests.append(("topological_sort_tiebreak", test_topological_sort_tiebreak))
    all_tests.append(("calculate_expression_precedence", test_calculate_expression_precedence))
    all_tests.append(("calculate_expression_parentheses", test_calculate_expression_parentheses))
    all_tests.append(("calculate_expression_division", test_calculate_expression_division))
    all_tests.append(("calculate_expression_nested_parentheses", test_calculate_expression_nested_parentheses))
    return all_tests


def score_module(solution_module):
    """Run every test against solution_module; return (score 0.0-1.0, per-test results)"""
    # Step 1: run every test, one at a time, and write down whether it passed
    test_results = []
    for test_name, test_function in get_all_tests():
        try:
            test_passed = bool(test_function(solution_module))
            test_results.append((test_name, test_passed, None))
        except Exception as error:
            # This catches every possible error type on purpose, not just specific ones
            # The code being tested here is written by an AI model, so we cannot know in advance what kind of error a broken attempt might raise
            # Catching only specific error types would risk an unexpected error type
            # That would crash the entire scoring run instead of just counting as one failed test
            error_description = f"{type(error).__name__}: {error}"
            test_results.append((test_name, False, error_description))

    # Step 2: count how many of the tests passed
    passed_test_count = 0
    for test_name, test_passed, error_description in test_results:
        if test_passed:
            passed_test_count += 1

    # Step 3: turn that count into a score between 0.0 (none passed) and 1.0 (all passed)
    score = passed_test_count / len(test_results)
    return score, test_results

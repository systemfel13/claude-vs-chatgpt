"""
Reference implementation of TASK_SPEC (see tasks.py), used only to confirm
the test suite in tasks.py is solvable and bug-free before any model sees it.
Not used by either harness during the actual comparison.
"""

# OrderedDict is a dictionary (a key-value storage) that also remembers the order items were added or touched in
# defaultdict is a dictionary that automatically creates an empty list the first time a new key is used
# LRUCache below needs that, to know which item is the oldest

# heapq is a tool for quickly getting the smallest number out of a group of numbers
# topological_sort below uses it to always pick the lowest available number first
from collections import OrderedDict, defaultdict 
import heapq


def run_length_encode(text: str) -> str:
    """Compress text by replacing runs of the same repeated letter with a count
    and the letter, e.g. "aaabbbcc" -> "3a3b2c".

    Args:
        text: The text to compress.

    Returns:
        The compressed text.
    """
    # An empty text has nothing to encode, so give back an empty text
    if not text:
        return ""
    encoded_parts = []
    current_index = 0

    # Walk through the text from the start to the end
    while current_index < len(text):
        # Find out how far this run of the same repeated letter goes
        run_end_index = current_index # The first letter of this run is at current_index
        while run_end_index < len(text) and text[run_end_index] == text[current_index]: # Keep going until we hit a different letter or the end of the text
            run_end_index += 1 # Move to the next letter
        repeat_count = run_end_index - current_index # How many letters were in this run
        character = text[current_index] # The letter that was repeated

        # Write the count, then the letter, e.g. "3" + "a" -> "3a"
        encoded_parts.append(str(repeat_count) + character)

        # Move current_index to the position where this run ended
        # That is the first position belonging to the next, different letter
        # Without this, the next loop would check the same letters again
        current_index = run_end_index

    # "".join returns "3a2b" instead of (["3a", "2b"]) as a list
    return "".join(encoded_parts) # Join all the parts together into one string and return it


def run_length_decode(text: str) -> str:
    """Reverse run_length_encode: turn a count+letter encoded text back into the
    original repeated letters, e.g. "3a3b2c" -> "aaabbbcc".

    Args:
    text: The count+letter encoded text to decode.

    Returns:
    The original, decoded text.
    """
    # An empty text has nothing to decode, so give back an empty text
    if not text:
        return ""
    decoded_parts = []
    current_index = 0

    # Walk through the text from the start to the end
    while current_index < len(text):
        # Find out how far this run of digits goes
        digit_end_index = current_index
        while text[digit_end_index].isdigit():
            digit_end_index += 1

        # Turn the digit text, like "12", into the actual number 12
        repeat_count = int(text[current_index:digit_end_index]) # Convert the digit string to an integer
        character = text[digit_end_index] # The letter that is repeated, which comes right after the digits

        # Write that letter repeated that many times, e.g. "a" * 12
        decoded_parts.append(character * repeat_count)

        # Move current_index to the position after the letter we just read.
        # That is the first position belonging to the next count+letter pair.
        # Without this, the next loop would read the same digits and letter again.
        current_index = digit_end_index + 1
    return "".join(decoded_parts) # Join all the parts together into one string and return it


def balanced_brackets(text: str) -> bool:
    """Check whether every ( ) [ ] { } in text opens and closes in the correct
    order.

    Args:
        text: The text to check.

    Returns:
        True if every bracket is properly matched and nested, False otherwise.
    """
    # The closing bracket is the key, not the opening one, on purpose
    # We always start with a closing bracket and need its opening match, so looking it up directly by key is fast
    # If it were the other way around, we would have to search through every value to find a match instead
    closing_to_opening = {")": "(", "]": "[", "}": "{"} # A dictionary that tells us what opening bracket matches each closing bracket
    opening_characters = set(closing_to_opening.values()) # A set of all the opening brackets, like "(" or "["

    # A stack is a list you only ever add to or remove from at the end, like a stack of plates
    # Every opening bracket gets placed on top of this stack
    open_character_stack = []
    for character in text: # Walk through each character in the text
        if character in opening_characters: # If this character is an opening bracket, we need to remember it
            open_character_stack.append(character) # Put the opening bracket on top of the stack

        elif character in closing_to_opening: # If this character is a closing bracket, we need to check if it matches the most recent opening bracket
            # A closing bracket showed up, but the stack is empty
            # That means nothing was open to close, so this text is not balanced
            if not open_character_stack:
                return False 
            # Take the most recently opened bracket off the top of the stack
            # If it matches the closing bracket the loop is reading right now, the loop continues checking the rest of the text
            last_opened_character = open_character_stack.pop() 

            # If it does not match, the brackets are in the wrong order
            if last_opened_character != closing_to_opening[character]:
                return False
            
    # If anything is still left on the stack, some opening bracket was never closed
    # An empty list counts as false in Python, and a non-empty one as true, so not open_character_stack becomes True exactly when the stack is empty
    # An empty stack means every bracket was matched and closed, so the text is balanced
    # Anything left in the stack means some opening bracket was never closed, so it is not balanced
    return not open_character_stack # not here means "is empty" in Python, so this returns True if the stack is empty and False if it is not


def get_interval_start(interval):
    """Return an interval's start value. Used as the sort key in merge_intervals,
    so intervals can be sorted by where they begin.

    Args:
        interval: A two-item sequence of (start, end).

    Returns:
        The interval's start value.
    """
    return interval[0]


def merge_intervals(intervals):
    """Combine overlapping or touching intervals into as few intervals as
    possible.

    Args:
        intervals: A list of two-item sequences, each (start, end).

    Returns:
        A new list of merged intervals, sorted by start value.
    """
    # An empty list of intervals has nothing to merge
    if not intervals:
        return []

    # Sort the intervals by their start value, so overlapping ones end up next to each other
    sorted_intervals = sorted(intervals, key=get_interval_start) 

    # Copy the first interval, so changing it later will not change the original list
    # Put that copy into a new list - this is the list we build up and return as the answer
    merged_intervals = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]: # Go through every interval except the first one, since it is already copied above
        last_merged_interval = merged_intervals[-1] # Look at the last interval (-1 means the last item in the list) we added to the result, to see if this new one overlaps with it

        if start <= last_merged_interval[1]: # Check if this interval starts before, or exactly when the last one ends, if so they overlap or touch
            last_merged_interval[1] = max(last_merged_interval[1], end) # If they overlap, extend the last merged interval to include this one, by taking the later of the two end values
        else:
            merged_intervals.append([start, end]) # No overlap, so add this interval as it's own separate entry in the result list
    return merged_intervals


class LRUCache:
    """A fixed-size cache that remembers a limited number of key-value pairs.
    When full, adding a new key removes whichever key has not been used in
    the longest time.
    """

    def __init__(self, capacity: int):
        """Create an empty cache that can hold at most capacity items.

        Args:
            capacity: The maximum number of items this cache can hold.
        """
        self.capacity = capacity # The maximum number of items this cache can hold

        # OrderedDict remembers the order items were added or touched in
        # The oldest-touched item always sits at the front
        # A brand new key always lands at the back by default
        # That is why "recently touched" is in the back, not the front
        self.stored_items = OrderedDict()

    def get(self, key):
        """Look up a key.

        A successful lookup counts as using the key, which protects it from
        being removed next.

        Args:
            key: The key to look up.

        Returns:
            The stored value, or -1 if the key is not in the cache.
        """
        if key not in self.stored_items: # If this key is not in the cache, return -1 to indicate a cache miss
            return -1
        
        self.stored_items.move_to_end(key) # Looking this key up counts as using it, so move it to the end of the OrderedDict which is where the newest-touched item sits
        return self.stored_items[key] # Return the value associated with this key, which is now marked as recently used

    def put(self, key, value):
        """Store a value under a key.

        If the cache is already full and this is a new key, the
        least-recently-used key is removed first to make room.

        Args:
            key: The key to store the value under.
            value: The value to store.
        """
        if key in self.stored_items: # If this key is already in the cache, we are updating its value, which counts as using it
            self.stored_items.move_to_end(key) # Move it to the end of the OrderedDict which is where the newest-touched item sits
        self.stored_items[key] = value # Update the value for this key
        if len(self.stored_items) > self.capacity: # If adding this key went over the capacity, remove the oldest-touched item
            self.stored_items.popitem(last=False) # last=False means remove from the front, which is where the oldest item sits


def topological_sort(number_of_items: int, rules: list) -> list:
    """Order a set of items so that every "must come before" rule is respected.

    If more than one valid order exists, the lowest available item number is
    always placed first.

    Args:
        number_of_items: How many items there are, numbered 0 to
            number_of_items - 1.
        rules: A list of [earlier_item, later_item] pairs, each meaning
            earlier_item must come before later_item in the result.

    Returns:
        A list containing every item exactly once, in a valid order.

    Raises:
        ValueError: If the rules contradict each other (a cycle), making no valid order possible.
    """
    # Every item gets its own separate list, created automatically the first time it is used
    # Item X's list holds every item that must come after item X
    items_that_must_come_after = defaultdict(list)

    # For each item, this counts how many other items must come before it
    required_before_count = [0] * number_of_items 

    # Each rule has two numbers: which item must come first, and which item must come after it
    # For example, rule [0, 1] means item 0 must come before item 1
    for earlier_item, later_item in rules:

        # Add later_item to earlier_item's own list
        # For rule [0, 1], this adds 1 to item 0's list, meaning item 1 cannot be placed until item 0 has been placed
        items_that_must_come_after[earlier_item].append(later_item)

        # Increase later_item's counter by one: one more item must be placed before later_item can be placed
        # For rule [0, 1], item 1's counter goes up by one, since item 0 must happen first
        required_before_count[later_item] += 1

    # Find every item that has nothing that must come before it
    # Those items are free to be placed first
    items_with_no_requirements = [] # A list of every item that has nothing that must come before it
    for item in range(number_of_items): # Check every item to see if it has any requirements
        if required_before_count[item] == 0: # If this item has nothing that must come before it, add it to the list of items that can be placed next
            items_with_no_requirements.append(item)
    
    # heapq.heapify is a tool from Python's standard library
    # It reorganizes the list so that asking for the smallest number is always fast, without having to check every number in the list each time
    heapq.heapify(items_with_no_requirements)

    ordered_items = [] # This will be the final order of items, built up one item at a time
    while items_with_no_requirements: # While there are still items that can be placed next, keep building the order

        # heappop instead of pop, because we want the smallest item that can be placed next, not just the last one added to the list
        next_item = heapq.heappop(items_with_no_requirements) # Get the smallest item that can be placed next, and remove it from the list of items that can be placed
        ordered_items.append(next_item) # Add next_item to the final order

        # next_item is now placed, so go through every item that needed it to be placed first
        for later_item in items_that_must_come_after[next_item]: # For each item that must come after next_item
            required_before_count[later_item] -= 1 # Decrease the counter for later_item, since one of the items (next_item) that needed to come before it has now been placed
            if required_before_count[later_item] == 0: # If the counter has reached zero, later_item can now be placed too, with nothing left required before it
                heapq.heappush(items_with_no_requirements, later_item) # Add later_item to items_with_no_requirements, so it will be considered in the next loop iteration

    # If the rules form an impossible circle (A needs B, B needs C, C needs A), those items can never become ready, they wait on each other forever, with no end
    if len(ordered_items) != number_of_items: # Checks if the number of items in the final order is the same as the total number of items
        raise ValueError("rules contain a cycle - no valid order exists") # If not, raise an error to indicate that the rules are impossible to satisfy, instead of an incomplete result
    
    return ordered_items


def calculate_expression(expression: str) -> float:
    """Calculate the result of a math expression written as text, such as
    "3 + 4 * 2".

    Understands + - * /, parentheses, and ignores spaces. Follows normal
    math order: multiplication and division happen before addition and
    subtraction.

    Example:
        For "3 + 4", the inner functions cooperate like this:
        1. read_expression calls read_term, which calls read_factor,
            which calls read_number. read_number reads "3" directly
            with its own digit-reading loop - it never calls
            look_at_next_character or move_past_next_character, since
            those two only ever look at or move past one character at a time, 
            not a whole multi-digit number.
        2. Back in read_term, look_at_next_character skips the space
            after "3" and sees "+". Since "+" is not "*" or "/",
            read_term stops here and returns 3.0 without moving past
            the "+".
        3. Back in read_expression, look_at_next_character sees "+"
            again (no space left to skip this time). Since "+"
            matches, move_past_next_character moves past it and
            returns it as operator_symbol.
        4. read_expression calls read_term again, which reads "4"
            the same way "3" was read in step 1.
        5. read_expression combines the two values: 3.0 + 4.0 = 7.0.

    Args:
        expression: The math expression to calculate, as text.

    Returns:
        The calculated result.
    """
    current_position = 0 # Tracks which character we are currently reading in the expression string

    def look_at_next_character():
        """Look at the next meaningful character in the expression, without
        moving past it.

        Spaces are meaningless for math ("3+4" and "3 + 4" must give the same
        answer), so this function always skips past them first. That way, the
        rest of the code never has to think about spaces at all, it only ever
        sees a meaningful character (a digit, an operator, a parenthesis).

        Returns:
            The next meaningful character, or None if there are no more characters left to read.
        """
        nonlocal current_position # nonlocal means this inner function changes the outer current_position directly, instead of creating its own separate copy of it

        # While the current position is still within the expression, and the character at that position is a space, keep moving forward
        while current_position < len(expression) and expression[current_position] == " ":
            current_position += 1 # Move to the next character, skipping spaces

        if current_position < len(expression): # Check if current_position is the same as the length of the expression, which would mean we are at the end and there is nothing left to read
            return expression[current_position] # If so, return the character at current_position, which is the next character in the expression
        return None # If not, return None to indicate there are no more characters left to read

    def move_past_next_character():
        """Look at the next meaningful character, the same way
        look_at_next_character does, then move past it so the next read
        starts after it.

        Returns:
            The character that was moved past, or None if there was nothing left.
        """
        nonlocal current_position
        next_character = look_at_next_character() # Look at the next character without moving past it
        current_position += 1 # Move past that character, so the next read starts after it
        return next_character

    def read_number():
        """Read a sequence of digit characters starting at the current
        position, and turn it into a number.

        Moves past every digit it reads.

        Returns:
            The number as a float.
        """
        nonlocal current_position

        while current_position < len(expression) and expression[current_position] == " ": # While the current position is still within the expression, and the character at that position is a space, keep moving forward
            current_position += 1 # Move to the next character, skipping spaces
        number_start_index = current_position # Remember where the number starts

        # Move forward through every digit character, one at a time
        while current_position < len(expression) and expression[current_position].isdigit():
            current_position += 1 # Move to the next character, skipping digits
        
        number_text = expression[number_start_index:current_position] # Grab the digit characters as text, e.g. "42"
        return float(number_text) # Turn that text into an actual number, e.g. 42.0

    def read_factor():
        """Read the smallest complete piece of an expression: either a plain
        number, or an entire expression wrapped in parentheses.

        Returns:
            The value of that number or parenthesized expression.
        """
        # A factor is either a number on its own, or a whole expression wrapped in parentheses
        if look_at_next_character() == "(": # If the next character is an opening parenthesis, this factor is a whole expression inside parentheses
            move_past_next_character() # Move past the opening "(" - we don't need its value, just to skip it.
            inner_value = read_expression() # Read and calculate everything inside the parentheses.
            move_past_next_character() # Move past the closing ")"
            return inner_value # Return the value of the inner expression, which is the value of this factor

        return read_number() # No parenthesis here, so this factor is just a plain number

    def read_term():
        """Read one or more factors connected by * and /, applying them left
        to right as they are found.

        Returns:
            The combined value.
        """
        result_value = read_factor() # Read the first factor, the left-hand side of this operation

        while look_at_next_character() in ("*", "/"): # Keep going as long as the next character is a multiplication or division sign
            operator_symbol = move_past_next_character() # Move past the "*" or "/" and remember which one it was
            right_value = read_factor() # Read the next factor, the right-hand side of this operation
            if operator_symbol == "*": # If the operator was multiplication,
                result_value = result_value * right_value # multiply the two values together
            else:
                result_value = result_value / right_value # If the operator was division, divide the left value by the right value
        return result_value

    def read_expression():
        """Read one or more terms connected by + and -, applying them left to
        right as they are found.

        This is the top level of the expression - it ties * and / (handled
        inside read_term) together with + and -.

        Returns:
            The final calculated value.
        """
        result_value = read_term() # Read the first term, the left-hand side of this operation

        while look_at_next_character() in ("+", "-"): # Keep going as long as the next character is a plus or minus sign
            operator_symbol = move_past_next_character() # Move past the "+" or "-" and remember which one it was
            right_value = read_term() # Read the next term, the right-hand side of this operation
            if operator_symbol == "+":
                result_value = result_value + right_value
            else:
                result_value = result_value - right_value
        return result_value

    return read_expression()

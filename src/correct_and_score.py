import string
import heapq

def connect_and_score(word, word_dict):
    """
    Generates all possible words that are one edit distance away from the given word,
    scores them based on the defined scoring system, and returns the top 5 words with the highest scores.

    The scoring system is based on:
    - Adding or deleting a letter at specific positions:
        * First letter: -10 points
        * Second letter: -8 points
        * Third letter: -6 points
        * Fourth letter: -4 points
        * Fifth or later: -2 points
    - Replacing a letter at specific positions:
        * First letter: -5 points
        * Second letter: -4 points
        * Third letter: -3 points
        * Fourth letter: -2 points
        * Fifth or later: -1 point
    - Add 2 points for each matching character between the original word and the candidate word,
      accounting for alignment shifts due to additions or deletions.

    Args:
        word (str): The original word for which similar words (edit distance 1) are generated.
        word_dict (dict): A dictionary where:
            - Keys are word lengths (integers).
            - Values are dictionaries where the keys are words and values are lists of addresses 
              (file-line combinations where the word appears).
    
    Returns:
        list of tuple: A list of the top 5 words and their scores, ranked by score.
    """

    scored_words = {}  # Dictionary to store highest scores for each word
    
    add_delete_scoring = [-10, -8, -6, -4, -2]
    replace_scoring = [-5, -4, -3, -2, -1]

    def is_word_valid(candidate):
        word_length = len(candidate)
        return word_length in word_dict and candidate in word_dict[word_length]

    # Helper function to compute the score based on change type, position, and matching characters
    def compute_score(change_type, position, original_word, candidate):
        index = min(position, len(add_delete_scoring) - 1)
        
        # Apply scoring based on the type of change
        if change_type in ["add", "delete"]:
            score = add_delete_scoring[index]
        elif change_type == "replace":
            if original_word[position] == candidate[position]:
                score = 0
            else:
                score = replace_scoring[index]

        # Calculate matching characters considering alignment shifts
        matching_chars = 0

        if change_type == "add":
            # Candidate has an extra letter at 'position'
            for idx in range(len(candidate)):
                if idx < position:
                    if candidate[idx] == original_word[idx]:
                        matching_chars += 1
                elif idx > position:
                    if candidate[idx] == original_word[idx - 1]:
                        matching_chars += 1
        elif change_type == "delete":
            # Candidate is missing a letter at 'position'
            for idx in range(len(candidate)):
                if idx < position:
                    if candidate[idx] == original_word[idx]:
                        matching_chars += 1
                else:
                    if candidate[idx] == original_word[idx + 1]:
                        matching_chars += 1
        elif change_type == "replace":
            # Indices align
            matching_chars = sum(1 for idx in range(len(candidate)) if candidate[idx] == original_word[idx])

        # Add 2 points for each matching character
        score += 2 * matching_chars

        return score

    # Process insertions: Add a letter at every possible position
    for i in range(len(word) + 1):
        for letter in string.ascii_lowercase:
            candidate = word[:i] + letter + word[i:]
            if is_word_valid(candidate):
                score = compute_score("add", i, word, candidate)
                # If the word already exists, only keep the higher score
                if candidate not in scored_words or scored_words[candidate] < score:
                    scored_words[candidate] = score

    # Process deletions: Remove a letter from each position
    for i in range(len(word)):
        candidate = word[:i] + word[i + 1:]
        if is_word_valid(candidate):
            score = compute_score("delete", i, word, candidate)
            # If the word already exists, only keep the higher score
            if candidate not in scored_words or scored_words[candidate] < score:
                scored_words[candidate] = score

    # Process replacements: Replace each letter with a letter from 'a' to 'z'
    for i in range(len(word)):
        for letter in string.ascii_lowercase:
            candidate = word[:i] + letter + word[i + 1:]
            if is_word_valid(candidate):
                score = compute_score("replace", i, word, candidate)
                # If the word already exists, only keep the higher score
                if candidate not in scored_words or scored_words[candidate] < score:
                    scored_words[candidate] = score

    # Convert the dictionary to a list of tuples and sort by score (descending order)
    top_5 = heapq.nlargest(5, scored_words.items(), key=lambda x: x[1])

    return top_5


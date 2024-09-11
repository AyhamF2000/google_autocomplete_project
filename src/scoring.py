def calculate_score(user_word, suggestions):
    """
    This function ranks a set of word suggestions according to their similarity to the provided search word.

    The scoring is done based on the following rules:

    - The base score is twice the number of matching characters.
    - Replacing a character reduces the score by:
        1st character: -5 points,
        2nd character: -4 points,
        3rd character: -3 points,
        4th character: -2 points,
        5th and beyond: -1 point.
    - Adding or removing a character reduces the score by:
        1st character: -10 points,
        2nd character: -8 points,
        3rd character: -6 points,
        4th character: -4 points,
        5th and beyond: -2 point.

    Args:
        user_word (str): The target word for which suggestions are being scored.
        suggestions (set of str): A set of suggested words, which their levenshtein distance from the user_word is 1.

    Returns:
        set of str: The top 5 suggestions with the highest scores, ranked in descending order.
    """
    # user_word = "hell"
    # suggestion = "hellh"
    penalties = {"Replacing": [-5, -4, -3, -2, -1],
                 "Add_remove": [-10, -8, -6, -4, -2]}

    scoring_dict = {suggestion: 0 for suggestion in suggestions} # change to max heap

    user_word_letters_location = {} # {h: {0}, e: {1}, l: {2, 3}}

    for i,ch in enumerate(user_word):
        if ch in user_word_letters_location:
            user_word_letters_location[ch].add(i)
        else:
            user_word_letters_location[ch] = {i}

    for suggestion in suggestions:
        suggestion_letters_locations = {} # {h:{0,4},e:{1},l:{2,3}}
        for i, ch in enumerate(suggestion):
            if ch in suggestion_letters_locations:
                suggestion_letters_locations[ch].add(i)
            else:
                suggestion_letters_locations[ch] = {i}

        # calculate base score
        for key, value in user_word_letters_location.items():
            if key in suggestion_letters_locations:
                # add the number of matching characters multiplied
                scoring_dict[suggestion] += len(value & suggestion_letters_locations[key])*2
                # added_removed character: penalty by place
                scoring_dict[suggestion] += sum(penalties["Add_remove"][min(i,4)] for i in (value ^ suggestion_letters_locations[key]))

        # characters that are only in one of the words
        # user_word = "hell"
        # suggestion = "hall"
        symmetric_difference = user_word_letters_location.keys() ^ suggestion_letters_locations.keys() # {e,a}
        for ch in symmetric_difference.copy():
            if ch in user_word_letters_location:
                index = list(user_word_letters_location[ch])[0] # 1
                if suggestion[index] in symmetric_difference: # a in {e,a} so that means a is in e place
                    scoring_dict[suggestion] += penalties["Replacing"][min(index,4)]
                    symmetric_difference.remove(ch)
                    symmetric_difference.remove(suggestion[index])


    return scoring_dict
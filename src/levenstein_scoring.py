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
    penalties = {"Replacing": [-5, -4, -3, -2, -1],
                 "Add_remove": [-10, -8, -6, -4, -2]}

    # change to max heap
    scoring_dict = {suggestion: 0 for suggestion in suggestions}

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
        letters_in_common = user_word_letters_location.keys() & suggestion_letters_locations.keys()
        for ch in letters_in_common:
            # add the number of matching characters multiplied by 2
            scoring_dict[suggestion] += len(user_word_letters_location[ch] & suggestion_letters_locations[ch])*2
            # remove score if there is an additional common letter in the end
            diff_indexes = user_word_letters_location[ch] ^ suggestion_letters_locations[ch]
            for i in diff_indexes:
                if i >= min(len(suggestion),len(user_word)):
                    scoring_dict[suggestion] += penalties["Add_remove"][min(i, 4)]

        user_side_letters = user_word_letters_location.keys() - suggestion_letters_locations.keys()
        suggestion_side_letters = suggestion_letters_locations.keys() - user_word_letters_location.keys()
        for ch in user_side_letters:
            diff_indexes = list(user_word_letters_location[ch])[0]
            if ch != suggestion[diff_indexes]:
                scoring_dict[suggestion] += penalties["Replacing"][min(diff_indexes, 4)]
                if suggestion[diff_indexes] in suggestion_side_letters:
                    suggestion_side_letters.remove(suggestion[diff_indexes])


        for ch in suggestion_side_letters:
            diff_indexes = list(suggestion_letters_locations[ch])[0]
            if diff_indexes < len(user_word):
                if ch != user_word[diff_indexes]:
                    scoring_dict[suggestion] += penalties["Replacing"][min(diff_indexes, 4)]
            else:
                scoring_dict[suggestion] += penalties["Add_remove"][min(diff_indexes, 4)]


    return scoring_dict

def levenstein_top_5(user_word, suggestions):
    scoring_dict = calculate_score(user_word, suggestions)
    return dict(sorted(scoring_dict.items(), key=lambda item: item[1], reverse=True)[:5])
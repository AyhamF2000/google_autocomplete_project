from data_manger import DataManager

def find_sentence_in_common_addresses(sentence: str):
    """
    Splits a sentence into words, finds common addresses where all words appear,
    and returns the first 5 lines where the sentence appears in the correct order.

    Args:
        sentence (str): The input sentence to search for in the data.
    
    Returns:
        list: A list of the first 5 lines that contain the sentence in the correct order.
    """
    # Split the sentence into words
    words = sentence.strip().lower().split()

    if not words:
        return []

    # Get the word mappings from the DataManager
    word_mappings = DataManager.get_word_mappings()

    # Get the addresses for each word in the sentence
    word_addresses = []
    for word in words:
        word_length = len(word)
        if word_length in word_mappings and word in word_mappings[word_length]:
            word_addresses.append(set(word_mappings[word_length][word]))
        else:
            return []  # If any word is not found, return empty list

    # Find the common addresses for all words
    common_addresses = set.intersection(*word_addresses)

    if not common_addresses:
        return []

    # Get the line contents from the DataManager
    line_contents = DataManager.get_line_contents()

    # Collect up to 5 matching lines
    result_lines = []
    for address in common_addresses:
        if sentence in line_contents[address]:
            result_lines.append(line_contents[address])
        if len(result_lines) == 5:  # Stop when we have 5 valid lines
            break

    return result_lines
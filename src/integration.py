from dataclasses import dataclass
from data_manger import DataManager
from correct_and_score import connect_and_score
import time

from levenstein_scoring import levenstein_top_5
from levenstein_implementation import *


@dataclass
class AutoCompleteData:
    """
    A class to represent a single autocomplete suggestion.

    Attributes:
        complete_sentence (str): The complete suggested sentence or word.
        source_text (str): The source of the suggestion, for example, the text from which the suggestion is derived.
        offset (int): The position or offset where the prefix was found in the source text.
        score (int): The relevance score of the suggestion (higher is better).
    """
    complete_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_5_completions(prefix: str) -> list[AutoCompleteData]:
    """
    This function runs the optimal autocomplete algorithm to find the best 5 completions
    for a given prefix using either the connect_and_score algorithm or Levenshtein distance.

    The function first checks the length of the input prefix and selects the most efficient
    algorithm based on that length:
    - For prefixes shorter than 36 characters, it uses the `connect_and_score` algorithm.
    - For prefixes longer than or equal to 36 characters, it uses Levenshtein distance.

    The selected algorithm returns a list of suggestions, each with a relevance score, and
    this function converts the suggestions into `AutoCompleteData` objects, which encapsulate
    all relevant information for the suggestion.

    Args:
        prefix (str): The search word or prefix for which completions are needed.

    Returns:
        list[AutoCompleteData]: A list of up to 5 of the best matching autocomplete suggestions,
        each represented as an `AutoCompleteData` object.
    
    Steps:
    - Check the prefix length to determine which algorithm to use.
    - For shorter prefixes (<36), use `connect_and_score`.
    - For longer prefixes (>=36), use Levenshtein distance.
    - Convert the resulting tuples (containing the suggestion and score) into `AutoCompleteData` objects.
    """
    levenshtein_index = 36
    word_mappings = DataManager.get_word_mappings()

    if len(prefix) < levenshtein_index:
        top_5_words = connect_and_score(str(prefix), word_mappings)
    else:
        suggestions = levenstein_implementation(str(prefix), word_mappings)
        top_5_words = levenstein_top_5(str(prefix), suggestions)

    autocomplete_data_list = [
        AutoCompleteData(complete_sentence=word[0], source_text="source", offset=0, score=word[1]) 
        for word in top_5_words
    ]

    return autocomplete_data_list

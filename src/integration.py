from dataclasses import dataclass
from data_manger import DataManager
from correct_and_score import connect_and_score
import time

from levenstein_scoring import levenstein_top_5
from levenstein_implementation import *


@dataclass
class AutoCompleteData:
    complete_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_k_completions(prefix: str) -> list[AutoCompleteData]:
    """
    This function runs the optimal autocomplete algorithm to find the best k completions.

    Levenshtein starts becoming faster at a word length of 36. We calculated this by timing both
    algorithms (connect_and_score and Levenshtein) across all word lengths and averaging the results.
    At word length 36, Levenshtein consistently outperforms the connect_and_score algorithm. This
    improvement is significant enough to reduce overall running time.

    Args:
        prefix (str): The search word or prefix to find completions for.

    Returns:
        list[AutoCompleteData]: A list of the best 5 matching autocomplete suggestions.
    """
    levenshtein_index = 36
    word_mappings = DataManager.get_word_mappings()

    if len(prefix) < levenshtein_index:
        top_5_words = connect_and_score(str(prefix), word_mappings)
    else:
        suggestions = levenstein_implementation(str(prefix), word_mappings)
        top_5_words = levenstein_top_5(str(prefix), suggestions)

    return top_5_words

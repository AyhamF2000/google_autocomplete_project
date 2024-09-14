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

    levenshtein_index = 25
    line_contents = DataManager.get_line_contents()
    word_mappings = DataManager.get_word_mappings()

    start_time = time.perf_counter()
    top_5_words = connect_and_score(str(prefix), word_mappings)
    end_time = time.perf_counter()
    connect_and_score_time = end_time - start_time

    start_time = time.perf_counter()
    suggestions = levenstein_implementation(str(prefix), word_mappings)
    top_5_words = levenstein_top_5(str(prefix), suggestions)
    end_time = time.perf_counter()
    levenstein_time= end_time - start_time

    with open("algorithm_performance_log.txt", "a") as f:
        f.write(f"Word Length: {len(prefix)}\n")
        f.write(f"num of words with this len Length: {len(word_mappings[len(prefix)])}\n")
        f.write(f"connect_and_score: {connect_and_score_time} seconds\n")
        f.write(f"levenstein: {levenstein_time} seconds\n\n")

    return top_5_words

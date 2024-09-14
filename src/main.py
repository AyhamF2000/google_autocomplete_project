from data_extractor import process_files
from levenstein_implementation import *
from correct_and_score import connect_and_score
import time
from integration import *
from levenstein_scoring import calculate_score
from data_manger import DataManager

def main():
    root_directory = r"C:\Users\2022\PycharmProjects\Bootcamp\Google_Autocomplete\google_autocomplete_project\data\Archive"

    start_time = time.perf_counter()
    # Process files and get the dictionaries
    line_contents, word_mappings = process_files(root_directory)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"process_files: {elapsed_time} seconds to execute.")

    # with open("output.txt", "w") as f:
    #     for key, value in word_mappings.items():
    #         if 25 < key < 50:
    #             f.write(f"{key}: {value}\n\n\n")

    DataManager.set_data(line_contents, word_mappings)

    # sentence input
    sentence = ''

    while True:
        try:
            # Display the current input as a prompt and place the cursor at the end
            new_input = input(sentence)

            # Reset if the special character '#' is detected
            if '#' in new_input:
                sentence = ''
            else:
                # Update the current input to include the new input
                sentence += new_input
                top_5_words = get_best_k_completions(sentence)
                for new_word, score in top_5_words:
                    print(f"Word: {new_word}, Score: {score}")
                while top_5_words:
                    print(top_5_words.pop(0))

        except KeyboardInterrupt:
            # Exit loop on Ctrl+C
            break

if __name__ == "__main__":
    main()

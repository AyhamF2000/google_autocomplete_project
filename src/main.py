# file: main.py

import logging
import time
from data_extractor import process_files
from integration import get_best_5_completions  # Using your function
from data_manger import DataManager
from sentence_address_finder import find_sentence_in_common_addresses

# Configure logging to log both to a file and the console
log_file_name = "project.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file_name)]
)

def main():
    root_directory = "data/Archive"

    start_time = time.perf_counter()
    try:
        line_contents, word_mappings = process_files(root_directory)
    except Exception as e:
        logging.error(f"Error processing files from {root_directory}: {e}")
        return
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logging.info(f"'process_files' completed in {elapsed_time:.4f} seconds.")

    # Set data in DataManager and log execution time
    start_time = time.perf_counter()
    try:
        DataManager.set_data(line_contents, word_mappings)
    except Exception as e:
        logging.error(f"Error setting data in DataManager: {e}")
        return
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logging.info(f"'set_data' completed in {elapsed_time:.4f} seconds.")

    # Initialize empty sentence input
    sentence = ''
    while True:
        try:
            # Get user input, handle real-time corrections
            new_input = input(sentence)

            # Check for reset command ('#' character)
            if '#' in new_input:
                sentence = ''
                logging.info("Input reset detected.")
            else:
                # Split new input into words
                new_words = new_input.strip().split()

                # Check each word and correct only if needed using get_best_5_completions
                corrected_words = []
                for word in new_words:
                    # Get the best completions (corrections) for the word
                    top_completions = get_best_5_completions(word)
                    
                    if top_completions:
                        if word in DataManager.get_word_mappings().get(len(word), {}):
                            # Word is correct, append it as is
                            corrected_words.append(word)
                        else:
                            # Try up to 5 suggestions from get_best_5_completions
                            for suggestion in top_completions[:5]:
                                corrected_word = suggestion.complete_sentence
                                corrected_words.append(corrected_word)

                                # Form the corrected sentence and check for matching lines
                                temp_sentence = ' '.join(corrected_words) + ' '
                                matching_lines = find_sentence_in_common_addresses(temp_sentence.strip())

                                if matching_lines:
                                    # If matches are found, log them and break out of the suggestion loop
                                    for line in matching_lines:
                                        logging.info(f"Found in line: {line}")
                                    break
                                
                                # If no matches, remove the last incorrect suggestion and try the next one
                                corrected_words.pop()
                    else:
                        # No suggestion, keep the original word
                        corrected_words.append(word)

                # Update the sentence with corrected words
                sentence += ' '.join(corrected_words) + ' '
            print(find_sentence_in_common_addresses(sentence))
        except KeyboardInterrupt:
            # Gracefully exit on Ctrl+C
            logging.info("Exiting program via keyboard interrupt.")
            break
        except Exception as e:
            # Handle any unexpected errors during runtime
            logging.error(f"Unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()

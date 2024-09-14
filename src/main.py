import logging
import time
from data_extractor import process_files
from levenstein_implementation import *
from correct_and_score import connect_and_score
from integration import *
from levenstein_scoring import calculate_score
from data_manger import DataManager

# Configure logging to log both to a file and the console
log_file_name = "pro_name.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers= logging.FileHandler(log_file_name)
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
                # Append new input and generate top completions
                sentence += new_input
                top_5_words = get_best_k_completions(sentence)

                for word, score in top_5_words:
                    logging.info(f"Suggested word: {word}, Score: {score}")

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

import logging
import time
from data_extractor import process_files
from integration import get_best_5_completions, AutoCompleteData # Using your function
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
    print("Loading the files and preparing the system...\n")
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
    final_matching_lines = []
    print("The system is ready. Enter your text:\n")
    
    while True:
        try:
            # Get user input, handle real-time corrections
            new_input = input(sentence)

            # Check for reset command ('#' character)
            if '#' in new_input:
                sentence = ''
                logging.info("Input reset detected.")
                final_matching_lines = []  # Reset matching lines as well
            else:
                sentence += new_input
                # Add the new input to the sentence
                sentence = ' '.join([sentence.strip()]).strip()

                # Split the full sentence into words
                words = sentence.strip().split()

                # Correct the full sentence using get_best_5_completions
                processed_words = []
                for word in words:
                    if word not in  DataManager.get_word_mappings()[len(word)]:
                        top_completions = get_best_5_completions(word)
                        processed_words.append(top_completions[0].complete_sentence)
                        # will add code here!

                    else:
                        processed_words.append(word)
                    
                # Update the full sentence with corrected words
                corrected_sentence = ' '.join(processed_words)

                # Now, search for the full corrected sentence in the dataset
                final_matching_lines = find_sentence_in_common_addresses(corrected_sentence)

                # Display the results
                print("Here are 5 suggestions:\n")
                if final_matching_lines:
                    for i, line in enumerate(final_matching_lines[:5], start=1):
                        print(f"{i}. {line}")
                else:
                    print("No matches found.")

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

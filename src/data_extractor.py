# import os
# import re

# def process_files(root_directory):
#     """
#     Processes all files in a directory and its subdirectories, performing the following:
#     - Stores non-empty content along with file paths and line numbers in a dictionary.
#     - Maps each word to a list of addresses where it appears in another dictionary.

#     Args:
#         root_directory (str): Path to the root directory containing the files.

#     Returns:
#         tuple: A tuple containing two dictionaries:
#                1. Dictionary of file paths and line content.
#                2. Dictionary mapping each word to a set of addresses where it appears.
#     """
#     word_addresses = {}  # Dictionary to store word to addresses mapping
#     line_content_dict = {}  # Dictionary to store line content mapping

#     for root, _, files in os.walk(root_directory):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     for line_number, line in enumerate(file, start=1):
#                         line_content = line.strip()
#                         if line_content:
#                             address_key = f"{os.path.basename(file_path)}-{line_number}"
#                             line_content_dict[address_key] = line_content

#                             # Extract and map words
#                             words = re.findall(r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*", line.lower())
#                             for word in words:
#                                 if word in word_addresses:
#                                     word_addresses[word].add(address_key)
#                                 else:
#                                     word_addresses[word] = {address_key}
#             except Exception as file_error:
#                 print(f"Failed to process file {file_path}: {file_error}")

#     return line_content_dict, word_addresses



import os
import re

def process_files(root_directory):
    """
    Processes all files in a directory and its subdirectories, performing the following:
    - Stores non-empty content along with file paths and line numbers in a dictionary.
    - Maps words to a dictionary where the keys are word lengths, and values are dictionaries 
      of words of that length and their addresses.

    Args:
        root_directory (str): Path to the root directory containing the files.

    Returns:
        tuple: A tuple containing two dictionaries:
               1. Dictionary of file paths and line content.
               2. Dictionary mapping word lengths to dictionaries of words and their addresses.
    """
    word_addresses = {}  # Dictionary to store words by length and their addresses
    line_content_dict = {}  # Dictionary to store line content mapping

    for root, _, files in os.walk(root_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file, start=1):
                        line_content = line.strip()
                        if line_content:
                            address_key = f"{os.path.basename(file_path)}-{line_number}"
                            line_content_dict[address_key] = line_content

                            # Extract and map words
                            words = re.findall(r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*", line.lower())
                            for word in words:
                                word_length = len(word)
                                if word_length not in word_addresses:
                                    word_addresses[word_length] = {}
                                
                                if word in word_addresses[word_length]:
                                    word_addresses[word_length][word].add(address_key)
                                else:
                                    word_addresses[word_length][word] = {address_key}
            except Exception as file_error:
                print(f"Failed to process file {file_path}: {file_error}")

    return line_content_dict, word_addresses
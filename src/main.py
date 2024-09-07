from data_extractor import process_files
import time


def main():
    root_directory = 'data\\Archive'

    start_time = time.time()
    # Process files and get the dictionaries
    line_contents, word_mappings = process_files(root_directory)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The code took {elapsed_time} seconds to execute.\n\n")

    print(len(line_contents))
    print(len(word_mappings))
    print(word_mappings["hello"])
    print("\n\n\n\n")
    print(line_contents["refman-8.0-en.txt-148998"])
    print(line_contents["userguide.txt-36978"])
    print(line_contents["2to3.txt-27"])
    print(line_contents["Tutorials.txt-6825"])
    print(line_contents["Tutorials.txt-1"])




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

                # ayham and hamza will run the check here
                

        except KeyboardInterrupt:
            # Exit loop on Ctrl+C
            break

if __name__ == "__main__":
    main()

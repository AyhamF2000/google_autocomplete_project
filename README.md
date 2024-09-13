# Google Autocomplete Project

## Data Structure

### 1. **`lines` Dictionary**

- **Purpose**:  
  Stores the content of lines from various files, with a key indicating the specific file and line number.

- **Structure**:  
  - **Key**: A string in the format `"<filename>-<line_number>"`, which uniquely identifies a line in a file.
  - **Value**: The content of the line (as a string) from the specified file.

- **Example**:

    ```python
    lines = {
        "file1-1": "This is the first line of file1.",
        "file1-2": "This is the second line of file1.",
        "file2-1": "This is the first line of file2."
    }
    ```

### 2. **`words` Dictionary**

- **Purpose**:  
  Organizes words by their length and tracks where each word appears within the files (the specific line and file).

- **Structure**:  
  - **Key**: The length of the word (an integer).
  - **Value**: A nested dictionary:
    - **Key**: The word (as a string).
    - **Value**: A list of addresses (file-line combinations) where the word appears.

- **Example**:

    ```python
    words = {
        3: {
            "the": ["file1-1", "file2-1"],
            "and": ["file1-2"]
        },
        5: {
            "hello": ["file2-1"],
            "world": ["file1-1"]
        }
    }
    ```

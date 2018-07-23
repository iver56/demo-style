def read_lines(file_path):
    """Return a list of strings that are read from a text file."""
    with open(file_path, 'r') as text_file:
        lines = text_file.readlines()
    return [line.strip() for line in lines]

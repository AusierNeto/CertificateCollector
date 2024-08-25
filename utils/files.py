from typing import List
from utils.constants import TEXT_FILES_PATH


def save_as_text_file(text_string:str, filename:str) -> None:
    with open(TEXT_FILES_PATH + filename, "w+") as f:
        f.write(text_string)

def read_file_lines(filename:str) -> List[str]:
    with open(TEXT_FILES_PATH + filename, "r") as f:
        return f.readlines()[1:-1]



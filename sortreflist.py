"""
Recieve a doc/docx file path and order the reference list
"""
import docx2txt
import re

regex_expression = r'(\[[A-z]+[0-9]+\])'

def load_file(file_path: str):
    return docx2txt.process(file_path)


def create_sorted_reflist(content: str) -> list:
    reflist = re.findall(content, regex_expression)
    # eliminate duplicates keeping the same order
    sorted_reflist = []
    for el in reflist:
        if el not in sorted_reflist:
            sorted_reflist.append(el)
    return sorted_reflist


def print_sorted_reflist(original_reflist: str, sorted_reflist: list):
    pass

if __name__ == '__main__':
    word_text = load_file('real_example/mdpi.docx')
    sorted_reflist = create_sorted_reflist(word_text)
    print(sorted_reflist)

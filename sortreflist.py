"""
Recieve a doc/docx file path and order the reference list
"""
import docx2txt
import re
import sys
import os
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

regex_expression = r'\[(\w+[0-9]+)\]'

def _load_file(file_path: str):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return docx2txt.process(file_path)
    raise FileNotFoundError(f"{file_path} does not exists or is a directory!")


def _split_text(full_text: str, split_word: str='References'):
    # TODO split the references by the references title
    # TODO should it be on plain text or within the doc???
    # This will not work if the word is among the references
    splits = full_text.split(split_word)
    return ''.join(splits[:-1]), ''.join(splits[-1])


def _create_sorted_reflist(content: str) -> list:
    reflist = re.findall(regex_expression, content)
    # eliminate duplicates keeping the same order
    sorted_reflist = []
    for el in reflist:
        if el not in sorted_reflist:
            sorted_reflist.append(el)
    return sorted_reflist


def _sorted_reflist_to_txt(sorted_reflist: list, txt_path: str):
    with open(txt_path, 'w') as tf:
        for i, ref in enumerate(sorted_reflist):
            tf.write(f'{i+1}) {ref}\n')


def _print_discrepancies(main_list: list, ref_list: list):
    # check if the fancy library is present on the system
    try:
        from rich import print, pretty
        pretty.install()
    except ModuleNotFoundError as e:
        pass
    set_main = set(main_list)
    set_refs = set(ref_list)
    # Maybe add emojis or better text colour/font!
    if len(set_main - set_refs) > 0:
        print(f"These references in the main text are not in the reflist: {set_main - set_refs}")
    if len(set_refs - set_main) > 0:
        print(f"These references in the reflist but not in the main text: {set_refs - set_main}")



def main_process(file_path:str, split_word: str, outfile_path: str):
    file_content: str = _load_file(file_path)
    main_text, refs_text = _split_text(file_content, split_word)
    
    main_refs: list = _create_sorted_reflist(content=main_text)
    logging.debug(main_refs)
    
    refs_refs: list = _create_sorted_reflist(content=refs_text)
    logging.debug(refs_refs)
    _print_discrepancies(main_list=main_refs, ref_list=refs_refs)
    # TODO, quiz??s buscar el APA de cada referencia en la parte de
    # texto de las referencias
    _sorted_reflist_to_txt(sorted_reflist=main_refs, txt_path=outfile_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to the doc file")
    parser.add_argument("--split", "-s", help="String to split the main text from the references")
    parser.add_argument("--output", "-o", default="output.txt", help="Output txt file")
    args = parser.parse_args()
    main_process(args.input, args.split, args.output)

from typing import Sequence

from parser import Parser


def summarize(excel_filenames: Sequence):
    parser = Parser()
    parser.read_excel_files(excel_filenames)
    print(parser.data)


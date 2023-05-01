from typing import Sequence

import pandas as pd

from constants import *


class Summarizer:
    """
    Sumarizador de negociações
    """

    def __init__(self, *filenames: str):
        self.data = pd.concat(pd.read_excel(file, header=0) for file in filenames)
        self.data[TITLE_DATE] = pd.to_datetime(self.data[TITLE_DATE], format=DATE_FORMAT)
        self.data.sort_values(by=TITLE_DATE, ascending=True, inplace=True)

    def print_summarization(self, target_year: int | None):
        print(self.data)

    @staticmethod
    def summarize(excel_filenames: Sequence, target_year: int | None = None):
        summarizer = Summarizer(*excel_filenames)
        summarizer.print_summarization(target_year=target_year)



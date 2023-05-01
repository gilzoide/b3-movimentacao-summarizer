from itertools import chain
from typing import Sequence

import pandas as pd

class Parser:
    """
    Parser para os arquivos Excel exportados pelo portal do investidor da B3
    """
    def __init__(self):
        self.data = pd.DataFrame()

    def read_excel_files(self, filenames: Sequence):
        self.data = pd.concat(chain([self.data], (pd.read_excel(file, index_col=0) for file in filenames)))

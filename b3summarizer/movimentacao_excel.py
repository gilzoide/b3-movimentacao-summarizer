import math
import warnings

import pandas as pd


class MovimentacaoExcel:
    """Classe que faz interface com os dados providos dos arquivos de Excel de Movimentação exportados pela B3"""

    # Nomes das colunas
    COLUMN_IN_OR_OUT = "Entrada/Saída"
    COLUMN_DATE = "Data"
    COLUMN_TYPE = "Movimentação"
    COLUMN_STOCK = "Produto"
    COLUMN_INSTITUTION = "Instituição"
    COLUMN_QUANTITY = "Quantidade"
    COLUMN_UNIT_PRICE = "Preço unitário"
    COLUMN_TOTAL_PRICE = "Valor da Operação"

    # Formato dos campos de data
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, *filenames: str):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.data = pd.concat((pd.read_excel(file, header=0) for file in filenames), copy=False)
        self.data[MovimentacaoExcel.COLUMN_DATE] = pd.to_datetime(self.data[MovimentacaoExcel.COLUMN_DATE], format=MovimentacaoExcel.DATE_FORMAT)
        self.data.sort_values(by=MovimentacaoExcel.COLUMN_DATE, ascending=True, inplace=True)

    def iterrows(self):
        for _, row in self.data.iterrows():
            yield MovimentacaoExcel.Row(row)

    class Row:
        """Classe que faz interface com cada linha dos arquivos Excel"""
        def __init__(self, row: pd.Series):
            self.row = row

        @property
        def is_credit(self) -> bool:
            return self.row.loc[MovimentacaoExcel.COLUMN_IN_OR_OUT] == 'Credito'

        @property
        def is_debit(self) -> bool:
            return self.row.loc[MovimentacaoExcel.COLUMN_IN_OR_OUT] == 'Debito'

        @property
        def date(self) -> pd.Timestamp:
            return self.row.loc[MovimentacaoExcel.COLUMN_DATE]

        @property
        def type(self) -> str:
            return self.row.loc[MovimentacaoExcel.COLUMN_TYPE]

        @property
        def stock(self) -> str:
            return self.row.loc[MovimentacaoExcel.COLUMN_STOCK].partition(' ')[0]

        @property
        def institution(self) -> str:
            return self.row.loc[MovimentacaoExcel.COLUMN_INSTITUTION]

        @property
        def quantity(self) -> int:
            return math.floor(self.row.loc[MovimentacaoExcel.COLUMN_QUANTITY])

        @property
        def unit_price(self) -> float:
            try:
                return float(self.row.loc[MovimentacaoExcel.COLUMN_UNIT_PRICE])
            except:
                return 0

        @property
        def total_price(self) -> float:
            try:
                return float(self.row.loc[MovimentacaoExcel.COLUMN_TOTAL_PRICE])
            except:
                return 0

        ## Stock Operations
        @property
        def is_buy(self) -> bool:
            return self.type == 'Transferência - Liquidação' and self.is_credit

        @property
        def is_sell(self) -> bool:
            return self.type == 'Transferência - Liquidação' and self.is_debit

        @property
        def is_transfer(self) -> bool:
            return self.type == 'Transferência' and self.is_credit

        @property
        def is_split(self) -> bool:
            return self.type == 'Desdobro'

        @property
        def is_combine(self) -> bool:
            return self.type == 'Grupamento'

        @property
        def is_bonus(self) -> bool:
            return self.type == 'Bonificação em Ativos'


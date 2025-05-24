import locale
import logging
from typing import Sequence

from movimentacao_excel import MovimentacaoExcel
from stock import StockMap


class Summarizer:
    """
    Sumarizador de negociações
    """
    class Month:
        """
        Sumarizador dos resultados de um mês
        """
        def __init__(self):
            self.result = 0

        def add_result(self, result: float):
            self.result += result

        def reset(self):
            self.result = 0


    def __init__(self, *filenames: str):
        self.data = MovimentacaoExcel(*filenames)

    def print_summarization(self, target_year: int | None):
        current_year = 0
        current_month = 0
        month_results = Summarizer.Month()
        stock_map = StockMap()

        def is_target_year(year: int):
            return target_year is None or target_year == year

        for row in self.data.iterrows():
            date = row.date

            if current_month != date.month:
                if is_target_year(current_year):
                    self.summarize_month(current_year, current_month, month_results)
                month_results.reset()
                current_month = date.month

            if current_year != date.year:
                if is_target_year(current_year):
                    self.summarize_year(current_year, stock_map)
                current_year = date.year

            if row.is_buy:
                stock_map.buy(row.stock, row.quantity, row.unit_price)
                logging.debug(f'  > ({date.date()}) COMPRA {row.stock}, {row.quantity}, {locale.currency(row.unit_price)}')
            elif row.is_sell:
                result = stock_map.sell(row.stock, row.quantity, row.unit_price)
                month_results.add_result(result)
                logging.debug(f'  > ({date.date()}) VENDA {row.stock}, {row.quantity}, {locale.currency(row.unit_price)}')
            elif row.is_transfer:
                stock_map.transfer(row.stock, row.quantity)
                logging.debug(f'  > ({date.date()}) TRANSFERÊNCIA {row.stock}, {row.quantity}')
            elif row.is_split:
                stock_map.split(row.stock, row.quantity)
                logging.debug(f'  > ({date.date()}) DESDOBRO {row.stock}, {row.quantity}')
            elif row.is_combine:
                stock_map.combine(row.stock, row.quantity)
                logging.debug(f'  > ({date.date()}) GRUPAMENTO {row.stock}, {row.quantity}')
            elif row.is_bonus:
                stock_map.buy(row.stock, row.quantity, row.unit_price)
                logging.debug(f'  > ({date.date()}) BÔNUS {row.stock}, {row.quantity}, {locale.currency(row.unit_price)}')

        if is_target_year(current_year):
            self.summarize_month(current_year, current_month, month_results)
            self.summarize_year(current_year, stock_map)

    @staticmethod
    def summarize_month(year: int, month: int, results: Month):
        if results.result == 0:
            return

        logging.info(f"[{year}-{month:02}] Resultado: {locale.currency(results.result)}")

    @staticmethod
    def summarize_year(year: int, stock_map: StockMap):
        if not stock_map:
            return

        logging.info(f"[{year}] Posição:")
        for (_, stock) in sorted(stock_map.stocks.items()):
            if stock:
                logging.info(f"  {stock}")
        logging.info('')

    @staticmethod
    def summarize(excel_filenames: Sequence, target_year: int | None = None):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        summarizer = Summarizer(*excel_filenames)
        summarizer.print_summarization(target_year=target_year)


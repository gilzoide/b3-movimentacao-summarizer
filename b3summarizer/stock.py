import locale
from typing import Any


class StockException(Exception):
    pass


class Stock:
    """
    Contador de quantidade de ações e preço médio
    """
    def __init__(self, name):
        self.name = name
        self.quantity: int = 0
        self.mean_price: float = 0

    def buy(self, quantity: int, price_per_unit: float):
        """Contabiliza a compra de ações"""
        previous_quantity = self.quantity
        previous_total_price = previous_quantity * self.mean_price
        added_total_price = quantity * price_per_unit
        self.quantity += quantity
        self.mean_price = (previous_total_price + added_total_price) / (previous_quantity + quantity)

    def sell(self, quantity: int, sell_price_per_unit: float) -> float:
        """
        Contabiliza a venda de ações

        Returns:
            Lucro ou prejuízo da operação, em relação ao preço médio de compra atual
        """
        if self.quantity < quantity:
            raise StockException(f"[{self.name}] Vendendo mais ações ({quantity}) que o possível ({self.quantity}). Talvez faltou importar algum arquivo?")
        self.quantity -= quantity
        buy_price = self.mean_price * quantity
        sell_price = sell_price_per_unit * quantity
        return sell_price - buy_price

    def split(self, quantity_added: int):
        """Desdobro de ações"""
        self.buy(quantity_added, price_per_unit=0)

    def combine(self, final_quantity: int):
        """Grupamento de ações"""
        if self.quantity < final_quantity:
            raise StockException(f"[{self.name}] Desdobrando mais ações ({final_quantity}) que o possível ({self.quantity}). Talvez faltou importar algum arquivo?")
        previous_quantity = self.quantity
        previous_total_price = previous_quantity * self.mean_price
        self.quantity = final_quantity
        self.mean_price = previous_total_price / final_quantity

    def __str__(self) -> str:
        return f"{self.name} (quantidade: {self.quantity}, preço médio: {locale.currency(self.mean_price)})"

    def __bool__(self) -> bool:
        return self.quantity > 0


class StockMap:
    """
    Coleção de ações
    """
    def __init__(self):
        self.stocks: dict[Any, Stock] = {}

    def buy(self, stock, quantity: int, price_per_unit: float):
        """Contabiliza a compra da ação de nome `stock`"""
        if stock not in self.stocks:
            self.stocks[stock] = Stock(stock)
        self.stocks[stock].buy(quantity, price_per_unit)

    def sell(self, stock, quantity: int, sell_price_per_unit: float) -> float:
        """
        Contabiliza a venda da ação de nome `stock`

        Returns:
            Lucro ou prejuízo da operação, em relação ao preço médio de compra atual
        """
        if stock not in self.stocks:
            raise StockException(f"Ação {stock} não consta no inventário")
        return self.stocks[stock].sell(quantity, sell_price_per_unit)

    def split(self, stock, quantity_added: int):
        """Desdobro de ações"""
        if stock not in self.stocks:
            raise StockException(f"Ação {stock} não consta no inventário")
        self.stocks[stock].split(quantity_added)

    def combine(self, stock, final_quantity: int):
        """Grupamento de ações"""
        if stock not in self.stocks:
            raise StockException(f"Ação {stock} não consta no inventário")
        self.stocks[stock].combine(final_quantity)

    def get_mean_price(self, stock):
        if stock not in self.stocks:
            raise StockException(f"Ação {stock} não consta no inventário")
        return self.stocks[stock].mean_price

    def __bool__(self):
        return any(bool(stock) for stock in self.stocks.values())

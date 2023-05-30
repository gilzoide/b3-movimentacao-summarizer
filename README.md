# B3 Movimentação Summarizer
Sumarizador de extratos de movimentação baixados pelo portal do investidor da B3.


## Como usar
1. Baixe os extratos de Movimentação no formato Excel de todos os anos possíveis
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Rode o script:
   ```sh
   python b3summarizer/main.py /pasta/pros/extratos/movimentacao-*.xlsx
   ```

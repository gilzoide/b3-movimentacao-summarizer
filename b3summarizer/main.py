"""
Sumarizador de extratos de negociação da B3 por ano, para ajudar no IRPF

Usage:
    b3summarizer <arquivo_excel>... [--ano=<ano>] [-v|--verbose]

Options:
    -a <ano>, --ano=<ano>    Mostra somente o resultado para o ano escolhido.
    -v, --verbose            Mostra todas as transações
"""
import logging

from docopt import docopt

from summarizer import Summarizer


def main():
    args = docopt(__doc__)
    logging.basicConfig(format='%(message)s',
                        level=logging.DEBUG if args.get('--verbose') else logging.INFO)
    target_year = int(args['--ano']) if args.get('--ano') else None
    Summarizer.summarize(args['<arquivo_excel>'], target_year=target_year)

if __name__ == '__main__':
    main()

"""
Sumarizador de extratos de negociação da B3

Usage:
    b3summarizer <arquivo_excel>...
"""

from docopt import docopt

from summarizer import summarize


def main():
    args = docopt(__doc__)
    summarize(args['<arquivo_excel>'])

if __name__ == '__main__':
    main()

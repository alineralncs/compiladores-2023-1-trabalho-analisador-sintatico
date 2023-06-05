from lexico.scanner import Scanner
from lexico.scanner import *


if __name__ == '__main__':
    file_code_font = 'exemplos.md'

    scanner = Scanner(file_code_font)
    tokens, errors = scanner.analyse()

    print("\nTokens Válidos \n")
    for token in tokens:
        print('<{}, {}>'.format(token[0], token[1]))

    # print("\nTokens Inválidos: \n")
    # for error in errors:
    #     print(errors[error])

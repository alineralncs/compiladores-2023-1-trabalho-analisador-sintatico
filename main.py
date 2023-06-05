from lexico.scanner import Scanner
from lexico.scanner import *
from sintatico.parser import Parser

# if __name__ == '__main__':
#     file_code_font = 'exemplos.md'

#     scanner = Scanner(file_code_font)
#     tokens, errors = scanner.analyse()

#     print("\nTokens Válidos \n")
#     for token in tokens:
#         print('<{}, {}>'.format(token[0], token[1]))

#     # print("\nTokens Inválidos: \n")
#     # for error in errors:
#     #     print(errors[error]
if __name__ == '__main__':
    file_code_font = 'exemplos.md'

    # Lexical analysis
    scanner = Scanner(file_code_font)
    tokens, errors = scanner.analyse()

    if errors:
        print("Lexical errors:")
        for error in errors:
            print(error)
    else:
        print("Tokens:")
        for token in tokens:
            print(token)

    # Syntactic analysis
    parser = Parser(tokens)
    try:
        parser.parseToken()
        parser.logicAnd()
    except SyntaxError as e:
        print("Syntax error:", str(e))

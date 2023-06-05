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
#     #     print(errors[error])
if __name__ == '__main__':
    file_code_font = 'exemplos.md'

    scanner = Scanner(file_code_font)
    tokens, errors = scanner.analyse()

    if errors:
        for error in errors:
            print(f"Erro léxico na linha {error[0]}: {error[1]}")
        exit(1)

    parser = Parser(tokens)
    try:
        parse_tree = parser.parse()
        print("Análise sintática concluída com sucesso!")
    except SyntaxError as e:
        print(f"Erro sintático: {str(e)}")

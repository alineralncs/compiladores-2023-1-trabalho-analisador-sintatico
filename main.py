from lexico.scanner import Scanner
from lexico.scanner import *
from sintatico.parser import *
if __name__ == '__main__':
    file_code_font = 'exemplos.md'

    # Lexical analysis
    scanner = Scanner(file_code_font)
    tokens, errors = scanner.analyse()

    if errors:
        print("Lexical errors:")
        for error in errors:
            print(error)

    # Syntactic analysis
    parser = Parser(tokens)
    print("oi")
    #parser.parseTokens()
    parser.program()
    print("deu certo")
    # try:
    #     parser.parseTokens()
    #     print("Análise sintática concluída sem erros.")
    # except SyntaxError as e:
    #     print("Syntax error:", str(e))

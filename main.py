from lexico.scanner import Scanner
from lexico.scanner import *
from sintatico.parser import *
if __name__        == '__main__':
   #file_code_font  = 'ex_1.md'
   #file_code_font  = 'ex_2.md'
    file_code_font  = 'ex_3.md'
   #file_code_font  = 'ex_4.md'
   #file_code_font  = 'ex_5.md'
   #file_code_font  = 'ex_6.md'

    # Lexical analysis
    scanner = Scanner(file_code_font)
    tokens, errors = scanner.analyse()

    if errors:
        print("Lexical errors:")
        for error in errors:
            print(error)

    # Syntactic analysis
    parser = Parser(tokens)
    
    try:
        parser.program()
        print('Análise Sintática feita com sucesso! \n ')
    except SyntaxError as e:
        print("\n ============ \n Syntax error: \n ", str(e))


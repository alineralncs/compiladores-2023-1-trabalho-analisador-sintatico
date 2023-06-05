class Parser:
    def _init_(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = None

    def parse(self):
        self.current_token = self.get_next_token()
        self.program()

        if self.current_token is not None:
            raise SyntaxError("Unexpected token: " + self.current_token[1])

    def program(self):
        while self.current_token is not None:
            self.declaration()

    def declaration(self):
        if self.current_token[0] == 'keyword' and self.current_token[1] == 'fun':
            self.consume('keyword', 'fun')
            self.function()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
            self.consume('keyword', 'var')
            self.consume('identifier')
            if self.current_token[0] == 'operator' and self.current_token[1] == '=':
                self.consume('operator', '=')
                self.expression()
            self.consume('delimiter', ';')
        else:
            self.statement()

    def function(self):
        self.consume('identifier')
        self.consume('delimiter', '(')
        self.parameters()
        self.consume('delimiter', ')')
        self.block()

    def parameters(self):
        if self.current_token[0] == 'identifier':
            self.consume('identifier')
            while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
                self.consume('delimiter', ',')
                self.consume('identifier')

    def statement(self):
        if self.current_token[0] == 'keyword' and self.current_token[1] == 'for':
            self.consume('keyword', 'for')
            self.consume('delimiter', '(')
            if self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
                self.varDecl()
            elif self.current_token[0] == 'identifier':
                self.exprStmt()
            else:
                self.consume('delimiter', ';')
            if self.current_token[0] != 'delimiter' or self.current_token[1] != ')':
                self.expression()
            self.consume('delimiter', ';')
            if self.current_token[0] != 'delimiter' or self.current_token[1] != ')':
                self.expression()
            self.consume('delimiter', ')')
            self.statement()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'if':
            self.consume('keyword', 'if')
            self.consume('delimiter', '(')
            self.expression()
            self.consume('delimiter', ')')
            self.statement()
            if self.current_token[0] == 'keyword' and self.current_token[1] == 'else':
                self.consume('keyword', 'else')
                self.statement()
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'print':
            self.consume('keyword', 'print')
            self.expression()
            self.consume('delimiter', ';')
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'return':
            self.consume('keyword', 'return')
            if self.current_token[0] != 'delimiter' or self.current_token[1] != ';':
                self.expression()
            self.consume('delimiter', ';')
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'while':
            self.consume('keyword', 'while')
            self.consume('delimiter', '(')
            self.expression()
            self.consume('delimiter', ')')
            self.statement()
        elif self.current_token[0] == 'delimiter' and self.current_token[1] == '{':
            self.block()
        else:
            self.exprStmt()

    def exprStmt(self):
        self.expression()
        self.consume('delimiter', ';')

    def varDecl(self):
        self.consume('keyword', 'var')
        self.consume('identifier')
        if self.current_token[0] == 'operator' and self.current_token[1] == '=':
            self.consume('operator', '=')
            self.expression()
        self.consume('delimiter', ';')

    def expression(self):
        self.assignment()

    def assignment(self):
        if self.current_token[0] == 'identifier':
            self.consume('identifier')
            if self.current_token[0] == 'operator' and self.current_token[1] == '=':
                self.consume('operator', '=')
                self.assignment()
        else:
            self.logic_or()

    def logic_or(self):
        self.logic_and()
        while self.current_token[0] == 'keyword' and self.current_token[1] == 'or':
            self.consume('keyword', 'or')
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.current_token[0] == 'keyword' and self.current_token[1] == 'and':
            self.consume('keyword', 'and')
            self.equality()

    def equality(self):
        self.comparison()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '!=' or self.current_token[1] == '=='):
            self.consume('operator')

    def comparison(self):
        self.term()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '>' or self.current_token[1] == '>=' or
                                                       self.current_token[1] == '<' or self.current_token[1] == '<='):
            self.consume('operator')
            self.term()

    def term(self):
        self.factor()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '-' or self.current_token[1] == '+'):
            self.consume('operator')
            self.factor()

    def factor(self):
        self.unary()
        while self.current_token[0] == 'operator' and (self.current_token[1] == '/' or self.current_token[1] == '*'):
            self.consume('operator')
            self.unary()

    def unary(self):
        if self.current_token[0] == 'operator' and (self.current_token[1] == '!' or self.current_token[1] == '-'):
            self.consume('operator')
            self.unary()
        else:
            self.call()

    def call(self):
        self.primary()
        if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
            self.consume('delimiter', '(')
            if self.current_token[0] != 'delimiter' or self.current_token[1] != ')':
                self.arguments()
            self.consume('delimiter', ')')
        elif self.current_token[0] == 'operator' and self.current_token[1] == '.':
            self.consume('operator', '.')
            self.consume('identifier')

    def primary(self):
        if self.current_token[0] == 'keyword' and (self.current_token[1] == 'true' or self.current_token[1] == 'false' or
                                                   self.current_token[1] == 'nil' or self.current_token[1] == 'this'):
            self.consume('keyword')
        elif self.current_token[0] == 'number' or self.current_token[0] == 'string':
            self.consume(self.current_token[0])
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        elif self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
            self.consume('delimiter', '(')
            self.expression()
            self.consume('delimiter', ')')
        elif self.current_token[0] == 'keyword' and self.current_token[1] == 'super':
            self.consume('keyword', 'super')
            self.consume('operator', '.')
            self.consume('identifier')

    def arguments(self):
        self.expression()
        while self.current_token[0] == 'delimiter' and self.current_token[1] == ',':
            self.consume('delimiter', ',')
            self.expression()

    def consume(self, token_type, expected_value=None):
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")

        if self.current_token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]}")

        if expected_value is not None and self.current_token[1] != expected_value:
            raise SyntaxError(f"Expected {expected_value}, got {self.current_token[1]}")

        self.current_token = self.get_next_token()

    def get_next_token(self):
        if self.token_index < len(self.tokens):
            next_token = self.tokens[self.token_index]
            self.token_index += 1
            return next_token
        else:
            return None

from lexico.scanner import *
"""
passar uma lista de tokens
validar os tokens de acordo com uma gramática
retornar os erros obtidos (lista de erros) -> o que é retornado do parser
Quais são os erros encontrados pelo analisador sintático: 
- ordem incorreta de tokens
- falta de símbolos ou símbolos não especificados pela gramática
- abertura e fechado de blocos incorretos (delimitadores incorretos)
"""

#análise sintática descendete: a árvore é formada da raiz às folhas
#tipo    de busca            : profundidade
#a lista de tokens é lida da esquerda para a direita

class Parser: 
  def  __init__(self, list_tokens): 
    self.list_tokens = list_tokens #lista de tokens validados pelo analisador léxico
    self.token_index = 0 #primeiro índice da pilha
    self.current_token = None #token atual
  #ler token por token : 
  def parseToken(self): 
    self.current_token = self.get_next_token()

  def get_next_token(self)               : 
    if self.token_index < len(self.list_tokens): 
      next_token = self.list_tokens[self.token_index]
      self.token_index += 1
      return next_token
    else:
      return None
    



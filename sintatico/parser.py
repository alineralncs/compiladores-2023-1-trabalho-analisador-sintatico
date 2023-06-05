from lexico.scanner import *

class Parser: 
  def  __init__(self, list_tokens): 
    self.list_tokens = list_tokens #lista de tokens validados pelo analisador léxico
    self.token_index = 0 #primeiro índice da pilha
    self.current_token = None #token atual
    self.keyword = False
    self.operator = False
    self.delimiter = False
    self.number = False
    self.string = False
    self.super = False
  #ler token por token : 
  def parseToken(self): 
    self.current_token = self.get_next_token()

  def get_next_token(self): 
    if self.token_index < len(self.list_tokens): 
      next_token = self.list_tokens[self.token_index]
      self.token_index += 1
      return next_token
    else:
      return None
  
  def update_token_info(self):
        if self.current_token is not None:
            self.keyword = self.current_token[0] == 'keyword'
            self.operator = self.current_token[0] == 'operator'
            self.delimiter = self.current_token[0] == 'delimiter'
            self.number = self.current_token[0] == 'number'
            self.string =  self.current_token[0] == 'string'
            self.super = self.current_token[1] == 'super'
        else:
            self.keyword = False
            self.operator = False
            self.delimiter = False
            self.number = False
            self.string = False
            self.super = False

  def logicAnd(self):
        self.equality()
        while self.keyword and self.current_token[1] == 'and':
            self.consume('keyword', 'and')
            self.equality()

  def equality(self):
        self.comparison()
        while self.operator and (self.current_token[1] == '!=' or self.current_token[1] == '=='):
            self.consume('operator')
            self.comparison()

  def comparison(self):
        self.term()
        while self.operator and (self.current_token[1] == '>' or self.current_token[1] == '>=' or
                                self.current_token[1] == '<' or self.current_token[1] == '<='):
            self.consume('operator')
            self.term()

  def term(self):
        self.factor()
        while self.operator and (self.current_token[1] == '-' or self.current_token[1] == '+'): 
            self.consume('operator')
            self.factor()

  def factor(self):
        self.unary()
        while self.operator and (self.current_token[1] == '/' or self.current_token[1] == '*'):
            self.consume('operator')
            self.unary()

  def unary(self):
        if self.operator and (self.current_token[1] == '!' or self.current_token[1] == '-'):
            self.consume('operator')
            self.unary()
        else:
            self.call()

  def call(self):
        self.primary()

        while self.operator and (self.current_token[1] == '(' or self.current_token[1] == '.'):
            if self.current_token[1] == '(':
                self.consume('delimiter', '(')
                if self.delimiter or self.current_token[1] != ')':
                    self.arguments()
                self.consume('delimiter', ')')
            elif self.current_token[1] == '.':
                self.consume('operator', '.')
                self.consume('identifier')

  def primary(self):
        if self.keyword and (self.current_token[1] == 'true' or self.current_token[1] == 'false' or
                             self.current_token[1] == 'nil' or self.current_token[1] == 'this'):
            self.consume('keyword')
        elif self.number or self.string:
            self.consume(self.current_token[0])
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        elif self.delimiter and self.current_token[1] == '(':
            self.consume('delimiter', '(')
           # self.expression()
            self.consume('delimiter', ')')
        elif self.keyword and self.super:
            self.consume('keyword', 'super')
            self.consume('operator', '.')
            self.consume('identifier')

  def arguments(self):
        self.expression()
        while self.delimiter and self.current_token[1] == ',':
            self.consume('delimiter', ',')
            self.expression()
 
  def consume(self, token_type, expected_value=None):
      if self.current_token is None:
          raise SyntaxError("Unexpected end of input")

      if self.current_token[0] != token_type:
          raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]} at {self.current_token[1]}")

      if expected_value is not None and self.current_token[1] != expected_value:
          raise SyntaxError(f"Expected {expected_value}, got {self.current_token[0]} at {self.current_token[1]}")

      self.current_token = self.get_next_token()

from scanner import *
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

    #verificar se a pilha ainda tem token não analisado
    # if self.current_token is not None: 
    #   raise SyntaxError("Unexpected token: ", self.current_token[1])
  def get_next_token(self)               : 
    if self.token_index < len(self.list_tokens): 
      next_token = self.list_tokens[self.token_index]
      self.token_index += 1
      return next_token
    else:
      return None
  
  def program(self): 
    while self.current_token is not None: 
      self.declaration()

  def declaration(self): 
    #se for função: 
    if(self.current_token[0] == 'keyword' and self.current_token[1] == 'fun'):
      self.funDecl() #var a = 1;
    #se for variável
    elif(self.current_token[0] == 'keyword' and self.current_token[1] == 'var'): 
      self.varDecl()
    else: 
      #se for statement
      self.statement()

  def funDecl(self): 
    if self.consume('keyword', 'fun'):
      self.function()
  def function(self): 
    pass

  def  varDecl(self): 
    self.consume('keyword', 'var')
    self.consume('identifier')
    if self.current_token[0] == 'operator' and self.current_token[1] == '=':
      self.consume('operator', '=')
    self.expression() #depois do sinal = podem vir muitas coisas
    self.consume('delimeter', ';')
          
  def statement(self)                      : 
    if  self.current_token[0] == 'identifier': 
      self.consume('identifier')
      self.exprStmt()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'for':
      self.forStmt()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'if':
      self.ifStmt()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'print':
      self.printStmt()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'return':
      self.returnStmt()
    elif self.current_token[0] == 'keyword' and self.current_token[1] == 'while':
      self.whileStmt()
    elif self.current_token[0] == 'delimiter' and self.current_token[1] == '{':
      self.block()

  def forStmt(self): 
    self.consume('keyword', 'for')
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      if self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
        self.varDecl()
      elif self.current_token[0] == 'identifier':
        self.exprStmt()
      else: 
        self.consume('delimiter', ';') #for(var i = 88; u jnjndjn;)
      if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
        self.expression()
        self.consume('delimiter', ';')
        if self.current_token[0] != 'delimiter' and self.current_token[1] != ')':
          self.expression()
        self.consume('delimiter', ')')
      self.statement()

  def ifStmt(self): 
    self.consume('keyword', 'if')
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      self.expression()
      self.consume('delimiter', ')')
      self.statement()
      #se ele não é um if, ele é um else
      if self.current_token[0] == 'keyword' and self.current_token[1] == 'else':
        self.consume('keyword', 'else')
        self.statement()

  def printStmt(self): 
    self.consume('keyword', 'print')
    self.expression()
    self.consume('delimiter', ';')
  
  def returnStmt(self): 
    self.consume('keyword', 'return')
    if self.current_token[0] != 'delimiter' or self.current_token[1] != ';':
      self.expression()
    self.consume('delimiter', ';')

  def whileStmt(self): 
    self.consume('keyword', 'while')
    if self.current_token[0] == 'delimiter' and self.current_token[1] == '(':
      self.consume('delimiter', '(')
      self.expression()
      self.consume('delimiter', ')')
      self.statement()
  def block(self): 
    self.consume('delimiter', '{')
    while self.current_token[0] != 'delimiter' and self.current_token[1] != '}':
      self.declaration()
    self.consume('delimiter', '}')

  def exprStmt(self): 
    self.expression() #depois precisa do ;
    self.consume('delimiter', ';')

  def expression(self): 
    self.assignment()

  def assignment(self): #var a = 1;
    if self.current_token[0] == 'identifier':
      self.consume('identifier')
      if (self.current_token[0] == 'operator' and self.current_token[1] == '='): 
        self.consume('operator', '=')
        self.assignment()
    else: 
      self.logic_or() #a and a ou a or a 
  def logic_or(self): 
    self.logic_and()
    while self.current_token[0] == 'keyword' and self.current_token[1] == 'or':
      self.consume('keyword', 'or')
      self.logic_and()

  def consume(self, token_type, expected_value=None): 
    if self.current_token is None: 
        raise SyntaxError("Unexpected end of input")

    if self.current_token[0] != token_type:
        raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]} at {self.current_token[1]}")

    if expected_value is not None and self.current_token[1] != expected_value:
        raise SyntaxError(f"Expected {expected_value}, got {self.current_token[0]} at {self.current_token[1]}")
    self.current_token = self.get_next_token()

    
    

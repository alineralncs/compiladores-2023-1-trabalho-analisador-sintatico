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
  
  def program(self)                 : 
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
    pass
  def varDecl(self): 
    pass
  def statement(self): 
    pass

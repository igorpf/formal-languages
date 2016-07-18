# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 08:45:35 2015
Grupo -> Christian Schmitz
    -> Igor Ferreira
    -> Augusto Boranga
    ->Mário Júnior
@author: igor
"""

class Celula():
    def __init__(self, d):
        self.variaveis = d
    variaveis = dict()
    def addVariaveis(self, variaveis):
        for variavel in variaveis.keys():
            #variável não foi gerada na celula ainda, adiciona sem problemas
            if variavel not in self.variaveis.keys():
                self.variaveis[variavel]=variaveis[variavel]
            else:
            #adiciona caminhamento na lista
                self.variaveis[variavel].append(variaveis[variavel])
    def getVariaveis(self):
        return self.variaveis


nome = 'formais.txt'
arq = open(nome, 'r')

terminais = arq.readline()#lixo
terminais = str(arq.readline()) #terminais
terminais = terminais.replace('{ ','').replace(' }','')
terminais = terminais.split('#')
terminais = terminais[0]
terminais = terminais.split(',')
for t in terminais:
    t=t.replace(' ','')
#aqui termina o tratamento dos terminais    
variaveis=arq.readline()#lixos
variaveis=str(arq.readline())#variaveis
variaveis= variaveis.replace('{ ','').replace(' }','')
variaveis = variaveis.split('#')
variaveis = variaveis[0]
variaveis = variaveis.split(',')
for t in variaveis:
    t=t.replace(' ','')
#aqui termina o tratamento de variaveis
inicial=arq.readline()#lixos
inicial=str(arq.readline())#variaveis
inicial= inicial.replace('{ ','').replace(' }','').replace('\t', '')
inicial = inicial.split('#')
inicial= inicial[0]
#aqui termina o tratamento do inicial
regras = dict()
buf = arq.readline()#lixo
buf = str(arq.readline())
while(buf!=""):
    buf= buf.replace(' ','').replace('{','').replace('}','')
    buf = buf.split('#')
    buf= buf[0]
    buf= buf.split('>')    
    key=buf[0]    
    if len(buf)>1:
        values = buf[1].replace('\t','').replace(';','').replace('\n','').split(',')
        if regras.has_key(key):
            regras[key].append(values)
        else:
            regras[key]=list()
            regras[key].append(values)
    buf = str(arq.readline())
#print regras
gramatica = [variaveis, regras, inicial]
arq.close()

#retorna todas as variaveis que produzem o terminal
def lexicalLookup(terminal, regras):
    cjto=dict()
    for var in regras.keys():
        if [terminal] in regras[var]:
            cjto[var]=["("+terminal+")"]
    return cjto
def aux(regras,b,c,r,s,k, matriz):    
        for var in regras.keys():
            if [b,c] in regras[var]:
                for caminhoB in matriz[r][k].getVariaveis()[b]:
                    for caminhoC in matriz[r+k+1][s-k-1].getVariaveis()[c]:                        
                        temp = "-"+str(r+(1))+str((r+k+1))+str(caminhoB)
                        temp2 = "-"+str(r+k+2)+str((r+s+1))+str(caminhoC)
                        completo = ("("+b+temp+","+c+temp2+")").replace("[]","").replace('\\','')
                        matriz[r][s].addVariaveis(dict(zip([var],[[completo]])))
def CYK(regras,frase):
    
    frase = frase.split(' ') #transforma a frase em uma lista de strings    
    matriz = [[Celula(dict()) for i in range(len(frase))] for i in range(len(frase))]
    for r in range(len(frase)):
        matriz[r][0].addVariaveis((lexicalLookup(frase[r],regras)))        
        print matriz[r][0].getVariaveis(), r
    for s in range(1,len(frase)):
        for r in range(len(frase)-s):
            for k in range(s):
                for b in matriz[r][k].getVariaveis().keys():
                    for c in matriz[r+k+1][s-k-1].getVariaveis().keys():
 
                       aux(regras,b,c,r,s,k, matriz)
                        

    for s in range(1,len(frase)):
       for r in range(len(frase)-s):
            print r+1,r+s+1,": ",matriz[r][s].getVariaveis()#,len(matriz[r][s].getVariaveis())
    if inicial in matriz[0][len(frase)-1].getVariaveis().keys():
        print "frase aceita!\n",matriz[0][len(frase)-1].getVariaveis()
    else:
        print "frase rejeitada!"

#CYK(regras,"a cat runs")
CYK(regras,"the cat cat cat runs")

 
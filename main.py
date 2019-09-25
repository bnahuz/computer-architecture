#A memória premcipal do IAS possui 
# 1024 palavras de 40 bits

#Cada palavra está associada a um endereço
#distemto, um número que varia de 0 até 1023.

from bitstring import BitArray, BitStream


class IAS:

    #Funções Essenciais
    def read(self, endereco):
        b_endereco = BitStream('0b' + endereco)
        return self.memoria[b_endereco.int]

    def input(self, endereco, valor):
        b_endereco = BitStream('0b' + endereco)
        self.memoria[b_endereco.int] = BitStream(int=valor, length=40)

    def instrucao(self, opcode, endereco):
        b_opcode = BitStream('0b' + opcode)
        b_endereco = BitStream('0b' + endereco)
        self.ops[b_opcode.read('bin:8')](b_endereco.int)   


    #TRANSFERÊNCA DE DADOS
    def loadToAC(self, registro):
        self.AC = self.MQ

    def loadToMQ(self, registro):
        self.MQ = BitStream(int=self.memoria[registro].int,length=40)

    def store(self, registro):
        self.memoria[registro] = self.AC

    def load(self, registro):
        self.AC = self.memoria[registro]

    def loadNeg(self, registro):
        self.AC = self.memoria[-registro] 

    def loadAbs(self, registro):
        aux = self.memoria[registro] >> 39
        aux ^ self.memoria[registro]
        self.AC = (aux^n)-aux
    
    def loadNegAbs(self, registro):
        aux = self.memoria[registro] >> 39
        aux ^ self.memoria[registro]
        self.AC = ((aux^n)-aux) 

    #DESVIO INCONDICIONAL    
    def jumpL(self, registro):
        ops[self.memoria[registro][0:19]](registro)
    
    def jumpR(self, registro):
        ops[self.memoria[registro][20:39]](registro)

    #DESVIO CONDICIONAL
    def condJumpL(self, registro):
        if(self.AC[39] == 1):
            ops[self.memoria[registro][0:7]](self.memoria[registro][8:19].int)
    
    def condJumpR(self, registro):
        if(self.AC[39] == 1):
            ops[self.memoria[registro][20:27]](self.memoria[registro][28:40].int)

    #ARITIMÉTICA
    def add(self, registro):
        self.AC = BitStream(int=self.AC.int + self.memoria[registro].int, length=40)    

    def addAbs(self, registro):
        self.AC = BitStream(int=self.AC.int + abs(self.memoria[registro].int), length=40)

    def sub(self, registro):
        self.AC = BitStream(int=self.AC.int - self.memoria[registro].int, length=40)    

    def subRem(self, registro):
        self.AC = BitStream(int=self.AC.int - abs(self.memoria[registro].int), length=40)

    def mul(self, registro):
        res = BitStream(int=self.MQ.int * self.memoria[registro].int, length=40)
        self.AC = BitStream(int=res[40:80].int, length=40)
        self.MQ = BitStream(int=res[0:39].int, length=40)

    def div(self, registro):
        quo = BitStream(int=(self.AC.int / self.memoria[registro].int), length=40)
        rem = BitStream(int=self.AC.int % self.memoria[registro].int, length=40)
        self.AC = quo
        self.MQ = rem

    def ls(self, registro):
        self.AC <<= 1      

    def rs(self, registro):
        self.AC >>= 1

    #MODIFICAÇÃO DE ENDEREÇO
    def storL(self, registro):
        self.memoria[registro][20:39] = self.AC[0:19]
    
    def storR(self, registro):
        self.memoria[registro][0:19] = self.AC[0:19]
      
    def __init__(self):
        self.ops = {
        #TRANSFERÊNCA DE DADOS
        '00001010': self.loadToAC, #LOAD MQ Transfere o conteúdo do registro MQ para o AC
        '00001001': self.loadToMQ, #LOAD MQ,M(X) Transfere o contéudo do local de memória X para MQ
        '00100001': self.store, #STOR M(X) Transfere o conteúdo de AC para o local de memória X       
        '00000001': self.load, #LOAD M(X) Transfere M(X) para o AC
        '00000010': self.loadNeg,  #LOAD -M(X) Transfere -M(X) para o AC
        '00000011': self.loadAbs, #LOAD |M(X)| Transfere o valor absoluto de M(X) para o AC
        '00000100': self.loadNegAbs, #LOAD -|M(X)| Transfere -|M(X)| para o acumulador
        #DESVIO INCONDICIONAL
        '00001101': self.jumpL, #JUMP M(X,0:19) Apanha a próxima instrução da metade esquerda de M(X)
        '00001110': self.jumpR, #JUMP M(X,20:39) Apanha a próxima instrução da metade direita de M(X)
        #DESVIO CONDICIONAL
        '00001111': self.condJumpL, #JUMP+M(X,0:19) Se o número no AC for não negativo, apanha a próxima instrução da metade esquerda de M(X)
        '00010000': self.condJumpR, #JUMP+M(X,20:39) Se o número no AC for não negativo, apanha a próxima instrução da metade direita de M(X)       
        #ARITIMÉTICA
        '00000101': self.add, #ADD M(X) Soma M(X) com AC; coloca o resultado em AC
        '00000111': self.addAbs, #ADD |M(X)| Soma |M(X)| com AC; coloca o resultado em AC
        '00000110': self.sub, #SUB M(X) Subitrai M(X) de AC; coloca o resultado em AC
        '00001000': self.subRem, #SUB |M(X)| Subitrai |M(X) de AC; coloca o resultado em AC
        '00001011': self.mul, #MUL M(X) Multiplica M(X) por M(Q); coloca os bits mais significativos do resultado em AC; coloca os bits menos significtivos em M(Q)
        '00001100': self.div, #DIV M(X) Divide AC por M(X); coloca cociente em MQ e o resto em AC        
        '00010100': self.ls, #LSH Multiplica o AC por 2; ou seja, desloca à esquerda uma posição de bit
        '00010101': self.rs, #RSH Divide o AC por 2; ou seja, desloca uma posição à direita
        #MODIFICAÇÃO DE ENDEREÇO
        '00010010': self.storL, #STOR M(X,8:19) Substitui campo de endereço da esquerda em M(X) por 12 bits mais aà direita de AC
        '00010011': self.storR, #STOR M(X,28:39) Substitui campo de endereço da direita em M(X) por 12 bits mais aà direita de AC
        }       
        self.AC = BitStream(int=0, length=40)
        self.MQ = BitStream(int=0, length=40)
        self.memoria = [] 

        for i in range(1024):
            self.memoria.append(BitStream(int=0, length=40))




'''
#Prefixo 0x para hexadecimal e 0b para bemário
#Em binário o primeiro 0 depois do b 

s = BitArray('0x000001b3, uemt:12=352, uemt:12=288')
premt(s)'''
from main import IAS

arquivo = open('progama.txt', 'r')
palavras = []
for linha in arquivo:
    lista_leitura = []
    binarios = linha.split(' ')
    for i in range(4):
        lista_leitura.append(binarios[i])
    palavras.append(lista_leitura)
arquivo.close()

#print(palavras)

ias = IAS()
PC = 0

for instrucao in palavras:
    PC += 1
    print('PC: {}'.format(PC))
    if instrucao[0] == '00000000':
        print("Fim do Progama")
        break
    else:
        print('Esquerda')
        print('Opcode: {}'.format(instrucao[0]))
        print('Endereço: {}'.format(instrucao[1]))
        ias.instrucao(instrucao[0], instrucao[1])
        print('Conteudo do AC: {}'.format(ias.AC.bin))
        print('Conteudo do MQ: {}'.format(ias.MQ.bin))
        print('----------------------')
    PC += 1
    print('PC: {}'.format(PC))
    if instrucao[2] == '00000000':
        print("Fim do Progama")
        break
    else:
        print('Direita')
        print('Opcode: {}'.format(instrucao[2]))
        print('Endereço: {}'.format(instrucao[3]))
        ias.instrucao(instrucao[2], instrucao[3])
        print('Conteudo do AC: {}'.format(ias.AC.bin))
        print('Conteudo do MQ: {}'.format(ias.MQ.bin))
        print('----------------------')
        
        

'''
for instrucao in palavras:
    print(instrucao[0])
    print(instrucao[1])
    ias.instrucao(instrucao[0], instrucao[1])
    print('-----------')
    print(instrucao[2])
    print(instrucao[3])
    ias.instrucao(instrucao[2], instrucao[3])
    print('-----------')
    #print(ias.AC)


adicionar = [['00000001','000000000010'],['00000101','000000000011'],['00100001','000000000100']]
multiplicar = [['00001001','000000000010'],['00001011','000000000011'],['00100001','000000000101']]
dividir = [['00000001','000000000010'],['00001100','000000000011'],['00100001','000000000101'],['00001010','000000000000'],['00100001','000000000110']]





ias.input('000000000011', 1)
ias.input('000000000010', 2)

for instrucao in adicionar:
    ias.instrucao(instrucao[0], instrucao[1])

#Resultado da soma
print(ias.read('000000000100'))
print('Ta funcionando esse bagulho?')

for instrucao in multiplicar:
    ias.instrucao(instrucao[0], instrucao[1])

#Resultado da multiplicação
print(ias.read('000000000101'))

for instrucao in dividir:
    ias.instrucao(instrucao[0], instrucao[1])

print(ias.read('000000000101')) # Ler o cociente
print(ias.read('000000000111')) # Ler o resto'''
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:02:14 2024

@author: miguel
"""
import math
import random
import numpy as np

def func(x, y):
    z = 15 + x * math.cos(2 * math.pi * x) + y * math.cos(14 * math.pi * y)
    return z

def gerarelementos(quantidade, lim_min, lim_max):
    elementos = [random.uniform(lim_min, lim_max) for _ in range(quantidade)]
    return elementos

def gerarElementosBinarios(decimal_listX, decimal_listY):
    binar = []
    for i in range(len(decimal_listX)):
        int_x = int(abs(decimal_listX[i] * 1023 / 12.1))  # Ajustar a escala para 10 bits
        int_y = int(abs(decimal_listY[i] * 1023 / 5.8))   # Ajustar a escala para 10 bits
        
        binario_com_zeros_x = bin(int_x)[2:].zfill(10)
        binario_com_zeros_y = bin(int_y)[2:].zfill(10)
        
        binarioxy = binario_com_zeros_x + binario_com_zeros_y
        binar.append(binarioxy)
        
    return binar

def gerarImagem(decimal_list_x, decimal_list_y):
    imagem = []
    for i in range(len(decimal_list_x)):
        z = func(decimal_list_x[i], decimal_list_y[i])
        imagem.append(z)
    return imagem

def gerarProbabilidades(imagemFuncao):
    aptidoes = sum(imagemFuncao)
    probrolet = [(imagemFuncao[i] / aptidoes) for i in range(len(imagemFuncao))]
    return probrolet

def separarVinteMelhores(probabRolet, popBin):
    melhores = []
    for _ in range(20):
        maiorprob = max(probabRolet)
        indice = probabRolet.index(maiorprob)
        probabRolet[indice] = 0
        melhores.append(popBin[indice])
    return melhores

def sortearCasais():
    casais = np.zeros((10, 2), dtype=int)
    numeros_sorteados = set()
    for i in range(10):
        for j in range(2):
            aleatorio = random.randint(0, 19)
            while aleatorio in numeros_sorteados:
                aleatorio = random.randint(0, 19)
            casais[i][j] = aleatorio
            numeros_sorteados.add(aleatorio)
    return casais

def gerarPontoDeCorte(quant):
    if quant == 1:
        pc = random.uniform(0.5, 0.95)
    elif quant == 2:
        pc = [random.uniform(0.1, 0.45), random.uniform(0.5, 0.95)]
    return pc

def recombinar(pontoCorte, melhores):
    filhos = []
    pai1 = melhores[0]
    pai2 = melhores[1]
    pc1 = int(pontoCorte[0] * len(pai1))
    pc2 = int(pontoCorte[1] * len(pai1))
    filho1 = pai1[:pc1] + pai2[pc1:pc2] + pai1[pc2:]
    filho2 = pai2[:pc1] + pai1[pc1:pc2] + pai2[pc2:]
    filhos.extend([filho1, filho2])
    return filhos

def efetuarMutacao(filhos):
    mutacao = 0.01
    filhosmutados = []
    for filho in filhos:
        novo_filho = ''.join(['1' if (bit == '0' and random.uniform(0, 1) < mutacao) else '0' if (bit == '1' and random.uniform(0, 1) < mutacao) else bit for bit in filho])
        filhosmutados.append(novo_filho)
    return filhosmutados

def novaPopulação(filhos):
    x = gerarelementos(48, -3.1, 12.1)
    y = gerarelementos(48, 4.1, 5.8)
    binar = gerarElementosBinarios(x, y)
    novapop = filhos + binar
    return novapop

def novosValoresDecimais(binar):
    decimal = np.zeros((len(binar), 2))
    for i in range(len(binar)):
        x = binar[i][:10]
        y = binar[i][10:]
        valorx = int(x, 2) * 12.1 / 1023  # Ajustar a escala de volta para os valores originais
        valory = int(y, 2) * 5.8 / 1023   # Ajustar a escala de volta para os valores originais
        decimal[i] = [valorx, valory]
    return decimal

def torneio(probab_roleta, pop_bin):
    participantes = random.sample(range(len(probab_roleta)), 20)
    participantes_prob = [probab_roleta[i] for i in participantes]
    melhores = sorted(participantes, key=lambda x: probab_roleta[x], reverse=True)[:2]
    return [pop_bin[melhores[0]], pop_bin[melhores[1]]]

def elitismo():
    return 0

def algoritmo_genetico():
    geracao = 0
    convergencia = 0
    limiteconverg = 100
    maximoglobal = -float('inf')
    x = gerarelementos(50, -3.1, 12.1)
    y = gerarelementos(50, 4.1, 5.8)
    
    while geracao < 10000 and convergencia < limiteconverg:
        popBin = gerarElementosBinarios(x, y)
        imagemFuncao = gerarImagem(x, y)
        probabRolet = gerarProbabilidades(imagemFuncao)
        sMelhores = torneio(probabRolet, popBin)
        pontoCorte = gerarPontoDeCorte(2)
        s_filhos = recombinar(pontoCorte, sMelhores)
        s_filhos = efetuarMutacao(s_filhos)
        popBin = novaPopulação(s_filhos)
        popDec = novosValoresDecimais(popBin)
        
        listax = [ind[0] for ind in popDec]
        listay = [ind[1] for ind in popDec]
        
        maximo = max(gerarImagem(listax, listay))
        if maximo > maximoglobal:
            maximoglobal = maximo
            convergencia = 0
        else:
            convergencia += 1
        
        print(f"Geração {geracao}: Melhor valor {maximoglobal}")
        geracao += 1

algoritmo_genetico()

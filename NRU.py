import random

matriz_swap = []
matriz_ram = []

for i in range(100):
    linha = []
    linha.append(i)
    linha.append(i + 1)
    linha.append(random.randint(1, 50))
    linha.append(0)
    linha.append(0)
    linha.append(random.randint(100, 9999))
    matriz_swap.append(linha)

paginas_usadas = []
for i in range(10):
    while True:
        n = random.randint(0, 99)
        if n not in paginas_usadas:
            paginas_usadas.append(n)
            matriz_ram.append(matriz_swap[n][:])
            break

def mostrar_matrizes():
    print("\nMATRIZ RAM:")
    print("   N    I    D    R    M    T")
    print("-" * 35)
    for linha in matriz_ram:
        print(" ".join(f"{x:4}" for x in linha))
    
    print("\nMATRIZ SWAP:")
    print("   N    I    D    R    M    T")
    print("-" * 35)
    for i in range(0, 100, 10):
        print(" ".join(f"{x:4}" for x in matriz_swap[i]))
    print("...")

# Algoritmo NRU
def executar_nru():
    page_faults = 0
    instrucoes = 0
    
    while instrucoes < 1000:
        instrucao = random.randint(1, 100)
        
        achou = False
        for i in range(10):
            if matriz_ram[i][1] == instrucao:
                achou = True
                matriz_ram[i][3] = 1
                
                if random.randint(0, 1) == 1:
                    matriz_ram[i][2] += 1
                    matriz_ram[i][4] = 1
                break
        
        if not achou:
            page_faults += 1
            
            classes = [[], [], [], []]
            for i in range(10):
                r = matriz_ram[i][3]
                m = matriz_ram[i][4]
                classe = 2 * r + m
                classes[classe].append(i)
            
            indice_sub = -1
            for c in range(4):
                if len(classes[c]) > 0:
                    indice_sub = classes[c][0]
                    break
            
            if matriz_ram[indice_sub][4] == 1:
                num_pag = matriz_ram[indice_sub][0]
                matriz_swap[num_pag][2] = matriz_ram[indice_sub][2]
                matriz_swap[num_pag][4] = 0

            for i in range(100):
                if matriz_swap[i][1] == instrucao:
                    matriz_ram[indice_sub] = matriz_swap[i][:]
                    matriz_ram[indice_sub][3] = 0
                    matriz_ram[indice_sub][4] = 0
                    break
        
        instrucoes += 1
        
        if instrucoes % 10 == 0:
            for i in range(10):
                matriz_ram[i][3] = 0

        if instrucoes % 100 == 0:
            print(f"Executadas {instrucoes} instruções... ({page_faults} page faults)")


print("Estado Inicial:")
mostrar_matrizes()

executar_nru()

print("\nEstado Final:")
mostrar_matrizes()

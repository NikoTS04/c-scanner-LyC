with open('sample.c', 'r') as file:
    programa_fuente = file.read()

p = 0
while p < len(programa_fuente):
    char = programa_fuente[p]

    #cositas de scanner
    p += 1
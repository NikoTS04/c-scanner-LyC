# Scanner para archivos .c
# Analiza tokens: variables, palabras reservadas, numeros, operadores

PALABRAS_RESERVADAS = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
    'volatile', 'while', 'include', 'define', 'printf', 'scanf', 'main'
]

OPERADORES = [
    '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
    '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
    '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=',
    '->', '.', '?', ':'
]

DELIMITADORES = ['(', ')', '{', '}', '[', ']', ';', ',']


def es_letra(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'


def es_digito(c):
    return '0' <= c <= '9'


def quitar_comentarios(codigo):
    resultado = []
    i = 0
    n = len(codigo)

    while i < n:
        # comentario de linea
        if i + 1 < n and codigo[i] == '/' and codigo[i+1] == '/':
            while i < n and codigo[i] != '\n':
                i += 1
        # comentario de bloque
        elif i + 1 < n and codigo[i] == '/' and codigo[i+1] == '*':
            i += 2
            while i + 1 < n:
                if codigo[i] == '*' and codigo[i+1] == '/':
                    i += 2
                    break
                i += 1
        else:
            resultado.append(codigo[i])
            i += 1

    return ''.join(resultado)


def es_operador_doble(codigo, pos):
    if pos + 1 >= len(codigo):
        return None

    doble = codigo[pos] + codigo[pos+1]

    # operadores triples
    if pos + 2 < len(codigo):
        triple = doble + codigo[pos+2]
        if triple in ['<<=', '>>=']:
            return triple

    if doble in OPERADORES:
        return doble
    return None


def analizar(codigo):
    tokens = []
    i = 0
    n = len(codigo)
    orden = 1

    while i < n:
        c = codigo[i]

        # saltar espacios y saltos de linea
        if c in ' \t\n\r':
            i += 1
            continue

        # cadenas de texto (las ignoramos para el analisis)
        if c == '"':
            i += 1
            while i < n and codigo[i] != '"':
                if codigo[i] == '\\' and i + 1 < n:
                    i += 2
                else:
                    i += 1
            i += 1
            continue

        # caracteres (tambien los ignoramos)
        if c == "'":
            i += 1
            while i < n and codigo[i] != "'":
                if codigo[i] == '\\' and i + 1 < n:
                    i += 2
                else:
                    i += 1
            i += 1
            continue

        # directivas del preprocesador (las saltamos completas)
        if c == '#':
            while i < n and codigo[i] != '\n':
                i += 1
            continue

        # identificadores o palabras reservadas
        if es_letra(c):
            inicio = i
            while i < n and (es_letra(codigo[i]) or es_digito(codigo[i])):
                i += 1

            palabra = codigo[inicio:i]

            if palabra in PALABRAS_RESERVADAS:
                tokens.append({
                    'tipo': 'PALABRA_RESERVADA',
                    'valor': palabra,
                    'orden': orden
                })
            else:
                tokens.append({
                    'tipo': 'VARIABLE',
                    'valor': palabra,
                    'orden': orden
                })
            orden += 1
            continue

        # numeros
        if es_digito(c):
            inicio = i
            tiene_punto = False

            while i < n and (es_digito(codigo[i]) or codigo[i] == '.'):
                if codigo[i] == '.':
                    if tiene_punto:
                        break
                    tiene_punto = True
                i += 1

            numero = codigo[inicio:i]

            if tiene_punto:
                tokens.append({
                    'tipo': 'NUMERO_REAL',
                    'valor': numero,
                    'orden': orden
                })
            else:
                tokens.append({
                    'tipo': 'NUMERO_ENTERO',
                    'valor': numero,
                    'orden': orden
                })
            orden += 1
            continue

        # operadores
        op_doble = es_operador_doble(codigo, i)
        if op_doble:
            tokens.append({
                'tipo': 'OPERADOR',
                'valor': op_doble,
                'orden': orden
            })
            orden += 1
            i += len(op_doble)
            continue

        if c in OPERADORES:
            tokens.append({
                'tipo': 'OPERADOR',
                'valor': c,
                'orden': orden
            })
            orden += 1
            i += 1
            continue

        # delimitadores (no los contamos como tokens principales)
        if c in DELIMITADORES:
            i += 1
            continue

        i += 1

    return tokens


def mostrar_estadisticas(tokens):
    contadores = {
        'VARIABLE': 0,
        'PALABRA_RESERVADA': 0,
        'NUMERO_ENTERO': 0,
        'NUMERO_REAL': 0,
        'OPERADOR': 0
    }

    por_tipo = {
        'VARIABLE': [],
        'PALABRA_RESERVADA': [],
        'NUMERO_ENTERO': [],
        'NUMERO_REAL': [],
        'OPERADOR': []
    }

    for token in tokens:
        tipo = token['tipo']
        contadores[tipo] += 1
        por_tipo[tipo].append(token)

    print("\n" + "="*60)
    print("           RESULTADO DEL ANALISIS LEXICO")
    print("="*60)

    print("\n--- ESTADISTICAS GENERALES ---\n")
    print(f"Total de tokens encontrados: {len(tokens)}")
    print(f"  - Palabras reservadas: {contadores['PALABRA_RESERVADA']}")
    print(f"  - Variables:           {contadores['VARIABLE']}")
    print(f"  - Numeros enteros:     {contadores['NUMERO_ENTERO']}")
    print(f"  - Numeros reales:      {contadores['NUMERO_REAL']}")
    print(f"  - Operadores:          {contadores['OPERADOR']}")

    print("\n" + "-"*60)
    print("--- DETALLE POR TIPO DE TOKEN ---")
    print("-"*60)

    nombres = {
        'PALABRA_RESERVADA': 'PALABRAS RESERVADAS',
        'VARIABLE': 'VARIABLES (IDENTIFICADORES)',
        'NUMERO_ENTERO': 'NUMEROS ENTEROS',
        'NUMERO_REAL': 'NUMEROS REALES',
        'OPERADOR': 'OPERADORES'
    }

    for tipo in ['PALABRA_RESERVADA', 'VARIABLE', 'NUMERO_ENTERO', 'NUMERO_REAL', 'OPERADOR']:
        print(f"\n[{nombres[tipo]}]")
        if por_tipo[tipo]:
            for t in por_tipo[tipo]:
                print(f"  Orden {t['orden']:3d}: {t['valor']}")
        else:
            print("  (ninguno encontrado)")

    print("\n" + "="*60)
    print("--- TOKENS EN ORDEN DE APARICION ---")
    print("="*60 + "\n")

    for token in tokens:
        print(f"  {token['orden']:3d}. [{token['tipo']:17s}] -> {token['valor']}")

    print("\n" + "="*60)


def main():
    print("\n*** SCANNER LEXICO PARA ARCHIVOS .C ***\n")

    ruta = input("Ingrese la ruta del archivo .c: ").strip()

    if not ruta:
        print("Error: No se ingreso ninguna ruta")
        return

    try:
        archivo = open(ruta, 'r', encoding='utf-8')
        contenido = archivo.read()
        archivo.close()
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo '{ruta}'")
        return
    except:
        print("Error: No se pudo leer el archivo")
        return

    print(f"\nArchivo cargado: {ruta}")
    print(f"Tamano: {len(contenido)} caracteres")

    # quitar comentarios primero
    codigo_limpio = quitar_comentarios(contenido)

    # analizar el codigo
    tokens = analizar(codigo_limpio)

    # mostrar resultados
    mostrar_estadisticas(tokens)


if __name__ == '__main__':
    main()


import unicodedata


def normalizar(texto):
    
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )

    return texto


def distancia_levenshtein(palabra1, palabra2):}
    
    palabra1 = normalizar(palabra1)
    palabra2 = normalizar(palabra2)

    filas = len(palabra1) + 1
    columnas = len(palabra2) + 1

    matriz = [[0] * columnas for _ in range(filas)]

    for i in range(filas):
        matriz[i][0] = i

    for j in range(columnas):
        matriz[0][j] = j

    for i in range(1, filas):
        for j in range(1, columnas):

            if palabra1[i - 1] == palabra2[j - 1]:
                costo = 0
            else:
                costo = 1

            matriz[i][j] = min(
                matriz[i - 1][j] + 1,
                matriz[i][j - 1] + 1,
                matriz[i - 1][j - 1] + costo
            )

    return matriz[-1][-1]


def calcular_similitud(palabra1, palabra2):
    
    palabra1 = normalizar(palabra1)
    palabra2 = normalizar(palabra2)

    mayor = max(len(palabra1), len(palabra2))

    if mayor == 0:
        return 100.0

    distancia = distancia_levenshtein(palabra1, palabra2)

    similitud = (1 - distancia / mayor) * 100

    return round(similitud, 2)


def evaluar_consulta(consulta, texto):

    palabras_consulta = normalizar(consulta).split()
    palabras_texto = normalizar(texto).split()

    if not palabras_consulta:
        return 0.0

    if not palabras_texto:
        return 0.0

    puntuaciones = []

    for palabra in palabras_consulta:

        mejor_similitud = 0

        for palabra_documento in palabras_texto:

            similitud = calcular_similitud(
                palabra,
                palabra_documento
            )

            if similitud > mejor_similitud:
                mejor_similitud = similitud

        puntuaciones.append(mejor_similitud)

    resultado = sum(puntuaciones) / len(puntuaciones)

    return round(resultado, 2)


if __name__ == "__main__":

    print("PRUEBA 1: DISTANCIA DE LEVENSHTEIN")
    print("-----------------------------------")

    palabra1 = "universiad"
    palabra2 = "universidad"

    distancia = distancia_levenshtein(palabra1, palabra2)
    porcentaje = calcular_similitud(palabra1, palabra2)

    print("Primera palabra:", palabra1)
    print("Segunda palabra:", palabra2)
    print("Distancia:", distancia)
    print("Similitud:", porcentaje, "%")

    print("\nPRUEBA 2: PALABRAS CON ERRORES")
    print("-----------------------------------")

    palabra1 = "hermosiyo"
    palabra2 = "hermosillo"

    distancia = distancia_levenshtein(palabra1, palabra2)
    porcentaje = calcular_similitud(palabra1, palabra2)

    print("Primera palabra:", palabra1)
    print("Segunda palabra:", palabra2)
    print("Distancia:", distancia)
    print("Similitud:", porcentaje, "%")

    print("\nPRUEBA 3: CONSULTA COMPLETA")
    print("-----------------------------------")

    consulta = "informe de evaluacion"

    texto_documento = (
        "informe anual de evaluación de resultados"
    )

    resultado = evaluar_consulta(
        consulta,
        texto_documento
    )

    print("Consulta:", consulta)
    print("Texto del documento:", texto_documento)
    print("Puntuacion:", resultado, "%")

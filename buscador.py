
import json
import os

from similitud import normalizar, evaluar_consulta

CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_INDICE = os.path.join(CARPETA_PROYECTO, "indice.json")

UMBRAL_SIMILITUD = 75.0


def cargar_indice():
    if not os.path.exists(ARCHIVO_INDICE):
        print("No se encontro el indice. Ejecuta primero indexador.py")
        return []

    with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_documentos(consulta, indice):
    resultados = []

    consulta_normalizada = normalizar(consulta)

    if not consulta_normalizada:
        return resultados

    for documento in indice:

        contenido = documento.get("contenido", "")

        if not contenido:
            continue

        contenido_normalizado = normalizar(contenido)

        if consulta_normalizada in contenido_normalizado:
            resultados.append(documento["nombre"])
            continue

        puntuacion = evaluar_consulta(
            consulta,
            contenido
        )

        if puntuacion >= UMBRAL_SIMILITUD:
            resultados.append(documento["nombre"])

    return resultados


def main():
    indice = cargar_indice()

    if not indice:
        return

    print("================================")
    print("      BUSCADOR DE ACTAS PDF")
    print("================================")

    consulta = input("Escribe lo que deseas buscar: ")

    resultados = buscar_documentos(consulta, indice)

    if resultados:
        print("\nDocumentos encontrados:")

        for documento in resultados:
            print("-", documento)

    else:
        print("\nNo se encontraron coincidencias.")


if __name__ == "__main__":
    main()

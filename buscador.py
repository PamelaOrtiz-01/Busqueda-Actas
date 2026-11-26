
import json
import os
import difflib
import re

ARCHIVO_INDICE = "indice.json"


def cargar_indice():
    if not os.path.exists(ARCHIVO_INDICE):
        print("No se encontro el indice. Ejecuta primero indexador.py")
        return []

    with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_documentos(consulta, indice):
    resultados = []

    consulta = consulta.lower().strip()

    for documento in indice:
        contenido = documento["contenido"]

        if consulta in contenido:
            resultados.append(documento["nombre"])
            continue

        palabras = re.findall(r'\b[a-záéíóúüñ]+\b', contenido)

        coincidencias = difflib.get_close_matches(
            consulta,
            palabras,
            n=1,
            cutoff=0.75
        )

        if coincidencias:
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


import os
import tempfile

from scraper import calcular_hash


CARPETA_PDF = "pdfs"


def probar_duplicados():

    print("===================================")
    print(" PRUEBA DE DETECCION DE DUPLICADOS")
    print("===================================")

    if not os.path.exists(CARPETA_PDF):
        print("No existe la carpeta pdfs.")
        return

    archivos = [
        nombre for nombre in os.listdir(CARPETA_PDF)
        if nombre.lower().endswith(".pdf")
        and os.path.isfile(os.path.join(CARPETA_PDF, nombre))
    ]

    if not archivos:
        print("No hay archivos PDF para comprobar.")
        return

    print("PDF encontrados:", len(archivos))

    hashes = {}

    for nombre in archivos:

        ruta = os.path.join(CARPETA_PDF, nombre)

        with open(ruta, "rb") as archivo:
            contenido = archivo.read()

        hash_pdf = calcular_hash(contenido)

        if hash_pdf in hashes:
            print("Duplicado encontrado:", nombre)
            print("Ya existe como:", hashes[hash_pdf])

        else:
            hashes[hash_pdf] = nombre

    print("\nPrueba con contenido idéntico:")

    contenido1 = b"%PDF-1.4 documento de prueba"
    contenido2 = b"%PDF-1.4 documento de prueba"

    if calcular_hash(contenido1) == calcular_hash(contenido2):
        print("Correcto: se detectaron como duplicados.")

    print("\nPrueba con contenido diferente:")

    contenido3 = b"%PDF-1.4 otro documento"

    if calcular_hash(contenido1) != calcular_hash(contenido3):
        print("Correcto: se identificaron como diferentes.")

    print("\nPrueba finalizada.")


if __name__ == "__main__":
    probar_duplicados()

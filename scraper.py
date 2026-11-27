
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import hashlib


CARPETA_PDF = "pdfs"


def calcular_hash(contenido):
    return hashlib.sha256(contenido).hexdigest()


def buscar_pdfs(url):

    try:
        respuesta = requests.get(url, timeout=15)
        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")

        enlaces_pdf = []

        for enlace in soup.find_all("a", href=True):

            enlace_completo = urljoin(url, enlace["href"])

            ruta = urlparse(enlace_completo).path.lower()

            if ruta.endswith(".pdf"):
                if enlace_completo not in enlaces_pdf:
                    enlaces_pdf.append(enlace_completo)

        return enlaces_pdf

    except requests.RequestException as error:
        print("Error al consultar la pagina:", error)
        return []


def descargar_pdfs(enlaces):

    os.makedirs(CARPETA_PDF, exist_ok=True)

    hashes_existentes = {}

    for nombre_archivo in os.listdir(CARPETA_PDF):

        ruta = os.path.join(CARPETA_PDF, nombre_archivo)

        if os.path.isfile(ruta) and nombre_archivo.lower().endswith(".pdf"):

            with open(ruta, "rb") as archivo:
                contenido = archivo.read()

            hash_archivo = calcular_hash(contenido)

            hashes_existentes[hash_archivo] = nombre_archivo

    for enlace in enlaces:

        try:
            respuesta = requests.get(enlace, timeout=30)
            respuesta.raise_for_status()

            contenido = respuesta.content

            if not contenido.startswith(b"%PDF"):
                print("El archivo no es un PDF valido:", enlace)
                continue

            hash_nuevo = calcular_hash(contenido)

            if hash_nuevo in hashes_existentes:

                print(
                    "PDF duplicado. Ya existe como:",
                    hashes_existentes[hash_nuevo]
                )

                continue

            nombre = os.path.basename(urlparse(enlace).path)

            if not nombre:
                nombre = "documento.pdf"

            ruta = os.path.join(CARPETA_PDF, nombre)

            if os.path.exists(ruta):

                nombre_base, extension = os.path.splitext(nombre)
                contador = 1

                while os.path.exists(ruta):
                    nuevo_nombre = f"{nombre_base}_{contador}{extension}"
                    ruta = os.path.join(CARPETA_PDF, nuevo_nombre)
                    contador += 1

                nombre = os.path.basename(ruta)

            with open(ruta, "wb") as archivo:
                archivo.write(contenido)

            hashes_existentes[hash_nuevo] = nombre

            print("PDF descargado correctamente:", nombre)

        except requests.RequestException as error:
            print("Error al descargar el documento:", error)


def main():

    print("====================================")
    print("     BUSCADOR DE ACTAS EN PDF")
    print("====================================")

    url = input("Ingresa la URL de la pagina web: ").strip()

    if not url.startswith(("http://", "https://")):
        print("Error: debes ingresar una URL valida.")
        return

    print("\nBuscando documentos PDF...")

    enlaces = buscar_pdfs(url)

    print("\nDocumentos encontrados:", len(enlaces))

    if enlaces:
        descargar_pdfs(enlaces)
    else:
        print("No se encontraron documentos PDF.")


if __name__ == "__main__":
    main()


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

CARPETA_PDF = "pdfs"


def buscar_pdfs(url):
    """
    Busca enlaces a documentos PDF dentro de una pagina web.
    """

    try:
        respuesta = requests.get(url, timeout=15)
        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")

        enlaces_pdf = []

        for enlace in soup.find_all("a", href=True):

            # Obtener la direccion completa del enlace
            enlace_completo = urljoin(url, enlace["href"])

            # Revisar si el enlace termina en PDF
            ruta = urlparse(enlace_completo).path.lower()

            if ruta.endswith(".pdf"):
                if enlace_completo not in enlaces_pdf:
                    enlaces_pdf.append(enlace_completo)

        return enlaces_pdf

    except requests.RequestException as error:
        print("Error al consultar la pagina:", error)
        return []


def descargar_pdfs(enlaces):
    """
    Descarga los documentos PDF encontrados.
    """

    os.makedirs(CARPETA_PDF, exist_ok=True)

    for enlace in enlaces:

        try:
            respuesta = requests.get(enlace, timeout=30)
            respuesta.raise_for_status()

            contenido = respuesta.content

            if not contenido.startswith(b"%PDF"):
                print("El archivo no es un PDF valido:", enlace)
                continue

            nombre = os.path.basename(urlparse(enlace).path)

            if not nombre:
                nombre = "documento.pdf"

            ruta = os.path.join(CARPETA_PDF, nombre)

            if os.path.exists(ruta):
                print("El archivo ya existe:", nombre)
                continue

            with open(ruta, "wb") as archivo:
                archivo.write(contenido)

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

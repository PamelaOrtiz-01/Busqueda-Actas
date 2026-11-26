
import os
import json
import re
from pdf_text_extract import extract_text_from_pdf

CARPETA_PDF = "pdfs"
ARCHIVO_INDICE = "indice.json"


def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def crear_indice():
    indice = []

    if not os.path.exists(CARPETA_PDF):
        print("No se encontró la carpeta pdfs.")
        return

    archivos = os.listdir(CARPETA_PDF)

    for archivo in archivos:
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(CARPETA_PDF, archivo)

            print("Indexando:", archivo)

            texto = extract_text_from_pdf(ruta)

            documento = {
                "nombre": archivo,
                "contenido": limpiar_texto(texto)
            }

            indice.append(documento)

    with open(ARCHIVO_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, ensure_ascii=False, indent=4)

    print("\nIndexación terminada.")
    print("Documentos indexados:", len(indice))
    print("Archivo creado:", ARCHIVO_INDICE)


if __name__ == "__main__":
    crear_indice()

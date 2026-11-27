
import os
import tempfile
import scraper


class RespuestaSimulada:
    def __init__(self, contenido):
        self.content = contenido

    def raise_for_status(self):
        pass


def ejecutar_prueba():

    print("======================================")
    print(" PRUEBA REAL DE DESCARGA CON SHA-256")
    print("======================================")

    contenido_original = b"%PDF-1.4 documento original"
    contenido_diferente = b"%PDF-1.4 documento diferente"

    respuestas = {
        "https://ejemplo.com/otro_nombre.pdf": contenido_original,
        "https://ejemplo.com/nuevo.pdf": contenido_diferente
    }

    carpeta_original = scraper.CARPETA_PDF
    get_original = scraper.requests.get

    try:
        with tempfile.TemporaryDirectory() as carpeta_temporal:

            scraper.CARPETA_PDF = carpeta_temporal

            ruta_original = os.path.join(
                carpeta_temporal,
                "original.pdf"
            )

            with open(ruta_original, "wb") as archivo:
                archivo.write(contenido_original)

            def descarga_simulada(url, timeout=30):
                return RespuestaSimulada(respuestas[url])

            scraper.requests.get = descarga_simulada

            print("\nPDF iniciales:", os.listdir(carpeta_temporal))

            print("\nPrueba 1: mismo contenido con otro nombre")

            scraper.descargar_pdfs([
                "https://ejemplo.com/otro_nombre.pdf"
            ])

            archivos = os.listdir(carpeta_temporal)

            if len(archivos) == 1:
                print("Correcto: no se guardó otra copia.")
            else:
                print("Error: se guardó un archivo duplicado.")

            print("\nPrueba 2: contenido diferente")

            scraper.descargar_pdfs([
                "https://ejemplo.com/nuevo.pdf"
            ])

            archivos = os.listdir(carpeta_temporal)

            if len(archivos) == 2 and "nuevo.pdf" in archivos:
                print("Correcto: el PDF nuevo se guardó.")
            else:
                print("Error: no se guardó correctamente.")

            print("\nArchivos finales:", archivos)

            print("\nPrueba finalizada.")

    finally:
        scraper.CARPETA_PDF = carpeta_original
        scraper.requests.get = get_original


if __name__ == "__main__":
    ejecutar_prueba()

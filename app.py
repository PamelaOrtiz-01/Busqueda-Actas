import datetime
import os

from flask import Flask, redirect, render_template, render_template_string, request, session, url_for
from buscador import cargar_indice, buscar_documentos

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Buscador de Actas PDF</title>
</head>
<body>
    <h1>Buscador de Actas en PDF</h1>

    <form method="POST">
        <input type="text" name="consulta"
               placeholder="Escribe lo que deseas buscar"
               required>
        <button type="submit">Buscar</button>
    </form>

    {% if consulta %}
        <h2>Resultados para: {{ consulta }}</h2>

        {% if resultados %}
            <ul>
                {% for documento in resultados %}
                    <li>{{ documento }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No se encontraron coincidencias.</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route('/')
def inicio():
    """ Route to display the home page and search for the PDfs"""
    resultados = []
    consulta = ""

    if request.method == "POST":
        consulta = request.form["consulta"]
        indice = cargar_indice()
        resultados = buscar_documentos(consulta, indice)    

    return render_template(
        "inicio.html",
        consulta=consulta,
        resultados=resultados
    )

# MENU DE ARCHIVOS DISPONIBLES
@app.route('/archivos_disponibles')
def archivos_disponibles():
    """ Route to display the available files in the repository """
    return render_template("archivos_disponibles.html")

@app.route('/autores_disponibles')
def autores_disponibles():
    """ Route to display files by author """
    return render_template("autores_disponibles.html")

@app.route('/anios_disponibles')
def anios_disponibles():
    """ Route to display files by year """
    return render_template("anios_disponibles.html")

# Pagina individual del autor
@app.route('/autor')
def autor():
    """ Route to display files by author """
    return render_template("autor_archivos.html")

# Pagina individual del año
@app.route('/anio')
def anio():
    """ Route to display files by year """
    return render_template("anio_archivos.html")

# Pagina individual del archivo
@app.route('/detalles')
def pdf_details():
    """ Route to display PDF details """
    return render_template("pdf_details.html")

@app.route('/guardados')
def guardados():
    """ Route to display the bookmarked files """
    return render_template("guardados.html")

@app.route('/descargas')
def descargas():
    """ Route to display the queued downloads """
    return render_template("descargas.html")

#OJITO AQUÍ
"""CODIGO ANTERIOR DE LA APP, MODIFIQUE EL return render_template_string POR return render_template 
PARA QUE FUNCIONE CON EL ARCHIVO HTML"""

"""@app.route("/", methods=["GET", "POST"])
def inicio():
    resultados = []
    consulta = ""

    if request.method == "POST":
        consulta = request.form["consulta"]
        indice = cargar_indice()
        resultados = buscar_documentos(consulta, indice)

    return render_template_string(
        HTML,
        consulta=consulta,
        resultados=resultados
    )"""

if __name__ == "__main__":
    app.run(debug=True)
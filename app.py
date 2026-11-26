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

@app.route("/", methods=["GET", "POST"])
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
    )

if __name__ == "__main__":
    app.run(debug=True)
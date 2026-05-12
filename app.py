from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "retomovil"

preguntas_reglas = [
    {
        "pregunta": "¿Cuántas faltas provocan el final del parcial?",
        "respuesta": "3"
    },
    {
        "pregunta": "¿Qué pasa si existe plagio?",
        "respuesta": "0"
    },
    {
        "pregunta": "¿Cómo deben entregarse las actividades?",
        "respuesta": "pdf"
    },
    {
        "pregunta": "¿Cuál es la duración mínima del video reporte?",
        "respuesta": "5"
    },
    {
        "pregunta": "¿Qué debe escucharse en el video reporte?",
        "respuesta": "voz"
    },
    {
        "pregunta": "¿Dónde se entregan las actividades?",
        "respuesta": "classroom"
    },
    {
        "pregunta": "¿Qué sucede si entregas trabajos incompletos?",
        "respuesta": "no se aceptan"
    }
]

@app.route("/")
def inicio():

    session["pregunta_actual"] = 0
    session["correctas"] = 0

    return render_template("index.html")

@app.route("/reglas", methods=["GET", "POST"])
def reglas():

    pregunta_actual = session.get("pregunta_actual", 0)
    correctas = session.get("correctas", 0)

    mensaje = ""

    if request.method == "POST":

        respuesta_usuario = request.form["respuesta"].lower()

        respuesta_correcta = preguntas_reglas[pregunta_actual]["respuesta"]

        if respuesta_correcta in respuesta_usuario:
            correctas += 1
            mensaje = "✅ Correcto"
        else:
            mensaje = "❌ Incorrecto"

        session["correctas"] = correctas
        session["pregunta_actual"] = pregunta_actual + 1

        if correctas >= 2:
            return redirect("/notas")

        pregunta_actual = session["pregunta_actual"]

    if pregunta_actual >= len(preguntas_reglas):
        return redirect("/")

    pregunta = preguntas_reglas[pregunta_actual]["pregunta"]

    return render_template(
        "reglas.html",
        pregunta=pregunta,
        mensaje=mensaje,
        correctas=correctas
    )

@app.route("/notas")
def notas():
    return render_template("notas.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

if __name__ == "__main__":
    app.run(debug=True)
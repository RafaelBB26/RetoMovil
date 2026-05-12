from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "retomovil"

preguntas_reglas = [

    {"pregunta": "¿Qué porcentaje de asistencia se requiere para tener derecho a evaluación?","respuesta": "80"},
    {"pregunta": "¿Cuántos minutos de tolerancia existen para entrar a clase?","respuesta": "10"},
    {"pregunta": "¿Después de cuántas horas ya no se aceptan justificantes?","respuesta": "24"},
    {"pregunta": "¿En qué plataforma deben subirse las tareas?","respuesta": "classroom"},
    {"pregunta": "¿Qué pasa con los trabajos entregados fuera de tiempo sin justificación?","respuesta": "no se aceptan"},
    {"pregunta": "¿Qué sucede si existe plagio en trabajos o exámenes?","respuesta": "reprobar"},
    {"pregunta": "¿Cuántas incidencias pueden provocar perder derecho a examen?","respuesta": "3"},
    {"pregunta": "¿Está permitido el uso de audífonos durante la clase?","respuesta": "no"},
    {"pregunta": "¿Está permitido comer dentro del salón?","respuesta": "no"},
    {"pregunta": "¿Qué tipo de archivos deben entregarse en Classroom?","respuesta": "pdf"},
]

preguntas_notas = [
    {"pregunta": "¿Cuánto vale conocimiento en el parcial 1?", "respuesta": "40"},
    {"pregunta": "¿Cuánto vale desempeño en el parcial 1?", "respuesta": "20"},
    {"pregunta": "¿Cuánto vale producto en el parcial 1?", "respuesta": "30"},
    {"pregunta": "¿Cuánto vale integrador en el parcial 1?", "respuesta": "10"},
    {"pregunta": "¿Cuánto vale conocimiento en el parcial 2?", "respuesta": "40"},
    {"pregunta": "¿Cuánto vale desempeño en el parcial 2?", "respuesta": "20"},
    {"pregunta": "¿Cuánto vale producto en el parcial 2?", "respuesta": "30"},
    {"pregunta": "¿Cuánto vale integrador en el parcial 2?", "respuesta": "10"},
    {"pregunta": "¿Cuánto vale conocimiento en el parcial 3?", "respuesta": "10"},
    {"pregunta": "¿Cuánto vale desempeño en el parcial 3?", "respuesta": "10"},
    {"pregunta": "¿Cuánto vale producto en el parcial 3?", "respuesta": "30"},
    {"pregunta": "¿Cuánto vale integrador en el parcial 3?", "respuesta": "50"}
]

preguntas_skills = [
    {"pregunta": "¿Qué lenguaje se usa antes de React Native?", "respuesta": "javascript"},
    {"pregunta": "¿Qué framework móvil se utilizará?", "respuesta": "react"},
    {"pregunta": "¿Cómo se llaman las pantallas en React Native?", "respuesta": "screens"},
    {"pregunta": "¿Qué permite cambiar entre pantallas?", "respuesta": "navigation"},
    {"pregunta": "¿Con qué se comunica una app para obtener datos?", "respuesta": "api"},
    {"pregunta": "¿Qué tipo de actividades incluye teoría?", "respuesta": "investigaciones"},
    {"pregunta": "¿Qué evidencias se subirán a GitHub?", "respuesta": "evidencias"},
    {"pregunta": "¿Qué lenguaje se abrevia como JS?", "respuesta": "javascript"}
]

preguntas_timeline = [
    {"pregunta": "¿Cuándo es el examen de primer parcial?", "respuesta": "02/06/26"},
    {"pregunta": "¿Cuándo es el examen de segundo parcial?", "respuesta": "07/07/26"},
    {"pregunta": "¿Cuándo es el examen de tercer parcial?", "respuesta": "11/08/26"},
    {"pregunta": "¿Cuándo es el examen final?", "respuesta": "17/08/26"},
    
]

@app.route("/")
def inicio():

    session.clear()

    session["vidas"] = 3

    session["pregunta_actual"] = 0
    session["correctas"] = 0

    session["pregunta_actual_notas"] = 0
    session["correctas_notas"] = 0

    session["pregunta_actual_skills"] = 0
    session["correctas_skills"] = 0

    session["pregunta_actual_timeline"] = 0
    session["correctas_timeline"] = 0

    return render_template("index.html")

def revisar_respuesta(respuesta_usuario, respuesta_correcta):

    vidas = session.get("vidas", 3)

    if respuesta_correcta in respuesta_usuario:
        return True

    vidas -= 1
    session["vidas"] = vidas

    if vidas <= 0:
        return "gameover"

    return False

@app.route("/reglas", methods=["GET", "POST"])
def reglas():

    pregunta_actual = session.get("pregunta_actual", 0)
    correctas = session.get("correctas", 0)

    mensaje = ""

    if request.method == "POST":

        respuesta_usuario = request.form["respuesta"].lower()

        respuesta_correcta = preguntas_reglas[pregunta_actual]["respuesta"]

        resultado = revisar_respuesta(
            respuesta_usuario,
            respuesta_correcta
        )

        if resultado == True:
            correctas += 1
            mensaje = "✅ Correcto"
        elif resultado == "gameover":
            return redirect("/gameover")
        else:
            mensaje = "❌ Incorrecto"

        session["correctas"] = correctas
        session["pregunta_actual"] = pregunta_actual + 1

        if correctas >= 2:
            session["mensaje_desbloqueo"] = "🔓 Nivel 1 completado"
            return redirect("/notas")

        pregunta_actual = session["pregunta_actual"]

    if pregunta_actual >= len(preguntas_reglas):
        return redirect("/")

    pregunta = preguntas_reglas[pregunta_actual]["pregunta"]

    return render_template(
        "reglas.html",
        pregunta=pregunta,
        mensaje=mensaje,
        correctas=correctas,
        vidas=session["vidas"]
    )

@app.route("/notas", methods=["GET", "POST"])
def notas():

    pregunta_actual = session.get("pregunta_actual_notas", 0)
    correctas = session.get("correctas_notas", 0)

    mensaje = ""

    if request.method == "POST":

        respuesta_usuario = request.form["respuesta"].lower()

        respuesta_correcta = preguntas_notas[pregunta_actual]["respuesta"]

        resultado = revisar_respuesta(
            respuesta_usuario,
            respuesta_correcta
        )

        if resultado == True:
            correctas += 1
            mensaje = "✅ Correcto"
        elif resultado == "gameover":
            return redirect("/gameover")
        else:
            mensaje = "❌ Incorrecto"

        session["correctas_notas"] = correctas
        session["pregunta_actual_notas"] = pregunta_actual + 1

        if correctas >= 2:
            session["mensaje_desbloqueo"] = "🔓 Nivel 2 completado"
            return redirect("/skills")

        pregunta_actual = session["pregunta_actual_notas"]

    if pregunta_actual >= len(preguntas_notas):
        return redirect("/")

    pregunta = preguntas_notas[pregunta_actual]["pregunta"]

    return render_template(
        "notas.html",
        pregunta=pregunta,
        mensaje=mensaje,
        correctas=correctas,
        vidas=session["vidas"],
        desbloqueo=session.get("mensaje_desbloqueo", "")
    )

@app.route("/skills", methods=["GET", "POST"])
def skills():

    pregunta_actual = session.get("pregunta_actual_skills", 0)
    correctas = session.get("correctas_skills", 0)

    mensaje = ""

    if request.method == "POST":

        respuesta_usuario = request.form["respuesta"].lower()

        respuesta_correcta = preguntas_skills[pregunta_actual]["respuesta"]

        resultado = revisar_respuesta(
            respuesta_usuario,
            respuesta_correcta
        )

        if resultado == True:
            correctas += 1
            mensaje = "✅ Correcto"
        elif resultado == "gameover":
            return redirect("/gameover")
        else:
            mensaje = "❌ Incorrecto"

        session["correctas_skills"] = correctas
        session["pregunta_actual_skills"] = pregunta_actual + 1

        if correctas >= 2:
            session["mensaje_desbloqueo"] = "🔓 Nivel 3 completado"
            return redirect("/timeline")

        pregunta_actual = session["pregunta_actual_skills"]

    if pregunta_actual >= len(preguntas_skills):
        return redirect("/")

    pregunta = preguntas_skills[pregunta_actual]["pregunta"]

    return render_template(
        "skills.html",
        pregunta=pregunta,
        mensaje=mensaje,
        correctas=correctas,
        vidas=session["vidas"],
        desbloqueo=session.get("mensaje_desbloqueo", "")
    )

@app.route("/timeline", methods=["GET", "POST"])
def timeline():

    pregunta_actual = session.get("pregunta_actual_timeline", 0)
    correctas = session.get("correctas_timeline", 0)

    mensaje = ""

    if request.method == "POST":

        respuesta_usuario = request.form["respuesta"].lower()

        respuesta_correcta = preguntas_timeline[pregunta_actual]["respuesta"].lower()

        resultado = revisar_respuesta(
            respuesta_usuario,
            respuesta_correcta
        )

        if resultado == True:
            correctas += 1
            mensaje = "✅ Correcto"
        elif resultado == "gameover":
            return redirect("/gameover")
        else:
            mensaje = "❌ Incorrecto"

        session["correctas_timeline"] = correctas
        session["pregunta_actual_timeline"] = pregunta_actual + 1

        if correctas >= 2:
            return redirect("/final")

        pregunta_actual = session["pregunta_actual_timeline"]

    if pregunta_actual >= len(preguntas_timeline):
        return redirect("/")

    pregunta = preguntas_timeline[pregunta_actual]["pregunta"]

    return render_template(
        "timeline.html",
        pregunta=pregunta,
        mensaje=mensaje,
        correctas=correctas,
        vidas=session["vidas"],
        desbloqueo=session.get("mensaje_desbloqueo", "")
    )

@app.route("/final")
def final():
    return render_template("final.html")

@app.route("/gameover")
def gameover():
    return render_template("gameover.html")

if __name__ == "__main__":
    app.run(debug=True)
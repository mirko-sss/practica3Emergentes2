from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


# Página principal: muestra la lista de inscritos
@app.route("/", methods=['GET', 'POST'])
def registro():
    if 'inscritos' not in session:
        session['inscritos'] = []
    inscritos = session.get('inscritos', [])
    return render_template("inscritoslist.html", inscritos=inscritos)


# Genera un nuevo ID para los inscritos
def generar_id():
    if 'inscritos' in session and len(session['inscritos']) > 0:
        return max(item['id'] for item in session['inscritos']) + 1
    else:
        return 1


# Registrar un nuevo inscrito

@app.route("/registro", methods=['GET', 'POST'])
def inscritos():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = []
        
        # Agregar seminarios a la lista según la selección
        if 'artificial' in request.form:
            seminarios.append('Inteligencia Artificial')
        if 'profundo' in request.form:
            seminarios.append('Machine Learning')
        if 'simulacion' in request.form:
            seminarios.append('Simulación con Arena')
        if 'robotica' in request.form:
            seminarios.append('Robótica Educativa')

        nuevo_inscrito = {
            'id': generar_id(),
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': ', '.join(seminarios)  # Convertir la lista a una cadena
        }

        if 'inscritos' not in session:
            session['inscritos'] = []
        session['inscritos'].append(nuevo_inscrito)
        session.modified = True
        return redirect(url_for('registro'))

    return render_template('registro.html')


# Editar un inscrito existente
@app.route("/editarlist/<int:id>", methods=['GET', 'POST'])
def editarlist(id):
    lista_inscritos = session.get('inscritos', [])
    inscrito = next((i for i in lista_inscritos if i['id'] == id), None)
    if not inscrito:
        return redirect(url_for('registro'))

    if request.method == 'POST':
        inscrito['fecha'] = request.form['fecha']
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellidos'] = request.form['apellidos']
        inscrito['turno'] = request.form['turno']
        inscrito['artificial'] = 'Sí' if 'artificial' in request.form else 'No'
        inscrito['profundo'] = 'Sí' if 'profundo' in request.form else 'No'
        inscrito['simulacion'] = 'Sí' if 'simulacion' in request.form else 'No'
        inscrito['robotica'] = 'Sí' if 'robotica' in request.form else 'No'
        session.modified = True
        return redirect(url_for('registro'))

    return render_template('editarlist.html', inscrito=inscrito)


# Eliminar un inscrito
@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    lista_inscritos = session.get('inscritos', [])
    inscrito = next((i for i in lista_inscritos if i['id'] == id), None)
    if inscrito:
        session['inscritos'].remove(inscrito)
        session.modified = True
    return redirect(url_for('registro'))


if __name__ == "__main__":
    app.run(debug=True)

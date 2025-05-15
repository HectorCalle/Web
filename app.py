from flask import Flask, render_template, request, url_for, redirect, session
from config import Config
from models import db, Usuario, Tarea
from datetime import datetime

app = Flask(__name__)
#Configuración de la aplicación Flask (donde se indica la base de datos a usar)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)
# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and usuario.verificar_contrasena(contrasena):
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for('list_tasks'))
        else:
            return "Correo o contraseña incorrectos."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        if Usuario.query.filter_by(correo=correo).first():
            return "El correo ya está registrado."
        else:
            nuevo_usuario = Usuario(nombre=nombre, correo=correo)
            nuevo_usuario.colocar_contrasena(contrasena)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tasks')
def list_tasks():
    tareas = Tarea.query.filter_by(usuario_id=session["usuario_id"]).all()
    return render_template('tasks.html', tareas=tareas)

@app.route('/task/<int:id>')
def view_task(id):
    tarea = Tarea.query.get_or_404(id)
    return render_template('task.html', tarea=tarea)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_vencimiento = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        prioridad = request.form['prioridad']
        try:
            nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion, fecha_vencimiento=fecha_vencimiento, prioridad=prioridad, usuario_id=session['usuario_id'])
            db.session.add(nueva_tarea)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            return f"Error al crear la tarea: {e}"
    return render_template('create_task.html')

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    tarea = Tarea.query.get_or_404(id)
    if request.method == 'POST':
        tarea.titulo = request.form['titulo']
        tarea.descripcion = request.form['descripcion']
        tarea.fecha_vencimiento = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        tarea.prioridad = request.form['prioridad']
        tarea.completada = request.form.get('completada') == 'on'
        try:        
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            return f"Error al editar la tarea: {e}"
    return render_template('edit_task.html', tarea=tarea)

@app.route('/task/delete/<int:id>')
def delete_task(id):
    tarea = Tarea.query.get_or_404(id)
    try:
        db.session.delete(tarea)
        db.session.commit()
    except Exception as e:
        return f"Error al eliminar la tarea la tarea: {e}"
    return redirect(url_for("list_tasks"))

@app.route('/task/complete/<int:id>', methods=['POST'])
def complete_task(id):
    tarea = Tarea.query.get_or_404(id)
    try:
        tarea.completada= not tarea.completada
        db.session.commit()
    except Exception as e:
        return f"Error al completar la tarea: {e}"
    return redirect(url_for("list_tasks"))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
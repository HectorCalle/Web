from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tasks')
def list_tasks():
    tareas = ["Lavar la ropa", "Limpiar la casa", "Hacer la compra", "Estudiar para el examen", "Hacer ejercicio", "Leer un libro"]
    return render_template('tasks.html', tareas=tareas)

@app.route('/task')
def view_task():
    return render_template('task.html')

@app.route('/task/create')
def create_task():
    return render_template('create_task.html')
#Crear una ruta y la vista correspondiente para renderizar un html llamado "create_task.html"



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'clave_secreta_para_flask'

# Función para validar formatos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # Obtener datos del formulario
        file = request.files.get('file')
        tipo_doc = request.form.get('tipo_doc')
        candidato = request.form.get('candidato')
        fecha_doc = request.form.get('fecha_doc')
        fuente = request.form.get('fuente')

        # Validar campos obligatorios
        if not file or file.filename == '' or not tipo_doc or not candidato or not fecha_doc:
            flash("Por favor complete todos los campos obligatorios y seleccione un archivo.")
            return redirect(request.url)

        # Validar formato de archivo
        if not allowed_file(file.filename):
            flash("Formato no permitido. Solo PDF, DOCX o TXT.")
            return redirect(request.url)

        # Guardar archivo con nombre seguro
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Registrar en consola (aquí iría la inserción en BD)
        print({
            "nombre_archivo": filename,
            "tipo_documento": tipo_doc,
            "candidato": candidato,
            "fecha": fecha_doc,
            "fuente": fuente,
            "ruta": save_path,
            "fecha_subida": datetime.now()
        })

        flash("Archivo subido exitosamente.")
        return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import boto3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.static_folder = 'static'
app.config['S3_BUCKET'] = 'lab09-nubes'  # Reemplaza con el nombre de tu bucket de S3
app.config['S3_REGION'] = 'us-east-1'  # Reemplaza con la región de tu bucket de S3

# Configuración de AWS
s3 = boto3.client('s3',
                   aws_access_key_id='AKIAVCYQDEOVCUKXFV6Z',
                   aws_secret_access_key='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',
                   region_name=app.config['S3_REGION']
                   )

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para subir una imagen
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Subir la imagen a S3
    s3.upload_file(filepath, app.config['S3_BUCKET'], filename)

    # Eliminar el archivo local
    os.remove(filepath)

    # Redireccionar a la página principal
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

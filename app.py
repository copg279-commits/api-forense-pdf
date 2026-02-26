import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app) # Esto es magia vital para que tu HTML de GitHub pueda hablar con este servidor

@app.route('/')
def hola():
    return "El cerebro funciona correctamente. Mándame PDFs."

@app.route('/extraer', methods=['POST'])
def extraer_imagenes():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No enviaste ningún archivo'})

    archivo_pdf = request.files['pdf']

    # Leer el PDF directamente desde la memoria (más rápido y seguro)
    doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")

    fotos_encontradas = []

    # Buscar en todas las páginas
    for pagina in range(len(doc)):
        lista_imagenes = doc[pagina].get_images(full=True)

        for img in lista_imagenes:
            referencia = img[0]
            imagen_base = doc.extract_image(referencia)
            bytes_imagen = imagen_base["image"]
            extension = imagen_base["ext"]

            # Convertir la foto a un texto (Base64) para poder enviarla por internet
            texto_foto = base64.b64encode(bytes_imagen).decode('utf-8')
            codigo_final = f"data:image/{extension};base64,{texto_foto}"

            fotos_encontradas.append(codigo_final)

    return jsonify({'total': len(fotos_encontradas), 'imagenes': fotos_encontradas})

# Este es el arranque para el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

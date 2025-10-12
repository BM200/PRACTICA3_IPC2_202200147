
from flask import Flask, jsonify, request
import json
import os

# Inicializar la aplicación Flask
app = Flask(__name__)

# Ruta al archivo JSON que funcionará como nuestra base de datos
INVENTARIO_FILE = 'inventario.json'

# --- Funciones Auxiliares para manejar el JSON ---

def leer_inventario():
    """Lee los datos del archivo JSON."""
    if not os.path.exists(INVENTARIO_FILE):
        return []
    with open(INVENTARIO_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def escribir_inventario(data):
    """Escribe los datos en el archivo JSON."""
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Endpoints de la API REST ---

# Endpoint para OBTENER todos los productos (GET /productos)
@app.route('/productos', methods=['GET'])
def get_productos():
    inventario = leer_inventario()
    return jsonify(inventario)

# Endpoint para OBTENER un producto por su ID (GET /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    inventario = leer_inventario()
    producto = next((p for p in inventario if p['id'] == producto_id), None)
    if producto:
        return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

# Endpoint para CREAR un nuevo producto (POST /productos)
@app.route('/productos', methods=['POST'])
def create_producto():
    nuevo_producto = request.json
    if not nuevo_producto or 'nombre' not in nuevo_producto or 'precio' not in nuevo_producto:
        return jsonify({'error': 'Datos incompletos'}), 400

    inventario = leer_inventario()

    # Asignar un nuevo ID
    nuevo_producto['id'] = max([p['id'] for p in inventario] or [0]) + 1
    
    inventario.append(nuevo_producto)
    escribir_inventario(inventario)
    
    return jsonify(nuevo_producto), 201

# Endpoint para ACTUALIZAR un producto existente (PUT /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    datos_actualizados = request.json
    inventario = leer_inventario()
    
    producto_encontrado = False
    for i, producto in enumerate(inventario):
        if producto['id'] == producto_id:
            # Actualiza el producto manteniendo su ID original
            inventario[i] = {**producto, **datos_actualizados, 'id': producto_id}
            producto_encontrado = True
            break
    
    if not producto_encontrado:
        return jsonify({'error': 'Producto no encontrado'}), 404
        
    escribir_inventario(inventario)
    return jsonify(inventario[i])

# Endpoint para ELIMINAR un producto (DELETE /productos/<id>)
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    inventario = leer_inventario()
    
    producto_original_len = len(inventario)
    inventario_filtrado = [p for p in inventario if p['id'] != producto_id]

    if len(inventario_filtrado) == producto_original_len:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    escribir_inventario(inventario_filtrado)
    return jsonify({'mensaje': 'Producto eliminado correctamente'})

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)


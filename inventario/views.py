# inventario/views.py

import requests
from django.shortcuts import render, redirect

# La URL base de nuestra API en Flask
API_URL = "http://127.0.0.1:5000/productos"

def listar_productos(request):
    """Muestra la lista de todos los productos."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Lanza un error si la petición falla
        productos = response.json()
    except requests.exceptions.RequestException as e:
        # Manejo de error si la API no está disponible
        productos = []
        print(f"Error al conectar con la API: {e}")
    
    return render(request, 'inventario/listar_productos.html', {'productos': productos})

def crear_producto(request):
    """Maneja la creación de un nuevo producto."""
    if request.method == 'POST':
        nuevo_producto = {
            'nombre': request.POST.get('nombre'),
            'categoria': request.POST.get('categoria'),
            'descripcion': request.POST.get('descripcion'),
            'precio': float(request.POST.get('precio')),
            'cantidad': int(request.POST.get('cantidad')),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento')
        }
        try:
            requests.post(API_URL, json=nuevo_producto)
            return redirect('listar_productos')
        except requests.exceptions.RequestException as e:
            print(f"Error al crear producto: {e}")
            # Aquí podrías pasar un mensaje de error a la plantilla
    
    return render(request, 'inventario/formulario_producto.html', {'accion': 'Crear'})

def editar_producto(request, producto_id):
    """Maneja la edición de un producto existente."""
    url_producto = f"{API_URL}/{producto_id}"

    if request.method == 'POST':
        producto_actualizado = {
            'nombre': request.POST.get('nombre'),
            'categoria': request.POST.get('categoria'),
            'descripcion': request.POST.get('descripcion'),
            'precio': float(request.POST.get('precio')),
            'cantidad': int(request.POST.get('cantidad')),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento')
        }
        try:
            requests.put(url_producto, json=producto_actualizado)
            return redirect('listar_productos')
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar producto: {e}")

    # Para el GET, obtenemos los datos actuales para rellenar el formulario
    try:
        response = requests.get(url_producto)
        producto = response.json()
        return render(request, 'inventario/formulario_producto.html', {'accion': 'Editar', 'producto': producto})
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener producto: {e}")
        return redirect('listar_productos')


def eliminar_producto(request, producto_id):
    """Elimina un producto."""
    url_producto = f"{API_URL}/{producto_id}"
    try:
        requests.delete(url_producto)
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar producto: {e}")
    
    return redirect('listar_productos')
import json
import os
from rich.console import Console

console = Console()
BASE_DIR = os.path.dirname(__file__)

# Rutas independientes para cada archivo JSON
PATH_PRODUCTOS = os.path.join(BASE_DIR, "productos.json")
PATH_CLIENTES = os.path.join(BASE_DIR, "clientes.json")
PATH_PEDIDOS = os.path.join(BASE_DIR, "pedidos.json")

# Diccionarios globales en memoria
productos = {}       
clientes = {}        
pedidos = {}         
contador_pedidos = 1 


# --- FUNCIONES DE GUARDADO ---

def guardar_productos():
    """Guarda la información de los productos en su propio archivo JSON."""
    global productos
    try:
        with open(PATH_PRODUCTOS, "w", encoding="utf-8") as f:
            json.dump(list(productos.values()), f, indent=4, ensure_ascii=False)
    except IOError:
        console.print("[red]Error al guardar productos en el disco.[/red]")

def guardar_clientes():
    """Guarda la información de los clientes en su propio archivo JSON."""
    global clientes
    try:
        with open(PATH_CLIENTES, "w", encoding="utf-8") as f:
            json.dump(list(clientes.values()), f, indent=4, ensure_ascii=False)
    except IOError:
        console.print("[red]Error al guardar clientes en el disco.[/red]")

def guardar_pedidos():
    """Guarda las transacciones de pedidos y el estado del contador en su archivo JSON."""
    global pedidos, contador_pedidos
    datos = {
        "pedidos": list(pedidos.values()),
        "contador_pedidos": contador_pedidos
    }
    try:
        with open(PATH_PEDIDOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError:
        console.print("[red]Error al guardar pedidos en el disco.[/red]")


# --- FUNCIONES DE CARGA ---

def cargar_todo():
    """Inicializa todo el sistema leyendo los tres archivos JSON independientes."""
    global productos, clientes, pedidos, contador_pedidos
    
    # Cargar Productos
    if os.path.exists(PATH_PRODUCTOS):
        try:
            with open(PATH_PRODUCTOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
            productos.clear()
            productos.update({p["id_producto"]: p for p in datos})
        except (json.JSONDecodeError, KeyError, TypeError):
            console.print("[yellow]Archivo de productos vacio o corrupto.[/yellow]")

    # Cargar Clientes
    if os.path.exists(PATH_CLIENTES):
        try:
            with open(PATH_CLIENTES, "r", encoding="utf-8") as f:
                datos = json.load(f)
            clientes.clear()
            clientes.update({c["id_cliente"]: c for c in datos})
        except (json.JSONDecodeError, KeyError, TypeError):
            console.print("[yellow]Archivo de clientes vacio o corrupto.[/yellow]")

    # Cargar Pedidos y Contador
    if os.path.exists(PATH_PEDIDOS):
        try:
            with open(PATH_PEDIDOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
            pedidos.clear()
            pedidos.update({pe["id_pedido"]: pe for pe in datos.get("pedidos", [])})
            contador_pedidos = datos.get("contador_pedidos", 1)
        except (json.JSONDecodeError, KeyError, TypeError):
            console.print("[yellow]Archivo de pedidos vacio o corrupto.[/yellow]")
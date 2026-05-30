import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DB_FILE = "data.json"

# ==========================================
# PERSISTENCIA (INTEGRANTE 1)
# ==========================================
def cargar_datos() -> dict:
    """Carga los datos desde el archivo JSON con manejo de errores."""
    if not os.path.exists(DB_FILE):
        return {"productos": [], "clientes": [], "pedidos": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        console.print("[red]Error al leer la base de datos. Se inició un diccionario vacío.[/red]")
        return {"productos": [], "clientes": [], "pedidos": []}

def guardar_datos(datos: dict) -> bool:
    """Guarda el diccionario de datos actual en el archivo JSON."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        console.print("[red]Error crítico: No se pudieron guardar los datos en el disco.[/red]")
        return False

# ==========================================
# CRUD ENTIDADES BÁSICAS (INTEGRANTE 1)
# ==========================================
def crear_producto():
    datos = cargar_datos()
    try:
        id_prod = input("ID Producto: ").strip()
        if any(p["id_producto"] == id_prod for p in datos["productos"]):
            return console.print("[yellow]El ID de producto ya existe.[/yellow]")
        
        nombre = input("Nombre: ").strip()
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
        
        datos["productos"].append({"id_producto": id_prod, "nombre": nombre, "precio": precio, "stock": stock})
        if guardar_datos(datos):
            console.print("[green]Producto registrado con éxito.[/green]")
    except ValueError:
        console.print("[red]Error: El precio y el stock deben ser valores numéricos.[/red]")

def listar_productos():
    datos = cargar_datos()
    if not datos["productos"]:
        return console.print("[yellow]No hay productos registrados.[/yellow]")
    
    tabla = Table(title="Inventario de Productos")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Precio", style="green")
    tabla.add_column("Stock", style="blue")
    
    for p in datos["productos"]:
        tabla.add_row(p["id_producto"], p["nombre"], f"${p['precio']:.2f}", str(p["stock"]))
    console.print(tabla)

def actualizar_producto():
    datos = cargar_datos()
    id_prod = input("ID del producto a actualizar: ").strip()
    for p in datos["productos"]:
        if p["id_producto"] == id_prod:
            try:
                p["nombre"] = input(f"Nuevo nombre ({p['nombre']}): ").strip() or p["nombre"]
                precio_in = input(f"Nuevo precio (${p['precio']}): ").strip()
                p["precio"] = float(precio_in) if precio_in else p["precio"]
                stock_in = input(f"Nuevo stock ({p['stock']}): ").strip()
                p["stock"] = int(stock_in) if stock_in else p["stock"]
                
                guardar_datos(datos)
                return console.print("[green]Producto actualizado correctamente.[/green]")
            except ValueError:
                return console.print("[red]Error: Datos numéricos inválidos.[/red]")
    console.print("[red]Producto no encontrado.[/red]")

def eliminar_producto():
    datos = cargar_datos()
    id_prod = input("ID del producto a eliminar: ").strip()
    original_len = len(datos["productos"])
    datos["productos"] = [p for p in datos["productos"] if p["id_producto"] != id_prod]
    
    if len(datos["productos"]) < original_len:
        guardar_datos(datos)
        console.print("[green]Producto eliminado exitosamente.[/green]")
    else:
        console.print("[red]Producto no encontrado.[/red]")

def buscar_producto_nombre():
    datos = cargar_datos()
    termino = input("Buscar producto por nombre: ").strip().lower()
    resultados = [p for p in datos["productos"] if termino in p["nombre"].lower()]
    
    if not resultados:
        return console.print("[yellow]No se encontraron productos coincidentes.[/yellow]")
    
    tabla = Table(title="Resultados de Búsqueda")
    tabla.add_column("ID")
    tabla.add_column("Nombre")
    tabla.add_column("Precio")
    tabla.add_column("Stock")
    for p in resultados:
        tabla.add_row(p["id_producto"], p["nombre"], f"${p['precio']:.2f}", str(p["stock"]))
    console.print(tabla)

# --- CRUD CLIENTES ---
def crear_cliente():
    datos = cargar_datos()
    id_cli = input("ID Cliente: ").strip()
    if any(c["id_cliente"] == id_cli for c in datos["clientes"]):
        return console.print("[yellow]El ID de cliente ya existe.[/yellow]")
    
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    
    datos["clientes"].append({"id_cliente": id_cli, "nombre": nombre, "email": email})
    if guardar_datos(datos):
        console.print("[green]Cliente registrado con éxito.[/green]")

def listar_clientes():
    datos = cargar_datos()
    if not datos["clientes"]:
        return console.print("[yellow]No hay clientes registrados.[/yellow]")
    
    tabla = Table(title="Lista de Clientes")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Email", style="green")
    
    for c in datos["clientes"]:
        tabla.add_row(c["id_cliente"], c["nombre"], c["email"])
    console.print(tabla)

def actualizar_cliente():
    datos = cargar_datos()
    id_cli = input("ID del cliente a actualizar: ").strip()
    for c in datos["clientes"]:
        if c["id_cliente"] == id_cli:
            c["nombre"] = input(f"Nuevo nombre ({c['nombre']}): ").strip() or c["nombre"]
            c["email"] = input(f"Nuevo email ({c['email']}): ").strip() or c["email"]
            guardar_datos(datos)
            return console.print("[green]Cliente actualizado correctamente.[/green]")
    console.print("[red]Cliente no encontrado.[/red]")

def eliminar_cliente():
    datos = cargar_datos()
    id_cli = input("ID del cliente a eliminar: ").strip()
    original_len = len(datos["clientes"])
    datos["clientes"] = [c for c in datos["clientes"] if c["id_cliente"] != id_cli]
    
    if len(datos["clientes"]) < original_len:
        guardar_datos(datos)
        console.print("[green]Cliente eliminado exitosamente.[/green]")
    else:
        console.print("[red]Cliente no encontrado.[/red]")

# ==========================================
# TRANSACCIONES Y VALIDACIÓN (INTEGRANTE 2)
# ==========================================
def crear_pedido():
    datos = cargar_datos()
    id_cli = input("ID del Cliente que compra: ").strip()
    
    # Validar si el cliente existe usando diccionarios mapeados para velocidad
    cliente_existe = any(c["id_cliente"] == id_cli for c in datos["clientes"])
    if not cliente_existe:
        return console.print("[red]Error: El cliente no existe. Regístrelo primero.[/red]")
        
    lista_productos_compra = []
    mapa_productos = {p["id_producto"]: p for p in datos["productos"]}
    
    console.print("[blue]Ingrese los IDs de los productos (deje vacío y presione Enter para terminar):[/blue]")
    while True:
        id_prod = input("-> ID Producto: ").strip()
        if not id_prod:
            break
        if id_prod not in mapa_productos:
            console.print("[yellow]Producto no encontrado en el inventario.[/yellow]")
            continue
        if mapa_productos[id_prod]["stock"] <= 0:
            console.print("[red]Sin stock disponible para este producto.[/red]")
            continue
            
        lista_productos_compra.append(id_prod)
        mapa_productos[id_prod]["stock"] -= 1  # Restar stock temporalmente
        console.print(f"[green]Agregado: {mapa_productos[id_prod]['nombre']}[/green]")

    if not lista_productos_compra:
        return console.print("[yellow]Pedido cancelado: No se añadieron productos.[/yellow]")
        
    id_ped = str(len(datos["pedidos"]) + 1)
    nuevo_pedido = {
        "id_pedido": id_ped,
        "id_cliente": id_cli,
        "id_productos": lista_productos_compra,
        "fecha_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    datos["pedidos"].append(nuevo_pedido)
    if guardar_datos(datos):
        console.print(Panel(f"[bold green]Pedido #{id_ped} creado con éxito.[/bold green]"))

# ==========================================
# REPORTES Y MENÚS (INTEGRANTE 3)
# ==========================================
def historial_pedidos_cliente():
    datos = cargar_datos()
    id_cli = input("ID del cliente a consultar: ").strip()
    
    pedidos_cliente = [p for p in datos["pedidos"] if p["id_cliente"] == id_cli]
    if not pedidos_cliente:
        return console.print("[yellow]Este cliente no registra pedidos en el historial.[/yellow]")
        
    mapa_prod = {p["id_producto"]: p for p in datos["productos"]}
    
    tabla = Table(title=f"Historial de Pedidos - Cliente: {id_cli}")
    tabla.add_column("ID Pedido", style="cyan")
    tabla.add_column("Fecha", style="blue")
    tabla.add_column("Artículos Comprados", style="magenta")
    
    for ped in pedidos_cliente:
        nombres_productos = [mapa_prod[i]["nombre"] for i in ped["id_productos"] if i in mapa_prod]
        tabla.add_row(ped["id_pedido"], ped["fecha_pedido"], ", ".join(nombres_productos))
    console.print(tabla)

def reporte_total_vendido():
    datos = cargar_datos()
    mapa_precios = {p["id_producto"]: p["precio"] for p in datos["productos"]}
    
    total_general = 0.0
    for ped in datos["pedidos"]:
        for id_prod in ped["id_productos"]:
            total_general += mapa_precios.get(id_prod, 0.0)
            
    console.print(Panel(f"[bold green]REPORTE GENERAL DE VENTAS[/bold green]\nTotal recaudado: [bold]${total_general:.2f}[/bold]", expand=False))

def menu_principal():
    while True:
        console.print("\n[bold purple]=== SISTEMA DE GESTIÓN DE TIENDA ===[/bold purple]")
        print("1. Registrar Producto  | 5. Registrar Cliente")
        print("2. Listar Productos    | 6. Listar Clientes")
        print("3. Actualizar Producto | 7. Actualizar Cliente")
        print("4. Eliminar Producto   | 8. Eliminar Cliente")
        print("9. Buscar por Nombre   | 10. CREAR NUEVO PEDIDO")
        print("11. Historial Cliente  | 12. REPORTES DE VENTAS")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        print("-" * 40)
        
        if opcion == "1": 
            crear_producto()
        elif opcion == "2": 
            listar_productos()
        elif opcion == "3": 
            actualizar_producto()
        elif opcion == "4": 
            eliminar_producto()
        elif opcion == "5": 
            crear_cliente()
        elif opcion == "6": 
            listar_clientes()
        elif opcion == "7": 
            actualizar_cliente()
        elif opcion == "8": 
            eliminar_cliente()
        elif opcion == "9": 
            buscar_producto_nombre()
        elif opcion == "10": 
            crear_pedido()
        elif opcion == "11": 
            historial_pedidos_cliente()
        elif opcion == "12": 
            reporte_total_vendido()
        elif opcion == "0":
            console.print("[bold yellow]Saliendo del sistema...[/bold yellow]")
            break
        else:
            console.print("[red]Opción no válida. Intente de nuevo.[/red]")

if __name__ == "__main__":
    menu_principal()
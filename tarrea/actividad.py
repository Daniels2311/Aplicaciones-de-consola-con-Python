import json
import os
from datetime import datetime

# Importaciones obligatorias de la librería rich para cumplir los estándares visuales
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt

console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(BASE_DIR, "tienda.json")

# ==========================================
# 1. GESTIÓN DE ARCHIVOS Y ERRORES (JSON)
# ==========================================
def inicializar_base_datos():
    """Crea la estructura inicial del archivo JSON si no existe."""
    if not os.path.exists(ARCHIVO_DB):
        estructura_inicial = {"productos": [], "clientes": [], "pedidos": []}
        guardar_datos(estructura_inicial)


def cargar_datos():
    """Lee y deserializa el archivo JSON con manejo de errores robusto."""
    inicializar_base_datos()
    try:
        with open(ARCHIVO_DB, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        console.print("[bold red]❌ Error:[/bold red] Archivo de datos no encontrado. Inicializando base vacía.")
        return {"productos": [], "clientes": [], "pedidos": []}
    except json.JSONDecodeError:
        console.print("[bold red]❌ Error CORRUPCIÓN:[/bold red] El archivo JSON está dañado o mal estructurado.")
        return {"productos": [], "clientes": [], "pedidos": []}


def guardar_datos(datos):
    """Serializa y escribe de forma segura los datos en el archivo JSON."""
    try:
        with open(ARCHIVO_DB, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        console.print(f"[bold red]❌ Error de escritura en disco:[/bold red] {e}")


# ==========================================
# 2. OPERACIONES CRUD: PRODUCTOS
# ==========================================
def crear_producto():
    datos = cargar_datos()
    console.print("\n[bold cyan]🏬 Registrar Nuevo Producto[/bold cyan]")
    id_prod = Prompt.ask("Ingrese ID del Producto (ej. P001)")

    if any(p["id_producto"] == id_prod for p in datos["productos"]):
        console.print("[bold red]❌ Error: El ID del producto ya existe.[/bold red]")
        return

    nombre = Prompt.ask("Nombre del producto")
    precio = FloatPrompt.ask("Precio del producto")
    stock = IntPrompt.ask("Cantidad en stock")

    nuevo_prod = {"id_producto": id_prod, "nombre": nombre, "precio": precio, "stock": stock}
    datos["productos"].append(nuevo_prod)
    guardar_datos(datos)
    console.print(f"[bold green]✅ Producto '{nombre}' creado exitosamente.[/bold green]")


def leer_productos():
    datos = cargar_datos()
    if not datos["productos"]:
        console.print("[yellow]⚠️ No hay productos registrados.[/yellow]")
        return

    tabla = Table(title="Lista de Productos Disponibles", header_style="bold magenta")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Nombre", justify="left")
    tabla.add_column("Precio", justify="right")
    tabla.add_column("Stock", justify="center")

    for p in datos["productos"]:
        color_stock = "green" if p["stock"] > 3 else "red"
        tabla.add_row(p["id_producto"], p["nombre"], f"${p['precio']:.2f}", f"[{color_stock}]{p['stock']}[/{color_stock}]")
    console.print(tabla)


def actualizar_producto():
    datos = cargar_datos()
    id_prod = Prompt.ask("\nIngrese el ID del producto que desea actualizar")
    producto = next((p for p in datos["productos"] if p["id_producto"] == id_prod), None)

    if not producto:
        console.print("[bold red]❌ Producto no encontrado.[/bold red]")
        return

    console.print(f"Modificando: [bold yellow]{producto['nombre']}[/bold yellow] (Deje vacío para mantener actual)")
    nuevo_nombre = Prompt.ask("Nuevo Nombre", default=producto["nombre"])
    nuevo_precio = FloatPrompt.ask("Nuevo Precio", default=producto["precio"])
    nuevo_stock = IntPrompt.ask("Nuevo Stock", default=producto["stock"])

    producto["nombre"] = nuevo_nombre
    producto["precio"] = nuevo_precio
    producto["stock"] = nuevo_stock
    guardar_datos(datos)
    console.print("[bold green]🔄 Producto actualizado correctamente.[/bold green]")


def eliminar_producto():
    datos = cargar_datos()
    id_prod = Prompt.ask("\nIngrese el ID del producto a eliminar")
    producto = next((p for p in datos["productos"] if p["id_producto"] == id_prod), None)

    if not producto:
        console.print("[bold red]❌ El producto no existe.[/bold red]")
        return

    datos["productos"].remove(producto)
    guardar_datos(datos)
    console.print("[bold green]🗑️ Producto eliminado exitosamente de la base de datos.[/bold green]")


def filtrar_productos_por_nombre():
    datos = cargar_datos()
    busqueda = Prompt.ask("\nEscriba el nombre o parte del nombre a buscar")
    resultados = [p for p in datos["productos"] if busqueda.lower() in p["nombre"].lower()]

    if not resultados:
        console.print("[bold yellow]🔍 No se encontraron coincidencias.[/bold yellow]")
        return

    tabla = Table(title=f"Resultados para: '{busqueda}'", header_style="bold cyan")
    tabla.add_column("ID")
    tabla.add_column("Nombre")
    tabla.add_column("Precio")
    for p in resultados:
        tabla.add_row(p["id_producto"], p["nombre"], f"${p['precio']:.2f}")
    console.print(tabla)


# ==========================================
# 3. OPERACIONES CRUD: CLIENTES
# ==========================================
def crear_cliente():
    datos = cargar_datos()
    console.print("\n[bold cyan]👤 Registrar Nuevo Cliente[/bold cyan]")
    id_cli = Prompt.ask("ID Cliente (ej. C001)")

    if any(c["id_cliente"] == id_cli for c in datos["clientes"]):
        console.print("[bold red]❌ El ID de cliente ya está registrado.[/bold red]")
        return

    nombre = Prompt.ask("Nombre completo")
    email = Prompt.ask("Correo electrónico")

    nuevo_cli = {"id_cliente": id_cli, "nombre": nombre, "email": email}
    datos["clientes"].append(nuevo_cli)
    guardar_datos(datos)
    console.print(f"[bold green]✅ Cliente '{nombre}' registrado.[/bold green]")


def leer_clientes():
    datos = cargar_datos()
    if not datos["clientes"]:
        console.print("[yellow]⚠️ No hay clientes registrados.[/yellow]")
        return
    tabla = Table(title="Directorio de Clientes", header_style="bold blue")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Nombre")
    tabla.add_column("Email")
    for c in datos["clientes"]:
        tabla.add_row(c["id_cliente"], c["nombre"], c["email"])
    console.print(tabla)


# ==========================================
# 4. LÓGICA RELACIONAL: PEDIDOS Y REPORTES
# ==========================================
def crear_pedido():
    datos = cargar_datos()
    console.print("\n[bold cyan]🛒 Generar Nueva Orden de Pedido[/bold cyan]")

    id_cliente = Prompt.ask("ID del Cliente que compra")
    cliente = next((c for c in datos["clientes"] if c["id_cliente"] == id_cliente), None)
    if not cliente:
        console.print("[bold red]❌ Error: El cliente no existe. Regístrelo primero.[/bold red]")
        return

    leer_productos()
    ids_entrada = Prompt.ask("Ingrese los IDs de productos separados por coma (ej: P001,P002)")
    lista_ids = [id_arr.strip() for id_arr in ids_entrada.split(",") if id_arr.strip()]

    if not lista_ids:
        console.print("[bold red]❌ No ingresó ningún ID válido.[/bold red]")
        return

    productos_seleccionados = []
    for id_p in lista_ids:
        prod = next((p for p in datos["productos"] if p["id_producto"] == id_p), None)
        if not prod:
            console.print(f"[bold red]❌ Producto {id_p} no existe. Operación abortada.[/bold red]")
            return
        if prod["stock"] <= 0:
            console.print(f"[bold red]❌ El producto '{prod['nombre']}' no tiene stock.[/bold red]")
            return
        productos_seleccionados.append(prod)

    for prod in productos_seleccionados:
        prod["stock"] -= 1

    id_pedido = f"PED-{len(datos['pedidos']) + 1:03d}"
    nuevo_pedido = {
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "id_productos": lista_ids,
        "fecha_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    datos["pedidos"].append(nuevo_pedido)
    guardar_datos(datos)
    console.print(f"[bold green]🎉 Pedido {id_pedido} procesado para {cliente['nombre']}. Stock actualizado.[/bold green]")


def ver_pedidos():
    datos = cargar_datos()
    if not datos["pedidos"]:
        console.print("[yellow]⚠️ No hay pedidos registrados.[/yellow]")
        return

    tabla = Table(title="Pedidos Registrados", header_style="bold gold1")
    tabla.add_column("ID Pedido", justify="center")
    tabla.add_column("Cliente")
    tabla.add_column("Fecha y Hora")
    tabla.add_column("Artículos (IDs)")

    for pedido in datos["pedidos"]:
        cliente_nombre = next((c["nombre"] for c in datos["clientes"] if c["id_cliente"] == pedido["id_cliente"]), pedido["id_cliente"])
        tabla.add_row(
            pedido["id_pedido"],
            cliente_nombre,
            pedido["fecha_pedido"],
            ", ".join(pedido["id_productos"])
        )
    console.print(tabla)


def ver_pedidos_cliente():
    datos = cargar_datos()
    id_cliente = Prompt.ask("\nIngrese el ID del cliente para consultar su historial")
    historial = [p for p in datos["pedidos"] if p["id_cliente"] == id_cliente]

    if not historial:
        console.print("[yellow]ℹ️ El cliente no registra compras anteriores.[/yellow]")
        return

    tabla = Table(title=f"Historial de Compras - Cliente {id_cliente}", header_style="bold yellow")
    tabla.add_column("ID Pedido")
    tabla.add_column("Fecha y Hora")
    tabla.add_column("Artículos (IDs)")
    for p in historial:
        tabla.add_row(p["id_pedido"], p["fecha_pedido"], ", ".join(p["id_productos"]))
    console.print(tabla)


def reporte_ventas_totales():
    datos = cargar_datos()
    precios = {p["id_producto"]: p["precio"] for p in datos["productos"]}
    total = sum(precios.get(id_p, 0) for ped in datos["pedidos"] for id_p in ped["id_productos"])

    panel_contenido = (
        f"[bold]Órdenes concretadas:[/bold] {len(datos['pedidos'])}\n"
        f"[bold]Ingresos Totales Brutos:[/bold] [green]${total:,.2f}[/green]"
    )
    console.print(Panel(panel_contenido, title="📊 RETO FINAL: REPORTE DE VENTAS", expand=False, border_style="green"))


# ==========================================
# 5. MENÚS INTERACTIVOS DE NAVEGACIÓN
# ==========================================
def menu_productos():
    while True:
        console.print("\n[bold magenta]📦 Menú de Gestión de Productos[/bold magenta]")
        console.print("1. Crear Producto")
        console.print("2. Ver Productos")
        console.print("3. Actualizar Producto")
        console.print("4. Eliminar Producto")
        console.print("5. Filtrar por Nombre")
        console.print("6. Volver al Menú Principal")

        opcion = IntPrompt.ask("Seleccione una opción", choices=[str(i) for i in range(1, 7)])

        if opcion == 1:
            crear_producto()
        elif opcion == 2:
            leer_productos()
        elif opcion == 3:
            actualizar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            filtrar_productos_por_nombre()
        elif opcion == 6:
            break


def menu_clientes():
    while True:
        console.print("\n[bold blue]👥 Menú de Gestión de Clientes[/bold blue]")
        console.print("1. Crear Cliente")
        console.print("2. Ver Clientes")
        console.print("3. Volver al Menú Principal")
        opcion = IntPrompt.ask("Seleccione una opción", choices=["1", "2", "3"])
        if opcion == 1:
            crear_cliente()
        elif opcion == 2:
            leer_clientes()
        elif opcion == 3:
            break


def menu_pedidos():
    while True:
        console.print("\n[bold cyan]🛍️ Menú de Gestión de Pedidos[/bold cyan]")
        console.print("1. Crear Pedido")
        console.print("2. Ver Pedidos")
        console.print("3. Ver Pedidos por Cliente")
        console.print("4. Reporte de Ventas Totales")
        console.print("5. Volver al Menú Principal")
        opcion = IntPrompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
        if opcion == 1:
            crear_pedido()
        elif opcion == 2:
            ver_pedidos()
        elif opcion == 3:
            ver_pedidos_cliente()
        elif opcion == 4:
            reporte_ventas_totales()
        elif opcion == 5:
            break


def menu_principal():
    while True:
        console.print("\n[bold green]🏪 Menú Principal - Gestión de Tienda Virtual[/bold green]")
        console.print("1. Gestión de Productos")
        console.print("2. Gestión de Clientes")
        console.print("3. Gestión de Pedidos")
        console.print("4. Salir")
        opcion = IntPrompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
        if opcion == 1:
            menu_productos()
        elif opcion == 2:
            menu_clientes()
        elif opcion == 3:
            menu_pedidos()
        elif opcion == 4:
            console.print("[bold yellow]👋 ¡Hasta luego![/bold yellow]")
            break


if __name__ == "__main__":
    menu_principal()

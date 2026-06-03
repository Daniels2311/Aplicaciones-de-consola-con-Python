from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import data.persistencia as db

console = Console()

def registrar_producto():
    id_producto = Prompt.ask("ID del Producto").strip()
    if id_producto in db.productos:
        console.print("[yellow]El producto ya existe en el inventario.[/yellow]")
        return

    nombre = Prompt.ask("Nombre del producto")
    marca = Prompt.ask("Marca")
    categoria = Prompt.ask("Categoria")
    try:
        precio = float(Prompt.ask("Precio"))
        stock = int(Prompt.ask("Stock Inicial"))
        if precio < 0 or stock < 0:
            raise ValueError
    except ValueError:
        console.print("[red]Valores invalidos. El precio y stock deben ser mayores o iguales a 0.[/red]")
        return

    db.productos[id_producto] = {
        "id_producto": id_producto, "nombre": nombre, "marca": marca,
        "categoria": categoria, "precio": precio, "stock": stock
    }
    db.guardar_productos()
    console.print("[green]Producto registrado con exito.[/green]")

def listar_productos():
    if not db.productos:
        console.print("[yellow]No hay productos registrados en la tienda.[/yellow]")
        return

    tabla = Table(title="Inventario General de Productos")
    tabla.add_column("ID", style="cyan"); tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Marca", style="green"); tabla.add_column("Categoria", style="blue")
    tabla.add_column("Precio", style="yellow"); tabla.add_column("Stock", style="white")

    for p in db.productos.values():
        tabla.add_row(p["id_producto"], p["nombre"], p["marca"], p["categoria"], f"${p['precio']:.2f}", str(p["stock"]))
    console.print(tabla)

def actualizar_producto():
    id_producto = Prompt.ask("ID del producto a actualizar").strip()
    if id_producto not in db.productos:
        console.print("[red]Producto no encontrado.[/red]")
        return

    p = db.productos[id_producto]
    p["nombre"] = Prompt.ask(f"Nuevo nombre ({p['nombre']})", default=p['nombre'])
    p["marca"] = Prompt.ask(f"Nueva marca ({p['marca']})", default=p['marca'])
    p["categoria"] = Prompt.ask(f"Nueva categoria ({p['categoria']})", default=p['categoria'])
    try:
        p["precio"] = float(Prompt.ask(f"Nuevo precio (${p['precio']:.2f})", default=str(p['precio'])))
        p["stock"] = int(Prompt.ask(f"Nuevo stock ({p['stock']})", default=str(p['stock'])))
    except ValueError:
        console.print("[red]Error: Entradas numericas invalidas.[/red]")
        return

    db.guardar_productos()
    console.print("[green]Producto actualizado correctamente.[/green]")

def eliminar_producto():
    id_producto = Prompt.ask("ID del producto a eliminar").strip()
    if id_producto not in db.productos:
        console.print("[red]Producto no encontrado.[/red]")
        return

    for ped in db.pedidos.values():
        if id_producto in ped["id_productos"]:
            console.print("[red]Error: No se puede eliminar. El producto esta vinculado a un historial de pedidos.[/red]")
            return

    del db.productos[id_producto]
    db.guardar_productos()
    console.print("[green]Producto eliminado exitosamente.[/green]")

def buscar_producto_por_nombre():
    termino = Prompt.ask("Ingrese el nombre o termino a buscar").strip().lower()
    resultados = [p for p in db.productos.values() if termino in p["nombre"].lower()]

    if not resultados:
        console.print("[yellow]No se encontraron productos coincidentes.[/yellow]")
        return

    tabla = Table(title="Resultados de Busqueda")
    tabla.add_column("ID", style="cyan"); tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Marca", style="green"); tabla.add_column("Precio", style="yellow")
    tabla.add_column("Stock", style="white")
    for p in resultados:
        tabla.add_row(p["id_producto"], p["nombre"], p["marca"], f"${p['precio']:.2f}", str(p["stock"]))
    console.print(tabla)

def comparar_productos():
    id1 = Prompt.ask("ID del primer producto").strip()
    id2 = Prompt.ask("ID del segundo producto").strip()

    if id1 not in db.productos or id2 not in db.productos:
        console.print("[red]Uno o ambos productos no existen.[/red]")
        return

    p1, p2 = db.productos[id1], db.productos[id2]
    tabla = Table(title="Comparativa de Atributos")
    tabla.add_column("Caracteristica", style="cyan")
    tabla.add_column(p1["nombre"], style="magenta"); tabla.add_column(p2["nombre"], style="blue")

    tabla.add_row("Precio", f"${p1['precio']:.2f}", f"${p2['precio']:.2f}")
    tabla.add_row("Marca", p1["marca"], p2["marca"])
    tabla.add_row("Categoria", p1["categoria"], p2["categoria"])
    tabla.add_row("Stock Disponible", str(p1["stock"]), str(p2["stock"]))
    console.print(tabla)
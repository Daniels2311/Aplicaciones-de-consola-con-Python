from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import data.persistencia as db

console = Console()

def crear_pedido():
    """Genera una transacción asociando un cliente con un producto y la cantidad exacta que desea comprar."""
    id_cliente = Prompt.ask("ID del cliente comprador").strip()
    if id_cliente not in db.clientes:
        console.print("[red]Error: El cliente no esta registrado en el sistema.[/red]")
        return

    id_prod = Prompt.ask("ID del producto a comprar").strip()
    if id_prod not in db.productos:
        console.print(f"[red]Error: El producto '{id_prod}' no existe.[/red]")
        return

    producto = db.productos[id_prod]

    # Validamos que el producto tenga existencias antes de preguntar la cantidad
    if producto["stock"] <= 0:
        console.print(f"[red]Error: El producto '{producto['nombre']}' no tiene stock disponible.[/red]")
        return

    # Validamos que el usuario ingrese un número entero válido y positivo para la cantidad
    try:
        cantidad = int(Prompt.ask(f"Cantidad que desea llevar (Stock disponible: {producto['stock']})"))
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Error: La cantidad debe ser un numero entero mayor a 0.[/red]")
        return

    # Verificamos si hay suficiente stock para cubrir la demanda
    if cantidad > producto["stock"]:
        console.print(f"[red]Error: No hay suficiente stock. Solo quedan {producto['stock']} unidades.[/red]")
        return

    # Calculamos el total multiplicando el precio unitario por la cantidad solicitada
    total_compra = producto["precio"] * cantidad

    # Descontamos la cantidad exacta del inventario global
    producto["stock"] -= cantidad

    id_pedido_str = str(db.contador_pedidos)
    
    # Guardamos el registro guardando tanto el ID del producto como la cantidad procesada
    db.pedidos[id_pedido_str] = {
        "id_pedido": id_pedido_str,
        "id_cliente": id_cliente,
        "id_producto": id_prod,
        "cantidad": cantidad,
        "total": total_compra,
        "fecha_pedido": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    db.contador_pedidos += 1
    
    # Sincronizamos los cambios en los archivos JSON correspondientes
    db.guardar_productos()
    db.guardar_pedidos()
    
    console.print(Panel(
        f"[bold green]Pedido #{id_pedido_str} creado con exito.[/bold green]\n"
        f"Articulo: [bold white]{producto['nombre']}[/bold white] x{cantidad}\n"
        f"Total transaccion: [bold yellow]${total_compra:.2f}[/bold yellow]"
    ))


def ver_historial_cliente():
    """Consulta la relación histórica de órdenes de compra ligadas a un usuario mostrando cantidades y totales."""
    id_cliente = Prompt.ask("ID del cliente a consultar").strip()
    if id_cliente not in db.clientes:
        console.print("[red]El cliente no existe.[/red]")
        return

    pedidos_cliente = [p for p in db.pedidos.values() if p["id_cliente"] == id_cliente]
    if not pedidos_cliente:
        console.print("[yellow]Este cliente no registra operaciones en el historial.[/yellow]")
        return

    tabla = Table(title=f"Historial de Compras - Cliente: {db.clientes[id_cliente]['nombre']}")
    tabla.add_column("ID Pedido", style="cyan")
    tabla.add_column("Fecha", style="blue")
    tabla.add_column("Producto (Cant.)", style="magenta")
    tabla.add_column("Total Pagado", style="yellow")

    for ped in pedidos_cliente:
        # Buscamos el nombre del producto en el inventario; si fue eliminado, muestra el ID
        id_p = ped.get("id_producto")
        nombre_prod = db.productos[id_p]["nombre"] if id_p in db.productos else f"Producto ID: {id_p}"
        
        cant = ped.get("cantidad", 1)
        total = ped.get("total", 0.0)
        
        tabla.add_row(
            ped["id_pedido"], 
            ped["fecha_pedido"], 
            f"{nombre_prod} (x{cant})", 
            f"${total:.2f}"
        )
    console.print(tabla)
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import data.persistencia as db

console = Console()

def registrar_cliente():
    id_cliente = Prompt.ask("ID del Cliente").strip()
    if id_cliente in db.clientes:
        console.print("[yellow]El ID del cliente ya esta registrado.[/yellow]")
        return

    nombre = Prompt.ask("Nombre Completo")
    email = Prompt.ask("Email")

    for c in db.clientes.values():
        if c["email"].lower() == email.lower():
            console.print("[red]Error: Ese correo electronico ya esta asignado a otro cliente.[/red]")
            return

    db.clientes[id_cliente] = {"id_cliente": id_cliente, "nombre": nombre, "email": email}
    db.guardar_clientes()
    console.print("[green]Cliente registrado de manera exitosa.[/green]")

def listar_clientes():
    if not db.clientes:
        console.print("[yellow]No existen clientes registrados.[/yellow]")
        return

    tabla = Table(title="Registro de Clientes")
    tabla.add_column("ID", style="cyan"); tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Email", style="green")

    for c in db.clientes.values():
        tabla.add_row(c["id_cliente"], c["nombre"], c["email"])
    console.print(tabla)
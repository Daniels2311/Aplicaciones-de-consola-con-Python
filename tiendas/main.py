import sys
from rich.console import Console
from rich.prompt import Prompt

sys.stdout.reconfigure(encoding='utf-8')
console = Console()

# Importaciones de los nuevos módulos independientes
import data.persistencia as db
from modulos.menu import mostrar_menu
import modulos.productos as prod
import modulos.clientes as cl
import modulos.pedidos as pe

def main():
    db.cargar_todo()
    while True:
        mostrar_menu()
        opcion = Prompt.ask("Seleccione una opcion", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        
        if opcion == "1": prod.registrar_producto()
        elif opcion == "2": prod.listar_productos()
        elif opcion == "3": prod.actualizar_producto()
        elif opcion == "4": prod.eliminar_producto()
        elif opcion == "5": prod.buscar_producto_por_nombre()
        elif opcion == "6": cl.registrar_cliente()
        elif opcion == "7": cl.listar_clientes()
        elif opcion == "8": pe.crear_pedido()
        elif opcion == "9": pe.ver_historial_cliente()
        elif opcion == "10": prod.comparar_productos()
        elif opcion == "0":
            console.print("[bold yellow]Todos los archivos JSON guardados de forma segura. Saliendo...[/bold yellow]")
            break

if __name__ == "__main__":
    main()
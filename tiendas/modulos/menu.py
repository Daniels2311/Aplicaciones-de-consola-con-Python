from rich.console import Console

console = Console()

def mostrar_menu():
    console.print("\n[bold purple]=== SISTEMA DE GESTIÓN ===[/bold purple]\n"
                "1. Registrar Producto   | 6. Registrar Cliente\n"
                "2. Lista de Productos     | 7. Lista de Clientes\n"
                "3. Actualizar Producto  | 8. Crear Nuevo Pedido\n"
                "4. Eliminar Producto    | 9. Historial Pedidos Cliente\n"
                "5. Buscar por Nombre    | 10. Comparar Dos Productos\n"
                "0. Salir")
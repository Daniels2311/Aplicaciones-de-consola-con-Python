⚙️ 1. Importaciones y Configuración Inicial
•	📁 import json: Lee y escribe archivos en formato JSON para almacenar datos estructurados.
•	💻 import os: Interactúa con el sistema operativo para manejar rutas de archivos.
•	🎨 from rich.console import Console: Muestra texto con estilos y colores en la terminal.
•	📍 BASE_DIR = os.path.dirname(__file__): Obtiene automáticamente la ruta de la carpeta del script.
•	🔄 Prevención: Evita errores de "archivo no encontrado" al cambiar de computadora.
📁 2. Rutas de Archivos y Estructuras en Memoria
•	🗺️ Rutas: PATH_PRODUCTOS, PATH_CLIENTES y PATH_PEDIDOS combinan la carpeta base con los archivos JSON.
•	🧠 Memoria RAM: productos, clientes y pedidos son diccionarios globales de acceso rápido.
•	🔢 contador_pedidos = 1: Variable global para asignar un número secuencial único a cada pedido.
💾 3. Funciones de Guardado (guardar_...)
Transforman los datos de la memoria RAM en archivos de texto dentro del disco duro.
•	📋 guardar_productos() y guardar_clientes():
o	🔄 Convierten los diccionarios en listas limpias usando list(valores).
o	✍️ Usan json.dump con indent=4 para que el archivo sea legible.
o	🔤 Aplican ensure_ascii=False para permitir tildes y la letra "ñ".
o	⚠️ Usan except IOError para atrapar errores si el disco está protegido o lleno.
•	📦 guardar_pedidos():
o	🔄 Guarda la lista de pedidos y el estado actual del contador.
o	🧠 Garantiza que el programa recuerde el último número de pedido al reiniciar.
📥 4. Función de Carga (cargar_todo())
Busca los archivos JSON en el disco duro y mueve la información a la memoria RAM al arrancar.
•	🌐 global: Avisa a Python que modificará las variables externas.
•	🔍 if os.path.exists: Verifica si el archivo existe para evitar fallos si es el primer arranque.
•	📖 with open(..., "r"): Abre los archivos en modo de solo lectura.
•	🧹 clear(): Limpia los diccionarios para no duplicar datos viejos.
•	⚡ update(): Transforma la lista JSON en diccionario usando compresión de diccionarios para búsquedas inmediatas.
•	⏱️ datos.get(): Extrae el contador de pedidos o usa el número 1 por defecto.
•	🛠️ except: Atrapa archivos corruptos o mal escritos y avisa al usuario sin detener el programa.
Si lo deseas, puedo ayudarte a avanzar con tu código mediante las siguientes opciones:
•	Escribir el código Python completo basado exactamente en esta estructura de funciones.
•	Agregar validaciones de datos para evitar que se guarden productos sin precio o clientes sin identificación.

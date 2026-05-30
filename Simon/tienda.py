import json
from datetime import datetime

# =====================================================================
# ENTIDADES (Modelos de datos)
# =====================================================================

class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

class Cliente:
    def __init__(self, id_cliente, nombre, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "email": self.email
        }

class Pedido:
    def __init__(self, id_pedido, id_cliente, id_productos, fecha_pedido=None):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_productos = id_productos  # Lista de IDs de productos
        self.fecha_pedido = fecha_pedido if fecha_pedido else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "id_productos": self.id_productos,
            "fecha_pedido": self.fecha_pedido
        }

# =====================================================================
# SISTEMA DE GESTIÓN (Lógica de Negocio / CRUD)
# =====================================================================

class SistemaGestion:
    def __init__(self):
        self.productos = {}  # {id_producto: Objeto Producto}
        self.clientes = {}   # {id_cliente: Objeto Cliente}
        self.pedidos = {}    # {id_pedido: Objeto Pedido}
        self.contador_pedidos = 1

    # -----------------------------------------------------------------
    # CRUD PRODUCTOS
    # -----------------------------------------------------------------
    def crear_producto(self, id_producto, nombre, precio, stock):
        if id_producto in self.productos:
            print(f"[ERROR] El producto con ID {id_producto} ya existe.")
            return False
        if stock < 0:
            print("[ERROR] El stock inicial no puede ser negativo.")
            return False
        
        nuevo_producto = Producto(id_producto, nombre, precio, stock)
        self.productos[id_producto] = nuevo_producto
        print(f"[OK] Producto '{nombre}' registrado con exito.")
        return True

    def obtener_producto(self, id_producto):
        return self.productos.get(id_producto, None)

    def actualizar_producto(self, id_producto, nombre=None, precio=None, stock=None):
        producto = self.obtener_producto(id_producto)
        if not producto:
            print("[ERROR] Producto no encontrado para actualizar.")
            return False
        
        if nombre is not None: 
            producto.nombre = nombre
        if precio is not None: 
            producto.precio = precio
        if stock is not None:
            if stock < 0:
                print("[ERROR] El stock no puede ser negativo.")
                return False
            producto.stock = stock
        
        print(f"[ACTUALIZADO] Producto ID {id_producto} actualizado.")
        return True

    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            print("[ERROR] El producto no existe.")
            return False
        
        # Validar si está en algún pedido
        for pedido in self.pedidos.values():
            if id_producto in pedido.id_productos:
                print("[ERROR] No se puede eliminar el producto porque ya esta asociado a un pedido.")
                return False
                
        del self.productos[id_producto]
        print(f"[ELIMINADO] Producto ID {id_producto} eliminado.")
        return True

    def buscar_producto_por_nombre(self, termino):
        resultados = [p.to_dict() for p in self.productos.values() if termino.lower() in p.nombre.lower()]
        return resultados

    # -----------------------------------------------------------------
    # CRUD CLIENTES
    # -----------------------------------------------------------------
    def crear_cliente(self, id_cliente, nombre, email):
        if id_cliente in self.clientes:
            print(f"[ERROR] El cliente con ID {id_cliente} ya existe.")
            return False
        
        # Validar email repetido
        for c in self.clientes.values():
            if c.email.lower() == email.lower():
                print(f"[ERROR] El email '{email}' ya esta registrado.")
                return False

        nuevo_cliente = Cliente(id_cliente, nombre, email)
        self.clientes[id_cliente] = nuevo_cliente
        print(f"[OK] Cliente '{nombre}' registrado con exito.")
        return True

    def obtener_cliente(self, id_cliente):
        return self.clientes.get(id_cliente, None)

    def actualizar_cliente(self, id_cliente, nombre=None, email=None):
        cliente = self.obtener_cliente(id_cliente)
        if not cliente:
            print("[ERROR] Cliente no encontrado.")
            return False
        
        if nombre is not None: 
            cliente.nombre = nombre
        if email is not None: 
            cliente.email = email
        print(f"[ACTUALIZADO] Cliente ID {id_cliente} actualizado.")
        return True

    def eliminar_cliente(self, id_cliente):
        if id_cliente not in self.clientes:
            print("[ERROR] El cliente no existe.")
            return False
        
        # Validar si tiene historial de pedidos
        for pedido in self.pedidos.values():
            if pedido.id_cliente == id_cliente:
                print("[ERROR] No se puede eliminar el cliente porque tiene pedidos asociados.")
                return False

        del self.clientes[id_cliente]
        print(f"[ELIMINADO] Cliente ID {id_cliente} eliminado.")
        return True

    # -----------------------------------------------------------------
    # GESTIÓN DE PEDIDOS
    # -----------------------------------------------------------------
    def crear_pedido(self, id_cliente, lista_id_productos):
        # 1. Validar Cliente
        if id_cliente not in self.clientes:
            print("[ERROR] El cliente no existe. No se puede crear el pedido.")
            return False
        
        if not lista_id_productos:
            print("[ERROR] El pedido debe contener al menos un producto.")
            return False

        # 2. Validar Existencia y Stock de todos los productos seleccionados
        productos_a_despachar = []
        for id_prod in lista_id_productos:
            prod = self.obtener_producto(id_prod)
            if not prod:
                print(f"[ERROR] El producto con ID {id_prod} no existe. Pedido cancelado.")
                return False
            if prod.stock <= 0:
                print(f"[ERROR] El producto '{prod.nombre}' no tiene stock disponible. Pedido cancelado.")
                return False
            productos_a_despachar.append(prod)

        # 3. Restar Stock
        for prod in productos_a_despachar:
            prod.stock -= 1

        # 4. Registrar Pedido
        id_pedido = self.contador_pedidos
        nuevo_pedido = Pedido(id_pedido, id_cliente, lista_id_productos)
        self.pedidos[id_pedido] = nuevo_pedido
        self.contador_pedidos += 1
        
        print(f"[PEDIDO] Pedido #{id_pedido} creado con exito para el cliente ID {id_cliente}.")
        return True

    def ver_historial_cliente(self, id_cliente):
        if id_cliente not in self.clientes:
            print("[ERROR] El cliente no existe.")
            return []
        
        historial = []
        for p in self.pedidos.values():
            if p.id_cliente == id_cliente:
                nombres_productos = [self.productos[id_prod].nombre for id_prod in p.id_productos]
                historial.append({
                    "id_pedido": p.id_pedido,
                    "fecha": p.fecha_pedido,
                    "productos_comprados": nombres_productos
                })
        return historial

    def exportar_datos_json(self):
        data = {
            "clientes": [c.to_dict() for c in self.clientes.values()],
            "productos": [p.to_dict() for p in self.productos.values()],
            "pedidos": [pe.to_dict() for pe in self.pedidos.values()]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
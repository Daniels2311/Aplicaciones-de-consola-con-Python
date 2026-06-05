```markdown
# 🎯 Sistema de Gestión de Pedidos para una Tienda

¡Bienvenido al repositorio del **Sistema de Gestión de Pedidos**! Esta es una aplicación de consola desarrollada en **Python** diseñada para administrar el flujo de inventario, clientes y ventas de una pequeña tienda, utilizando archivos **JSON** como mecanismo de persistencia de datos local.

---

## 📝 Descripción del Proyecto

El sistema permite gestionar de forma integral el núcleo operativo de un comercio. Su objetivo principal es facilitar el registro, actualización y consulta de productos y clientes, integrándolos dinámicamente mediante la creación de pedidos en tiempo real con control automático de existencias.

---

## ✨ Funcionalidades Clave

* 📦 **CRUD Completo para Productos:** Registro, lectura, actualización y eliminación de los productos disponibles en la tienda.
* 👥 **CRUD Completo para Clientes:** Administración detallada de los datos de los compradores.
* 🛒 **Gestión de Pedidos Inteligente:** Permite crear un nuevo pedido seleccionando un cliente y múltiples productos, calculando los totales y **actualizando automáticamente el stock** disponible.
* 🔍 **Búsqueda Avanzada:** Motor de búsqueda rápida de productos filtrando directamente por su nombre.
* 📜 **Historial de Clientes:** Consulta específica y ordenada de todos los pedidos realizados por un cliente en particular.
* 📊 **Reto Final (Reporte de Ventas):** Módulo analítico integrado para generar un reporte de ventas simple que calcula y muestra de forma clara el **total acumulado vendido** por la tienda.

---

## 📐 Entidades y Estructura de Datos (JSON)

El almacenamiento de la información se organiza a través de estructuras bien definidas dentro de los archivos JSON:

1. **Productos:**
   * `id_producto`:
   * `nombre`: 
   * `precio`: 
   * `stock`: 

2. **Clientes:**
   * `id_cliente`:
   * `nombre`: 
   * `email`: 

3. **Pedidos:**
   * `id_pedido`:
   * `id_cliente`: 
   * `id_productos`: 

---

## 🛠️ Tecnologías e Instrumentos

* **Lenguaje de Programación:** Python 3.x
* **Persistencia Local:** JSON nativo (Manejo de listas y diccionarios)
* **Control de Versiones:** Git & GitHub

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para clonar el repositorio e iniciar la aplicación en tu entorno local:

1. **Clonar el repositorio:**
```bash
   git clone [https://github.com/tu-usuario/sistema-gestion-pedidos.git](https://github.com/tu-usuario/sistema-gestion-pedidos.git)

```

2. **Ingresar a la carpeta del proyecto:**

```bash
   cd sistema-gestion-pedidos

```

3. **Ejecutar la aplicación principal:**

```bash
   python main.py

```

---

## 👥 Equipo Desarrollador (Integrantes)

Este proyecto ha sido estructurado y codificado por:

* **Daniel Santiago Granados Castañeda** 
* **Simon Pineda** 
* **Manuel** 

```

```

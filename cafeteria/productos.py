import json
import os

class Productos:
    def __init__(self, inventario, archivo="productos.json"):
        self.archivo = archivo
        self.inventario = inventario
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                return json.load(f)
        return {}

    def guardar_productos(self):
        with open(self.archivo, "w") as f:
            json.dump(self.productos, f, indent=4)  #guarda el diccionario sel.productos dentro del archivo

    def mostrar_productos(self):
        if not self.productos:
            print("No hay productos cargados.")
        else:
            print("Productos disponibles:")
            for nombre in self.productos:
                print(f"- {nombre}")

    def obtener_receta(self, nombre_producto):
        producto = self.productos.get(nombre_producto)
        if producto and "ingredientes" in producto:
            return producto["ingredientes"]
        return {}

    def agregar_producto(self, nombre, ingredientes_necesarios, precio_unitario, rinde):
        self.productos[nombre] = {
            "ingredientes": ingredientes_necesarios,
            "precio_unitario": precio_unitario,
            "rinde": rinde
        }
        self.guardar_productos()
        print("Producto agregado con éxito.")
    
    def verificar_disponibilidad(self, nombre_producto, cantidad):
        cantidad_actual = self.inventario.ingredientes.get(nombre_producto, 0)
        return cantidad_actual >= cantidad
        
        
    def menu(self):
        while True:
            print("========MENU CONFITERIA========")
            print("1. Ver productos")
            print("2. Agregar producto")
            print("3. Volver al menú principal")

            opcion = input("Elegí una opción: ")

            if opcion == "1":
                self.mostrar_productos()

            elif opcion == "2":
                nombre = input("Nombre del producto: ").strip().lower()
                ingredientes = {}
                print("Agregá los ingredientes que usa (uno por uno, escribí 'fin' para terminar): ")
                while True:
                    ingr = input("Ingrediente: ").strip().lower()
                    if ingr == "fin":
                        break
                    stock_actual = self.inventario.obtener_stock(ingr)
                    if isinstance(stock_actual, dict):
                        cantidad = stock_actual.get("cantidad", 0.0)
                        unidad = stock_actual.get("unidad", "g/ml")
                        print(f"Stock actual de {ingr}: {cantidad} {unidad}")
                    else:
                        print(f"No hay stock registrado para {ingr}.")

                    
                    try:
                        cantidad = float(input(f"Cantidad de {ingr} (en gramos/ml): "))
                        ingredientes[ingr] = cantidad
                    except ValueError:
                        print("Cantidad inválida. Intentalo de nuevo.")

                try:
                    rinde = int(input("¿Cuántas unidades salen con esta receta?: "))
                    if rinde <= 0:
                        print("El rinde debe ser mayor que cero.")
                        continue
                    puede_preparar = True
                    for ingr, cantidad in ingredientes.items():
                        cantidad_por_unidad = cantidad / rinde
                        stock_disponible = self.inventario.obtener_stock(ingr)
                        if isinstance(stock_disponible, dict):
                            cantidad_stock = stock_disponible.get("cantidad", 0.0)
                        elif isinstance(stock_disponible, float) or isinstance(stock_disponible, int):
                            cantidad_stock = stock_disponible
                        else:
                            print(f"{ingr} no esta registrado en el inventario")
                            return
                        if cantidad_stock< cantidad_por_unidad:
                            print(f"No hay suficiente stock {ingr} en stock.")
                            return
                    
                    if not puede_preparar:
                        print("No se puede guardar el producto porque no hay suficiente stock para producir ni una unidad.")
                        continue
                    precio_unitario = float(input("Precio de venta por unidad: "))
                    self.agregar_producto(nombre, ingredientes, precio_unitario, rinde)
                
                except ValueError:
                    print("Valor inválido. Intentalo de nuevo.")

            elif opcion == "3":
                break

            else:
                print("Opción no válida.")
        def verificar_disponibilidad(self, nombre_prod, cantidad):
            
            if nombre_prod not in self.productos:
                return False

            producto = self.productos[nombre_prod]
            receta = producto["ingredientes"]
            rinde = producto.get("rinde", 1)

            for ingr, cantidad_total_receta in receta.items():
                cantidad_necesaria = (cantidad_total_receta / rinde) * cantidad
                disponible = 0.0
                if isinstance(stock_disponible, dict):
                    disponible = stock_disponible.get("cantidad", 0.0)
                elif isinstance(stock_disponible, (int, float)):
                    disponible = stock_disponible

                if disponible < cantidad_necesaria:
                    return False

            return True

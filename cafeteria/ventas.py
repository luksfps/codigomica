import json
import os 
from datetime import datetime


class Ventas:
    def __init__(self, archivo="ventas.json"):
        self.archivo = archivo
        self.ventas = self.cargar_ventas()
    
    def cargar_ventas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r")as f:
                return json.load(f)
        return[]
    
    def guardar_ventas(self):
        with open(self.archivo, "w") as f:
            json.dump(self.ventas, f, indent=4)
            
    def registrar_venta(self, producto, cantidad, precio_unitario):
        from tkinter import messagebox
        # Verificar disponibilidad antes de vender
        if not self.productos.verificar_disponibilidad(producto, cantidad, self.inventario.ingredientes):
            messagebox.showerror("Error", "No hay suficiente stock para realizar la venta.")
            return

        total = round(precio_unitario * cantidad,2)
        fecha= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta= {
            "producto":producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "fecha": fecha
        }
        
        self.ventas.append(venta)
        self.guardar_ventas()
        
        #descontar ingredientes del inventario
        receta = self.productos.obtener_receta(producto)
        rinde = self.productos.productos[producto]["rinde"]
        ingredientes_usados = {}

        for ing, cant in receta.items():
            total_utilizado = (cant / rinde) * cantidad
            ingredientes_usados[ing] = total_utilizado

        self.inventario.descontar_ingredientes(ingredientes_usados)
        
        self.generar_ticket(venta)
        self.exportar_ticket_txt(venta)
        

    def registrar_ventas_multiples(self, lista_productos):
        total = 0
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#GENERAR TICKET

        print("\n======== TICKET DE VENTA CAFETERÍA ========")
        for item in lista_productos:
            nombre = item["nombre"]
            cantidad = item["cantidad"]
            precio = item["precio"]
            subtotal = precio * cantidad
            total += subtotal

            print(f"\nProducto: { nombre}")
            print(f"Precio unitario: ${precio:.2f}")
            print(f"Cantidad: {cantidad}")
            print(f"Subtotal: ${subtotal:.2f}")
        print(f"\nTotal: ${total:.2f}")
        print(f"Fecha: {fecha}")
        print("==================================\n")


        venta = {
            "productos": lista_productos,
            "total": total,
            "fecha": fecha
            }
        self.ventas.append(venta)
        self.guardar_ventas()
        self.exportar_ticket_txt(venta, multiple=True)

    def generar_ticket(self, venta):
        print("\n======== TICKET DE VENTA CAFETERÍA ========")
        print(f"\nProducto: {venta['producto']}")
        print(f"Precio unitario: ${venta['precio_unitario']:.2f}")
        print(f"Cantidad: {venta['cantidad']}")
        print(f"Total: ${venta['total']:.2f}")
        print(f"Fecha: {venta['fecha']}")
        print("==================================\n")
        
    def exportar_ticket_txt(self, venta, multiple=False):
        carpeta_tickets = os.path.join(os.path.dirname(__file__), "tickets")
        os.makedirs(carpeta_tickets, exist_ok=True)
    #formatear nombre del archivo
        fecha_archivo = venta['fecha'].replace(":", "-").replace(" ", "_")
        nombre_archivo = f"ticket_{fecha_archivo}.txt"
        ruta_completa = os.path.join(carpeta_tickets, nombre_archivo)


        with open(nombre_archivo, "w") as f:
            f.write("======== TICKET DE VENTA CAFETERÍA ========\n")
            if multiple:
                for item in venta["productos"]:
                    f.write(f"\nProducto: {item['nombre']}\n")
                    f.write(f"Precio unitario: ${item['precio']:.2f}\n")
                    f.write(f"Cantidad: {item['cantidad']}\n")
                    f.write(f"Subtotal: ${item['precio'] * item['cantidad']:.2f}\n")
            else:
                f.write(f"\nProducto: {venta['producto']}\n")
                f.write(f"Precio unitario: ${venta['precio_unitario']:.2f}\n")
                f.write(f"Cantidad: {venta['cantidad']}\n")
            f.write(f"\nTotal: ${venta['total']:.2f}\n")
            f.write(f"Fecha: {venta['fecha']}\n")
            f.write("===========================================\n")

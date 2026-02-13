from inventario import Inventario
from productos import Productos
from ventas import Ventas

from colorama import Fore, Style, init
init(autoreset=True)

def print_aviso(texto):
    print(Fore.YELLOW + texto)
def print_error(texto):
    print(Fore.RED + texto)
def print_ok(texto):
    print(Fore.GREEN + texto)

def pausar():
    input(Fore.CYAN + "\nPresioná ENTER para continuar...")
def mostrar_titulo():
    print(Fore.CYAN + """
=========================================
     SISTEMA DE VENTAS - CAFETERÍA  
==========================================
""")

def main():
    inventario = Inventario()
    productos= Productos(inventario=inventario)
    ventas= Ventas()
    mostrar_titulo()

    
    
    while True:
        print (Fore.BLUE + "\n----------SISTEMA CAFETERIA-------")
        print("1. Gestionar ingredientes")
        print("2. Gestionar productos")
        print("3. Registrar venta de productos")
        print("4.Ver historial de tickets")
        print("5.Salir")

        opcion= input ("Elegi una opcion: ")
        
        if opcion == "1":
            inventario.menu_ingredientes()
            pausar()
            
        elif opcion == "2":
            productos.menu()
            pausar()
            
        elif opcion == "3":
            productos_vendidos=[]
            while True:
                productos.mostrar_productos()
                nombre =input("¿Qué producto se vendió?: ").strip().lower()
                receta= productos.obtener_receta(nombre)
            
                if not receta:
                    print_error("Producto no encontrado.")
                    continue
            
                rinde = productos.productos[nombre].get("rinde", 1)   
                     
                try:
                    cantidad_vendida= int(input("¿Cuántas unidades se vendieron?: "))
                    escala= cantidad_vendida/ rinde
                    if inventario.ingredientes.descontar_ingredientes(receta, rinde=1 /escala):
                        precio= productos.productos[nombre]["precio_unitario"]
                        productos_vendidos.append({
                            "nombre": nombre,
                            "cantidad": cantidad_vendida,
                            "precio": precio
                        })
                        print_ok("Producto agregado correctamente.")
                    else:
                        print_error("No hay suficientes ingredientes.")
                except ValueError:
                    print_error("Cantidad inválida. ") 
                seguir = input("¿Desea agregar otro producto a esta venta? (si/no): ").strip().lower()
                if seguir != "si":
                    break
            if productos_vendidos:
                ventas.registrar_ventas_multiples(productos_vendidos)
                print_ok("Venta registrada con exito.")
                pausar()
        
        elif opcion == "4":
            if ventas.ventas:
                print(Fore.CYAN + "\n======== HISTORIAL DE VENTAS ========")
                for i, venta in enumerate(ventas.ventas, 1):
                    print(f"\n--- Venta {i} ---")
                    if "productos" in venta:
                        for prod in venta["productos"]:
                            print(f"Producto: {prod['nombre']}")
                            print(f"Cantidad: {prod['cantidad']}")
                            print(f"Precio unitario: ${prod['precio']:.2f}")
                    else:
                    # Para ventas individuales
                        print(f"Producto: {venta['producto']}")
                        print(f"Cantidad: {venta['cantidad']}")
                        print(f"Precio unitario: ${venta['precio_unitario']:.2f}")
                    print(f"Total: ${venta['total']:.2f}")
                    print(f"Fecha: {venta['fecha']}")
                print("=====================================\n")
            else:
                print_aviso("No hay ventas registradas.")
            pausar()

        elif opcion == "5":
            print_ok("Saliendo...")
            break
        else:
            print_error("Opción inválida.")
            pausar()
                
                    
if __name__=="__main__":
    main()
    
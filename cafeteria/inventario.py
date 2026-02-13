
from ingredientes import Ingredientes
from productos import Productos

class Inventario:
    def __init__(self):
        self.ingredientes = Ingredientes() 
        from productos import Productos
        self.productos = Productos(inventario=self)        
    def menu_ingredientes(self):
        while True:
            print("=====MENU INGREDIENTES=====")
            print("1.Ver ingredientes")
            print("2.Agregar ingrediente")
            print("3.Volver")
            
            opcion= input("Elegí una opción: ")
            if opcion =="1":
                self.ingredientes.mostrar_ingredientes()
            elif opcion =="2":
                nombre= input ("Nombre del ingrediente: ").strip().lower()
                entrada = input("Cantidad y unidad (ej: 300 g):  ").strip().split()
                if len(entrada)!= 2:
                    print("Formato incorrecto.")
                    continue
                cantidad= float(entrada[0])
                unidad = entrada[1]
                minimo = float(input("Stock mínimo: "))
                self.ingredientes.agregar_ingredientes(nombre, cantidad, unidad,minimo)
            elif opcion=="3":
                break
            else:
                print("Opción inválida.")
    def obtener_stock(self, ingrediente):
        return self.ingredientes.ingredientes.get(ingrediente,0.0)
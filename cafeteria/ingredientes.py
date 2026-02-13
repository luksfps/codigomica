import json
import os

class Ingredientes:
    def __init__(self, archivo="ingredientes.json"):
        self.archivo = archivo
        self.ingredientes = self.cargar_ingredientes()
        self.datos = {}

    def get(self, clave, valor_por_defecto=None):
        return self.datos.get(clave, valor_por_defecto)
    
    def cargar_ingredientes(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                return json.load(f)
        return {}

    def guardar_ingredientes(self):
        with open(self.archivo, "w") as f:
            json.dump(self.ingredientes, f, indent=4)

    def agregar_ingredientes(self, nombre, cantidad, unidad, minimo):
        unidad = unidad.lower()
        if unidad in ["kg", "kilo", "kilos"]:
            cantidad *= 1000
            minimo *= 1000
            unidad = "g"
        elif unidad in ["l", "litro", "litros"]:
            cantidad *= 1000
            minimo *= 1000
            unidad = "ml"
        elif unidad not in ["g", "ml"]:
            print("Unidad no válida.")
            return False

        # Si el ingrediente ya existe, sumar la cantidad (manteniendo unidad)
        if nombre in self.ingredientes:
            existente = self.ingredientes[nombre]
            if existente.get("unidad") != unidad:
                print("Unidad incompatible con ingrediente existente.")
                return False
            existente["cantidad"] = existente.get("cantidad", 0) + cantidad
            # Actualizar mínimo si el proporcionado es mayor que el existente
            try:
                if minimo is not None and minimo > existente.get("minimo", 0):
                    existente["minimo"] = minimo
            except Exception:
                pass
        else:
            self.ingredientes[nombre] = {
                "cantidad": cantidad,
                "unidad": unidad,
                "minimo": minimo
            }

        self.guardar_ingredientes()
        return True

    def mostrar_ingredientes(self):
        if not self.ingredientes:
            print("No hay ingredientes cargados.")
            return
        for nombre, datos in self.ingredientes.items():
            print(f"{nombre}: {datos['cantidad']} {datos['unidad']} (mínimo: {datos['minimo']})")

    def descontar_ingredientes(self, receta, rinde=1, mostrar_alerta=False):
        for ingr, cant in receta.items():
            total = cant / rinde
            if ingr not in self.ingredientes:
                print(f"Falta el ingrediente '{ingr}'")
                return False
            if self.ingredientes[ingr]["cantidad"] < total:
                print(f"No hay suficiente '{ingr}'")
                return False
        for ingr, cant in receta.items():
            total = cant / rinde
            self.ingredientes[ingr]["cantidad"] -= total
        self.guardar_ingredientes()
        
        if mostrar_alerta:
            from tkinter import messagebox
            for ingr, datos in self.ingredientes.items():
                if datos["cantidad"]<= datos.get("minimo", 0):
                    messagebox.showwarning("¡Stock bajo!", f"El stock de '{ingr}' esta por debajo del minimo ({datos['cantidad']} {datos['unidad']})")
                    
            
        return True


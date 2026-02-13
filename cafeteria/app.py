import tkinter as tk            
from tkinter import messagebox          #
from tkinter import simpledialog
from inventario import Inventario
from productos import Productos
from ventas import Ventas
class CafeteriaApp:
    def __init__(self, root):
        self.root = root            #ventana
        self.root.title("Sistema de Cafetería")
        self.root.geometry("400x400")

        self.inventario = Inventario()
        self.productos = Productos(self.inventario)
        self.ventas = Ventas()

        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text=" Sistema de Cafetería", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="1. Gestionar ingredientes", width=30, command=self.gestionar_ingredientes).pack(pady=5)
        tk.Button(self.root, text="2. Gestionar productos", width=30, command=self.gestionar_productos).pack(pady=5)
        tk.Button(self.root, text="3. Registrar venta", width=30, command=self.registrar_venta).pack(pady=5)
        tk.Button(self.root, text="4. Ver historial de tickets", width=30, command=self.ver_historial).pack(pady=5)
        tk.Button(self.root, text="5. Salir", width=30, command=self.root.quit).pack(pady=20)

    def gestionar_ingredientes(self):
        # Si la ventana ya existe, traerla al frente
        if hasattr(self, 'ventana_ing') and getattr(self, 'ventana_ing') is not None:
            try:
                if self.ventana_ing.winfo_exists():
                    try:
                        self.ventana_ing.deiconify()
                        self.ventana_ing.lift()
                        self.ventana_ing.focus_force()
                        return
                    except Exception:
                        pass
            except Exception:
                pass

        ventana_ing = tk.Toplevel(self.root)
        ventana_ing.title("Gestión de Ingredientes")
        ventana_ing.geometry("800x900")
        self.ventana_ing = ventana_ing

    # Lista de ingredientes
        texto = tk.Text(ventana_ing, height=15)
        texto.pack(pady=5)

        def mostrar_ingredientes_gui():
            texto.delete(1.0, tk.END)
            if not self.inventario.ingredientes.ingredientes:
                texto.insert(tk.END, "No hay ingredientes cargados.\n")
            else:
                for nombre, datos in self.inventario.ingredientes.ingredientes.items():
                    texto.insert(tk.END, f"{nombre}: {datos['cantidad']} {datos['unidad']} (mínimo: {datos['minimo']})\n")

        mostrar_ingredientes_gui()

    

    # Selector y acciones para ingredientes
        ingredientes_nombres = list(self.inventario.ingredientes.ingredientes.keys())
        if ingredientes_nombres:
            ingrediente_var = tk.StringVar(ventana_ing)
            ingrediente_var.set(ingredientes_nombres[0])
            menu_ingredientes = tk.OptionMenu(ventana_ing, ingrediente_var, *ingredientes_nombres)
            menu_ingredientes.pack(pady=5)

            def agregar_stock():
                nombre = ingrediente_var.get()
                try:
                    cantidad = simpledialog.askfloat("Agregar stock", f"Cantidad a agregar a {nombre} (g/ml):", parent=ventana_ing)
                    if cantidad is None:
                        return
                    if cantidad <= 0:
                        messagebox.showerror("Error", "Cantidad inválida.")
                        return
                    # Usar la función existente para sumar (maneja unidades si se indica)
                    unidad = simpledialog.askstring("Unidad", "Unidad (g, kg, ml, l):", parent=ventana_ing)
                    if unidad is None:
                        return
                    unidad = unidad.strip().lower()
                    minimo_actual = self.inventario.ingredientes.ingredientes.get(nombre, {}).get("minimo", 0)
                    resultado = self.inventario.ingredientes.agregar_ingredientes(nombre, cantidad, unidad, minimo_actual)
                    if resultado:
                        messagebox.showinfo("Éxito", f"Se agregó {cantidad} {unidad} a {nombre}.")
                        try:
                            ventana_ing.destroy()
                        except Exception:
                            pass
                        self.gestionar_ingredientes()
                    else:
                        messagebox.showerror("Error", "No se pudo agregar stock (unidad incompatible).")
                except Exception:
                    messagebox.showerror("Error", "Cantidad inválida.")

            def reducir_stock():
                nombre = ingrediente_var.get()
                try:
                    cantidad = simpledialog.askfloat("Reducir stock", f"Cantidad a reducir de {nombre} (g/ml):", parent=ventana_ing)
                    if cantidad is None:
                        return
                    if cantidad <= 0:
                        messagebox.showerror("Error", "Cantidad inválida.")
                        return
                    actuales = self.inventario.ingredientes.ingredientes.get(nombre, {}).get("cantidad", 0)
                    if cantidad >= actuales:
                        if messagebox.askyesno("Confirmar", f"La reducción eliminará todo el stock de {nombre}. ¿Deseas eliminarlo?"):
                            del self.inventario.ingredientes.ingredientes[nombre]
                        else:
                            return
                    else:
                        self.inventario.ingredientes.ingredientes[nombre]["cantidad"] = actuales - cantidad
                    self.inventario.ingredientes.guardar_ingredientes()
                    messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' actualizado.")
                    try:
                        ventana_ing.destroy()
                    except Exception:
                        pass
                    self.gestionar_ingredientes()
                except Exception:
                    messagebox.showerror("Error", "Cantidad inválida.")

            def eliminar_ingrediente():
                nombre = ingrediente_var.get()
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el ingrediente {nombre.title()}?"):
                    try:
                        del self.inventario.ingredientes.ingredientes[nombre]
                        self.inventario.ingredientes.guardar_ingredientes()
                        messagebox.showinfo("Éxito", f"Ingrediente {nombre.title()} eliminado con éxito.")
                        try:
                            ventana_ing.destroy()
                        except Exception:
                            pass
                        self.gestionar_ingredientes()
                    except KeyError:
                        messagebox.showerror("Error", "Ingrediente no encontrado.")

            tk.Button(ventana_ing, text="Agregar stock al ingrediente seleccionado", command=agregar_stock).pack(pady=5)
            tk.Button(ventana_ing, text="Reducir stock del ingrediente seleccionado", command=reducir_stock).pack(pady=5)
            tk.Button(ventana_ing, text="Eliminar ingrediente seleccionado", command=eliminar_ingrediente).pack(pady=5)

        # Botón único para crear un nuevo ingrediente (abre diálogos)
        def agregar_nuevo_ingrediente_dialog():
            try:
                nombre = simpledialog.askstring("Nuevo Ingrediente", "Nombre:", parent=ventana_ing)
                if not nombre:
                    return
                nombre = nombre.strip().lower()
                cantidad = simpledialog.askfloat("Nuevo Ingrediente", "Cantidad:", parent=ventana_ing)
                if cantidad is None:
                    return
                unidad = simpledialog.askstring("Nuevo Ingrediente", "Unidad (g, kg, ml, l):", parent=ventana_ing)
                if unidad is None:
                    return
                minimo = simpledialog.askfloat("Nuevo Ingrediente", "Stock mínimo:", parent=ventana_ing)
                if minimo is None:
                    minimo = 0
                resultado = self.inventario.ingredientes.agregar_ingredientes(nombre, cantidad, unidad.strip().lower(), minimo)
                if resultado:
                    messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' agregado.")
                    try:
                        ventana_ing.destroy()
                    except Exception:
                        pass
                    self.gestionar_ingredientes()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el ingrediente (unidad inválida o incompatible).")
            except Exception:
                messagebox.showerror("Error", "Datos inválidos.")

        tk.Button(ventana_ing, text="Agregar un nuevo ingrediente", command=agregar_nuevo_ingrediente_dialog).pack(pady=10)
                   
    def gestionar_productos(self):
        # Si la ventana ya existe, traerla al frente
        if hasattr(self, 'ventana_prod') and getattr(self, 'ventana_prod') is not None:
            try:
                if self.ventana_prod.winfo_exists():
                    try:
                        self.ventana_prod.deiconify()
                        self.ventana_prod.lift()
                        self.ventana_prod.focus_force()
                        return
                    except Exception:
                        pass
            except Exception:
                pass

        ventana_prod = tk.Toplevel(self.root)
        ventana_prod.title("Gestión de Productos")
        ventana_prod.geometry("500x500")
        self.ventana_prod = ventana_prod

        texto = tk.Text(ventana_prod, height=10)
        texto.pack(pady=5)

        def mostrar_productos_gui():
            texto.delete(1.0, tk.END)
            if not self.productos.productos:
                texto.insert(tk.END, "No hay productos cargados.\n")
            else:
                for nombre, datos in self.productos.productos.items():
                    texto.insert(tk.END, f"{nombre} - ${datos['precio_unitario']:.2f}\nRinde: {datos['rinde']}\nIngredientes:\n")
                    for ing, cant in datos["ingredientes"].items():
                        texto.insert(tk.END, f"  - {ing}: {cant}\n")
                    texto.insert(tk.END, "\n")

        mostrar_productos_gui()

        # Selector para elegir producto existente (para eliminar rápidamente)
        productos_nombres = list(self.productos.productos.keys())
        if productos_nombres:
            producto_var_selector = tk.StringVar(ventana_prod)
            producto_var_selector.set(productos_nombres[0])
            menu_prod_sel = tk.OptionMenu(ventana_prod, producto_var_selector, *productos_nombres)
            menu_prod_sel.pack(pady=5)

            def eliminar_producto_seleccionado():
                nombre = producto_var_selector.get()
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el producto {nombre.title()}?"):
                    if nombre.lower() in self.productos.productos:
                        del self.productos.productos[nombre.lower()]
                        self.productos.guardar_productos()
                        messagebox.showinfo("Éxito", f"Producto {nombre.title()} eliminado con éxito.")
                        try:
                            ventana_prod.destroy()
                        except Exception:
                            pass
                        self.gestionar_productos()
                    else:
                        messagebox.showerror("Error", "Producto no encontrado.")

            tk.Button(ventana_prod, text="Eliminar producto seleccionado", command=eliminar_producto_seleccionado).pack(pady=5)

        # Botones y selector para gestionar productos
        # (selector creado arriba si hay productos)
        def editar_producto_seleccionado():
            try:
                nombre = producto_var_selector.get()
            except Exception:
                messagebox.showerror("Error", "No hay producto seleccionado.")
                return
            datos = self.productos.productos.get(nombre)
            if not datos:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            # Editar precio
            try:
                nuevo_precio = simpledialog.askfloat("Editar Precio", f"Nuevo precio para {nombre}:", initialvalue=datos.get("precio_unitario"), parent=ventana_prod)
                if nuevo_precio is not None:
                    datos["precio_unitario"] = float(nuevo_precio)
            except Exception:
                messagebox.showerror("Error", "Precio inválido.")
                return

            # Editar rinde
            try:
                nuevo_rinde = simpledialog.askinteger("Editar Rinde", f"Nuevo rinde para {nombre}:", initialvalue=datos.get("rinde"), parent=ventana_prod)
                if nuevo_rinde is not None and nuevo_rinde > 0:
                    datos["rinde"] = int(nuevo_rinde)
            except Exception:
                messagebox.showerror("Error", "Rinde inválido.")
                return

            # Editar ingredientes como cadena
            try:
                # Mostrar como ing:cant,ing2:cant2
                actuales = ",".join([f"{k}:{v}" for k, v in datos.get("ingredientes", {}).items()])
                ingresados = simpledialog.askstring("Editar Ingredientes", "Ingredientes (formato: ing1:cantidad,ing2:cantidad):", initialvalue=actuales, parent=ventana_prod)
                if ingresados is not None:
                    nuevos = {}
                    if ingresados.strip():
                        pares = [p.strip() for p in ingresados.split(",") if p.strip()]
                        for par in pares:
                            ing, cant = par.split(":")
                            nuevos[ing.strip().lower()] = float(cant.strip())
                    datos["ingredientes"] = nuevos
            except Exception:
                messagebox.showerror("Error", "Formato de ingredientes inválido.")
                return

            self.productos.guardar_productos()
            messagebox.showinfo("Éxito", "Producto editado con éxito.")
            try:
                ventana_prod.destroy()
            except Exception:
                pass
            self.gestionar_productos()

        tk.Button(ventana_prod, text="Editar producto seleccionado", command=editar_producto_seleccionado).pack(pady=5)

        # Botón para agregar nuevo producto usando diálogos
        def agregar_nuevo_producto_dialog():
            try:
                nombre = simpledialog.askstring("Nuevo Producto", "Nombre:", parent=ventana_prod)
                if not nombre:
                    return
                nombre = nombre.strip().lower()
                if nombre in self.productos.productos:
                    messagebox.showerror("Error", "Ya existe un producto con ese nombre.")
                    return
                precio = simpledialog.askfloat("Nuevo Producto", "Precio por unidad:", parent=ventana_prod)
                if precio is None:
                    return
                rinde = simpledialog.askinteger("Nuevo Producto", "¿Cuántas unidades salen con esta receta? (rinde):", parent=ventana_prod)
                if rinde is None or rinde <= 0:
                    messagebox.showerror("Error", "Rinde inválido.")
                    return
                ingresados = simpledialog.askstring("Nuevo Producto", "Ingredientes (formato: ing1:cantidad,ing2:cantidad):", parent=ventana_prod)
                if not ingresados:
                    messagebox.showerror("Error", "Debe ingresar al menos un ingrediente.")
                    return
                ingredientes_nuevos = {}
                pares = [p.strip() for p in ingresados.split(",") if p.strip()]
                for par in pares:
                    ing, cant = par.split(":")
                    ingredientes_nuevos[ing.strip().lower()] = float(cant.strip())
                self.productos.agregar_producto(nombre, ingredientes_nuevos, float(precio), int(rinde))
                messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado.")
                try:
                    ventana_prod.destroy()
                except Exception:
                    pass
                self.gestionar_productos()
            except Exception:
                messagebox.showerror("Error", "Datos inválidos.")

        tk.Button(ventana_prod, text="Agregar nuevo producto", command=agregar_nuevo_producto_dialog).pack(pady=10)
        
        
    def registrar_venta(self):
        # Si la ventana de venta ya está abierta, traerla al frente
        if hasattr(self, 'ventana_venta') and getattr(self, 'ventana_venta') is not None:
            try:
                if self.ventana_venta.winfo_exists():
                    try:
                        self.ventana_venta.deiconify()
                        self.ventana_venta.lift()
                        self.ventana_venta.focus_force()
                        return
                    except Exception:
                        pass
            except Exception:
                pass

        ventana_venta = tk.Toplevel(self.root)
        ventana_venta.title("Registrar Venta")
        ventana_venta.geometry("400x300")
        self.ventana_venta = ventana_venta

        tk.Label(ventana_venta, text="Seleccioná un producto:").pack(pady=5)
        productos_nombres = list(self.productos.productos.keys())

        if not productos_nombres:
            messagebox.showerror("Error", "No hay productos cargados.")
            ventana_venta.destroy()
            return

        producto_var = tk.StringVar(ventana_venta)
        producto_var.set(productos_nombres[0])
        menu_productos = tk.OptionMenu(ventana_venta, producto_var, *productos_nombres)
        menu_productos.pack(pady=5)

        tk.Label(ventana_venta, text="Cantidad:").pack(pady=5)
        entrada_cantidad = tk.Entry(ventana_venta)
        entrada_cantidad.pack(pady=5)

        def confirmar_venta():
            producto = producto_var.get()
            try:
                cantidad = int(entrada_cantidad.get())
                if cantidad <= 0:
                    raise ValueError

                # Verificar disponibilidad de ingredientes
                if not self.productos.verificar_disponibilidad(producto, cantidad):
                    messagebox.showerror("Error", f"No hay suficientes ingredientes para preparar {cantidad} unidad(es) de {producto}.")
                    return

                    # Descontar ingredientes
                self.productos.descontar_ingredientes(producto, cantidad)

                # Registrar la venta
                precio_unitario = self.productos.productos[producto]["precio"]
                total = precio_unitario * cantidad
                self.ventas.ventas.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "total": total,
                    "fecha": self.ventas.obtener_fecha()
                })

                messagebox.showinfo("Venta realizada", f"Total: ${total:.2f}")
                # Reiniciar ventanas abiertas para reflejar cambios en stock
                try:
                    if hasattr(self, 'ventana_ing') and self.ventana_ing.winfo_exists():
                        try:
                            self.ventana_ing.destroy()
                        except Exception:
                            pass
                        self.gestionar_ingredientes()
                except Exception:
                    pass

                try:
                    if hasattr(self, 'ventana_prod') and self.ventana_prod.winfo_exists():
                        try:
                            self.ventana_prod.destroy()
                        except Exception:
                            pass
                        self.gestionar_productos()
                except Exception:
                    pass

                ventana_venta.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana_venta, text="Confirmar Venta", command=confirmar_venta).pack(pady=15)

             

    def ver_historial(self):
        if not self.ventas.ventas:
            messagebox.showinfo("Historial de Ventas", "No hay ventas registradas.")
            return

        # Si la ventana de historial ya está abierta, traerla al frente
        if hasattr(self, 'ventana_hist') and getattr(self, 'ventana_hist') is not None:
            try:
                if self.ventana_hist.winfo_exists():
                    try:
                        self.ventana_hist.deiconify()
                        self.ventana_hist.lift()
                        self.ventana_hist.focus_force()
                        return
                    except Exception:
                        pass
            except Exception:
                pass

        ventana_hist = tk.Toplevel(self.root)
        ventana_hist.title("Historial de Ventas")
        ventana_hist.geometry("600x400")
        self.ventana_hist = ventana_hist

        texto = tk.Text(ventana_hist, height=15)
        texto.pack(pady=5)

        ventas_list = []
        for i, venta in enumerate(self.ventas.ventas, 1):
            texto.insert(tk.END, f"Venta {i}:\n")
            if "productos" in venta:
                for prod in venta["productos"]:
                    texto.insert(tk.END, f"- {prod['nombre']} x{prod['cantidad']} - ${prod['precio']:.2f}\n")
            else:
                texto.insert(tk.END, f"- {venta['producto']} x{venta['cantidad']} - ${venta['precio_unitario']:.2f}\n")
            texto.insert(tk.END, f"Total: ${venta['total']:.2f} - Fecha: {venta['fecha']}\n\n")
            display = f"{i} - {venta.get('producto', 'varios')} - ${venta.get('total', 0):.2f} - {venta.get('fecha') }"
            ventas_list.append(display)

        venta_var = tk.StringVar(ventana_hist)
        venta_var.set(ventas_list[0])
        menu_ventas = tk.OptionMenu(ventana_hist, venta_var, *ventas_list)
        menu_ventas.pack(pady=5)

        def eliminar_venta_seleccionada():
            seleccion = venta_var.get()
            try:
                indice = int(seleccion.split(" - ")[0]) - 1
            except Exception:
                messagebox.showerror("Error", "Selección inválida.")
                return
            if messagebox.askyesno("Confirmar", f"¿Deseas eliminar la venta {indice+1}?"):
                try:
                    del self.ventas.ventas[indice]
                    self.ventas.guardar_ventas()
                    messagebox.showinfo("Éxito", "Venta eliminada.")
                    try:
                        ventana_hist.destroy()
                    except Exception:
                        pass
                    self.ver_historial()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        tk.Button(ventana_hist, text="Eliminar venta seleccionada", command=eliminar_venta_seleccionada).pack(pady=10)

# Ejecutar interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = CafeteriaApp(root) 
    root.mainloop()

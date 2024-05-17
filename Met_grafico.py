import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, Eq, solve
from fractions import Fraction


def resolver_problema_programacion_lineal(funcion_objetivo, inecuaciones, objetivo):
    intersecciones = calcular_intersecciones(inecuaciones)

    if not intersecciones:
        return "El sistema de inecuaciones no tiene solución."

    intersecciones_validas = validar_intersecciones(intersecciones, inecuaciones)

    if not intersecciones_validas:
        return "El sistema de inecuaciones no tiene solución válida en el primer cuadrante."

    valores_z = evaluar_en_funcion_objetivo(intersecciones_validas, funcion_objetivo)

    if objetivo == 'max':
        indice_optimo = valores_z.index(max(valores_z))
    else:
        indice_optimo = valores_z.index(min(valores_z))

    x_optimo, y_optimo, z_optimo = None, None, None

    if indice_optimo is not None:
        x_optimo = intersecciones_validas[indice_optimo]['x']
        y_optimo = intersecciones_validas[indice_optimo]['y']
        z_optimo = valores_z[indice_optimo]

    graficar_lineas(inecuaciones, intersecciones_validas, x_optimo=x_optimo, y_optimo=y_optimo, z_optimo=z_optimo)
    return f"Punto Óptimo: ({x_optimo}, {y_optimo}), Z = {z_optimo}"


def calcular_intersecciones(inecuaciones):
    intersecciones = []

    # Intersecciones entre inecuaciones
    for i in range(len(inecuaciones) - 1):
        for j in range(i + 1, len(inecuaciones)):
            x, y = symbols('x y')
            ecuacion1 = Eq(inecuaciones[i]['coeficientes'][0] * x + inecuaciones[i]['coeficientes'][1] * y, inecuaciones[i]['coeficientes'][2])
            ecuacion2 = Eq(inecuaciones[j]['coeficientes'][0] * x + inecuaciones[j]['coeficientes'][1] * y, inecuaciones[j]['coeficientes'][2])

            solucion = solve((ecuacion1, ecuacion2), (x, y))
            if solucion:
                intersecciones.append({'x': solucion[x], 'y': solucion[y]})

    # Intersecciones con ejes x e y
    for inecuacion in inecuaciones:
        a, b, c = inecuacion['coeficientes']

        if a == 0 and b != 0:
            y_interseccion = max(0, c / b)
            intersecciones.append({'x': 0, 'y': y_interseccion})
        elif a != 0 and b == 0:
            x_interseccion = max(0, c / a)
            intersecciones.append({'x': x_interseccion, 'y': 0})

    # Intersección con el origen (0, 0)
    intersecciones.append({'x': 0, 'y': 0})

    return intersecciones

def validar_intersecciones(intersecciones, inecuaciones):
    intersecciones_validas = []

    for punto in intersecciones:
        x, y = punto['x'], punto['y']
        cumple_inecuaciones = all(
            eval(f"{inecuacion['coeficientes'][0]}*{x} + {inecuacion['coeficientes'][1]}*{y} {inecuacion['tipo']} {inecuacion['coeficientes'][2]}")
            for inecuacion in inecuaciones
        )

        if cumple_inecuaciones and x >= 0 and y >= 0:
            intersecciones_validas.append({'x': x, 'y': y})

    return intersecciones_validas

def evaluar_en_funcion_objetivo(intersecciones_validas, funcion_objetivo):
    valores_z = []

    for punto in intersecciones_validas:
        x, y = punto['x'], punto['y']
        z = funcion_objetivo['coeficientes'][0] * x + funcion_objetivo['coeficientes'][1] * y
        valores_z.append(z)

    return valores_z

def graficar_lineas(inecuaciones, intersecciones_validas, x_optimo=None, y_optimo=None, z_optimo=None):
    max_x_values = [c / a if a != 0 else 10 for a, _, c in (inecuacion['coeficientes'] for inecuacion in inecuaciones) if a != 0]

    max_x = max(max_x_values) if max_x_values else 10

    x_vals = np.linspace(0, max_x, 400)

    plt.axvline(0, color='darkmagenta', linewidth=1, linestyle='--', label='x >= 0')
    plt.axhline(0, color='darkmagenta', linewidth=1, linestyle='--', label='y >= 0')

    for i, inecuacion in enumerate(inecuaciones):
        a, b, c = inecuacion['coeficientes']
        tipo = inecuacion['tipo']

        if a != 0 and b != 0:
            y_vals = (c - a * x_vals) / b
            plt.plot(x_vals, y_vals, label=f'{a}x + {b}y {tipo} {c}')
        elif a != 0:
            plt.axvline(max(0, c/a), color=np.random.rand(3,), linewidth=1, linestyle='-', label=f'x = max(0, {c/a}) (Inecuación {i+1})')
        elif b != 0:
            plt.axhline(max(0, c/b), color=np.random.rand(3,), linewidth=1, linestyle='-', label=f'y = max(0, {c/b}) (Inecuación {i+1})')

    for i, punto in enumerate(intersecciones_validas):
        x, y = punto['x'], punto['y']
        plt.scatter(x, y, color='red', marker=f"${chr(65 + i)}$", s=100)

    if x_optimo is not None and y_optimo is not None and z_optimo is not None:
        x_optimo_str = "{:.2f}".format(round(float(x_optimo), 2))
        y_optimo_str = "{:.2f}".format(round(float(y_optimo), 2))
        z_optimo_str = "{:.2f}".format(round(float(z_optimo), 2))
        letra_optima = chr(65 + intersecciones_validas.index({'x': x_optimo, 'y': y_optimo}))

        plt.scatter(float(x_optimo), float(y_optimo), color='green', marker='*', s=200, label=f'Punto Óptimo ({letra_optima}): Z = {z_optimo_str}')

        offset = 5
        texto_punto_optimo = f'({x_optimo_str}, {y_optimo_str})\nZ = {z_optimo_str}'
        plt.text(float(x_optimo) + offset, float(y_optimo) + offset, texto_punto_optimo, ha='left', va='bottom', color='black', fontsize=8, bbox=dict(facecolor='grey', edgecolor='blue', boxstyle='round,pad=0.5'))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.legend()
    plt.axis('equal')

    plt.show()



class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Graficador de Funciones y Líneas")

        # Botón para seleccionar entre Max y Min
        mensaje_informativo = tk.Label(root, text="Ingresar y *Guardar* valores de la FO antes de \n *Agregar* inecuaciones para el correcto \nfuncionamiento del programa.", fg="blue",font=("TkDefaultFont", 10, "bold"))
        mensaje_informativo.pack(side=tk.RIGHT)       
        self.tipo_label = tk.Label(root, text="Tipo de optimización:")
        self.tipo_label.pack()
        self.tipo_var = tk.StringVar()
        self.tipo_combobox = ttk.Combobox(root, textvariable=self.tipo_var, values=["Maximizar", "Minimizar"])
        self.tipo_combobox.pack()

        self.guardado_label = tk.Label(root, text="", fg="green")
        self.guardado_label.pack()
                # Botón Limpiar
        self.limpiar_button = tk.Button(root, text="Limpiar", fg="red", command=self.limpiar_interfaz)
        self.limpiar_button.pack()


        # Lista para almacenar las inecuaciones ingresadas
        self.inecuaciones = []

        # Arreglo para almacenar los coeficientes de la función objetivo
        self.coeficientes_funcion_objetivo = []

        # String para almacenar el tipo de optimización
        self.objetivo  = ""

       

        self.coeficientes_label = tk.Label(root, text="Coeficientes de la función objetivo:")
        self.coeficientes_label.pack()

        self.coef_x_label = tk.Label(root, text="Coeficiente x:")
        self.coef_x_label.pack()
        self.coef_x_entry = tk.Entry(root)
        self.coef_x_entry.pack()

        self.coef_y_label = tk.Label(root, text="Coeficiente y:")
        self.coef_y_label.pack()
        self.coef_y_entry = tk.Entry(root)
        self.coef_y_entry.pack()

        # Mensaje informativo a la derecha


        self.guardar_button = tk.Button(root, text="Guardar", command=self.guardar_configuracion)
        self.guardar_button.pack()

        self.inecuaciones_label = tk.Label(root, text="Inecuaciones:",font=("TkDefaultFont", 12, "bold"))
        self.inecuaciones_label.pack()

        self.coef_a_label = tk.Label(root, text="Coeficiente (x):")
        self.coef_a_label.pack()
        self.coef_a_entry = tk.Entry(root)
        self.coef_a_entry.pack()

        self.coef_b_label = tk.Label(root, text="Coeficiente (y):")
        self.coef_b_label.pack()
        self.coef_b_entry = tk.Entry(root)
        self.coef_b_entry.pack()

        self.coef_c_label = tk.Label(root, text="Valor constante:")
        self.coef_c_label.pack()
        self.coef_c_entry = tk.Entry(root)
        self.coef_c_entry.pack()

        self.inecuacion_label = tk.Label(root, text="Tipo de inecuación (>= ó <=):")
        self.inecuacion_label.pack()
        self.inecuacion_var = tk.StringVar()
        self.inecuacion_combobox = ttk.Combobox(root, textvariable=self.inecuacion_var, values=["<=", ">="])
        self.inecuacion_combobox.pack()

        self.agregar_button = tk.Button(root, text="Agregar", command=self.agregar_inecuacion)
        self.agregar_button.pack()

        self.in_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.in_listbox.pack()

        self.graficar_button = tk.Button(root, text="Graficar", command=self.graficar_lineas)
        self.graficar_button.pack()
        

    def agregar_inecuacion(self):
        # Obtener coeficientes de la inecuación
        coef_a = self.coef_a_entry.get()
        coef_b = self.coef_b_entry.get()
        coef_c = self.coef_c_entry.get()
        tipo_inecuacion = self.inecuacion_var.get()

        # Convertir coeficientes a números fraccionarios
        try:
            coef_a = Fraction(coef_a)
            coef_b = Fraction(coef_b)
            coef_c = Fraction(coef_c)
        except ValueError:
            messagebox.showwarning("Error", "Los coeficientes deben ser números válidos.")
            return

        # Agregar la inecuación a la lista
        inecuacion = {'coeficientes': (coef_a, coef_b, coef_c), 'tipo': tipo_inecuacion}
        self.inecuaciones.append(inecuacion)

        # Limpiar los campos de entrada
        self.coef_a_entry.delete(0, tk.END)
        self.coef_b_entry.delete(0, tk.END)
        self.coef_c_entry.delete(0, tk.END)

        # Actualizar la lista de inecuaciones en el Listbox
        inecuacion_str = f"{coef_a}x + {coef_b}y {tipo_inecuacion} {coef_c}"
        self.in_listbox.insert(tk.END, inecuacion_str)

        # Limpiar los campos de entrada
        self.coef_a_entry.delete(0, tk.END)
        self.coef_b_entry.delete(0, tk.END)
        self.coef_c_entry.delete(0, tk.END)

    def limpiar_interfaz(self):
        # Limpiar todos los valores ingresados
        self.tipo_var.set("")  # Limpiar tipo de optimización
        self.coef_x_entry.delete(0, tk.END)
        self.coef_y_entry.delete(0, tk.END)
        self.guardado_label.config(text="", font=("TkDefaultFont", 12))  # Restablecer mensaje de guardado
        self.inecuaciones = []  # Limpiar lista de inecuaciones
        self.in_listbox.delete(0, tk.END)  # Limpiar Listbox
        self.coef_a_entry.delete(0, tk.END)
        self.coef_b_entry.delete(0, tk.END)
        self.coef_c_entry.delete(0, tk.END)
        self.coef_x_entry.delete(0, tk.END)
        self.coef_y_entry.delete(0, tk.END)       

    def actualizar_tipo_optimizacion(self):
        # Actualizar el tipo de optimización
        objetivo = self.tipo_var.get()
        if objetivo == "Maximizar":
            self.objetivo = "max"
        elif objetivo == "Minimizar":
            self.objetivo = "min"



    def agregar_coeficientes_funcion_objetivo(self):
        # Obtener coeficientes de la función objetivo
        coef_x = self.coef_x_entry.get()
        coef_y = self.coef_y_entry.get()

        # Convertir coeficientes a números fraccionarios
        try:
            coef_x = Fraction(coef_x)
            coef_y = Fraction(coef_y)
        except ValueError:
            messagebox.showwarning("Error", "Los coeficientes deben ser números válidos.")
            return

        # Agregar los coeficientes a un diccionario
        self.coeficientes_funcion_objetivo = {'coeficientes': [coef_x, coef_y]}

    def guardar_configuracion(self):
        # Verificar si se han ingresado valores necesarios
        tipo_optimizacion = self.tipo_var.get()
        coef_x = self.coef_x_entry.get()
        coef_y = self.coef_y_entry.get()

        if not tipo_optimizacion or not coef_x or not coef_y:
            messagebox.showwarning("Error", "Faltan valores por agregar.")
            return

        self.actualizar_tipo_optimizacion()
        self.agregar_coeficientes_funcion_objetivo()

        # Mostrar el mensaje "Guardado" en negrita
        self.guardado_label.config(text="Guardado", fg="green", font=("TkDefaultFont", 12, "bold"))

        # Después de 2000 milisegundos (2 segundos), restablecer el texto y ocultar en negrita
        self.guardado_label.after(2000, lambda: self.restablecer_mensaje_guardado())

    def restablecer_mensaje_guardado(self):
        # Restablecer el texto y ocultar en negrita
        self.guardado_label.config(text="", font=("TkDefaultFont", 12))


    def restablecer_mensaje_guardado(self):
        # Restablecer el texto y ocultar en negrita
        self.guardado_label.config(text="", font=("TkDefaultFont", 12))

    def graficar_lineas(self):
        # Verificar si hay al menos una inecuación ingresada
        if not self.inecuaciones:
            messagebox.showwarning("Error", "No se ha ingresado ninguna inecuación.")
            return

        # Verificar si se han ingresado coeficientes de la función objetivo
        if not self.coeficientes_funcion_objetivo:
            messagebox.showwarning("Error", "Faltan valores por agregar. Asegúrate de ingresar los coeficientes de la función objetivo y el tipo de optimización antes de graficar.")
            return
        # Llamar a la función resolver_problema_programacion_lineal con los datos capturados
        result = resolver_problema_programacion_lineal(
            self.coeficientes_funcion_objetivo,
            self.inecuaciones,
            self.objetivo
        )

        if result is not None:
            # Mostrar mensaje en ventana emergente
            messagebox.showinfo("Resultado", result)
    
if __name__ == "__main__":
    
    root = tk.Tk()
    app = InterfazGrafica(root)    
    root.resizable(False,False)
    root.mainloop()


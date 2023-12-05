import json
from tkinter import *
from tkinter.messagebox import *
import orm
from Tablas.Alumnos import Alumnos
import os

db=orm.SQLiteORM("Registros alumnos")
db.crear_tabla(Alumnos)

def f_limpiar(ventana):
    if not ventana:
        ventana = Tk()  # Usa la ventana actual si no se proporciona ninguna ventana

    ventana.nombre_texto.delete(0, END)
    ventana.cantidad_texto.delete(0, END)
    ventana.precio_texto.delete(0, END)
    ventana.nombre_texto.focus()

def f_nuevo(ventana):
    nombre=ventana.nombre_texto.get()
    cantidad=ventana.cantidad_texto.get()
    precio=ventana.precio_texto.get()
    ventana.tabla_datos.insert("",END,text=nombre,values=(cantidad,precio))
    date={
        "Nombre":nombre,
        "Apellido":cantidad,
        "DNI":precio
    }
    db.insertarUno('Alumnos',date)
    showinfo(title="Nuevo",message="Nuevo producto agregado")
    id=db.mostrar('Alumnos',where=f'DNI={precio}')[0][0]
    f_limpiar(ventana)

def f_eliminar(ventana):
    item_seleccionado = ventana.tabla_datos.selection()

    if item_seleccionado:
        dato = ventana.tabla_datos.item(item_seleccionado)['text']

        # Eliminar de la base de datos
        if db.eliminar('Alumnos', where=f"Nombre='{dato}'"):
            showinfo(title="ELIMINAR", message="Se eliminó con éxito el producto de la base de datos")
        else:
            showinfo(title="ERROR", message="Se eliminó con éxito el producto de la base de datos")

        # Eliminar de la tabla
        ventana.tabla_datos.delete(item_seleccionado)
        f_limpiar(ventana)
    else:
        showinfo(title="ADVERTENCIA", message="Selecciona una fila para eliminar.")

def f_actualizar(ventana):
    if not ventana.nombre_texto.get():
        showerror(title="SIN DATOS", message="No hay nada para actualizar")
    else:
        nombre = ventana.nombre_texto.get()
        cantidad = ventana.cantidad_texto.get()
        precio = ventana.precio_texto.get()
        elem_actualizar = ventana.tabla_datos.selection()

        mensaje = askyesno(title="Actualizar", message="¿Estás seguro que deseas actualizar?")

        if mensaje:
            # Actualizar en la base de datos
            data = {"Nombre": nombre, "Apellido": cantidad, "DNI": precio}
            db.actualizar('Alumnos', data, f"Nombre='{nombre}'")

            # Refrescar toda la tabla
            f_mostrar_tabla(ventana)

            showinfo(title="ACTUALIZAR", message="Se actualizó con éxito el registro")
            f_limpiar(ventana)
            ventana.tabla_datos.selection_remove(elem_actualizar)
        else:
            showinfo(title="NO ACTUALIZO", message="No se actualizó ningún registro")
            f_limpiar(ventana)
            ventana.tabla_datos.selection_remove(elem_actualizar)


# Función para mostrar todos los registros en la tabla
def f_mostrar_tabla(ventana):
    # Limpiar la tabla
    for item in ventana.tabla_datos.get_children():
        ventana.tabla_datos.delete(item)

    # Obtener todos los registros de la base de datos
    registros = json.loads(db.mostrar('Alumnos'))

    # Insertar registros en la tabla
    for registro in registros:
        nombre = registro["Nombre"]
        cantidad = registro["Apellido"]
        precio = registro["DNI"]
        ventana.tabla_datos.insert("", END, text=nombre, values=(cantidad, precio))
def f_dobleClick(ventana,event):
    elem_actualizar=ventana.tabla_datos.selection()
    captura_datos=ventana.tabla_datos.item(elem_actualizar)
    mensaje=askyesno(title="ACTUALIZAR",message="Desea actualizar los datos")
    if mensaje == True:
        nombre=captura_datos["text"]
        cantidad=captura_datos["values"][0]
        precio=captura_datos["values"][1]
        ventana.nombre_texto.insert(0,nombre)
        ventana.cantidad_texto.insert(0,cantidad)
        ventana.precio_texto.insert(0,precio)
        ventana.tabla_datos.selection_remove(elem_actualizar)
    else:
        showinfo(title="ACTUALIZAR",message="Ningun registro seleccionado para actualizar")
        ventana.tabla_datos.selection_remove(elem_actualizar)
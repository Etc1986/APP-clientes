from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()

root.title('@etcD  CRM')

conn = sqlite3.connect('crm.db')

c = conn.cursor()

c.execute("""
          CREATE TABLE if not exists cliente(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT NOT NULL,
          telefono TEXT NOT NULL,
          empresa TEXT NOT NULL,
          email TEXT NOT NULL
          );
""")
def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3], row[4]))
 
def insertar(cliente):
    c.execute("""
              INSERT INTO cliente (nombre, telefono, empresa, email) VALUES (?, ?, ?, ?)
    """,(cliente['nombre'], cliente['telefono'], cliente['empresa'], cliente['email']))
    conn.commit()
    render_clientes()

def nuevo_cliente():
    def guardar():
        if not nombre.get():
            messagebox.showerror('Error', 'el nombre es necesario')
            return 
        if not telefono.get():
            messagebox.showerror('Error', 'el telefono es necesario')
            return
        if not empresa.get():
            messagebox.showerror('Error' , 'el empresa es necesario')
            return
        if not email.get():
            messagebox.showerror('Error', 'el email es necesario')
            return

        cliente = {
            'nombre': nombre.get(),
            'telefono': telefono.get(),
            'empresa': empresa.get(),
            'email': email.get()
        }
        insertar(cliente)
        top.destroy()

    top = Toplevel()
    top.title('Nuevo Cliente')

    lnombre = Label(top, text='Nombre')
    nombre = Entry(top, width=45)
    lnombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)

    ltelefono = Label(top, text='Telefono')
    telefono = Entry(top, width=45)
    ltelefono.grid(row=1, column=0)
    telefono.grid(row=1, column=1)
    
    lempresa = Label(top, text='Empresa')
    empresa = Entry(top, width=45)
    lempresa.grid(row=2, column=0)
    empresa.grid(row=2, column=1)
    
    lemail = Label(top, text='Email')
    email = Entry(top, width=45)
    lemail.grid(row=3, column=0)
    email.grid(row=3, column=1)

    guardar = Button(top, text='Guardar', command=guardar)
    guardar.grid(row=4, column=1)

    top.mainloop()

def delete_cliente():
    id = tree.selection()[0]
    
    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id, )).fetchone()
    respuesta = messagebox.askokcancel('Seguro?', 'estás seguro de querer eliminar el cliente '+ cliente[1] +'?')
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?",(id, ))
        conn.commit()
        render_clientes()
    else:
        pass

btn = Button(root, text='Nuevo Cliente', command= nuevo_cliente)
btn.grid(column=0, row=0)


btn_eliminar = Button(root, text='Eliminar Cliente', command= delete_cliente)
btn_eliminar.grid(column=1, row=0)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Telefono', 'Empresa', 'Email')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')
tree.column('Email')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Telefono')
tree.heading('Empresa', text='Empresa')
tree.heading('Email', text='Email')
tree.grid(column=0, row=1, columnspan=2)

render_clientes()

root.mainloop()

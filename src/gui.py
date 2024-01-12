import tkinter as tk
import threading as th
from tkinter import messagebox, filedialog
from main import main


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def select_template_file():
    template_path = filedialog.askopenfilename(filetypes=[("All files", "*")])
    template_entry.delete(0, tk.END)
    template_entry.insert(0, template_path)

def select_data_file():
    data_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    data_entry.delete(0, tk.END)
    data_entry.insert(0, data_path)

def execute_script():
    popup = tk.Toplevel(root)
    popup.title("Aguarde")
    popup.geometry("200x100")
    label = tk.Label(popup, text="Criando relatórios...")
    label.pack()

    try:
        folder = folder_entry.get()
        template = template_entry.get()
        data = data_entry.get()

        process = th.Thread(target=main, args=(data, folder, template))
        process.start()
        process.join()
        messagebox.showinfo("Sucesso", "Relatórios criados com sucesso!", parent=root, icon="info", type="ok")
        popup.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        return

root = tk.Tk()
root.title("TOPINV - Gerador de Relatórios")


# Styling
root.geometry("700x200")
root.resizable(False, False)
root.tk_setPalette(background="#2D353A")

label_font = ("Arial", 12)
entry_font = ("Arial", 10)

# Labels
folder_label = tk.Label(root, text="Pasta de destino:", font=label_font, bg="#2D353A", fg="white")
folder_label.grid(row=0, column=0, pady=10)

template_label = tk.Label(root, text="Arquivo de template:", font=label_font, bg="#2D353A", fg="white")
template_label.grid(row=1, column=0, pady=10)

data_label = tk.Label(root, text="Planilha de dados:", font=label_font, bg="#2D353A", fg="white")
data_label.grid(row=2, column=0, pady=10)

# logo_label = ttk.Label(root, image=logo_image)
# logo_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

# Entries
folder_entry = tk.Entry(root, font=entry_font, width=40, bg="#f0f0f0", fg="#2D353A")
folder_entry.grid(row=0, column=1, padx=10)

template_entry = tk.Entry(root, font=entry_font, width=40, bg="#f0f0f0", fg="#2D353A")
template_entry.grid(row=1, column=1, padx=10)

data_entry = tk.Entry(root, font=entry_font, width=40, bg="#f0f0f0", fg="#2D353A")
data_entry.grid(row=2, column=1, padx=10)

# Buttons
folder_button = tk.Button(root, text="Selecionar Pasta de Destino", command=select_folder, font=label_font, bg="#2D353A", fg="white")
folder_button.grid(row=0, column=2, padx=15)

template_button = tk.Button(root, text="Selecionar Template", command=select_template_file, font=label_font, bg="#2D353A", fg="white")
template_button.grid(row=1, column=2, padx=15)

data_button = tk.Button(root, text="Selecionar Planilha de Dados", command=select_data_file, font=label_font, bg="#2D353A", fg="white")
data_button.grid(row=2, column=2, padx=15)

run_button = tk.Button(root, text="Criar relatórios", command=execute_script, font=label_font, bg="#5cb85c", fg="#2D353A")
run_button.grid(row=3, columnspan=3, pady=15)
root.mainloop()
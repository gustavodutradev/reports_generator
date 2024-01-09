import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
from tkinter import messagebox

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

def run_main():
    def execute_script():

        popup = tk.Toplevel(root)
        popup.title("Aguarde")
        popup.geometry("200x100")
        label = tk.Label(popup, text="Criando relatórios...")
        label.pack()

        folder = folder_entry.get()
        template = template_entry.get()
        data = data_entry.get()
        subprocess.run(["python", "main.py", folder, template, data])

        popup.destroy()

        messagebox.showinfo("Sucesso", "Relatórios criados com sucesso!")

    thread = threading.Thread(target=execute_script)
    thread.start()

root = tk.Tk()
root.title("Selecionar Pasta e Arquivos")

# Styling
root.geometry("800x200")
root.configure(bg="#f0f0f0")

label_font = ("Arial", 12)
entry_font = ("Arial", 10)

# Labels
folder_label = tk.Label(root, text="Selecione a pasta:", font=label_font, bg="#f0f0f0")
folder_label.grid(row=0, column=0, pady=5)

template_label = tk.Label(root, text="Selecione o arquivo de template:", font=label_font, bg="#f0f0f0")
template_label.grid(row=1, column=0, pady=5)

data_label = tk.Label(root, text="Selecione o arquivo de dados:", font=label_font, bg="#f0f0f0")
data_label.grid(row=2, column=0, pady=5)

# Entries
folder_entry = tk.Entry(root, font=entry_font, width=30)
folder_entry.grid(row=0, column=1, padx=10)

template_entry = tk.Entry(root, font=entry_font, width=30)
template_entry.grid(row=1, column=1, padx=10)

data_entry = tk.Entry(root, font=entry_font, width=30)
data_entry.grid(row=2, column=1, padx=10)

# Buttons
folder_button = tk.Button(root, text="Selecionar Pasta de Destino", command=select_folder, font=label_font, bg="#d3d3d3")
folder_button.grid(row=0, column=2, padx=15)

template_button = tk.Button(root, text="Selecionar Template", command=select_template_file, font=label_font, bg="#d3d3d3")
template_button.grid(row=1, column=2, padx=15)

data_button = tk.Button(root, text="Selecionar Planilha de Dados", command=select_data_file, font=label_font, bg="#d3d3d3")
data_button.grid(row=2, column=2, padx=15)

run_button = tk.Button(root, text="Criar relatórios", command=run_main, font=label_font, bg="#5cb85c", fg="white")
run_button.grid(row=3, columnspan=3, pady=15)

root.mainloop()

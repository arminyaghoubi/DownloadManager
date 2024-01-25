import ttkbootstrap as ttk
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from urllib.request import urlretrieve
from urllib.parse import urlparse
import csv
import os

window = ttk.Window("Download Manager", themename="darkly")
window.config(pady=10, padx=20)

url_label = ttk.Label(text="URL ")
url_label.grid(row=0, column=0, pady=10, padx=10)

url_variable = ttk.StringVar()

url_entry = ttk.Entry(width=50, textvariable=url_variable)
url_entry.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

save_as_path = "SaveAsHistory.csv"


def get_save_as_history():
    history_list = []
    if os.path.exists(save_as_path):
        with open(save_as_path) as history_file:
            reader = csv.reader(history_file)
            for item in reader:
                history_list.append(item)
    return history_list


def add_save_as_history(path):
    history_list = get_save_as_history()
    if path not in history_list:
        with open(save_as_path, mode="a", encoding="utf-8", newline="") as history_file:
            writer = csv.writer(history_file)
            writer.writerow([path])


save_label = ttk.Label(text="Save as ")
save_label.grid(row=1, column=0, pady=10, padx=10)

path_variable = ttk.StringVar()

save_combobox = ttk.Combobox(width=40, textvariable=path_variable, state="readonly", values=get_save_as_history())
save_combobox.grid(row=1, column=1, pady=10, padx=10)


def browse_button_clicked():
    path = askdirectory(title="Browse Directory")
    if path:
        path_variable.set(path)


browse_button = ttk.Button(text="...", bootstyle="info-outline", command=browse_button_clicked)
browse_button.grid(row=1, column=2, pady=10, padx=10)


def download_button_clicked():
    if not (url_variable.get() and save_combobox.get()):
        Messagebox.show_error("Url and Save as Address is required!", "Required Error!!!")
    else:
        try:
            url = urlparse(url_variable.get())
            filename = os.path.basename(url.path)
            urlretrieve(url_variable.get(), f"{save_combobox.get()}/{filename}")
        except:
            Messagebox.show_error("Invalid URL!", "Invalid URL Error!!!")
        else:
            Messagebox.show_info("The download was done successfully.", "Information")
        finally:
            add_save_as_history(save_combobox.get())
            save_combobox.config(values=get_save_as_history())


download_button = ttk.Button(text="Start Download", bootstyle="primary", command=download_button_clicked)
download_button.grid(row=2, column=1, pady=10, padx=10)

window.mainloop()

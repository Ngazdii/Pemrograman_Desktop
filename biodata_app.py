import tkinter as tk
from tkinter import messagebox

def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return
    
    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    jenis_kelamin = var_jk.get()

    if not nama or not nim or not jurusan:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("Data Tersimpan", hasil)

def validate_form(*args):
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    setuju_valid = var_setuju.get() == 1

    if nama_valid and nim_valid and jurusan_valid and setuju_valid:
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Form Biodata Mahasiswa")
window.geometry("500x600")
window.resizable(True, True)
window.minsize(500, 600)

main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.grid_columnconfigure(1, weight=1)

var_jk = tk.StringVar(value="Pria")
var_setuju = tk.IntVar()

var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()

var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)

label_jk = tk.Label(master=main_frame, text="Jenis Kelamin:", font=("times new roman", 12))
label_jk.grid(row=4, column=0, sticky="W", pady=5)

frame_jk = tk.Frame(master=main_frame)
frame_jk.grid(row=4, column=1, sticky="W")

radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
radio_pria.pack(side=tk.LEFT)

radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
radio_wanita.pack(side=tk.LEFT)

check_setuju = tk.Checkbutton(
    master=main_frame,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("times new roman", 10),
    command=validate_form  # Tambahkan ini
)

check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit Biodata", 
    font=("Arial", 12, "bold"),
    command=submit_data,
    state=tk.DISABLED  # Tambahkan ini
)
btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

label_judul = tk.Label(master=main_frame, text="FORM BIODATA MAHSISWA", font=("times new roman", 16, "bold"), fg="white", bg="blue")
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

label_nama = tk.Label(master=main_frame, text="Nama Lengkap:", font=("times new roman", 12))
label_nama.grid(row=1, column=0, sticky="W", pady=5)
entry_nama = tk.Entry(master=frame_input, width=30, font=("times new roman", 12), textvariable=var_nama)
entry_nama.grid(row=1, column=1, pady=5)

label_nim = tk.Label(master=main_frame, text="NIM:", font=("times new roman", 12))
label_nim.grid(row=2, column=0, sticky="W", pady=5)
entry_nim = tk.Entry(master=frame_input, width=30, font=("times new roman", 12), textvariable=var_nim)
entry_nim.grid(row=2, column=1, pady=5)

label_jurusan = tk.Label(master=main_frame, text="Jurusan:", font=("times new roman", 12))
label_jurusan.grid(row=3, column=0, sticky="W", pady=5)
entry_jurusan = tk.Entry(master=frame_input, width=30, font=("times new roman", 12), textvariable=var_jurusan)
entry_jurusan.grid(row=3, column=1, pady=5)

main_frame.columnconfigure(1, weight=1)
window.configure(bg="skyblue")
window.mainloop()
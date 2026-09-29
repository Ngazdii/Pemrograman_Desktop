import tkinter as tk
from tkinter import messagebox
import datetime

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("500x600")
        self.resizable(True, True)

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "azdi": "sidamulya123",
            "mahasiswa": "123456"
        }

        # Status login
        self.current_user = None

        # Warna background berdasarkan username
        self.warna_per_user = {
            "admin": "#dfeeff",
            "azdi": "#dff7df",
            "mahasiswa": "#ffd9cc"
        }

        # Atribut untuk manajemen frame
        self.frame_aktif = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)
        

    def _buat_tampilan_biodata(self):  

        # --- Variabel Kontrol Tkinter ---
        # Variabel-variabel berikut sekarang menjadi atribut dari instance kelas
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # --- Frame Utama ---
        # Frame utama juga menjadi atribut
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)

        # --- Membuat dan Menempatkan Widget ---
        # Header halaman biodata
        self.frame_header = tk.Frame(master=self.frame_biodata)
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky="EW", pady=(0, 14))
        self.frame_header.grid_columnconfigure(1, weight=1)

        self.label_judul = tk.Label(
            master=self.frame_header, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, sticky="W")

        self.btn_logout = tk.Button(
            master=self.frame_header,
            text="Logout",
            font=("Arial", 10, "bold"),
            bg="#c62828",
            fg="#ffffff",
            activebackground="#a61f1f",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._logout
        )
        self.btn_logout.grid(row=0, column=1, sticky="E", padx=(12, 0))

        # Frame khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.frame_biodata, 
            relief=tk.GROOVE, 
            borderwidth=2, 
            padx=10, 
            pady=10
        )

        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input, 
            text="Nama Lengkap:", 
            font=("Arial", 12)
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input, 
            text="NIM:", 
            font=("Arial", 12)
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, pady=2)

        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input, 
            text="Jurusan:", 
            font=("Arial", 12)
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input alamat dengan Text widget
        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat:", 
            font=("Arial", 12)
        )
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(
            master=self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=1
        )

        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(
            master=self.frame_alamat,
            height=5, 
            width=28, 
            font=("Arial", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=3, column=1, pady=2)

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(row=4, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=4, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk,
            text="Pria", 
            variable=self.var_jk, 
            value="Pria"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT
        )
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        # (Di sini kita akan meletakkan semua kode GUI nantinya)

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=30, pady=30, bg="#e9ecef")
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_rowconfigure(0, weight=1)

        self.panel_login = tk.Frame(
            master=self.frame_login,
            bg="#ffffff",
            padx=30,
            pady=28,
            highlightbackground="#d1d5da",
            highlightthickness=1
        )
        self.panel_login.grid(row=0, column=0)
        self.panel_login.grid_columnconfigure(0, weight=1)

        self.label_login_judul = tk.Label(
            self.panel_login,
            text="BIODATA MAHASISWA",
            font=("Arial", 17, "bold"),
            bg="#41464d",
            fg="#ffffff",
            padx=18,
            pady=14
        )
        self.label_login_judul.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.label_login_subjudul = tk.Label(
            self.panel_login,
            text="Silakan masuk untuk melanjutkan",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#6c757d"
        )
        self.label_login_subjudul.grid(row=1, column=0, sticky="w", pady=(0, 18))

        tk.Label(
            self.panel_login,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#343a40"
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.entry_username = tk.Entry(
            self.panel_login,
            width=32,
            font=("Arial", 11),
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#ced4da",
            highlightcolor="#6c757d"
        )
        self.entry_username.grid(row=3, column=0, sticky="ew", ipady=6, pady=(0, 14))

        tk.Label(
            self.panel_login,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#343a40"
        ).grid(row=4, column=0, sticky="w", pady=(0, 5))

        self.entry_password = tk.Entry(
            self.panel_login,
            width=32,
            font=("Arial", 11),
            show="*",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#ced4da",
            highlightcolor="#6c757d"
        )
        self.entry_password.grid(row=5, column=0, sticky="ew", ipady=6)

        self.btn_login = tk.Button(
            self.panel_login,
            text="MASUK",
            font=("Arial", 11, "bold"),
            bg="#495057",
            fg="#ffffff",
            activebackground="#343a40",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._coba_login
        )
        self.btn_login.grid(row=6, column=0, sticky="ew", ipady=7, pady=(20, 16))

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        self.label_info_login = tk.Label(
            self.panel_login,
            text="AKUN DEMO\nadmin / 123   |   azdi / sidamulya123\nmahasiswa / 123456",
            font=("Arial", 9),
            fg="#6c757d",
            bg="#f1f3f5",
            justify=tk.LEFT,
            padx=10,
            pady=9
        )
        self.label_info_login.grid(row=7, column=0, sticky="ew")

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.grid_remove()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.grid(row=0, column=0, sticky="NSEW")

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _coba_login(self):
        """Method untuk memproses attempt login"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Validasi input kosong
        if not username or not password:
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._atur_warna_berdasarkan_user()
            self._buat_menu()
            self._pindah_ke(self.frame_biodata)
            # Bersihkan field login setelah berhasil
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            # Bersihkan password dan focus ke username
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _atur_warna_berdasarkan_user(self):
        """Ubah background aplikasi sesuai username yang sedang aktif."""
        if self.current_user and self.current_user in self.warna_per_user:
            warna = self.warna_per_user[self.current_user]
        else:
            warna = "#f0f0f0"

        self.configure(bg=warna)

        if hasattr(self, "frame_biodata"):
            self.frame_biodata.configure(bg=warna)
        if hasattr(self, "frame_header"):
            self.frame_header.configure(bg=warna)
        if hasattr(self, "frame_input"):
            self.frame_input.configure(bg=warna)
        if hasattr(self, "frame_alamat"):
            self.frame_alamat.configure(bg=warna)
        if hasattr(self, "frame_jk"):
            self.frame_jk.configure(bg=warna)

        for widget in [
            getattr(self, "label_judul", None),
            getattr(self, "label_nama", None),
            getattr(self, "label_nim", None),
            getattr(self, "label_jurusan", None),
            getattr(self, "label_alamat", None),
            getattr(self, "label_jk", None),
            getattr(self, "radio_pria", None),
            getattr(self, "radio_wanita", None),
            getattr(self, "check_setuju", None),
            getattr(self, "label_hasil", None),
        ]:
            if widget is not None:
                widget.configure(bg=warna, fg="#222222")

        for widget in [
            getattr(self, "btn_submit", None),
        ]:
            if widget is not None:
                widget.configure(bg="#f7f7f7")

        for widget in [
            getattr(self, "entry_nama", None),
            getattr(self, "entry_nim", None),
            getattr(self, "entry_jurusan", None),
            getattr(self, "text_alamat", None),
            getattr(self, "entry_username", None),
            getattr(self, "entry_password", None),
        ]:
            if widget is not None:
                widget.configure(bg="#ffffff")

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                self._tampilkan_error_nim()
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Tampilkan hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def _tampilkan_error_nim(self):
        dialog = tk.Toplevel(self)
        dialog.title("Format NIM Salah")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.configure(bg="#f1f3f5")

        panel = tk.Frame(dialog, bg="#ffffff", padx=22, pady=20)
        panel.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        panel.grid_columnconfigure(1, weight=1)

        icon = tk.Canvas(
            panel,
            width=48,
            height=48,
            bg="#ffffff",
            highlightthickness=0
        )
        icon.create_oval(4, 4, 44, 44, fill="#dc3545", outline="#dc3545")
        icon.create_text(24, 23, text="!", fill="#ffffff", font=("Arial", 22, "bold"))
        icon.grid(row=0, column=0, rowspan=2, padx=(0, 14), sticky="n")

        tk.Label(
            panel,
            text="NIM tidak valid",
            font=("Arial", 12, "bold"),
            fg="#343a40",
            bg="#ffffff"
        ).grid(row=0, column=1, sticky="w")
        tk.Label(
            panel,
            text="NIM harus berupa angka minimal 8 digit.",
            font=("Arial", 10),
            fg="#495057",
            bg="#ffffff",
            wraplength=260,
            justify=tk.LEFT
        ).grid(row=1, column=1, sticky="w", pady=(4, 0))

        tombol_ok = tk.Button(
            panel,
            text="OK",
            font=("Arial", 10, "bold"),
            bg="#495057",
            fg="#ffffff",
            activebackground="#343a40",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=dialog.destroy
        )
        tombol_ok.grid(row=2, column=1, sticky="e", pady=(18, 0))

        dialog.bind("<Return>", lambda event: dialog.destroy())
        dialog.bind("<Escape>", lambda event: dialog.destroy())
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        dialog.grab_set()
        tombol_ok.focus_set()
        dialog.wait_window()

    def validate_form(self, *args):
        form_is_valid = all((
            self.var_nama.get().strip(),
            self.var_nim.get().strip(),
            self.var_jurusan.get().strip(),
            self.var_setuju.get() == 1,
        ))

        if hasattr(self, "btn_submit"):
            self.btn_submit.config(
                state=tk.NORMAL if form_is_valid else tk.DISABLED
            )

    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def _logout(self):
        """Method untuk logout dan kembali ke halaman login"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            # Reset status user
            self.current_user = None
            # Hapus menu
            self._hapus_menu()
            # Update title
            self._update_title_with_user()
            # Reset background ke default
            self._atur_warna_berdasarkan_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    def on_enter(self, event):
        if self.btn_submit["state"] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event):
        self.submit_data()
        return "break"

    

# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()
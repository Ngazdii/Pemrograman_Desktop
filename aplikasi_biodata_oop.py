import tkinter as tk
from tkinter import messagebox
import calendar
import datetime
import logging
from pathlib import Path
import re

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x760")
        self.resizable(True, True)
        self.username_storage_path = Path(__file__).with_name(".username_tersimpan")
        self.remembered_username = self._muat_username_tersimpan()
        self.password_visible = False

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
            "admin": "#649bda",
            "azdi": "#95cb95",
            "mahasiswa": "#DEA48B"
        }

        # Atribut untuk manajemen frame
        self.frame_aktif = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        self._buat_menu()
        self.protocol("WM_DELETE_WINDOW", self.keluar_aplikasi)

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        # Log aplikasi start
        logging.info("Aplikasi dimulai")
        

    def _buat_tampilan_biodata(self):  

        # --- Variabel Kontrol Tkinter ---
        # Variabel-variabel berikut sekarang menjadi atribut dari instance kelas
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tanggal_lahir = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_tanggal_lahir.trace_add("write", self.validate_form)

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

        # Input email
        self.label_email = tk.Label(
            master=self.frame_input,
            text="Email:",
            font=("Arial", 12)
        )
        self.label_email.grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_email
        )
        self.entry_email.grid(row=3, column=1, pady=2)

        # Input telepon hanya menerima angka
        validasi_telepon = (self.register(self._hanya_angka), "%P")
        self.label_telepon = tk.Label(
            master=self.frame_input,
            text="Telepon:",
            font=("Arial", 12)
        )
        self.label_telepon.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_telepon,
            validate="key",
            validatecommand=validasi_telepon
        )
        self.entry_telepon.grid(row=4, column=1, pady=2)

        # Pilih tanggal lahir melalui kalender
        self.label_tanggal_lahir = tk.Label(
            master=self.frame_input,
            text="Tanggal Lahir:",
            font=("Arial", 12)
        )
        self.label_tanggal_lahir.grid(row=5, column=0, sticky="W", pady=2)
        self.frame_tanggal_lahir = tk.Frame(master=self.frame_input)
        self.frame_tanggal_lahir.grid(row=5, column=1, sticky="EW", pady=2)
        self.frame_tanggal_lahir.grid_columnconfigure(0, weight=1)
        self.entry_tanggal_lahir = tk.Entry(
            master=self.frame_tanggal_lahir,
            width=20,
            font=("Arial", 12),
            textvariable=self.var_tanggal_lahir,
            state="readonly"
        )
        self.entry_tanggal_lahir.grid(row=0, column=0, sticky="EW")
        self.btn_pilih_tanggal = tk.Button(
            master=self.frame_tanggal_lahir,
            text="Pilih",
            command=self._buka_kalender
        )
        self.btn_pilih_tanggal.grid(row=0, column=1, padx=(6, 0))

        # Input alamat dengan Text widget
        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat:", 
            font=("Arial", 12)
        )
        self.label_alamat.grid(row=6, column=0, sticky="NW", pady=2)

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
        self.frame_alamat.grid(row=6, column=1, pady=2)

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=7, column=1, sticky="W")

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
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
        self.frame_actions = tk.Frame(master=self.frame_biodata)
        self.frame_actions.grid(row=6, column=0, columnspan=2, sticky="EW", pady=20)
        self.frame_actions.grid_columnconfigure(0, weight=1)
        self.frame_actions.grid_columnconfigure(1, weight=1)

        self.btn_reset = tk.Button(
            master=self.frame_actions,
            text="Reset Form",
            font=("Arial", 12, "bold"),
            bg="#f7f7f7",
            command=self._reset_form_biodata
        )
        self.btn_reset.grid(row=0, column=0, sticky="EW", padx=(0, 6))

        self.btn_submit = tk.Button(
            master=self.frame_actions,
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=0, column=1, sticky="EW", padx=(6, 0))

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
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

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

        self.frame_password = tk.Frame(master=self.panel_login, bg="#ffffff")
        self.frame_password.grid(row=5, column=0, sticky="ew")
        self.frame_password.grid_columnconfigure(0, weight=1)

        self.entry_password = tk.Entry(
            self.frame_password,
            width=32,
            font=("Arial", 11),
            show="*",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#ced4da",
            highlightcolor="#6c757d"
        )
        self.entry_password.grid(row=0, column=0, sticky="ew", ipady=6)

        self.btn_toggle_password = tk.Canvas(
            self.frame_password,
            width=32,
            height=26,
            bg="#ffffff",
            highlightthickness=0,
            cursor="hand2",
            takefocus=True
        )
        self.btn_toggle_password.grid(row=0, column=1, padx=(8, 0))
        self.btn_toggle_password.bind("<Button-1>", self._toggle_password_visibility)
        self.btn_toggle_password.bind("<Return>", self._toggle_password_visibility)
        self.btn_toggle_password.bind("<space>", self._toggle_password_visibility)
        self._gambar_ikon_password()

        self.var_remember_me = tk.BooleanVar(value=bool(self.remembered_username))
        if self.remembered_username:
            self.entry_username.insert(0, self.remembered_username)

        self.check_remember_me = tk.Checkbutton(
            self.panel_login,
            text="Ingat username",
            variable=self.var_remember_me,
            command=self._ubah_remember_me,
            font=("Arial", 9),
            bg="#ffffff",
            fg="#343a40",
            activebackground="#ffffff",
            anchor="w"
        )
        self.check_remember_me.grid(row=6, column=0, sticky="w", pady=(8, 0))

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
        self.btn_login.grid(row=7, column=0, sticky="ew", ipady=7, pady=(14, 16))

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
        self.label_info_login.grid(row=8, column=0, sticky="ew")

    def _muat_username_tersimpan(self):
        try:
            return self.username_storage_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return ""
        except OSError:
            logging.exception("Gagal membaca username yang tersimpan")
            messagebox.showerror(
                "Gagal Membaca Preferensi",
                "Username tersimpan tidak dapat dibaca."
            )
            return ""

    def _simpan_username_tersimpan(self, username):
        try:
            if username:
                self.username_storage_path.write_text(username, encoding="utf-8")
            elif self.username_storage_path.exists():
                self.username_storage_path.unlink()
        except OSError:
            logging.exception("Gagal menyimpan preferensi username")
            messagebox.showerror(
                "Gagal Menyimpan Preferensi",
                "Preferensi username tidak dapat disimpan."
            )

    def _ubah_remember_me(self):
        if not self.var_remember_me.get():
            self.remembered_username = ""
            self._simpan_username_tersimpan("")

    def _toggle_password_visibility(self, event):
        event.widget.focus_set()
        self.password_visible = not self.password_visible
        self.entry_password.configure(show="" if self.password_visible else "*")
        self._gambar_ikon_password()
        return "break"

    def _gambar_ikon_password(self):
        self.btn_toggle_password.delete("all")
        self.btn_toggle_password.create_polygon(
            3, 13, 10, 6, 16, 4, 22, 6, 29, 13, 22, 20, 16, 22, 10, 20,
            smooth=True,
            fill="#ffffff",
            outline="#495057",
            width=2
        )
        self.btn_toggle_password.create_oval(
            12, 9, 20, 17,
            fill="#495057",
            outline="#495057"
        )
        if not self.password_visible:
            self.btn_toggle_password.create_line(
                5, 22, 27, 4,
                fill="#495057",
                width=2
            )

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
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            self.remembered_username = username if self.var_remember_me.get() else ""
            self._simpan_username_tersimpan(self.remembered_username)
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._atur_warna_berdasarkan_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_password.configure(show="*")
            self.password_visible = False
            self._gambar_ikon_password()
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tanggal_lahir.set("")
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
        if hasattr(self, "frame_actions"):
            self.frame_actions.configure(bg=warna)
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
            getattr(self, "label_email", None),
            getattr(self, "label_telepon", None),
            getattr(self, "label_tanggal_lahir", None),
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
            getattr(self, "entry_email", None),
            getattr(self, "entry_telepon", None),
            getattr(self, "entry_tanggal_lahir", None),
            getattr(self, "text_alamat", None),
            getattr(self, "entry_username", None),
            getattr(self, "entry_password", None),
        ]:
            if widget is not None:
                widget.configure(bg="#ffffff")
        if hasattr(self, "frame_tanggal_lahir"):
            self.frame_tanggal_lahir.configure(bg=warna)
        if hasattr(self, "entry_tanggal_lahir"):
            self.entry_tanggal_lahir.configure(readonlybackground="#ffffff")

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
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tanggal_lahir = self.var_tanggal_lahir.get().strip()
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

            if not self._email_valid(email):
                messagebox.showwarning("Format Email Salah", "Masukkan alamat email dengan format yang valid.")
                self.entry_email.focus_set()
                return

            if not self._telepon_valid(telepon):
                messagebox.showwarning(
                    "Format Telepon Salah",
                    "Telepon harus berupa 10-13 digit yang diawali 08, atau 11-14 digit yang diawali 628."
                )
                self.entry_telepon.focus_set()
                return

            if not self._tanggal_lahir_valid(tanggal_lahir):
                messagebox.showwarning("Tanggal Lahir Salah", "Pilih tanggal lahir yang valid dan tidak di masa depan.")
                self.btn_pilih_tanggal.focus_set()
                return

            # Tampilkan hasil
            hasil = (
                f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                f"Email: {email}\nTelepon: {telepon}\nTanggal Lahir: {tanggal_lahir}\n"
                f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            )
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            # Log successful data submission
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.exception(f"Error in submit_data by {self.current_user}")
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
            self._email_valid(self.var_email.get().strip()),
            self._telepon_valid(self.var_telepon.get().strip()),
            self._tanggal_lahir_valid(self.var_tanggal_lahir.get().strip()),
            self.var_setuju.get() == 1,
        ))

        if hasattr(self, "btn_submit"):
            self.btn_submit.config(
                state=tk.NORMAL if form_is_valid else tk.DISABLED
            )

    @staticmethod
    def _hanya_angka(value):
        return all("0" <= karakter <= "9" for karakter in value)

    @staticmethod
    def _email_valid(email):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))

    @staticmethod
    def _telepon_valid(telepon):
        return bool(re.fullmatch(r"(?:08\d{8,11}|628\d{8,11})", telepon))

    @staticmethod
    def _tanggal_lahir_valid(tanggal_lahir):
        try:
            tanggal = datetime.datetime.strptime(tanggal_lahir, "%d/%m/%Y").date()
        except ValueError:
            return False
        return tanggal <= datetime.date.today()

    def _buka_kalender(self):
        tanggal_terpilih = None
        if self._tanggal_lahir_valid(self.var_tanggal_lahir.get()):
            tanggal_terpilih = datetime.datetime.strptime(
                self.var_tanggal_lahir.get(), "%d/%m/%Y"
            ).date()
        tanggal_awal = tanggal_terpilih or datetime.date.today()

        dialog = tk.Toplevel(self)
        dialog.title("Pilih Tanggal Lahir")
        dialog.resizable(False, False)
        dialog.transient(self)

        bulan_indonesia = (
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        )
        bulan_tampil = {"tahun": tanggal_awal.year, "bulan": tanggal_awal.month}
        header = tk.Frame(dialog, padx=8, pady=8)
        header.pack(fill=tk.X)
        tombol_bulan_sebelumnya = tk.Button(header, text="<", width=3)
        tombol_bulan_sebelumnya.pack(side=tk.LEFT)
        frame_judul_bulan = tk.Frame(header)
        frame_judul_bulan.pack(side=tk.LEFT, expand=True)
        tombol_pilih_bulan = tk.Button(
            frame_judul_bulan,
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        tombol_pilih_bulan.pack(side=tk.LEFT)
        tombol_pilih_tahun = tk.Button(
            frame_judul_bulan,
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        tombol_pilih_tahun.pack(side=tk.LEFT, padx=(4, 0))
        tombol_bulan_selanjutnya = tk.Button(header, text=">", width=3)
        tombol_bulan_selanjutnya.pack(side=tk.RIGHT)

        frame_konten = tk.Frame(dialog, padx=8, pady=4)
        frame_konten.pack(pady=(0, 8))
        frame_hari = tk.Frame(frame_konten)
        frame_bulan = tk.Frame(frame_konten)
        frame_tahun = tk.Frame(frame_konten)
        variabel_tahun = tk.StringVar(value=str(tanggal_awal.year))

        def tampilkan_kalender():
            frame_bulan.pack_forget()
            frame_tahun.pack_forget()
            frame_hari.pack()
            gambar_kalender()

        def pilih_bulan(bulan):
            bulan_tampil["bulan"] = bulan
            tampilkan_kalender()

        def pilih_tahun():
            try:
                tahun = int(variabel_tahun.get())
            except ValueError:
                messagebox.showwarning("Tahun Tidak Valid", "Masukkan tahun berupa angka.", parent=dialog)
                return
            if not 1 <= tahun <= datetime.date.today().year:
                messagebox.showwarning(
                    "Tahun Tidak Valid",
                    f"Tahun harus antara 1 dan {datetime.date.today().year}.",
                    parent=dialog
                )
                return
            bulan_tampil["tahun"] = tahun
            tampilkan_kalender()

        def tampilkan_pemilih_bulan():
            frame_hari.pack_forget()
            frame_tahun.pack_forget()
            for widget in frame_bulan.winfo_children():
                widget.destroy()
            for bulan, nama_bulan in enumerate(bulan_indonesia, start=1):
                tk.Button(
                    frame_bulan,
                    text=nama_bulan,
                    width=11,
                    command=lambda nilai=bulan: pilih_bulan(nilai)
                ).grid(row=(bulan - 1) // 3, column=(bulan - 1) % 3, padx=2, pady=2)
            frame_bulan.pack()

        def tampilkan_pemilih_tahun():
            frame_hari.pack_forget()
            frame_bulan.pack_forget()
            for widget in frame_tahun.winfo_children():
                widget.destroy()
            variabel_tahun.set(str(bulan_tampil["tahun"]))
            tk.Label(
                frame_tahun,
                text=f"Tahun (1–{datetime.date.today().year}):",
                font=("Arial", 10)
            ).pack(pady=(4, 6))
            tk.Spinbox(
                frame_tahun,
                from_=1,
                to=datetime.date.today().year,
                textvariable=variabel_tahun,
                width=10,
                justify=tk.CENTER,
                font=("Arial", 12)
            ).pack(pady=(0, 8))
            tk.Button(
                frame_tahun,
                text="Pilih Tahun",
                command=pilih_tahun
            ).pack()
            frame_tahun.pack()

        def pilih_tanggal(hari):
            tanggal = datetime.date(bulan_tampil["tahun"], bulan_tampil["bulan"], hari)
            self.var_tanggal_lahir.set(tanggal.strftime("%d/%m/%Y"))
            dialog.destroy()

        def ubah_bulan(perubahan):
            bulan = bulan_tampil["bulan"] + perubahan
            tahun = bulan_tampil["tahun"]
            if bulan < 1:
                bulan, tahun = 12, tahun - 1
            elif bulan > 12:
                bulan, tahun = 1, tahun + 1
            bulan_tampil.update(tahun=tahun, bulan=bulan)
            gambar_kalender()

        def gambar_kalender():
            for widget in frame_hari.winfo_children():
                widget.destroy()
            for kolom, nama_hari in enumerate(("Sn", "Sl", "Rb", "Km", "Jm", "Sb", "Mg")):
                tk.Label(
                    frame_hari,
                    text=nama_hari,
                    width=4,
                    font=("Arial", 9, "bold")
                ).grid(row=0, column=kolom, pady=(0, 4))

            tahun = bulan_tampil["tahun"]
            bulan = bulan_tampil["bulan"]
            tombol_pilih_bulan.config(text=bulan_indonesia[bulan - 1])
            tombol_pilih_tahun.config(text=str(tahun))
            variabel_tahun.set(str(tahun))
            bulan_sekarang = (tahun, bulan) >= (datetime.date.today().year, datetime.date.today().month)
            tombol_bulan_selanjutnya.config(
                state=tk.DISABLED if bulan_sekarang else tk.NORMAL
            )
            tombol_bulan_sebelumnya.config(
                state=tk.DISABLED if (tahun, bulan) <= (1, 1) else tk.NORMAL
            )

            for baris, minggu in enumerate(calendar.monthcalendar(tahun, bulan), start=1):
                for kolom, hari in enumerate(minggu):
                    if hari:
                        tanggal = datetime.date(tahun, bulan, hari)
                        tk.Button(
                            frame_hari,
                            text=str(hari),
                            width=4,
                            state=tk.NORMAL if tanggal <= datetime.date.today() else tk.DISABLED,
                            command=lambda nilai=hari: pilih_tanggal(nilai)
                        ).grid(row=baris, column=kolom, padx=1, pady=1)

        tombol_bulan_sebelumnya.config(command=lambda: ubah_bulan(-1))
        tombol_bulan_selanjutnya.config(command=lambda: ubah_bulan(1))
        tombol_pilih_bulan.config(command=tampilkan_pemilih_bulan)
        tombol_pilih_tahun.config(command=tampilkan_pemilih_tahun)
        tampilkan_kalender()
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        dialog.grab_set()
        dialog.wait_window()

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

            logging.info(f"Biodata saved by user: {self.current_user} - file: {filename}")
            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            logging.exception("Permission error while saving biodata for user: %s", self.current_user)
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            logging.exception("Error while saving biodata for user: %s", self.current_user)
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            self._atur_warna_berdasarkan_user()
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_password.configure(show="*")
            self.password_visible = False
            self._gambar_ikon_password()
            if self.var_remember_me.get():
                self.entry_username.insert(0, self.remembered_username)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

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
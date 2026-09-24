def __init__(self):
        # Memanggil constructor dari kelas induk (tk.Tk)
        super().__init__()

        # Mengkonfigurasi window utama
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Atribut untuk manajemen frame
        self.frame_aktif = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        def _coba_login(self):
                akun_valid = {
                    "admin": "123",
                    "user1": "password1",
                    "mahasiswa": "123456",
                }
                username = self.entry_username.get().strip()
                password = self.entry_password.get()
        
                if akun_valid.get(username) == password:
                    self._pindah_ke(self.frame_biodata)
                else:
                    messagebox.showerror("Login Gagal", "Username atau password salah.")
import tkinter as tk
from tkinter import messagebox, ttk
import random

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("740x600")
        self.window.resizable(False, False)
        
        # Atur warna latar belakang utama gelap (Dark Theme)
        self.window.configure(bg="#0F172A") # Deep Navy

        # 10 Data Soal (Multiple Choice)
        self.questions = [
            {
                "question": "1. Apa itu event-driven programming?",
                "options": [
                    "Program yang berjalan berurutan",
                    "Program yang merespons kejadian (event)",
                    "Program tanpa GUI",
                    "Program berbasis web"
                ],
                "correct": 1
            },
            {
                "question": "2. Widget Tkinter apa yang digunakan untuk pilihan tunggal (single-choice)?",
                "options": ["Checkbutton", "Entry", "Radiobutton", "Listbox"],
                "correct": 2
            },
            {
                "question": "3. Metode Tkinter apa yang digunakan untuk membuat loop timer/delay?",
                "options": ["sleep()", "after()", "delay()", "wait()"],
                "correct": 1
            },
            {
                "question": "4. Method apa yang dipanggil untuk memulai main loop Tkinter?",
                "options": ["window.start()", "window.run()", "window.mainloop()", "window.execute()"],
                "correct": 2
            },
            {
                "question": "5. Pengelola tata letak (layout manager) mana di Tkinter yang berbasis grid (baris & kolom)?",
                "options": ["pack", "grid", "place", "align"],
                "correct": 1
            },
            {
                "question": "6. Variabel khusus Tkinter untuk menyimpan data tipe integer pada state management adalah...",
                "options": ["IntVar()", "StringVar()", "BooleanVar()", "DoubleVar()"],
                "correct": 0
            },
            {
                "question": "7. Untuk menghubungkan event keyboard/mouse ke fungsi handler digunakan method...",
                "options": ["connect()", "listen()", "bind()", "attach()"],
                "correct": 2
            },
            {
                "question": "8. Widget mana yang digunakan untuk menampilkan indikator progress secara visual?",
                "options": ["Scale", "Spinbox", "Progressbar", "Scrollbar"],
                "correct": 2
            },
            {
                "question": "9. Apa fungsi dari 'command' attribute pada widget Button Tkinter?",
                "options": [
                    "Menentukan warna tombol",
                    "Menentukan fungsi callback saat tombol diklik",
                    "Menentukan teks tombol",
                    "Menentukan posisi tombol"
                ],
                "correct": 1
            },
            {
                "question": "10. Apa kegunaan utama dari refactoring kode ke struktur OOP pada GUI?",
                "options": [
                    "Membuat aplikasi berjalan lebih cepat di internet",
                    "Membuat kode lebih rapi, terstruktur, dan mudah dikembangkan",
                    "Menghilangkan kebutuhan akan fungsi/method",
                    "Mengubah tampilan GUI menjadi 3D"
                ],
                "correct": 1
            }
        ]

        # Acak urutan soal
        random.shuffle(self.questions)

        # State management
        self.current_question = 0
        self.score = 0
        self.time_left = 30
        self.timer_job = None
        self.selected_answer = tk.IntVar(value=-1)

        # Inisialisasi UI dan Event Binding
        self.buat_interface()
        self.setup_keyboard_shortcuts()
        self.load_question()
        self.start_timer()

    def buat_interface(self):
        # Styling Ttk Progressbar Custom
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", 
                        troughcolor="#1E293B", 
                        background="#06B6D4", # Cyan
                        thickness=12)

        # ----------------- HEADER PANEL -----------------
        self.header_frame = tk.Frame(self.window, bg="#1E293B", height=70)
        self.header_frame.pack(fill="x", side="top", ipady=12)

        # Score Badge (Pill Style)
        self.score_badge = tk.Label(
            self.header_frame,
            text=f"Score: {self.score}",
            font=("Segoe UI", 12, "bold"),
            bg="#10B981", # Emerald Green
            fg="white",
            padx=18,
            pady=6,
            relief="flat"
        )
        self.score_badge.pack(side="left", padx=25)

        # Title
        self.title_label = tk.Label(
            self.header_frame,
            text=" QUIZ INTERAKTIF ",
            font=("Segoe UI", 14, "bold"),
            bg="#1E293B",
            fg="#F1F5F9"
        )
        self.title_label.pack(side="left", expand=True)

        # Timer Badge (Warning Style)
        self.timer_badge = tk.Label(
            self.header_frame,
            text=f"Sisa Waktu: {self.time_left}s ⏱️",
            font=("Segoe UI", 12, "bold"),
            bg="#EF4444", # Red
            fg="white",
            padx=15,
            pady=6,
            relief="flat"
        )
        self.timer_badge.pack(side="right", padx=25)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.window,
            orient="horizontal",
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill="x", padx=25, pady=15)

        # ----------------- CARD CONTENT -----------------
        # Card Background
        self.card_frame = tk.Frame(self.window, bg="#1E293B", bd=0, highlightbackground="#334155", highlightthickness=1)
        self.card_frame.pack(fill="both", expand=True, padx=25, pady=5)

        # Feedback & Stat Subtitle
        self.stat_label = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#38BDF8", # Soft Blue
            padx=8,
            pady=4
        )
        self.stat_label.pack(anchor="w", padx=25, pady=(15, 5))

        # Question Label
        self.question_label = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            wraplength=640,
            justify="left",
            bg="#1E293B",
            fg="#F8FAFC"
        )
        self.question_label.pack(anchor="w", padx=25, pady=(5, 15))

        # Radiobuttons (Modern beralaskan panel)
        self.radio_frames = []
        self.radio_buttons = []
        
        for i in range(4):
            # Frame untuk membungkus radio button agar seperti card opsi
            f = tk.Frame(self.card_frame, bg="#111827", bd=1, highlightbackground="#475569", highlightthickness=1)
            f.pack(fill="x", padx=25, pady=6, ipady=4)
            self.radio_frames.append(f)

            rb = tk.Radiobutton(
                f,
                text="",
                variable=self.selected_answer,
                value=i,
                font=("Segoe UI", 10, "bold"),
                fg="#F1F5F9",
                bg="#111827",
                activebackground="#1E293B",
                activeforeground="#06B6D4",
                selectcolor="#1F2937",
                anchor="w",
                justify="left",
                relief="flat",
                bd=0,
                padx=15,
                pady=5,
                command=lambda idx=i: self.on_select_option(idx)
            )
            rb.pack(fill="both", expand=True)
            self.radio_buttons.append(rb)

        # Feedback Animasi Teks & Visual
        self.feedback_label = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg="#1E293B",
            fg="#1E293B"
        )
        self.feedback_label.pack(pady=5)

        # ----------------- FOOTER PANEL -----------------
        self.footer_frame = tk.Frame(self.window, bg="#0F172A")
        self.footer_frame.pack(fill="x", side="bottom", pady=25, padx=25)

        # Skip Button
        self.skip_btn = tk.Button(
            self.footer_frame,
            text="Skip (Esc)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0", # Light Gray
            fg="#0F172A",
            activebackground="#CBD5E1",
            activeforeground="#0F172A",
            padx=18,
            pady=8,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.skip_question
        )
        self.skip_btn.pack(side="left")

        # Submit Button
        self.submit_btn = tk.Button(
            self.footer_frame,
            text="SUBMIT ANSWER (Enter)",
            font=("Segoe UI", 11, "bold"),
            bg="#3B82F6", # Bright Royal Blue
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            padx=25,
            pady=8,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.submit_answer
        )
        self.submit_btn.pack(side="right")

    def setup_keyboard_shortcuts(self):
        self.window.bind("<Return>", lambda event: self.submit_answer())
        self.window.bind("<Escape>", lambda event: self.skip_question())

    def on_select_option(self, index):
        # Beri visual feed highlight ke frame opsi yg diklik
        for i, frame in enumerate(self.radio_frames):
            if i == index:
                frame.config(highlightbackground="#06B6D4") # Highlight Cyan
            else:
                frame.config(highlightbackground="#475569")

    def load_question(self):
        # Update progress bar
        progress_val = ((self.current_question) / len(self.questions)) * 100
        self.progress_bar["value"] = progress_val

        # Reset selection state & visuals
        self.selected_answer.set(-1)
        self.feedback_label.config(text="", bg="#1E293B", fg="#1E293B")
        for frame in self.radio_frames:
            frame.config(highlightbackground="#475569", bg="#111827")
        for rb in self.radio_buttons:
            rb.config(bg="#111827")

        # Set teks soal dan opsi
        q_data = self.questions[self.current_question]
        self.stat_label.config(text=f"SOAL {self.current_question + 1} / {len(self.questions)}")
        self.question_label.config(text=q_data['question'])

        for i, option in enumerate(q_data["options"]):
            self.radio_buttons[i].config(text=option)

        # Reset timer per soal
        self.time_left = 30
        self.timer_badge.config(text=f"Sisa Waktu: {self.time_left}s ⏱️", bg="#EF4444")

    def start_timer(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_badge.config(text=f"Sisa Waktu: {self.time_left}s ⏱️")
            self.time_left -= 1
            self.timer_job = self.window.after(1000, self.update_timer)
        else:
            self.animate_feedback(correct=False, timeout=True)

    def animate_feedback(self, correct, timeout=False):
        # Set panel warna correct/incorrect yang menawan
        if timeout:
            text = "⏳ WAKTU HABIS!"
            color = "#EF4444" # Danger Red
            bg_card = "#3F1E1E" # Dark red-ish tint
        elif correct:
            text = "✅ JAWABAN BENAR!"
            color = "#10B981" # Safe Emerald Green
            bg_card = "#162E27" # Dark emerald-ish tint
        else:
            text = "❌ JAWABAN SALAH!"
            color = "#EF4444"
            bg_card = "#3F1E1E"

        # Terapkan visual feedback transisi
        self.card_frame.config(bg=bg_card)
        self.question_label.config(bg=bg_card)
        for frame in self.radio_frames:
            frame.config(bg=bg_card)
        for rb in self.radio_buttons:
            rb.config(bg=bg_card)

        self.feedback_label.config(text=text, fg=color, bg=bg_card)

        # Beri jeda 800ms baru pindah ke soal berikutnya
        self.window.after(850, self.reset_feedback_and_next)

    def reset_feedback_and_next(self):
        self.card_frame.config(bg="#1E293B")
        self.question_label.config(bg="#1E293B")
        for frame in self.radio_frames:
            frame.config(bg="#111827")
        for rb in self.radio_buttons:
            rb.config(bg="#111827")

        self.next_question()

    def submit_answer(self):
        ans = self.selected_answer.get()

        if ans == -1:
            messagebox.showwarning("Peringatan", "Pilihlah salah satu jawaban sebelum submit!")
            return

        correct_ans = self.questions[self.current_question]["correct"]
        if int(ans) == int(correct_ans):
            self.score += 10
            self.score_badge.config(text=f"Score: {self.score}")
            self.animate_feedback(correct=True)
        else:
            self.animate_feedback(correct=False)

    def skip_question(self):
        self.animate_feedback(correct=False, timeout=False)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
            self.start_timer()
        else:
            self.show_result()

    def show_result(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

        self.progress_bar["value"] = 100

        messagebox.showinfo(
            " Quiz Selesai ",
            f"Selamat! Kamu telah menyelesaikan quiz ini.\n\n"
            f"🎯 Skor Akhir: {self.score} / {len(self.questions) * 10}\n"
            f"🎉 Jawaban Benar: {self.score // 10} dari {len(self.questions)} soal"
        )
        self.window.destroy()

    def jalankan(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
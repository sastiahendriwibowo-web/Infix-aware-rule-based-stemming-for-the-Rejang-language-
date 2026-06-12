import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import time
import csv
import os

# ==========================================
# 1. ENGINE STEMMING (BERDASARKAN DRAF PAPER)
# ==========================================

class RejangStemmer:
    def __init__(self, lexicon_set=None):
        self.lexicon = lexicon_set if lexicon_set else set()
        self.deletion_order = ['confix', 'prefix', 'infix', 'suffix']
        
        # 18 Aturan Morfologi Bahasa Rejang
        self.rules = {
            'confix': [
                (r'^ke(.*)an$', r'\1'),  # Aturan 1: ke- -an
                (r'^pe(.*)an$', r'\1'),  # Aturan 2: pe- -an
                (r'^be(.*)an$', r'\1'),  # Aturan 3: be- -an
                (r'^se(.*)an$', r'\1'),  # Aturan 4: se- -an
            ],
            'prefix': [
                (r'^be', ''),            # Aturan 5: Awalan be-
                (r'^ke', ''),            # Aturan 6: Awalan ke-
                (r'^pe', ''),            # Aturan 7: Awalan pe-
                (r'^me', ''),            # Aturan 8: Awalan me-
                (r'^di', ''),            # Aturan 9: Awalan di-
                (r'^te', ''),            # Aturan 10: Awalan te-
                (r'^se', ''),            # Aturan 11: Awalan se-
                (r'^de', ''),            # Aturan 12: Awalan de-
            ],
            'infix': [
                (r'^t(em)elak$', 'telak'), # Aturan 13: Spesifik temelak -> telak
                (r'^([^aeiouy])er(.*)$', r'\1\2'), # Aturan 14: Sisipan -er-
                (r'^([^aeiouy])el(.*)$', r'\1\2'), # Aturan 15: Sisipan -el-
                (r'^([^aeiouy])em(.*)$', r'\1\2'), # Aturan 16: Sisipan -em-
            ],
            'suffix': [
                (r'an$', ''),            # Aturan 17: Akhiran -an
                (r'ne$', ''),            # Aturan 18: Akhiran -ne khas Rejang
                (r'ke$', ''),            # Akhiran -ke
                (r'en$', ''),            # Akhiran -en
                (r'i$', ''),             # Akhiran -i
            ]
        }

    def normalize(self, word):
        if not word:
            return ""
        word = str(word).lower().strip()
        word = re.sub(r'[^a-z]', '', word)
        return word

    def stem(self, word):
        original_word = self.normalize(word)
        if original_word in self.lexicon:
            return original_word
            
        current_word = original_word
        for step in self.deletion_order:
            step_rules = self.rules.get(step, [])
            for pattern, replacement in step_rules:
                if re.search(pattern, current_word):
                    modified_word = re.sub(pattern, replacement, current_word)
                    if modified_word in self.lexicon:
                        return modified_word
                    current_word = modified_word
                    
        return current_word if current_word in self.lexicon else original_word


# ==========================================
# 2. ANTARMUKA GUI (USER FRIENDLY TKINTER)
# ==========================================

class StemmerAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pengujian Stemming Bahasa Rejang")
        self.root.geometry("950x650")
        self.root.configure(bg="#F4F6F9")
        
        self.lexicon_set = set()
        self.test_dataset = []
        self.stemmer = RejangStemmer(self.lexicon_set)
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#F4F6F9")
        self.style.configure("TFrame", background="#F4F6F9")
        
        self.create_widgets()
        self.auto_load_files()

    def create_widgets(self):
        # Header Panel
        header = tk.Frame(self.root, bg="#2C3E50", height=70)
        header.pack(fill=tk.X)
        lbl_title = tk.Label(header, text="Rejang Language Stemming Testing Tool", 
                             fg="white", bg="#2C3E50", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=15)

        # Main Layout (Notebook)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- TAB 1: PENGUJIAN DATASET ---
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="  Pengujian Massal  ")

        # Top Control Frame
        ctrl_frame = tk.Frame(tab1, bg="#F4F6F9")
        ctrl_frame.pack(fill=tk.X, pady=10)
        
        btn_run = tk.Button(ctrl_frame, text="▶ Jalankan Pengujian", bg="#27AE60", fg="white",
                            font=("Helvetica", 10, "bold"), command=self.run_testing, relief=tk.FLAT, padx=10, pady=5)
        btn_run.pack(side=tk.LEFT, padx=5)

        btn_load = tk.Button(ctrl_frame, text="📂 Buka Dataset Baru", bg="#2980B9", fg="white",
                             font=("Helvetica", 10), command=self.manual_import_dataset, relief=tk.FLAT, padx=10, pady=5)
        btn_load.pack(side=tk.LEFT, padx=5)
        
        btn_load_lex = tk.Button(ctrl_frame, text="📖 Buka Lexicon Baru", bg="#8E44AD", fg="white",
                             font=("Helvetica", 10), command=self.manual_import_lexicon, relief=tk.FLAT, padx=10, pady=5)
        btn_load_lex.pack(side=tk.LEFT, padx=5)

        # Status Bar Info File
        self.lbl_status_file = tk.Label(tab1, text="Status Berkas: Menyiapkan...", font=("Helvetica", 10, "italic"), bg="#F4F6F9", fg="#2C3E50")
        self.lbl_status_file.pack(anchor=tk.W, padx=5, pady=2)

        # Tabel Pengujian
        table_frame = tk.Frame(tab1)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("no", "word", "ground_truth", "prediction", "status", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("no", text="No")
        self.tree.heading("word", text="Kata Berimbuhan")
        self.tree.heading("ground_truth", text="Ground Truth")
        self.tree.heading("prediction", text="Hasil Stemming")
        self.tree.heading("status", text="Status Validasi")
        self.tree.heading("duration", text="Waktu (Detik)")

        self.tree.column("no", width=60, anchor=tk.CENTER)
        self.tree.column("word", width=180, anchor=tk.W)
        self.tree.column("ground_truth", width=180, anchor=tk.W)
        self.tree.column("prediction", width=180, anchor=tk.W)
        self.tree.column("status", width=160, anchor=tk.CENTER)
        self.tree.column("duration", width=110, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel Metrik
        self.metric_frame = tk.LabelFrame(tab1, text=" Ringkasan Metrik Evaluasi ", font=("Helvetica", 10, "bold"), bg="white")
        self.metric_frame.pack(fill=tk.X, pady=10)
        
        self.lbl_accuracy = tk.Label(self.metric_frame, text="Accuracy: -", font=("Helvetica", 11, "bold"), bg="white", fg="#2980B9")
        self.lbl_accuracy.pack(side=tk.LEFT, padx=35, pady=10)
        
        self.lbl_precision = tk.Label(self.metric_frame, text="Precision: -", font=("Helvetica", 11, "bold"), bg="white", fg="#27AE60")
        self.lbl_precision.pack(side=tk.LEFT, padx=35, pady=10)
        
        self.lbl_recall = tk.Label(self.metric_frame, text="Recall: -", font=("Helvetica", 11, "bold"), bg="white", fg="#E67E22")
        self.lbl_recall.pack(side=tk.LEFT, padx=35, pady=10)
        
        self.lbl_f1 = tk.Label(self.metric_frame, text="F1-Score: -", font=("Helvetica", 11, "bold"), bg="white", fg="#9B59B6")
        self.lbl_f1.pack(side=tk.LEFT, padx=35, pady=10)

        # --- TAB 2: UJI SATUAN KATA ---
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="  Uji Satuan Kata  ")
        
        single_frame = tk.Frame(tab2, bg="white", bd=1, relief=tk.SOLID)
        single_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        tk.Label(single_frame, text="Masukkan Kata Berimbuhan Bahasa Rejang:", font=("Helvetica", 11), bg="white").pack(pady=10)
        self.entry_word = tk.Entry(single_frame, font=("Helvetica", 12), width=30)
        self.entry_word.pack(pady=5)
        
        btn_single_stem = tk.Button(single_frame, text="Proses Stemming", bg="#34495E", fg="white", 
                                    font=("Helvetica", 11, "bold"), command=self.run_single_stem, relief=tk.FLAT)
        btn_single_stem.pack(pady=10)
        
        self.lbl_single_result = tk.Label(single_frame, text="", font=("Helvetica", 14, "bold"), fg="#27AE60", bg="white")
        self.lbl_single_result.pack(pady=20)

    def auto_load_files(self):
        """Mencari file default secara cerdas di direktori aktif"""
        possible_lexicons = ["rejang_stemming_dataset_package.xlsx - Lexicon.csv", "Lexicon.csv"]
        possible_datasets = ["rejang_morphology_dataset.csv", "rejang_stemming_dataset_package.xlsx - Morphology_Dataset.csv"]
        
        lex_file = next((f for f in possible_lexicons if os.path.exists(f)), None)
        dat_file = next((f for f in possible_datasets if os.path.exists(f)), None)

        if lex_file:
            self.load_lexicon_from_path(lex_file)
        if dat_file:
            self.load_dataset_from_path(dat_file)
            
        self.update_status_label()

    def update_status_label(self):
        msg = f"Kamus Terbaca: {len(self.lexicon_set)} kata dasar | Baris Dataset Siap Uji: {len(self.test_dataset)}"
        self.lbl_status_file.config(text=msg)

    def load_lexicon_from_path(self, path):
        try:
            new_lexicon = set()
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                header = [h.strip().lower() for h in next(reader, [])]
                
                # Cari indeks kolom yang memuat kata kunci 'root' atau ambil kolom pertama
                target_idx = 0
                for idx, h in enumerate(header):
                    if 'root' in h:
                        target_idx = idx
                        break
                        
                for row in reader:
                    if row and len(row) > target_idx:
                        val = row[target_idx].strip().lower()
                        if val:
                            new_lexicon.add(val)
            
            self.lexicon_set = new_lexicon
            self.stemmer.lexicon = self.lexicon_set
            return True
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal membaca kamus:\n{str(e)}")
            return False

    def load_dataset_from_path(self, path):
        try:
            new_dataset = []
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                header = [h.strip().lower() for h in next(reader, [])]
                
                # Deteksi letak indeks kolom secara dinamis (Insensitive-case)
                affixed_idx, root_idx = 0, 1
                for idx, h in enumerate(header):
                    if 'affix' in h:
                        affixed_idx = idx
                    elif 'root' in h:
                        root_idx = idx
                        
                for row in reader:
                    if row and len(row) > max(affixed_idx, root_idx):
                        w = row[affixed_idx].strip()
                        gt = row[root_idx].strip()
                        if w and gt:
                            new_dataset.append((w, gt))
                            
            self.test_dataset = new_dataset
            self.load_dataset_to_table()
            return True
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal membaca dataset:\n{str(e)}")
            return False

    def load_dataset_to_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, data in enumerate(self.test_dataset, 1):
            self.tree.insert("", tk.END, values=(i, data[0], data[1], "?", "Belum Diuji", "-"))

    def manual_import_lexicon(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            if self.load_lexicon_from_path(file_path):
                self.update_status_label()
                messagebox.showinfo("Berhasil", f"Berhasil memperbarui kamus dasar!")

    def manual_import_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            if self.load_dataset_from_path(file_path):
                self.update_status_label()
                messagebox.showinfo("Berhasil", f"Berhasil memuat dataset pengujian!")

    def run_testing(self):
        if not self.test_dataset:
            messagebox.showwarning("Data Kosong", "Tidak ada dataset pengujian yang tersedia!\n\nSilakan klik tombol '📂 Buka Dataset Baru' untuk memilih berkas rejang_morphology_dataset.csv Anda.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        tp, fp, fn, tn = 0, 0, 0, 0
        total_time = 0

        for i, (word, ground_truth) in enumerate(self.test_dataset, 1):
            start_time = time.time()
            prediction = self.stemmer.stem(word)
            duration = time.time() - start_time
            total_time += duration
            
            w_clean = word.lower().strip()
            gt_clean = ground_truth.lower().strip()
            pred_clean = prediction.lower().strip()
            
            is_input_base = (w_clean == gt_clean)
            
            if pred_clean == gt_clean:
                if is_input_base:
                    status = "True Negative (TN)"
                    tn += 1
                else:
                    status = "True Positive (TP)"
                    tp += 1
            else:
                if pred_clean == w_clean:
                    status = "False Negative (FN)"
                    fn += 1
                else:
                    status = "False Positive (FP)"
                    fp += 1
            
            self.tree.insert("", tk.END, values=(i, word, ground_truth, prediction, status, f"{duration:.5f}"))

        total_data = tp + tn + fp + fn
        accuracy = (tp + tn) / total_data if total_data > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        self.lbl_accuracy.config(text=f"Accuracy: {accuracy*100:.2f}%")
        self.lbl_precision.config(text=f"Precision: {precision*100:.2f}%")
        self.lbl_recall.config(text=f"Recall: {recall*100:.2f}%")
        self.lbl_f1.config(text=f"F1-Score: {f1_score*100:.2f}%")
        
        avg_time = total_time / len(self.test_dataset)
        messagebox.showinfo("Sukses", f"Pengujian selesai!\nRata-rata waktu: {avg_time:.5f} detik/kata.")

    def run_single_stem(self):
        input_word = self.entry_word.get()
        if not input_word:
            messagebox.showwarning("Peringatan", "Silakan masukkan kata terlebih dahulu!")
            return
        result = self.stemmer.stem(input_word)
        self.lbl_single_result.config(text=f"Kata Dasar: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StemmerAppGUI(root)
    root.mainloop()
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

LANGUAGES = {
    "en": {
        "title": "Framanen DirLens - Folder Size Analyzer",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "menu_about": "About Framanen DirLens",
        "about_title": "About Framanen DirLens",
        "about_text": "Framanen DirLens - Folder Size Analyzer\n\nVersion: 1.0.0\nDeveloper: Burak Duman\n\nThis software is open-source and free to use.",
        "folder_label": "Folder:",
        "browse_btn": "Browse",
        "scan_btn": "Scan",
        "up_btn": "Up Folder",
        "status_select": "Select a folder to scan.",
        "status_scanning": "Scanning...",
        "status_done": "{count} items | Total: {size}",
        "hdr_name": "Name",
        "hdr_size": "Size",
        "hdr_ratio": "Ratio",
        "hdr_delete": "Delete",
        "err_invalid_path": "Enter a valid folder path.",
        "err_title": "Error",
        "err_open_file": "Failed to open file: {e}",
        "confirm_del_title": "Delete Confirmation",
        "confirm_del_msg": "Are you sure you want to permanently delete the {item_type} named '{name}'?",
        "type_folder": "folder",
        "type_file": "file",
        "success_title": "Success",
        "success_msg": "'{name}' deleted successfully.",
        "err_delete_failed": "Deletion failed:\n{e}"
    },
    "tr": {
        "title": "Framanen DirLens - Klasör Boyutu Analizcisi",
        "menu_settings": "Ayarlar",
        "menu_help": "Yardım",
        "menu_about": "Framanen DirLens Hakkında",
        "about_title": "Framanen DirLens Hakkında",
        "about_text": "Framanen DirLens - Klasör Boyutu Analizcisi\n\nSürüm: 1.0.0\nGeliştirici: Burak Duman\n\nBu yazılım açık kaynaklı ve kullanımı ücretsizdir.",
        "folder_label": "Klasör:",
        "browse_btn": "Gözat",
        "scan_btn": "Tara",
        "up_btn": "Üst Klasör",
        "status_select": "Taramak için bir klasör seçin.",
        "status_scanning": "Taranıyor…",
        "status_done": "{count} öğe | Toplam: {size}",
        "hdr_name": "Ad",
        "hdr_size": "Boyut",
        "hdr_ratio": "Oran",
        "hdr_delete": "Sil",
        "err_invalid_path": "Geçerli bir klasör yolu girin.",
        "err_title": "Hata",
        "err_open_file": "Dosya açılamadı: {e}",
        "confirm_del_title": "Silme Onayı",
        "confirm_del_msg": "'{name}' isimli {item_type} kalıcı olarak silmek istediğinize emin misiniz?",
        "type_folder": "klasörü",
        "type_file": "dosyayı",
        "success_title": "Başarılı",
        "success_msg": "'{name}' başarıyla silindi.",
        "err_delete_failed": "Silme işlemi başarısız oldu:\n{e}"
    },
    "es": {
        "title": "Framanen DirLens - Analizador de Tamaño de Carpetas",
        "menu_settings": "Configuración",
        "menu_help": "Ayuda",
        "menu_about": "Acerca de Framanen DirLens",
        "about_title": "Acerca de Framanen DirLens",
        "about_text": "Framanen DirLens - Analizador de Tamaño de Carpetas\n\nVersión: 1.0.0\nDesarrollador: Burak Duman\n\nEste software es de código abierto y de uso gratuito.",
        "folder_label": "Carpeta:",
        "browse_btn": "Examinar",
        "scan_btn": "Escanear",
        "up_btn": "Carpeta Sup.",
        "status_select": "Seleccione una carpeta para escanear.",
        "status_scanning": "Escaneando...",
        "status_done": "{count} elementos | Total: {size}",
        "hdr_name": "Nombre",
        "hdr_size": "Tamaño",
        "hdr_ratio": "Proporción",
        "hdr_delete": "Eliminar",
        "err_invalid_path": "Ingrese una ruta de carpeta válida.",
        "err_title": "Error",
        "err_open_file": "No se pudo abrir el archivo: {e}",
        "confirm_del_title": "Confirmación de eliminación",
        "confirm_del_msg": "¿Está seguro de que desea eliminar permanentemente el {item_type} llamado '{name}'?",
        "type_folder": "carpeta",
        "type_file": "archivo",
        "success_title": "Éxito",
        "success_msg": "'{name}' se eliminó con éxito.",
        "err_delete_failed": "La eliminación falló:\n{e}"
    },
    "de": {
        "title": "Framanen DirLens - Ordnergrößen-Analysator",
        "menu_settings": "Einstellungen",
        "menu_help": "Hilfe",
        "menu_about": "Über Framanen DirLens",
        "about_title": "Über Framanen DirLens",
        "about_text": "Framanen DirLens - Ordnergrößen-Analysator\n\nVersion: 1.0.0\nEntwickler: Burak Duman\n\nDiese Software ist Open-Source und kostenlos nutzbar.",
        "folder_label": "Ordner:",
        "browse_btn": "Durchsuchen",
        "scan_btn": "Scannen",
        "up_btn": "Übergeordneter Ordner",
        "status_select": "Wählen Sie einen Ordner zum Scannen aus.",
        "status_scanning": "Scannen...",
        "status_done": "{count} Elemente | Gesamt: {size}",
        "hdr_name": "Name",
        "hdr_size": "Größe",
        "hdr_ratio": "Verhältnis",
        "hdr_delete": "Löschen",
        "err_invalid_path": "Geben Sie einen gültigen Ordnerpfad ein.",
        "err_title": "Fehler",
        "err_open_file": "Datei konnte nicht geöffnet werden: {e}",
        "confirm_del_title": "Löschen bestätigen",
        "confirm_del_msg": "Sind Sie sicher, dass Sie den/die {item_type} namens '{name}' dauerhaft löschen möchten?",
        "type_folder": "Ordner",
        "type_file": "Datei",
        "success_title": "Erfolgreich",
        "success_msg": "'{name}' wurde erfolgreich gelöscht.",
        "err_delete_failed": "Löschen fehlgeschlagen:\n{e}"
    },
    "ko": {
        "title": "Framanen DirLens - 폴더 크기 분석기",
        "menu_settings": "설정",
        "menu_help": "도움말",
        "menu_about": "Framanen DirLens 정보",
        "about_title": "Framanen DirLens 정보",
        "about_text": "Framanen DirLens - 폴더 크기 분석기\n\n버전: 1.0.0\n개발자: Burak Duman\n\n이 소프트웨어는 오픈 소스이며 무료로 사용할 수 있습니다.",
        "folder_label": "폴더:",
        "browse_btn": "찾아보기",
        "scan_btn": "스캔",
        "up_btn": "상위 폴더",
        "status_select": "스캔할 폴더를 선택하십시오.",
        "status_scanning": "스캔 중...",
        "status_done": "{count}개 항목 | 합계: {size}",
        "hdr_name": "이름",
        "hdr_size": "크기",
        "hdr_ratio": "비율",
        "hdr_delete": "삭제",
        "err_invalid_path": "올바른 폴더 경로를 입력하십시오.",
        "err_title": "오류",
        "err_open_file": "파일을 열지 못했습니다: {e}",
        "confirm_del_title": "삭제 확인",
        "confirm_del_msg": "'{name}' {item_type}을(를) 영구적으로 삭제하시겠습니까?",
        "type_folder": "폴더",
        "type_file": "파일",
        "success_title": "성공",
        "success_msg": "'{name}'이(가) 성공적으로 삭제되었습니다.",
        "err_delete_failed": "삭제 실패:\n{e}"
    },
    "zh": {
        "title": "Framanen DirLens - 文件夹大小分析器",
        "menu_settings": "设置",
        "menu_help": "帮助",
        "menu_about": "关于 Framanen DirLens",
        "about_title": "关于 Framanen DirLens",
        "about_text": "Framanen DirLens - 文件夹大小分析器\n\n版本: 1.0.0\n开发者: Burak Duman\n\n本软件为开源软件，免费使用。",
        "folder_label": "文件夹:",
        "browse_btn": "浏览",
        "scan_btn": "扫描",
        "up_btn": "上级文件夹",
        "status_select": "选择要扫描的文件夹。",
        "status_scanning": "正在扫描...",
        "status_done": "{count} 个项目 | 总计: {size}",
        "hdr_name": "名称",
        "hdr_size": "大小",
        "hdr_ratio": "比例",
        "hdr_delete": "删除",
        "err_invalid_path": "请输入有效的文件夹路径。",
        "err_title": "错误",
        "err_open_file": "无法打开文件: {e}",
        "confirm_del_title": "确认删除",
        "confirm_del_msg": "您确定要永久删除名为 '{name}' 的 {item_type} 吗？",
        "type_folder": "文件夹",
        "type_file": "文件",
        "success_title": "成功",
        "success_msg": "'{name}' 已成功删除。",
        "err_delete_failed": "删除失败:\n{e}"
    },
    "it": {
        "title": "Framanen DirLens - Analizzatore Dimensione Cartelle",
        "menu_settings": "Impostazioni",
        "menu_help": "Aiuto",
        "menu_about": "Informazioni su Framanen DirLens",
        "about_title": "Informazioni su Framanen DirLens",
        "about_text": "Framanen DirLens - Analizzatore Dimensione Cartelle\n\nVersione: 1.0.0\nSviluppatore: Burak Duman\n\nQuesto software è open-source e gratuito da usare.",
        "folder_label": "Cartella:",
        "browse_btn": "Sfoglia",
        "scan_btn": "Scansiona",
        "up_btn": "Cartella Sup.",
        "status_select": "Seleziona una cartella da scansionare.",
        "status_scanning": "Scansione in corso...",
        "status_done": "{count} elementi | Totale: {size}",
        "hdr_name": "Nome",
        "hdr_size": "Dimensione",
        "hdr_ratio": "Rapporto",
        "hdr_delete": "Elimina",
        "err_invalid_path": "Inserisci un percorso cartella valido.",
        "err_title": "Errore",
        "err_open_file": "Impossibile aprire il file: {e}",
        "confirm_del_title": "Conferma eliminazione",
        "confirm_del_msg": "Sei sicuro di voler eliminare definitivamente il {item_type} chiamato '{name}'?",
        "type_folder": "cartella",
        "type_file": "file",
        "success_title": "Successo",
        "success_msg": "'{name}' eliminato con successo.",
        "err_delete_failed": "Eliminazione fallita:\n{e}"
    }
}


def get_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_size(entry.path)
            except (PermissionError, OSError):
                pass
    except (PermissionError, OSError):
        pass
    return total


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


class FolderSizeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = "tr"
        self.geometry("850x570")
        self.configure(bg="#1e1e2e")
        self._scanning = False
        self._build_ui()
        self._update_language(self.current_lang)

    def _build_ui(self):
        # Create Menu Bar for Settings/Language Selection
        self.menu_bar = tk.Menu(self, tearoff=0, bg="#313244", fg="#cdd6f4", activebackground="#45475a", activeforeground="#cdd6f4")
        self.config(menu=self.menu_bar)
        
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#313244", fg="#cdd6f4", activebackground="#45475a", activeforeground="#cdd6f4")
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.settings_menu.add_radiobutton(label="English", variable=self.lang_var, value="en", command=lambda: self._update_language("en"))
        self.settings_menu.add_radiobutton(label="Türkçe", variable=self.lang_var, value="tr", command=lambda: self._update_language("tr"))
        self.settings_menu.add_radiobutton(label="Español", variable=self.lang_var, value="es", command=lambda: self._update_language("es"))
        self.settings_menu.add_radiobutton(label="Deutsch", variable=self.lang_var, value="de", command=lambda: self._update_language("de"))
        self.settings_menu.add_radiobutton(label="한국어", variable=self.lang_var, value="ko", command=lambda: self._update_language("ko"))
        self.settings_menu.add_radiobutton(label="中文", variable=self.lang_var, value="zh", command=lambda: self._update_language("zh"))
        self.settings_menu.add_radiobutton(label="Italiano", variable=self.lang_var, value="it", command=lambda: self._update_language("it"))

        # Create Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#313244", fg="#cdd6f4", activebackground="#45475a", activeforeground="#cdd6f4")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About Framanen DirLens", command=self._show_about)

        top = tk.Frame(self, bg="#1e1e2e", pady=10)
        top.pack(fill="x", padx=16)

        self.lbl_folder = tk.Label(top, text="Klasör:", bg="#1e1e2e", fg="#cdd6f4",
                                   font=("Segoe UI", 10))
        self.lbl_folder.pack(side="left")

        self.path_var = tk.StringVar(value=os.path.expanduser("~"))
        entry = tk.Entry(top, textvariable=self.path_var, width=55,
                         bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4",
                         relief="flat", font=("Segoe UI", 10))
        entry.pack(side="left", padx=8, ipady=4)

        self.btn_browse = tk.Button(top, text="Gözat", command=self._browse,
                                    bg="#89b4fa", fg="#1e1e2e", relief="flat",
                                    font=("Segoe UI", 10, "bold"), padx=10,
                                    cursor="hand2")
        self.btn_browse.pack(side="left", padx=4)

        self.btn_scan = tk.Button(top, text="Tara", command=self._start_scan,
                                  bg="#a6e3a1", fg="#1e1e2e", relief="flat",
                                  font=("Segoe UI", 10, "bold"), padx=10,
                                  cursor="hand2")
        self.btn_scan.pack(side="left", padx=4)

        self.btn_up = tk.Button(top, text="Üst Klasör", command=self._go_up,
                                bg="#f9e2af", fg="#1e1e2e", relief="flat",
                                font=("Segoe UI", 10, "bold"), padx=10,
                                cursor="hand2")
        self.btn_up.pack(side="left", padx=4)

        self.status = tk.Label(self, text="Taramak için bir klasör seçin.",
                               bg="#1e1e2e", fg="#6c7086",
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(fill="x", padx=16)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=16, pady=(2, 6))
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#181825", foreground="#cdd6f4",
                         fieldbackground="#181825", rowheight=26,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#313244",
                         foreground="#cdd6f4", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#45475a")])

        cols = ("name", "size", "pct", "delete")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                  selectmode="browse")
        self.tree.heading("name", text="Ad", anchor="w",
                           command=lambda: self._sort("name"))
        self.tree.heading("size", text="Boyut", anchor="e",
                           command=lambda: self._sort("size"))
        self.tree.heading("pct", text="Oran", anchor="e",
                           command=lambda: self._sort("pct"))
        self.tree.heading("delete", text="Sil", anchor="center")
        self.tree.column("name", width=410, anchor="w")
        self.tree.column("size", width=120, anchor="e")
        self.tree.column("pct", width=100, anchor="e")
        self.tree.column("delete", width=50, anchor="center")
        self.tree.bind("<Button-1>", self._on_click)
        self.tree.bind("<Double-1>", self._on_double_click)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", padx=(0, 6))
        self.tree.pack(fill="both", expand=True, padx=(16, 0), pady=(0, 12))

        self.tree.tag_configure("bar_high", foreground="#f38ba8")
        self.tree.tag_configure("bar_mid", foreground="#fab387")
        self.tree.tag_configure("bar_low", foreground="#a6e3a1")

        self._data = []
        self._sort_key = "size"
        self._sort_rev = True

    def _browse(self):
        d = filedialog.askdirectory(initialdir=self.path_var.get())
        if d:
            self.path_var.set(d)

    def _start_scan(self):
        if self._scanning:
            return
        path = self.path_var.get()
        t = LANGUAGES[self.current_lang]
        if not os.path.isdir(path):
            messagebox.showerror(t["err_title"], t["err_invalid_path"])
            return
        self._scanning = True
        self.tree.delete(*self.tree.get_children())
        self._data = []
        self.progress.start(10)
        self.status.config(text=t["status_scanning"])
        threading.Thread(target=self._scan, args=(path,), daemon=True).start()

    def _scan(self, path):
        results = []
        try:
            entries = list(os.scandir(path))
        except PermissionError:
            self.after(0, lambda: self._done([]))
            return

        for entry in entries:
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_size(entry.path)
                    results.append((entry.name, size, entry.path, "dir"))
                else:
                    size = entry.stat(follow_symlinks=False).st_size
                    results.append((entry.name, size, entry.path, "file"))
            except (PermissionError, OSError):
                pass

        self.after(0, lambda: self._done(results))

    def _done(self, results):
        self._scanning = False
        self.progress.stop()
        self._data = results
        self._populate()
        total = sum(r[1] for r in results)
        t = LANGUAGES[self.current_lang]
        self.status.config(
            text=t["status_done"].format(count=len(results), size=format_size(total)))

    def _populate(self):
        self.tree.delete(*self.tree.get_children())
        if not self._data:
            return
        key_map = {"name": 0, "size": 1, "pct": 1}
        self._data.sort(key=lambda r: r[key_map[self._sort_key]],
                        reverse=self._sort_rev)
        total = sum(r[1] for r in self._data) or 1
        for name, size, path, kind in self._data:
            pct = size / total * 100
            bar = "▓" * int(pct / 5)
            prefix = "📁 " if kind == "dir" else "📄 "
            tag = "bar_high" if pct >= 30 else ("bar_mid" if pct >= 10 else "bar_low")
            self.tree.insert("", "end", iid=path,
                             values=(prefix + name,
                                     format_size(size),
                                     f"{bar:<20} {pct:5.1f}%",
                                     "🗑️"),
                             tags=(tag,))

    def _sort(self, key):
        if self._sort_key == key:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_key = key
            self._sort_rev = True
        self._populate()

    def _go_up(self):
        current_path = self.path_var.get()
        parent_path = os.path.dirname(current_path)
        if parent_path and parent_path != current_path:
            self.path_var.set(parent_path)
            self._start_scan()

    def _on_double_click(self, event):
        column = self.tree.identify_column(event.x)
        if column == "#4":
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        if os.path.isdir(item):
            self.path_var.set(item)
            self._start_scan()
        elif os.path.isfile(item):
            try:
                os.startfile(item)
            except Exception as e:
                t = LANGUAGES[self.current_lang]
                messagebox.showerror(t["err_title"], t["err_open_file"].format(e=e))

    def _on_click(self, event):
        column = self.tree.identify_column(event.x)
        if column == "#4":
            item = self.tree.identify_row(event.y)
            if item:
                self._confirm_delete(item)

    def _confirm_delete(self, path):
        name = os.path.basename(path)
        is_dir = os.path.isdir(path)
        t = LANGUAGES[self.current_lang]
        item_type = t["type_folder"] if is_dir else t["type_file"]
        
        confirm = messagebox.askyesno(
            t["confirm_del_title"],
            t["confirm_del_msg"].format(name=name, item_type=item_type),
            icon="warning"
        )
        
        if confirm:
            try:
                if is_dir:
                    import shutil
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                
                messagebox.showinfo(t["success_title"], t["success_msg"].format(name=name))
                self._start_scan()
            except Exception as e:
                messagebox.showerror(t["err_title"], t["err_delete_failed"].format(e=e))

    def _update_language(self, lang_code):
        self.current_lang = lang_code
        t = LANGUAGES[lang_code]
        
        self.title(t["title"])
        self.lbl_folder.config(text=t["folder_label"])
        self.btn_browse.config(text=t["browse_btn"])
        self.btn_scan.config(text=t["scan_btn"])
        self.btn_up.config(text=t["up_btn"])
        
        self.tree.heading("name", text=t["hdr_name"])
        self.tree.heading("size", text=t["hdr_size"])
        self.tree.heading("pct", text=t["hdr_ratio"])
        self.tree.heading("delete", text=t["hdr_delete"])
        
        self.menu_bar.entryconfig(0, label=t["menu_settings"])
        self.menu_bar.entryconfig(1, label=t["menu_help"])
        self.help_menu.entryconfig(0, label=t["menu_about"])
        
        if not self._scanning:
            if not self._data:
                self.status.config(text=t["status_select"])
            else:
                total = sum(r[1] for r in self._data)
                self.status.config(text=t["status_done"].format(count=len(self._data), size=format_size(total)))
        else:
            self.status.config(text=t["status_scanning"])

    def _show_about(self):
        t = LANGUAGES[self.current_lang]
        messagebox.showinfo(t["about_title"], t["about_text"])


if __name__ == "__main__":
    app = FolderSizeApp()
    app.mainloop()

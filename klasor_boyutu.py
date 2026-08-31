import ftplib
import os
import posixpath
import stat as stat_module
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_VERSION = "2.0.0"

LANGUAGES = {
    "en": {
        "title": "Framanen DirLens - Folder Size Analyzer",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "menu_about": "About Framanen DirLens",
        "about_title": "About Framanen DirLens",
        "about_text": "Framanen DirLens - Folder Size Analyzer\n\nVersion: {version}\nDeveloper: Burak Duman\n\nScans local disks, FTP/FTPS servers and SSH (SFTP) servers.\n\nThis software is open-source and free to use.",
        "folder_label": "Folder:",
        "browse_btn": "Browse",
        "scan_btn": "Scan",
        "up_btn": "Up Folder",
        "stop_btn": "Stop",
        "status_select": "Select a folder to scan.",
        "status_scanning": "Scanning...",
        "status_scanning_item": "Scanning: {name}",
        "status_done": "{count} items | Total: {size}",
        "status_cancelled": "Scan cancelled. {count} items listed.",
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
        "err_delete_failed": "Deletion failed:\n{e}",
        "menu_connection": "Connection",
        "conn_local": "Local Disk",
        "conn_remote": "FTP / SSH Connection...",
        "conn_disconnect": "Disconnect",
        "conn_title": "FTP / SSH Connection",
        "conn_mode": "Protocol:",
        "conn_host": "Host:",
        "conn_port": "Port:",
        "conn_user": "Username:",
        "conn_pass": "Password:",
        "conn_key": "SSH key file (optional):",
        "conn_path": "Start folder:",
        "conn_connect": "Connect",
        "conn_cancel": "Cancel",
        "conn_anonymous": "Anonymous login",
        "mode_local": "Local disk",
        "status_connecting": "Connecting to {host}...",
        "status_connected": "Connected: {info}",
        "status_disconnected": "Disconnected. Local disk mode.",
        "err_connect_title": "Connection Error",
        "err_connect_failed": "Connection failed:\n{e}",
        "err_paramiko": "SFTP (SSH) support requires the 'paramiko' package.\n\nInstall it with:\n    pip install paramiko",
        "err_host_required": "Enter a host address.",
        "err_port_invalid": "Enter a valid port number.",
        "err_list_failed": "Folder could not be listed:\n{e}",
        "err_remote_open_file": "Remote files cannot be opened directly.\nDownload the file first.",
        "warn_remote_scan": "Scanning a remote folder recursively may take a long time. Use Stop to cancel."
    },
    "tr": {
        "title": "Framanen DirLens - Klasör Boyutu Analizcisi",
        "menu_settings": "Ayarlar",
        "menu_help": "Yardım",
        "menu_about": "Framanen DirLens Hakkında",
        "about_title": "Framanen DirLens Hakkında",
        "about_text": "Framanen DirLens - Klasör Boyutu Analizcisi\n\nSürüm: {version}\nGeliştirici: Burak Duman\n\nYerel diskleri, FTP/FTPS sunucularını ve SSH (SFTP) sunucularını tarar.\n\nBu yazılım açık kaynaklı ve kullanımı ücretsizdir.",
        "folder_label": "Klasör:",
        "browse_btn": "Gözat",
        "scan_btn": "Tara",
        "up_btn": "Üst Klasör",
        "stop_btn": "Durdur",
        "status_select": "Taramak için bir klasör seçin.",
        "status_scanning": "Taranıyor…",
        "status_scanning_item": "Taranıyor: {name}",
        "status_done": "{count} öğe | Toplam: {size}",
        "status_cancelled": "Tarama durduruldu. {count} öğe listelendi.",
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
        "err_delete_failed": "Silme işlemi başarısız oldu:\n{e}",
        "menu_connection": "Bağlantı",
        "conn_local": "Yerel Disk",
        "conn_remote": "FTP / SSH Bağlantısı...",
        "conn_disconnect": "Bağlantıyı Kes",
        "conn_title": "FTP / SSH Bağlantısı",
        "conn_mode": "Protokol:",
        "conn_host": "Sunucu:",
        "conn_port": "Port:",
        "conn_user": "Kullanıcı adı:",
        "conn_pass": "Parola:",
        "conn_key": "SSH anahtar dosyası (isteğe bağlı):",
        "conn_path": "Başlangıç klasörü:",
        "conn_connect": "Bağlan",
        "conn_cancel": "İptal",
        "conn_anonymous": "Anonim giriş",
        "mode_local": "Yerel disk",
        "status_connecting": "{host} sunucusuna bağlanılıyor...",
        "status_connected": "Bağlandı: {info}",
        "status_disconnected": "Bağlantı kesildi. Yerel disk modu.",
        "err_connect_title": "Bağlantı Hatası",
        "err_connect_failed": "Bağlantı kurulamadı:\n{e}",
        "err_paramiko": "SFTP (SSH) desteği için 'paramiko' paketi gerekir.\n\nKurmak için:\n    pip install paramiko",
        "err_host_required": "Bir sunucu adresi girin.",
        "err_port_invalid": "Geçerli bir port numarası girin.",
        "err_list_failed": "Klasör listelenemedi:\n{e}",
        "err_remote_open_file": "Uzak sunucudaki dosyalar doğrudan açılamaz.\nÖnce dosyayı indirin.",
        "warn_remote_scan": "Uzak klasörlerin özyinelemeli taraması uzun sürebilir. Durdurmak için Durdur'u kullanın."
    },
    "es": {
        "title": "Framanen DirLens - Analizador de Tamaño de Carpetas",
        "menu_settings": "Configuración",
        "menu_help": "Ayuda",
        "menu_about": "Acerca de Framanen DirLens",
        "about_title": "Acerca de Framanen DirLens",
        "about_text": "Framanen DirLens - Analizador de Tamaño de Carpetas\n\nVersión: {version}\nDesarrollador: Burak Duman\n\nAnaliza discos locales, servidores FTP/FTPS y servidores SSH (SFTP).\n\nEste software es de código abierto y de uso gratuito.",
        "folder_label": "Carpeta:",
        "browse_btn": "Examinar",
        "scan_btn": "Escanear",
        "up_btn": "Carpeta Sup.",
        "stop_btn": "Detener",
        "status_select": "Seleccione una carpeta para escanear.",
        "status_scanning": "Escaneando...",
        "status_scanning_item": "Escaneando: {name}",
        "status_done": "{count} elementos | Total: {size}",
        "status_cancelled": "Escaneo cancelado. {count} elementos listados.",
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
        "err_delete_failed": "La eliminación falló:\n{e}",
        "menu_connection": "Conexión",
        "conn_local": "Disco local",
        "conn_remote": "Conexión FTP / SSH...",
        "conn_disconnect": "Desconectar",
        "conn_title": "Conexión FTP / SSH",
        "conn_mode": "Protocolo:",
        "conn_host": "Servidor:",
        "conn_port": "Puerto:",
        "conn_user": "Usuario:",
        "conn_pass": "Contraseña:",
        "conn_key": "Archivo de clave SSH (opcional):",
        "conn_path": "Carpeta inicial:",
        "conn_connect": "Conectar",
        "conn_cancel": "Cancelar",
        "conn_anonymous": "Acceso anónimo",
        "mode_local": "Disco local",
        "status_connecting": "Conectando a {host}...",
        "status_connected": "Conectado: {info}",
        "status_disconnected": "Desconectado. Modo disco local.",
        "err_connect_title": "Error de conexión",
        "err_connect_failed": "No se pudo conectar:\n{e}",
        "err_paramiko": "La compatibilidad con SFTP (SSH) requiere el paquete 'paramiko'.\n\nInstálelo con:\n    pip install paramiko",
        "err_host_required": "Ingrese una dirección de servidor.",
        "err_port_invalid": "Ingrese un número de puerto válido.",
        "err_list_failed": "No se pudo listar la carpeta:\n{e}",
        "err_remote_open_file": "Los archivos remotos no se pueden abrir directamente.\nDescargue el archivo primero.",
        "warn_remote_scan": "El escaneo recursivo de una carpeta remota puede tardar. Use Detener para cancelar."
    },
    "de": {
        "title": "Framanen DirLens - Ordnergrößen-Analysator",
        "menu_settings": "Einstellungen",
        "menu_help": "Hilfe",
        "menu_about": "Über Framanen DirLens",
        "about_title": "Über Framanen DirLens",
        "about_text": "Framanen DirLens - Ordnergrößen-Analysator\n\nVersion: {version}\nEntwickler: Burak Duman\n\nAnalysiert lokale Datenträger, FTP/FTPS-Server und SSH-Server (SFTP).\n\nDiese Software ist Open-Source und kostenlos nutzbar.",
        "folder_label": "Ordner:",
        "browse_btn": "Durchsuchen",
        "scan_btn": "Scannen",
        "up_btn": "Übergeordneter Ordner",
        "stop_btn": "Stopp",
        "status_select": "Wählen Sie einen Ordner zum Scannen aus.",
        "status_scanning": "Scannen...",
        "status_scanning_item": "Scannen: {name}",
        "status_done": "{count} Elemente | Gesamt: {size}",
        "status_cancelled": "Scan abgebrochen. {count} Elemente aufgelistet.",
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
        "err_delete_failed": "Löschen fehlgeschlagen:\n{e}",
        "menu_connection": "Verbindung",
        "conn_local": "Lokaler Datenträger",
        "conn_remote": "FTP-/SSH-Verbindung...",
        "conn_disconnect": "Verbindung trennen",
        "conn_title": "FTP-/SSH-Verbindung",
        "conn_mode": "Protokoll:",
        "conn_host": "Server:",
        "conn_port": "Port:",
        "conn_user": "Benutzername:",
        "conn_pass": "Passwort:",
        "conn_key": "SSH-Schlüsseldatei (optional):",
        "conn_path": "Startordner:",
        "conn_connect": "Verbinden",
        "conn_cancel": "Abbrechen",
        "conn_anonymous": "Anonyme Anmeldung",
        "mode_local": "Lokaler Datenträger",
        "status_connecting": "Verbinde mit {host}...",
        "status_connected": "Verbunden: {info}",
        "status_disconnected": "Verbindung getrennt. Lokaler Modus.",
        "err_connect_title": "Verbindungsfehler",
        "err_connect_failed": "Verbindung fehlgeschlagen:\n{e}",
        "err_paramiko": "SFTP-(SSH-)Unterstützung erfordert das Paket 'paramiko'.\n\nInstallation:\n    pip install paramiko",
        "err_host_required": "Geben Sie eine Serveradresse ein.",
        "err_port_invalid": "Geben Sie eine gültige Portnummer ein.",
        "err_list_failed": "Ordner konnte nicht aufgelistet werden:\n{e}",
        "err_remote_open_file": "Entfernte Dateien können nicht direkt geöffnet werden.\nLaden Sie die Datei zuerst herunter.",
        "warn_remote_scan": "Das rekursive Scannen eines entfernten Ordners kann lange dauern. Mit Stopp abbrechen."
    },
    "ko": {
        "title": "Framanen DirLens - 폴더 크기 분석기",
        "menu_settings": "설정",
        "menu_help": "도움말",
        "menu_about": "Framanen DirLens 정보",
        "about_title": "Framanen DirLens 정보",
        "about_text": "Framanen DirLens - 폴더 크기 분석기\n\n버전: {version}\n개발자: Burak Duman\n\n로컬 디스크, FTP/FTPS 서버 및 SSH(SFTP) 서버를 검사합니다.\n\n이 소프트웨어는 오픈 소스이며 무료로 사용할 수 있습니다.",
        "folder_label": "폴더:",
        "browse_btn": "찾아보기",
        "scan_btn": "스캔",
        "up_btn": "상위 폴더",
        "stop_btn": "중지",
        "status_select": "스캔할 폴더를 선택하십시오.",
        "status_scanning": "스캔 중...",
        "status_scanning_item": "스캔 중: {name}",
        "status_done": "{count}개 항목 | 합계: {size}",
        "status_cancelled": "스캔이 취소되었습니다. {count}개 항목이 표시되었습니다.",
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
        "err_delete_failed": "삭제 실패:\n{e}",
        "menu_connection": "연결",
        "conn_local": "로컬 디스크",
        "conn_remote": "FTP / SSH 연결...",
        "conn_disconnect": "연결 끊기",
        "conn_title": "FTP / SSH 연결",
        "conn_mode": "프로토콜:",
        "conn_host": "호스트:",
        "conn_port": "포트:",
        "conn_user": "사용자 이름:",
        "conn_pass": "비밀번호:",
        "conn_key": "SSH 키 파일(선택 사항):",
        "conn_path": "시작 폴더:",
        "conn_connect": "연결",
        "conn_cancel": "취소",
        "conn_anonymous": "익명 로그인",
        "mode_local": "로컬 디스크",
        "status_connecting": "{host}에 연결하는 중...",
        "status_connected": "연결됨: {info}",
        "status_disconnected": "연결이 끊어졌습니다. 로컬 디스크 모드.",
        "err_connect_title": "연결 오류",
        "err_connect_failed": "연결하지 못했습니다:\n{e}",
        "err_paramiko": "SFTP(SSH) 지원에는 'paramiko' 패키지가 필요합니다.\n\n설치 방법:\n    pip install paramiko",
        "err_host_required": "호스트 주소를 입력하십시오.",
        "err_port_invalid": "올바른 포트 번호를 입력하십시오.",
        "err_list_failed": "폴더를 나열할 수 없습니다:\n{e}",
        "err_remote_open_file": "원격 파일은 직접 열 수 없습니다.\n먼저 파일을 다운로드하십시오.",
        "warn_remote_scan": "원격 폴더의 재귀 스캔은 오래 걸릴 수 있습니다. 중지 버튼으로 취소하십시오."
    },
    "zh": {
        "title": "Framanen DirLens - 文件夹大小分析器",
        "menu_settings": "设置",
        "menu_help": "帮助",
        "menu_about": "关于 Framanen DirLens",
        "about_title": "关于 Framanen DirLens",
        "about_text": "Framanen DirLens - 文件夹大小分析器\n\n版本: {version}\n开发者: Burak Duman\n\n可扫描本地磁盘、FTP/FTPS 服务器和 SSH (SFTP) 服务器。\n\n本软件为开源软件，免费使用。",
        "folder_label": "文件夹:",
        "browse_btn": "浏览",
        "scan_btn": "扫描",
        "up_btn": "上级文件夹",
        "stop_btn": "停止",
        "status_select": "选择要扫描的文件夹。",
        "status_scanning": "正在扫描...",
        "status_scanning_item": "正在扫描: {name}",
        "status_done": "{count} 个项目 | 总计: {size}",
        "status_cancelled": "扫描已取消。已列出 {count} 个项目。",
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
        "err_delete_failed": "删除失败:\n{e}",
        "menu_connection": "连接",
        "conn_local": "本地磁盘",
        "conn_remote": "FTP / SSH 连接...",
        "conn_disconnect": "断开连接",
        "conn_title": "FTP / SSH 连接",
        "conn_mode": "协议:",
        "conn_host": "主机:",
        "conn_port": "端口:",
        "conn_user": "用户名:",
        "conn_pass": "密码:",
        "conn_key": "SSH 密钥文件（可选）:",
        "conn_path": "起始文件夹:",
        "conn_connect": "连接",
        "conn_cancel": "取消",
        "conn_anonymous": "匿名登录",
        "mode_local": "本地磁盘",
        "status_connecting": "正在连接到 {host}...",
        "status_connected": "已连接: {info}",
        "status_disconnected": "已断开连接。本地磁盘模式。",
        "err_connect_title": "连接错误",
        "err_connect_failed": "连接失败:\n{e}",
        "err_paramiko": "SFTP (SSH) 支持需要 'paramiko' 软件包。\n\n安装方法:\n    pip install paramiko",
        "err_host_required": "请输入主机地址。",
        "err_port_invalid": "请输入有效的端口号。",
        "err_list_failed": "无法列出文件夹:\n{e}",
        "err_remote_open_file": "无法直接打开远程文件。\n请先下载该文件。",
        "warn_remote_scan": "递归扫描远程文件夹可能需要较长时间。可使用停止按钮取消。"
    },
    "it": {
        "title": "Framanen DirLens - Analizzatore Dimensione Cartelle",
        "menu_settings": "Impostazioni",
        "menu_help": "Aiuto",
        "menu_about": "Informazioni su Framanen DirLens",
        "about_title": "Informazioni su Framanen DirLens",
        "about_text": "Framanen DirLens - Analizzatore Dimensione Cartelle\n\nVersione: {version}\nSviluppatore: Burak Duman\n\nAnalizza dischi locali, server FTP/FTPS e server SSH (SFTP).\n\nQuesto software è open-source e gratuito da usare.",
        "folder_label": "Cartella:",
        "browse_btn": "Sfoglia",
        "scan_btn": "Scansiona",
        "up_btn": "Cartella Sup.",
        "stop_btn": "Ferma",
        "status_select": "Seleziona una cartella da scansionare.",
        "status_scanning": "Scansione in corso...",
        "status_scanning_item": "Scansione: {name}",
        "status_done": "{count} elementi | Totale: {size}",
        "status_cancelled": "Scansione annullata. {count} elementi elencati.",
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
        "err_delete_failed": "Eliminazione fallita:\n{e}",
        "menu_connection": "Connessione",
        "conn_local": "Disco locale",
        "conn_remote": "Connessione FTP / SSH...",
        "conn_disconnect": "Disconnetti",
        "conn_title": "Connessione FTP / SSH",
        "conn_mode": "Protocollo:",
        "conn_host": "Host:",
        "conn_port": "Porta:",
        "conn_user": "Nome utente:",
        "conn_pass": "Password:",
        "conn_key": "File chiave SSH (opzionale):",
        "conn_path": "Cartella iniziale:",
        "conn_connect": "Connetti",
        "conn_cancel": "Annulla",
        "conn_anonymous": "Accesso anonimo",
        "mode_local": "Disco locale",
        "status_connecting": "Connessione a {host}...",
        "status_connected": "Connesso: {info}",
        "status_disconnected": "Disconnesso. Modalità disco locale.",
        "err_connect_title": "Errore di connessione",
        "err_connect_failed": "Connessione non riuscita:\n{e}",
        "err_paramiko": "Il supporto SFTP (SSH) richiede il pacchetto 'paramiko'.\n\nInstallalo con:\n    pip install paramiko",
        "err_host_required": "Inserisci un indirizzo host.",
        "err_port_invalid": "Inserisci un numero di porta valido.",
        "err_list_failed": "Impossibile elencare la cartella:\n{e}",
        "err_remote_open_file": "I file remoti non possono essere aperti direttamente.\nScarica prima il file.",
        "warn_remote_scan": "La scansione ricorsiva di una cartella remota può richiedere tempo. Usa Ferma per annullare."
    }
}


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


class ScanCancelled(Exception):
    """Raised inside a backend walk when the user presses Stop."""


def _stopped(should_stop):
    return bool(should_stop and should_stop())


class LocalBackend:
    """Filesystem access on the machine running the application."""

    scheme = "local"
    is_remote = False

    def describe(self, t):
        return t["mode_local"]

    def default_path(self):
        return os.path.expanduser("~")

    def join(self, path, name):
        return os.path.join(path, name)

    def parent(self, path):
        return os.path.dirname(os.path.normpath(path))

    def basename(self, path):
        return os.path.basename(os.path.normpath(path)) or path

    def is_dir(self, path):
        return os.path.isdir(path)

    def exists(self, path):
        return os.path.exists(path)

    def list_dir(self, path):
        """Return [(name, kind, size_or_None)] for one directory level."""
        entries = []
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    entries.append((entry.name, "dir", None))
                else:
                    entries.append((entry.name, "file",
                                    entry.stat(follow_symlinks=False).st_size))
            except OSError:
                pass
        return entries

    def file_size(self, path):
        try:
            return os.stat(path, follow_symlinks=False).st_size
        except OSError:
            return 0

    def dir_size(self, path, should_stop=None):
        total = 0
        try:
            entries = list(os.scandir(path))
        except OSError:
            return 0
        for entry in entries:
            if _stopped(should_stop):
                raise ScanCancelled
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += self.dir_size(entry.path, should_stop)
            except OSError:
                pass
        return total

    def delete(self, path, is_dir):
        if is_dir:
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)

    def open_file(self, path):
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def close(self):
        pass


class RemoteBackend:
    """Shared helpers for the FTP and SFTP backends (POSIX style paths)."""

    is_remote = True

    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user

    def describe(self, t):
        user = f"{self.user}@" if self.user else ""
        return f"{self.scheme}://{user}{self.host}:{self.port}"

    def join(self, path, name):
        return posixpath.join(path or "/", name)

    def parent(self, path):
        parent = posixpath.dirname(posixpath.normpath(path or "/"))
        return parent or "/"

    def basename(self, path):
        return posixpath.basename(posixpath.normpath(path or "/")) or path

    def open_file(self, path):
        raise NotImplementedError


class FTPBackend(RemoteBackend):
    """Directory sizes over FTP / FTPS using MLSD with a LIST fallback."""

    def __init__(self, host, port=21, user="", password="", tls=False,
                 timeout=20):
        super().__init__(host, port, user)
        self.scheme = "ftps" if tls else "ftp"
        self.ftp = ftplib.FTP_TLS() if tls else ftplib.FTP()
        self.ftp.connect(host, port, timeout=timeout)
        self.ftp.login(user or "anonymous", password or "anonymous@")
        if tls:
            self.ftp.prot_p()
        self.ftp.set_pasv(True)
        self._binary()
        self._use_mlsd = True

    def _binary(self):
        # SIZE is only reliable in binary mode, and retrlines switches to ASCII.
        try:
            self.ftp.voidcmd("TYPE I")
        except ftplib.all_errors:
            pass

    def default_path(self):
        try:
            return self.ftp.pwd() or "/"
        except ftplib.all_errors:
            return "/"

    def _list_cwd(self):
        if self._use_mlsd:
            try:
                entries = []
                for name, facts in self.ftp.mlsd():
                    if name in (".", ".."):
                        continue
                    kind = (facts.get("type") or "").lower()
                    if kind in ("cdir", "pdir"):
                        continue
                    if kind == "dir":
                        entries.append((name, "dir", None))
                    elif kind == "file":
                        raw = facts.get("size", "")
                        size = int(raw) if raw.isdigit() else None
                        entries.append((name, "file", size))
                return entries
            except (ftplib.error_perm, ftplib.error_proto, ftplib.error_temp,
                    ValueError, IndexError):
                # Server does not speak MLSD - fall back to LIST for good.
                self._use_mlsd = False
        lines = []
        self.ftp.retrlines("LIST", lines.append)
        self._binary()
        parsed = []
        for line in lines:
            entry = _parse_list_line(line)
            if entry:
                parsed.append(entry)
        return parsed

    def list_dir(self, path):
        self.ftp.cwd(path)
        return self._list_cwd()

    def is_dir(self, path):
        current = None
        try:
            current = self.ftp.pwd()
        except ftplib.all_errors:
            pass
        try:
            self.ftp.cwd(path)
            return True
        except ftplib.all_errors:
            return False
        finally:
            if current:
                try:
                    self.ftp.cwd(current)
                except ftplib.all_errors:
                    pass

    def exists(self, path):
        if self.is_dir(path):
            return True
        try:
            self.ftp.cwd(self.parent(path))
            names = [name for name, _kind, _size in self._list_cwd()]
            return self.basename(path) in names
        except ftplib.all_errors:
            return False

    def _size_in_cwd(self, name):
        self._binary()
        try:
            return self.ftp.size(name) or 0
        except ftplib.all_errors:
            return 0

    def file_size(self, path):
        try:
            self.ftp.cwd(self.parent(path))
        except ftplib.all_errors:
            return 0
        return self._size_in_cwd(self.basename(path))

    def dir_size(self, path, should_stop=None):
        total = 0
        stack = [path]
        while stack:
            if _stopped(should_stop):
                raise ScanCancelled
            current = stack.pop()
            try:
                self.ftp.cwd(current)
                entries = self._list_cwd()
            except (ftplib.error_perm, ftplib.error_temp):
                continue
            for name, kind, size in entries:
                if kind == "dir":
                    stack.append(posixpath.join(current, name))
                else:
                    total += size if size is not None else self._size_in_cwd(name)
        return total

    def delete(self, path, is_dir):
        if is_dir:
            self._rmtree(path)
        else:
            self.ftp.delete(path)

    def _rmtree(self, path):
        self.ftp.cwd(path)
        for name, kind, _size in self._list_cwd():
            child = posixpath.join(path, name)
            if kind == "dir":
                self._rmtree(child)
            else:
                self.ftp.cwd(path)
                self.ftp.delete(name)
        self.ftp.cwd(self.parent(path))
        self.ftp.rmd(path)

    def close(self):
        try:
            self.ftp.quit()
        except Exception:
            try:
                self.ftp.close()
            except Exception:
                pass


def _parse_list_line(line):
    """Parse one LIST line (unix or MS-DOS style) into (name, kind, size)."""
    parts = line.split(None, 8)
    if len(parts) >= 9 and line[:1] in "dl-bcps":
        name = parts[8]
        if name in (".", ".."):
            return None
        if line[0] == "d":
            return (name, "dir", None)
        if line[0] == "l":  # symlink: "name -> target"
            name = name.split(" -> ", 1)[0]
            return (name, "file", 0)
        try:
            return (name, "file", int(parts[4]))
        except ValueError:
            return (name, "file", None)
    # MS-DOS: "08-31-25  10:25PM       <DIR>          name"
    parts = line.split(None, 3)
    if len(parts) == 4:
        name = parts[3]
        if name in (".", ".."):
            return None
        if parts[2].upper() == "<DIR>":
            return (name, "dir", None)
        try:
            return (name, "file", int(parts[2]))
        except ValueError:
            return None
    return None


class SFTPBackend(RemoteBackend):
    """Directory sizes over SSH (SFTP), requires the paramiko package."""

    scheme = "sftp"

    def __init__(self, host, port=22, user="", password="", key_file="",
                 timeout=20):
        super().__init__(host, port, user)
        import paramiko

        self.client = paramiko.SSHClient()
        try:
            self.client.load_system_host_keys()
        except Exception:
            pass
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=host,
            port=port,
            username=user or None,
            password=password or None,
            key_filename=key_file or None,
            timeout=timeout,
            allow_agent=True,
            look_for_keys=True,
        )
        self.sftp = self.client.open_sftp()

    def default_path(self):
        try:
            return self.sftp.normalize(".")
        except Exception:
            return "/"

    def list_dir(self, path):
        entries = []
        for attr in self.sftp.listdir_attr(path):
            if attr.filename in (".", ".."):
                continue
            if attr.st_mode is not None and stat_module.S_ISDIR(attr.st_mode):
                entries.append((attr.filename, "dir", None))
            else:
                entries.append((attr.filename, "file", attr.st_size or 0))
        return entries

    def is_dir(self, path):
        try:
            return stat_module.S_ISDIR(self.sftp.stat(path).st_mode)
        except IOError:
            return False

    def exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except IOError:
            return False

    def file_size(self, path):
        try:
            return self.sftp.stat(path).st_size or 0
        except IOError:
            return 0

    def dir_size(self, path, should_stop=None):
        total = 0
        stack = [path]
        while stack:
            if _stopped(should_stop):
                raise ScanCancelled
            current = stack.pop()
            try:
                attrs = self.sftp.listdir_attr(current)
            except IOError:
                continue
            for attr in attrs:
                if attr.filename in (".", ".."):
                    continue
                if attr.st_mode is not None and stat_module.S_ISDIR(attr.st_mode):
                    stack.append(posixpath.join(current, attr.filename))
                else:
                    total += attr.st_size or 0
        return total

    def delete(self, path, is_dir):
        if is_dir:
            self._rmtree(path)
        else:
            self.sftp.remove(path)

    def _rmtree(self, path):
        for attr in self.sftp.listdir_attr(path):
            child = posixpath.join(path, attr.filename)
            if attr.st_mode is not None and stat_module.S_ISDIR(attr.st_mode):
                self._rmtree(child)
            else:
                self.sftp.remove(child)
        self.sftp.rmdir(path)

    def close(self):
        try:
            self.sftp.close()
        except Exception:
            pass
        try:
            self.client.close()
        except Exception:
            pass


BG = "#1e1e2e"
BG_ALT = "#313244"
FG = "#cdd6f4"

DEFAULT_PORTS = {"ftp": 21, "ftps": 21, "sftp": 22}


class ConnectionDialog(tk.Toplevel):
    """Modal dialog collecting FTP / FTPS / SFTP connection settings."""

    def __init__(self, parent, t, last=None):
        super().__init__(parent)
        self.t = t
        self.result = None
        last = last or {}
        self.title(t["conn_title"])
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        self.mode_var = tk.StringVar(value=last.get("mode", "ftp"))
        self.host_var = tk.StringVar(value=last.get("host", ""))
        self.port_var = tk.StringVar(value=str(last.get("port", 21)))
        self.user_var = tk.StringVar(value=last.get("user", ""))
        self.pass_var = tk.StringVar(value="")
        self.key_var = tk.StringVar(value=last.get("key_file", ""))
        self.path_var = tk.StringVar(value=last.get("path", "/"))
        self.anon_var = tk.BooleanVar(value=last.get("anonymous", False))

        body = tk.Frame(self, bg=BG, padx=16, pady=14)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=t["conn_mode"], bg=BG, fg=FG,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=4)
        modes = tk.Frame(body, bg=BG)
        modes.grid(row=0, column=1, sticky="w", pady=4)
        for value, label in (("ftp", "FTP"), ("ftps", "FTPS (TLS)"),
                             ("sftp", "SFTP (SSH)")):
            tk.Radiobutton(modes, text=label, value=value,
                           variable=self.mode_var, command=self._on_mode_change,
                           bg=BG, fg=FG, selectcolor=BG_ALT,
                           activebackground=BG, activeforeground=FG,
                           font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))

        rows = (
            (1, t["conn_host"], self.host_var, False),
            (2, t["conn_port"], self.port_var, False),
            (3, t["conn_user"], self.user_var, False),
            (4, t["conn_pass"], self.pass_var, True),
        )
        for row, label, var, secret in rows:
            tk.Label(body, text=label, bg=BG, fg=FG,
                     font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w",
                                                 pady=4)
            entry = tk.Entry(body, textvariable=var, width=34, bg=BG_ALT, fg=FG,
                             insertbackground=FG, relief="flat",
                             font=("Segoe UI", 10),
                             show="*" if secret else "")
            entry.grid(row=row, column=1, sticky="we", pady=4, ipady=3)

        tk.Checkbutton(body, text=t["conn_anonymous"], variable=self.anon_var,
                       command=self._on_anonymous, bg=BG, fg=FG,
                       selectcolor=BG_ALT, activebackground=BG,
                       activeforeground=FG,
                       font=("Segoe UI", 9)).grid(row=5, column=1, sticky="w")

        self.key_label = tk.Label(body, text=t["conn_key"], bg=BG, fg=FG,
                                  font=("Segoe UI", 10))
        self.key_label.grid(row=6, column=0, sticky="w", pady=4)
        key_row = tk.Frame(body, bg=BG)
        key_row.grid(row=6, column=1, sticky="we", pady=4)
        self.key_entry = tk.Entry(key_row, textvariable=self.key_var, width=26,
                                  bg=BG_ALT, fg=FG, insertbackground=FG,
                                  relief="flat", font=("Segoe UI", 10))
        self.key_entry.pack(side="left", ipady=3)
        self.key_btn = tk.Button(key_row, text="...", command=self._pick_key,
                                 bg=BG_ALT, fg=FG, relief="flat",
                                 font=("Segoe UI", 9, "bold"), cursor="hand2")
        self.key_btn.pack(side="left", padx=6)

        tk.Label(body, text=t["conn_path"], bg=BG, fg=FG,
                 font=("Segoe UI", 10)).grid(row=7, column=0, sticky="w", pady=4)
        tk.Entry(body, textvariable=self.path_var, width=34, bg=BG_ALT, fg=FG,
                 insertbackground=FG, relief="flat",
                 font=("Segoe UI", 10)).grid(row=7, column=1, sticky="we",
                                             pady=4, ipady=3)

        buttons = tk.Frame(body, bg=BG)
        buttons.grid(row=8, column=0, columnspan=2, sticky="e", pady=(12, 0))
        tk.Button(buttons, text=t["conn_cancel"], command=self._cancel,
                  bg=BG_ALT, fg=FG, relief="flat", padx=12,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side="left",
                                                                     padx=4)
        tk.Button(buttons, text=t["conn_connect"], command=self._ok,
                  bg="#a6e3a1", fg=BG, relief="flat", padx=12,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(side="left")

        self._on_mode_change(keep_port=True)
        self._on_anonymous()
        self.bind("<Return>", lambda _e: self._ok())
        self.bind("<Escape>", lambda _e: self._cancel())
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.update_idletasks()
        self.grab_set()

    def _on_mode_change(self, keep_port=False):
        mode = self.mode_var.get()
        if not keep_port or not self.port_var.get().strip():
            self.port_var.set(str(DEFAULT_PORTS[mode]))
        elif self.port_var.get().strip() in [str(p) for p in DEFAULT_PORTS.values()]:
            self.port_var.set(str(DEFAULT_PORTS[mode]))
        state = "normal" if mode == "sftp" else "disabled"
        self.key_entry.config(state=state)
        self.key_btn.config(state=state)
        self.key_label.config(fg=FG if mode == "sftp" else "#6c7086")

    def _on_anonymous(self):
        if self.anon_var.get():
            self.user_var.set("anonymous")
            self.pass_var.set("anonymous@")

    def _pick_key(self):
        path = filedialog.askopenfilename(parent=self)
        if path:
            self.key_var.set(path)

    def _ok(self):
        host = self.host_var.get().strip()
        if not host:
            messagebox.showerror(self.t["err_title"],
                                 self.t["err_host_required"], parent=self)
            return
        try:
            port = int(self.port_var.get().strip())
            if not 0 < port < 65536:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.t["err_title"],
                                 self.t["err_port_invalid"], parent=self)
            return
        self.result = {
            "mode": self.mode_var.get(),
            "host": host,
            "port": port,
            "user": self.user_var.get().strip(),
            "password": self.pass_var.get(),
            "key_file": self.key_var.get().strip(),
            "path": self.path_var.get().strip() or "/",
            "anonymous": self.anon_var.get(),
        }
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()


class FolderSizeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = "tr"
        self.geometry("900x600")
        self.configure(bg=BG)
        self._scanning = False
        self._stop_requested = False
        self.backend = LocalBackend()
        self._last_conn = None
        self._build_ui()
        self._update_language(self.current_lang)

    # ------------------------------------------------------------------ UI

    def _build_ui(self):
        # Create Menu Bar for Settings/Language Selection
        self.menu_bar = tk.Menu(self, tearoff=0, bg=BG_ALT, fg=FG, activebackground="#45475a", activeforeground=FG)
        self.config(menu=self.menu_bar)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0, bg=BG_ALT, fg=FG, activebackground="#45475a", activeforeground=FG)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.lang_var = tk.StringVar(value=self.current_lang)
        self.settings_menu.add_radiobutton(label="English", variable=self.lang_var, value="en", command=lambda: self._update_language("en"))
        self.settings_menu.add_radiobutton(label="Türkçe", variable=self.lang_var, value="tr", command=lambda: self._update_language("tr"))
        self.settings_menu.add_radiobutton(label="Español", variable=self.lang_var, value="es", command=lambda: self._update_language("es"))
        self.settings_menu.add_radiobutton(label="Deutsch", variable=self.lang_var, value="de", command=lambda: self._update_language("de"))
        self.settings_menu.add_radiobutton(label="한국어", variable=self.lang_var, value="ko", command=lambda: self._update_language("ko"))
        self.settings_menu.add_radiobutton(label="中文", variable=self.lang_var, value="zh", command=lambda: self._update_language("zh"))
        self.settings_menu.add_radiobutton(label="Italiano", variable=self.lang_var, value="it", command=lambda: self._update_language("it"))

        # Create Connection Menu (local disk / FTP / SFTP)
        self.conn_menu = tk.Menu(self.menu_bar, tearoff=0, bg=BG_ALT, fg=FG, activebackground="#45475a", activeforeground=FG)
        self.menu_bar.add_cascade(label="Connection", menu=self.conn_menu)
        self.conn_menu.add_command(label="Local Disk", command=self._use_local)
        self.conn_menu.add_command(label="FTP / SSH", command=self._open_connection_dialog)
        self.conn_menu.add_command(label="Disconnect", command=self._disconnect)

        # Create Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, bg=BG_ALT, fg=FG, activebackground="#45475a", activeforeground=FG)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About Framanen DirLens", command=self._show_about)

        top = tk.Frame(self, bg=BG, pady=10)
        top.pack(fill="x", padx=16)

        self.lbl_folder = tk.Label(top, text="Klasör:", bg=BG, fg=FG,
                                   font=("Segoe UI", 10))
        self.lbl_folder.pack(side="left")

        self.path_var = tk.StringVar(value=os.path.expanduser("~"))
        entry = tk.Entry(top, textvariable=self.path_var, width=48,
                         bg=BG_ALT, fg=FG, insertbackground=FG,
                         relief="flat", font=("Segoe UI", 10))
        entry.pack(side="left", padx=8, ipady=4)

        self.btn_browse = tk.Button(top, text="Gözat", command=self._browse,
                                    bg="#89b4fa", fg=BG, relief="flat",
                                    font=("Segoe UI", 10, "bold"), padx=10,
                                    cursor="hand2")
        self.btn_browse.pack(side="left", padx=4)

        self.btn_scan = tk.Button(top, text="Tara", command=self._start_scan,
                                  bg="#a6e3a1", fg=BG, relief="flat",
                                  font=("Segoe UI", 10, "bold"), padx=10,
                                  cursor="hand2")
        self.btn_scan.pack(side="left", padx=4)

        self.btn_up = tk.Button(top, text="Üst Klasör", command=self._go_up,
                                bg="#f9e2af", fg=BG, relief="flat",
                                font=("Segoe UI", 10, "bold"), padx=10,
                                cursor="hand2")
        self.btn_up.pack(side="left", padx=4)

        self.btn_stop = tk.Button(top, text="Durdur", command=self._request_stop,
                                  bg="#f38ba8", fg=BG, relief="flat",
                                  font=("Segoe UI", 10, "bold"), padx=10,
                                  cursor="hand2", state="disabled")
        self.btn_stop.pack(side="left", padx=4)

        self.lbl_conn = tk.Label(self, text="", bg=BG, fg="#89b4fa",
                                 font=("Segoe UI", 9, "bold"), anchor="w")
        self.lbl_conn.pack(fill="x", padx=16)

        self.status = tk.Label(self, text="Taramak için bir klasör seçin.",
                               bg=BG, fg="#6c7086",
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(fill="x", padx=16)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=16, pady=(2, 6))
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#181825", foreground=FG,
                         fieldbackground="#181825", rowheight=26,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=BG_ALT,
                         foreground=FG, font=("Segoe UI", 10, "bold"))
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
        self.tree.column("name", width=450, anchor="w")
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
        self._kinds = {}
        self._sort_key = "size"
        self._sort_rev = True

    # ------------------------------------------------------- connection

    def _open_connection_dialog(self):
        if self._scanning:
            return
        t = LANGUAGES[self.current_lang]
        dialog = ConnectionDialog(self, t, self._last_conn)
        self.wait_window(dialog)
        if not dialog.result:
            return
        params = dialog.result
        self._last_conn = {k: v for k, v in params.items() if k != "password"}
        if params["mode"] == "sftp":
            try:
                import paramiko  # noqa: F401
            except ImportError:
                messagebox.showerror(t["err_connect_title"], t["err_paramiko"])
                return
        self._scanning = True
        self.btn_scan.config(state="disabled")
        self.progress.start(10)
        self.status.config(text=t["status_connecting"].format(host=params["host"]))
        threading.Thread(target=self._connect, args=(params,),
                         daemon=True).start()

    def _connect(self, params):
        try:
            if params["mode"] == "sftp":
                backend = SFTPBackend(params["host"], params["port"],
                                      params["user"], params["password"],
                                      params["key_file"])
            else:
                backend = FTPBackend(params["host"], params["port"],
                                     params["user"], params["password"],
                                     tls=params["mode"] == "ftps")
        except Exception as exc:
            self.after(0, lambda e=exc: self._connect_failed(e))
            return
        self.after(0, lambda: self._connected(backend, params["path"]))

    def _connect_failed(self, exc):
        self._scanning = False
        self.progress.stop()
        self.btn_scan.config(state="normal")
        t = LANGUAGES[self.current_lang]
        self.status.config(text=t["status_select"])
        messagebox.showerror(t["err_connect_title"],
                             t["err_connect_failed"].format(e=exc))

    def _connected(self, backend, path):
        self._scanning = False
        self.progress.stop()
        self.btn_scan.config(state="normal")
        self._close_backend()
        self.backend = backend
        self._clear_results()
        self.path_var.set(path or backend.default_path())
        t = LANGUAGES[self.current_lang]
        self.btn_browse.config(state="disabled")
        self._refresh_conn_label()
        self.status.config(text=t["status_connected"].format(
            info=backend.describe(t)))
        self._start_scan()

    def _use_local(self):
        self._disconnect()

    def _disconnect(self):
        if self._scanning:
            return
        if not self.backend.is_remote:
            return
        self._close_backend()
        self.backend = LocalBackend()
        self._clear_results()
        self.path_var.set(self.backend.default_path())
        self.btn_browse.config(state="normal")
        self._refresh_conn_label()
        self.status.config(text=LANGUAGES[self.current_lang]["status_disconnected"])

    def _close_backend(self):
        try:
            self.backend.close()
        except Exception:
            pass

    def _refresh_conn_label(self):
        t = LANGUAGES[self.current_lang]
        self.lbl_conn.config(text=self.backend.describe(t))

    def _clear_results(self):
        self.tree.delete(*self.tree.get_children())
        self._data = []
        self._kinds = {}

    # ------------------------------------------------------------- scan

    def _browse(self):
        if self.backend.is_remote:
            return
        d = filedialog.askdirectory(initialdir=self.path_var.get())
        if d:
            self.path_var.set(d)

    def _start_scan(self):
        if self._scanning:
            return
        path = self.path_var.get().strip()
        t = LANGUAGES[self.current_lang]
        if not self.backend.is_remote and not os.path.isdir(path):
            messagebox.showerror(t["err_title"], t["err_invalid_path"])
            return
        self._scanning = True
        self._stop_requested = False
        self._clear_results()
        self.btn_stop.config(state="normal")
        self.progress.start(10)
        self.status.config(text=t["warn_remote_scan"] if self.backend.is_remote
                           else t["status_scanning"])
        threading.Thread(target=self._scan, args=(path, self.backend),
                         daemon=True).start()

    def _request_stop(self):
        self._stop_requested = True

    def _scan(self, path, backend):
        try:
            entries = backend.list_dir(path)
        except Exception as exc:
            self.after(0, lambda e=exc: self._scan_failed(e))
            return

        results = []
        cancelled = False
        for name, kind, size in entries:
            if self._stop_requested:
                cancelled = True
                break
            full = backend.join(path, name)
            try:
                if kind == "dir":
                    self.after(0, lambda n=name: self._scanning_item(n))
                    size = backend.dir_size(full, lambda: self._stop_requested)
                elif size is None:
                    size = backend.file_size(full)
            except ScanCancelled:
                cancelled = True
                break
            except Exception:
                size = size or 0
            results.append((name, size or 0, full, kind))

        self.after(0, lambda: self._done(results, cancelled))

    def _scanning_item(self, name):
        if not self._scanning:
            return
        t = LANGUAGES[self.current_lang]
        self.status.config(text=t["status_scanning_item"].format(name=name))

    def _scan_failed(self, exc):
        self._scanning = False
        self._stop_requested = False
        self.progress.stop()
        self.btn_stop.config(state="disabled")
        t = LANGUAGES[self.current_lang]
        self.status.config(text=t["status_select"])
        messagebox.showerror(t["err_title"], t["err_list_failed"].format(e=exc))

    def _done(self, results, cancelled=False):
        self._scanning = False
        self._stop_requested = False
        self.progress.stop()
        self.btn_stop.config(state="disabled")
        self._data = results
        self._populate()
        total = sum(r[1] for r in results)
        t = LANGUAGES[self.current_lang]
        if cancelled:
            self.status.config(
                text=t["status_cancelled"].format(count=len(results)))
        else:
            self.status.config(
                text=t["status_done"].format(count=len(results),
                                             size=format_size(total)))

    def _populate(self):
        self.tree.delete(*self.tree.get_children())
        self._kinds = {}
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
            self._kinds[path] = kind
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
        parent_path = self.backend.parent(current_path)
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
        t = LANGUAGES[self.current_lang]
        if self._kinds.get(item) == "dir":
            self.path_var.set(item)
            self._start_scan()
        elif self.backend.is_remote:
            messagebox.showinfo(t["err_title"], t["err_remote_open_file"])
        else:
            try:
                self.backend.open_file(item)
            except Exception as e:
                messagebox.showerror(t["err_title"], t["err_open_file"].format(e=e))

    def _on_click(self, event):
        column = self.tree.identify_column(event.x)
        if column == "#4":
            item = self.tree.identify_row(event.y)
            if item:
                self._confirm_delete(item)

    def _confirm_delete(self, path):
        if self._scanning:
            return
        name = self.backend.basename(path)
        is_dir = self._kinds.get(path) == "dir"
        t = LANGUAGES[self.current_lang]
        item_type = t["type_folder"] if is_dir else t["type_file"]

        confirm = messagebox.askyesno(
            t["confirm_del_title"],
            t["confirm_del_msg"].format(name=name, item_type=item_type),
            icon="warning"
        )

        if confirm:
            try:
                self.backend.delete(path, is_dir)
                messagebox.showinfo(t["success_title"], t["success_msg"].format(name=name))
                self._start_scan()
            except Exception as e:
                messagebox.showerror(t["err_title"], t["err_delete_failed"].format(e=e))

    # --------------------------------------------------------- language

    def _update_language(self, lang_code):
        self.current_lang = lang_code
        t = LANGUAGES[lang_code]

        self.title(t["title"])
        self.lbl_folder.config(text=t["folder_label"])
        self.btn_browse.config(text=t["browse_btn"])
        self.btn_scan.config(text=t["scan_btn"])
        self.btn_up.config(text=t["up_btn"])
        self.btn_stop.config(text=t["stop_btn"])

        self.tree.heading("name", text=t["hdr_name"])
        self.tree.heading("size", text=t["hdr_size"])
        self.tree.heading("pct", text=t["hdr_ratio"])
        self.tree.heading("delete", text=t["hdr_delete"])

        self.menu_bar.entryconfig(0, label=t["menu_settings"])
        self.menu_bar.entryconfig(1, label=t["menu_connection"])
        self.menu_bar.entryconfig(2, label=t["menu_help"])
        self.conn_menu.entryconfig(0, label=t["conn_local"])
        self.conn_menu.entryconfig(1, label=t["conn_remote"])
        self.conn_menu.entryconfig(2, label=t["conn_disconnect"])
        self.help_menu.entryconfig(0, label=t["menu_about"])
        self._refresh_conn_label()

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
        messagebox.showinfo(t["about_title"],
                            t["about_text"].format(version=APP_VERSION))

    def destroy(self):
        self._close_backend()
        super().destroy()


if __name__ == "__main__":
    app = FolderSizeApp()
    app.mainloop()

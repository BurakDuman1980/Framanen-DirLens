# Framanen DirLens — Proje Dokümanı

Bu dosya projenin **teknik** dokümanıdır: mimari, modül haritası, veri akışı ve
geliştirme notları. Kurulum ve son kullanıcı anlatımı için [README.md](README.md)
dosyasına bakın.

* **Sürüm:** 2.0.0 (`APP_VERSION`, `klasor_boyutu.py:11`)
* **Geliştirici:** Burak Duman
* **Depo:** https://github.com/BurakDuman1980/Framanen-DirLens

---

## 1. Amaç

Bir klasör ağacında yerin nereye gittiğini göstermek. Uygulama seçilen klasörün
bir seviye altındaki her öğeyi listeler, klasörleri **özyinelemeli** ölçer ve
sonucu boyuta göre sıralayıp oran çubuğuyla gösterir. 2.0.0 ile aynı işi uzak
sunucularda da yapar: **FTP**, **FTPS (TLS)** ve **SSH (SFTP)**.

Tasarım hedefleri:

* **Tek dosya, tek bağımlılık.** Yerel + FTP + FTPS modları yalnızca standart
  kütüphaneyle çalışır; `paramiko` sadece SFTP için ve isteğe bağlıdır.
* **Tek arayüz.** Uzak mod ayrı bir ekran değil; aynı liste, aynı gezinme, aynı
  silme akışı farklı bir depolama arka ucuyla çalışır.
* **Kaçış yolu her zaman açık.** Uzak taramalar uzun sürebildiği için her tarama
  **Durdur** ile iptal edilebilir.

---

## 2. Dosya düzeni

| Yol | İçerik |
|---|---|
| `klasor_boyutu.py` | Uygulamanın tamamı (~1460 satır): diller, arka uçlar, arayüz |
| `requirements.txt` | Yalnızca `paramiko` (SFTP için opsiyonel) |
| `README.md` | Kullanıcı dokümanı, kurulum, changelog |
| `PROJECT.md` | Bu dosya — teknik doküman |
| `dist/Framanen_DirLens.exe` | Yayınlanan 64-bit Windows derlemesi (2.0.0) |
| `dist/klasor_boyutu.zip` | Aynı exe'nin sıkıştırılmış kopyası |
| `screenshot2.jpg` | Ana ekran görüntüsü |
| `screenshot_connection.png` | FTP/SSH bağlantı diyaloğu görüntüsü |

Tek dosyada kalmak bilinçli bir tercih: PyInstaller ile paketleme tek komuta
iner ve kaynak koddan çalıştırmak için depoyu klonlamak bile gerekmez.

---

## 3. Mimari

Kod dört katmana ayrılır. Katmanlar arasındaki tek bağ, arka uç arayüzüdür.

```
LANGUAGES  (satır 13)      7 dilin metin sözlükleri, dilde 57 anahtar
    │
    ├── Arka uçlar (satır 438-853)
    │     LocalBackend            os / os.scandir
    │     RemoteBackend           POSIX yol yardımcıları (ortak taban)
    │       ├── FTPBackend        ftplib, MLSD → LIST yedeği
    │       └── SFTPBackend       paramiko (opsiyonel içe aktarma)
    │
    ├── ConnectionDialog (satır 863)   protokol/kimlik bilgisi formu
    │
    └── FolderSizeApp (satır 1013)     Tk penceresi, tarama akışı, liste
```

### 3.1 Arka uç sözleşmesi

Her arka uç aynı yöntemleri sunar; `FolderSizeApp` bunların dışında hiçbir
depolama detayı bilmez:

| Yöntem | Görevi |
|---|---|
| `list_dir(path)` | Bir seviye listeler → `[(ad, "dir"\|"file", boyut_veya_None)]` |
| `dir_size(path, should_stop)` | Klasörü özyinelemeli ölçer; iptalde `ScanCancelled` |
| `file_size(path)` | Listelemede boyut gelmediyse tek dosyayı ölçer |
| `is_dir` / `exists` | Yol sorguları |
| `join` / `parent` / `basename` | Yol işlemleri (yerelde `os.path`, uzakta `posixpath`) |
| `delete(path, is_dir)` | Dosya siler, klasörü özyinelemeli siler |
| `open_file(path)` | Yerelde sistem uygulamasıyla açar; uzakta desteklenmez |
| `describe(t)` | Durum çubuğundaki bağlantı etiketi |
| `default_path()` | Bağlantı sonrası başlangıç klasörü |
| `close()` | Bağlantıyı kapatır |

`is_remote` bayrağı arayüzün küçük farkları için kullanılır (Gözat düğmesi uzak
modda kapalı, uzak dosya çift tıklaması açmak yerine bilgi verir).

### 3.2 FTP ayrıntıları (`FTPBackend`, satır 558)

* Listeleme önce **`MLSD`** ile denenir — tip ve boyut doğrudan gelir.
* Sunucu MLSD desteklemiyorsa (`error_perm`/`error_proto`) bayrak kalıcı olarak
  düşer ve **`LIST`** çıktısı `_parse_list_line` (satır 711) ile ayrıştırılır:
  UNIX biçimi, MS-DOS biçimi ve sembolik bağlar.
* Boyut listelemede yoksa `SIZE` komutuna düşülür. `SIZE` yalnızca binary modda
  güvenilir olduğu ve `retrlines` bağlantıyı ASCII moda aldığı için her
  listelemeden sonra `TYPE I` yeniden gönderilir (`_binary`, satır 574).
* Özyinelemeli ölçüm yığın tabanlıdır (özyineleme değil) — derin ağaçlarda
  yığın taşması olmaz.

### 3.3 SFTP ayrıntıları (`SFTPBackend`, satır 742)

* `paramiko` **fonksiyon içinde** içe aktarılır; paket yoksa uygulama yine
  açılır, yalnızca SFTP seçildiğinde "paramiko kurun" uyarısı çıkar.
* Bilinen sunucu anahtarları yüklenir, bilinmeyen sunucular ilk bağlantıda
  kabul edilir (`AutoAddPolicy`).
* **Parola veya anahtar dosyası verilmişse yalnızca o kullanılır**
  (`allow_agent=False`, `look_for_keys=False`). Hiçbir kimlik bilgisi
  verilmediğinde SSH ajanı ve varsayılan anahtarlar denenir. Bu ayrım, frozen
  exe testinde ajan yoklamasının geçerli bir parola girişini iptal etmesi
  üzerine eklendi.

---

## 4. Tarama akışı

```
Tara / çift tıklama / Üst Klasör
        │
        ▼
_start_scan (1249)      arayüzü kilitler, Durdur'u açar, iş parçacığı başlatır
        │
        ▼  (worker thread)
_scan (1270)            backend.list_dir → her klasör için backend.dir_size
        │                her öğede _stop_requested kontrol edilir
        ▼  self.after(0, ...) ile ana iş parçacığına döner
_done (1314)            _populate ile ağacı doldurur, durum satırını yazar
```

* Tüm ağ ve disk işi arka plandaki tek bir iş parçacığında yapılır; Tk çağrıları
  `self.after(0, ...)` ile ana iş parçacığına aktarılır.
* Aynı anda yalnızca bir tarama çalışır (`_scanning` bayrağı). Bu, arka uçların
  iş parçacığı güvenli olmamasını sorun olmaktan çıkarır.
* **Durdur** yalnızca bir bayrak (`_stop_requested`) kaldırır; arka uçlar bunu
  `should_stop()` üzerinden okuyup `ScanCancelled` fırlatır. İptal edilen tarama
  o ana kadar ölçülen öğeleri gösterir, hata olarak değil "durduruldu" olarak
  raporlanır.
* Bağlanma da iş parçacığında yapılır (`_connect`, 1170) — yavaş bir sunucu
  arayüzü dondurmaz.

---

## 5. Çoklu dil

* `LANGUAGES` sözlüğü: `en, tr, es, de, ko, zh, it` — dil başına **57 anahtar**.
* Dil değişimi çalışırken yapılır: `_update_language` (1418) başlığı, düğmeleri,
  sütun başlıklarını, menü etiketlerini ve durum satırını yeniden yazar.
* Sürüm numarası metinlerde sabit değil; `about_text` içindeki `{version}`
  yer tutucusu `APP_VERSION` ile doldurulur.

Yeni dil eklerken: `LANGUAGES`'e aynı 57 anahtarı içeren bir giriş ve
`_build_ui` içindeki dil menüsüne bir `add_radiobutton` satırı yeterlidir.
Anahtar setinin tutarlılığı şu tek satırla doğrulanabilir:

```bash
python3 -c "
import klasor_boyutu as a
base=set(a.LANGUAGES['en'])
print({k: base ^ set(v) for k,v in a.LANGUAGES.items() if set(v)!=base} or 'tutarlı')"
```

---

## 6. Çalıştırma ve paketleme

```bash
python klasor_boyutu.py                # kaynaktan (Python 3.x + Tkinter)
pip install -r requirements.txt        # yalnızca SFTP için gerekir
```

Windows exe:

```bash
pip install pyinstaller paramiko
pyinstaller --onefile --noconsole --hidden-import paramiko klasor_boyutu.py
```

`--hidden-import paramiko` gerekir çünkü paramiko koşullu olarak içe aktarılır
ve PyInstaller'ın statik çözümleyicisi onu göremez. Depodaki
`dist/Framanen_DirLens.exe` tam olarak bu komutla üretilmiştir.

---

## 7. Test yaklaşımı

Depoda test dosyası tutulmuyor; doğrulama, sahte nesneler yerine **gerçek
sunucular ve gerçek bir pencere** üzerinden yapılır:

| Alan | Yöntem |
|---|---|
| FTP | `pyftpdlib` ile canlı sunucu; MLSD ve LIST yolları ayrı ayrı |
| LIST ayrıştırıcı | UNIX / MS-DOS / sembolik bağ / bozuk satır birim testleri |
| SFTP | Süreç içi paramiko SFTP sunucusu |
| Arayüz | Xvfb altında gerçek `mainloop`, `after` ile sürülen adımlar |
| Exe | Wine altında çalıştırma + frozen koddan canlı FTP/SFTP bağlantısı |

Arayüz testinde dikkat edilecek iki nokta: `mainloop` çalışmadan başka bir iş
parçacığından `after` çağrılamaz, ve `messagebox` çağrıları testte bloklar —
kaydeden birer sahte fonksiyonla değiştirilmeleri gerekir.

---

## 8. Bilinen sınırlar

* Uzak klasör boyutu ağaç üzerinde gezilerek hesaplanır; derin ağaçlarda
  gecikme protokolün doğasıdır, **Durdur** bu yüzden var.
* Uzak dosyalar çift tıklamayla açılamaz (indirme özelliği yok).
* Silme kalıcıdır — geri dönüşüm kutusu kullanılmaz, yerelde de uzakta da.
* Bağlantı parolaları hiçbir yere yazılmaz; diyalog yalnızca protokol, sunucu,
  kullanıcı adı ve yolu oturum boyunca hatırlar.
* SFTP'de bilinmeyen sunucu anahtarı ilk bağlantıda sorulmadan kabul edilir.

---

## 9. Olası sonraki adımlar

* Uzak dosyayı indirip açma (çift tıklama davranışının tamamlanması).
* Tarama sonucunu CSV/JSON dışa aktarma.
* Klasör ağacını genişletilebilir hiyerarşi olarak gösterme.
* Windows exe'sini üreten bir GitHub Actions iş akışı (şu an derleme elle).
* Bağlantı profillerini (parolasız) kaydetme.

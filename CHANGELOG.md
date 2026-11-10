# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning.

## [Unreleased]

---

## [v1.1.0] - 2026-11-10

### Added
- Dukungan Android (APK) — `main.py` menjalankan game yang sama di UI terminal berbasis Kivy: output berwarna, tombol perintah cepat, input teks, tombol `A-` / `A+` untuk ukuran font, auto-scroll
- `buildozer.spec` — konfigurasi build APK; versi dibaca otomatis dari `core/version.py`
- `.github/workflows/build-apk.yml` — build APK di GitHub Actions (push tag `v*` atau manual), APK dilampirkan ke Release
- `assets/DejaVuSansMono.ttf` dan `assets/DejaVu-LICENSE.txt` — font monospace yang memiliki glyph block/box-drawing untuk banner di Android
- `core/game.py` — main loop dan dispatcher command dipindah dari `blacknet.py`, dipakai bersama oleh terminal dan Android; tabel command dengan validasi jumlah argumen dan pesan `usage:` seragam
- `core/paths.py` — lokasi data tunggal; terminal memakai `data/` proyek (tidak lagi bergantung pada working directory), Android memakai penyimpanan privat aplikasi; env `BLACKNET_HOME` untuk lokasi kustom; seed data disalin otomatis dan file world statis diperbarui saat versi naik tanpa menimpa progress
- `core/store.py` — baca/tulis JSON aman (tahan file rusak, tulis atomik) dan validasi nama target
- `core/bridge.py` dan `core/ansi.py` — jembatan stdout/input dan emulator terminal (warna ANSI, `\r`, clear screen, wrap kolom, fallback emoji) untuk UI Android
- `core/version.py` — sumber tunggal nomor versi
- `blacknet.py --version` dan `--help`
- Env `BLACKNET_FAST=1` untuk mematikan animasi dan jeda ketikan
- `tests/test_blacknet.py` — 30 unit test (filesystem, auth, blue team, pivot, persistence, jobs, sync, storage, layer Android, sesi game penuh)
- `ls [path]`, `cd ..` dan path relatif/normalisasi path di filesystem
- `reconnect [target]` — target opsional
- `engine.connect()`, `engine.disconnect()`, `engine.cool_down()` dan `engine.current_node`
- Penanda node aktif (`*`) di `netmap`, `[NODE:...]` di status bar, dan baris `Node` di `status`
- Help dan man page untuk `sudo`, `complete`, `reconnect`, `lay-low`, `ids`, `ids-clear`, `status`, `pull`, `push`
- `.gitignore`: `.buildozer/`, `bin/`, `*.apk`, `*.aab`, `.kivy/`

### Changed
- `blacknet.py` — sekarang hanya wrapper tipis ke `core.game.main()`; import tidak lagi langsung menjalankan game
- `core/*.py` — semua `DATA = "data"` relatif diganti `core.paths.DATA`
- `core/ui.py` — `clear()` memakai escape ANSI (`cls` di Windows) bukan `os.system("clear")`; `status_bar(engine, p=None)`
- `core/netmap.py` — pesan error jelas untuk data jaringan rusak; `name` jaringan opsional
- `core/jobs.py` — `reward` menerima angka atau `{"credits", "rep"}` sesuai JOB_SPEC; ID job tidak peka huruf besar/kecil (`take job-004`)
- `core/net/protocol.py` dan `core/net/sync.py` — `world.json` menyimpan data per player (`players`), `rep_avg` dihitung ulang, `jobs_done` unik
- Nama command dibaca huruf kecil (keyboard Android/Termux sering mengkapitalisasi huruf pertama)
- `data/jobs.json` — target JOB-004 dipindah dari `bank-neo` ke `gov-id-01` (node `internal-db` hanya ada di jaringan gov-id-01)
- `data/wordlist.txt` — ditambah `admin123`
- `README.md`, `docs/WORLD_SPEC.md`, `docs/JOB_SPEC.md`, `CONTRIBUTING.md` — disesuaikan dengan kode (sintaks `ssh`/`crack`, field `role`, format reward, format `jobs_taken`/`jobs_done`, cara build APK, cara tes)
- `.github/workflows/python-app.yml` — smoke test sungguhan (compile, unit test, `--version`, `--help`) menggantikan `python blacknet.py --help || true` yang menjalankan game dan menyembunyikan error
- `.github/workflows/codeql.yml` — juga berjalan di branch `master`

### Fixed
- `core/blueteam.py` — respons blue team hanya dipicu saat level deteksi naik; sebelumnya TRACE bertambah +1 sampai +3 pada setiap perintah selama bukti lama masih ada, sehingga pemain terputus hanya dengan mengetik `ls`
- `core/forensics.py` — `auth log wiped` / `system log wiped` tidak lagi muncul sebagai false positive tepat setelah `ssh` (log baru yang kosong dianggap dihapus); filter IDS memakai token `target=<nama> ` bukan substring
- `core/logs.py` — mencatat jumlah entri yang pernah ditulis (`_written`) untuk mendeteksi penghapusan log secara benar
- `core/filesystem.py` dan `core/vfs.py` — `ls` di `/` target `gov-id-01` selalu "not a directory", `cd /var/log` dan `cd /home/admin` gagal, `cd ..` tidak berfungsi, direktori kosong tidak bisa dimasuki, `leaks/` tidak menampilkan file; loader sekarang menerima format flat, nested, dan spec
- `core/admin_ai.py` — `patrol()` tidak lagi memutus sesi yang tidak ada (pesan "terminating session" saat tidak terhubung)
- `core/engine.py` — saat terputus (blue team / admin) `cwd`, node, dan user ikut di-reset; sebelumnya `cwd` basi membuat filesystem lokal tidak bisa dipakai
- `core/stealth.py` — `lay-low` bekerja saat tidak terhubung dan selalu membersihkan counter-hack; sebelumnya setelah diputus status counter-hack tidak bisa dihapus sehingga peringatan dan jeda muncul selamanya
- `core/pivot.py` — pivot mengganti node aktif, bukan `current_target`; sebelumnya setelah pivot pemain terdampar di "target" tanpa data jaringan, user, dan filesystem
- `core/persistence.py` — `reconnect` bekerja setelah sesi terputus (memakai target terakhir); sebelumnya mustahil karena target sudah `None`; `except:` telanjang diganti penanganan spesifik; file persistence parsial tidak lagi `KeyError`
- `core/war.py` — `contest` tanpa faksi tidak lagi crash (`my.upper()` pada `None`)
- `core/status.py` — "Nodes owned" tidak lagi menghitung node tanpa owner saat faksi kosong; tidak crash pada data jaringan rusak
- `core/faction.py` — profil rusak tidak crash; pembatalan pemilihan faksi mengakhiri game dengan rapi (sebelumnya lanjut dengan faksi kosong)
- `core/player.py` — `load()` menggabungkan default dan tahan file rusak; `add_trace()` tidak `KeyError`
- `core/crack.py` — password `admin` (`admin123`) ternyata tidak ada di wordlist sehingga `ssh admin` mustahil; IDS mencatat target yang di-crack, bukan target aktif
- `core/exploit.py` — IDS `exploit chain initiated` dicatat pada target yang diserang
- `core/net/github_sync.py` — nama file report memakai `hashlib` (`hash()` Python berubah tiap proses); ukuran download dibatasi 1 MB; sertifikat `certifi` dipakai bila tersedia (diperlukan di Android)
- `core/net/sync.py` — `sync` berulang tidak lagi menggandakan `rep_avg`; riwayat job diambil dari `jobs_done.json`
- `blacknet.py` — `Ctrl+C` saat setup lalu memilih tidak keluar tidak lagi melompati pemilihan alias/faksi; `Ctrl+D` / EOF tidak lagi traceback; command tanpa argumen (`exploit`, `pivot`, `persist`) menampilkan `usage:` bukan "command not found"; error internal pada satu command tidak menutup game
- `core/man.py` — contoh `crack ssh` dan "SUPPORTED SERVICES" tidak sesuai sintaksis; diganti `crack <target> <user>`
- `core/apropos.py` — hapus import tidak terpakai

### Security
- `core/crack.py` — nama target divalidasi (`[A-Za-z0-9._-]`, tanpa `..`) sebelum dipakai membentuk path file
- Semua penulisan JSON bersifat atomik (file sementara + `os.replace`); semua `open()` memakai `with` dan encoding UTF-8
- `pull` membatasi ukuran respons dan hasilnya hanya disimpan sebagai cache, tidak dieksekusi

### Removed
- `core/take.py`, `core/network.py` — masih ada di repo meski dicatat dihapus di v1.0.4; tidak diimpor di mana pun
- `core/net/jobs.py` — duplikat `core/jobs.py` yang tidak diimpor di mana pun

---

## [v1.0.4] - 2026-08-13

### Fixed
- `core/pivot.py` — pivot sekarang mengakses `net["nodes"][host]` bukan `net[host]` yang salah format
- `core/net/protocol.py` — `pack()` sekarang menerima dict player bukan module langsung
- `core/net/sync.py` — `sync()` memanggil `player.load()` sebelum passing ke `pack()`
- `core/net/github_sync.py` — `push_report()` tidak lagi mengakses `player.alias` / `player.rep` sebagai atribut module; sekarang pakai `player.load()`; tambah error handling pada `pull_world()`
- `core/logs.py` — standardisasi key log dari `"system.log"` menjadi `"sys.log"` agar konsisten dengan `forensics.py` dan `persistence.py`; ganti `open()` dengan `with open()`
- `core/forensics.py` — IDS log sekarang dibaca dari `data/ids.log` (flat file) bukan dari JSON target log yang tidak pernah berisi IDS events; fix key `"sys.log"` vs `"system.log"`; fix `"ssh_key"` menjadi `"backdoor"` di deteksi persistence
- `core/admin_ai.py` — gunakan `p.get("trace", 0)` untuk menghindari KeyError
- `core/exploit.py` — hapus no-op `if not engine.current_target: engine.current_target = None`; tambah error handling saat buka `targets.json`
- `core/jobs.py` — `init()` sekarang dipanggil otomatis oleh semua fungsi publik; `complete()` menggunakan `.get()` agar tidak crash jika field kosong
- `core/privilage.py` — hapus hardcoded password `admin123`; verifikasi password lewat `users.json`; tambah guard untuk target tidak ada
- `core/vfs.py` — typo "Oficial" diperbaiki menjadi "Official"
- `core/war.py` — tambah error handling pada `json.load`; gunakan `with open()` di `save_net()`
- `blacknet.py` — `patrol()` sekarang dipanggil di setiap iterasi loop utama; import `netmap` dari `core.netmap` bukan `core.network`; tambah command `sudo`

### Added
- `WORLD_SPEC.md` — dokumentasi spesifikasi world/target, tersedia di root sesuai link di README
- `JOBS_SPEC.md` — dokumentasi spesifikasi sistem job, tersedia di root sesuai link di README
- `data/jobs.json` — diisi dengan 4 job awal (JOB-001 s/d JOB-004) lengkap dengan field `title`, `target`, `objective`, `difficulty`
- `data/network_gov-id-01.json` — perbaikan format: hapus entri lama format flat, semua node sekarang di dalam `nodes{}` dengan field `trust`; tambah node `internal-db`
- Command `sudo <password>` ditambahkan ke main loop
- `.gitignore` diperluas: tambah `__pycache__`, `*.pyc`, `data/logs_*.json`, `data/persist_*.json`, `data/creds_*.json`, `data/jobs_taken.json`, `data/jobs_done.json`, `data/world_cache.json`, `data/reports/`, `data/player.json`, `data/profile.json`

### Removed
- `core/take.py` — dead code (duplikat fungsi dari `core/jobs.py`), tidak pernah diimport
- `core/network.py` — duplikat dari `core/netmap.py` yang lebih lengkap; semua import dialihkan ke `core.netmap`

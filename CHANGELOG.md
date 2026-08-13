# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning.

## [Unreleased]

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

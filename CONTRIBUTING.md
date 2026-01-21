# 🤝 Contributing to BLACKNET

Terima kasih sudah tertarik berkontribusi ke **BLACKNET** 🎯
Project ini adalah **terminal-based hacking simulation** untuk edukasi keamanan siber.

Semua kontribusi **sangat dihargai**, baik berupa:
- fitur baru
- perbaikan bug
- peningkatan dokumentasi
- world / job content

---

## 📌 RULES & PHILOSOPHY

### ⚠️ IMPORTANT
BLACKNET adalah **SIMULASI**.
❌ Jangan menambahkan:
- exploit nyata
- payload berbahaya
- koneksi ke sistem real
- malware atau backdoor sungguhan

Semua aksi **harus berbasis simulasi dan file JSON lokal**.

---

## 🧩 WHAT YOU CAN CONTRIBUTE

### 1️⃣ Code / Features
Contoh:
- command baru (`scan`, `loot`, `deface`)
- sistem IDS / firewall
- AI blue team enhancement
- stealth / cooldown mechanics
- UI ASCII & animasi terminal

📁 Lokasi utama:
core/

---

### 2️⃣ World Data (Paling Disarankan)
Kontribusi **tanpa coding berat**.

#### 📌 Target baru
Tambahkan **SATU target** dengan 3 file:
Folder data/
- network_*.json
- users_*.json
- fs_*.json

Contoh:
- network_gov-id-01.json
- users_gov-id-01.json
- fs_gov-id-01.json
⚠️ Jangan mengubah target existing tanpa diskusi.

---

### 3️⃣ Community Jobs
Tambah job baru ke:
Folder data/jobs.json
Format:
```json
{
  "id": "job-004",
  "title": "Compromise Internal Router",
  "target": "gov-id-01",
  "objective": "Capture router1 node",
  "reward": 500,
  "difficulty": "HARD"
}
```
📌 Tambahkan saja, jangan hapus job lama.

---

### 4️⃣ Documentation
Dokumentasi sama pentingnya dengan code
- README.md
- CONTRIBUTING.md
- docs/
- help / man page

---

### 🧪 TESTING RULES
Sebelum submit PR(Pull Request):
- Jalankan project lokal
- Pastikan tidak error saat startup
- Pastikan command baru tidak crash
- Cek TRACE & blue team response

Contoh test cepat:
```
python3 blacknet.py
exploit alpha
netmap
contest router1
```

---

### 🧼 CODING STYLE
- Python 3.8+
- Simpel & readable
- Hindari dependensi eksternal
- Gunakan fungsi modular
- Jangan hardcode path absolute

---

### 🌍 GITHUB WORKFLOW
1. Fork repository
2. Buat branch baru
contoh:
```git checkout -b example/my-example```
atau:
```git checkout -b example```
3. Commit dengan pesan jelas
contoh:
git commit -m "add new network target gov-id-01"
4. Push & buat Pull Request

---

### ❌ DO NOT COMMIT
🚫 Jangan commit file ini:
- `logs_*.json`
- `jobs_taken.json`
- `jobs_done.json`
- `persist_*.json`
- `player.json`
File tersebut otomatis dibuat runtime.

---

### 🛡️ SECURITY & ETHICS
Jika kamu menemukan:
- celah logic
- exploit tidak disengaja
- perilaku berbahaya
Laporkan via issue, jangan dipublikasikan sebagai exploit nyata.

---

### ❤️ FINAL NOTES
BLACKNET dibangun untuk:
- belajar offensive & defensive security
- memahami forensics & detection
- bermain dengan konsep cyber warfare

Kontribusi kamu membantu project ini tumbuh 🚀

Terima kasih!

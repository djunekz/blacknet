# 🧾 BLACKNET Job System Specification

Dokumen ini menjelaskan **sistem job komunitas di BLACKNET**:
- bagaimana job dibuat
- bagaimana job dibagikan
- bagaimana player mengambil & menyelesaikan job
- bagaimana sinkronisasi via GitHub bekerja

---

## 🧠 KONSEP DASAR JOB

Job di BLACKNET adalah **misi asinkron berbasis file JSON**  
yang **dibagikan via GitHub**, bukan server realtime.

📌 Artinya:
- Developer **mempublish job**
- Player **mengambil job**
- Progress & hasil **lokal**
- Tidak ada konflik antar player

---

## 📁 STRUKTUR FILE JOB

### 📌 File yang di-commit oleh developer
```text
data/
  └── jobs.json
```
### 📌 File lokal (otomatis, JANGAN di-commit)
```text
data/ 
  ├── jobs_taken.json
  └── jobs_done.json
```

---

## 1️⃣ jobs.json (SHARED / GITHUB)

File ini berisi **daftar job global** yang tersedia untuk semua player.

### Contoh:
```json
[
  {
    "id": "JOB-001",
    "title": "Infiltrate Gov Router",
    "target": "gov-id-01",
    "objective": "capture router1",
    "reward": {
      "credits": 300,
      "rep": 2
    },
    "difficulty": "medium"
  },
  {
    "id": "JOB-002",
    "title": "Persistence Deployment",
    "target": "corp-01",
    "objective": "install backdoor",
    "reward": {
      "credits": 200,
      "rep": 1
    },
    "difficulty": "easy"
  }
]
```
Field penting:
| Field      | Deskripsi            |
|:-----------|:---------------------|
| id         | ID unik job          |
| title      | Judul job            |
| target     | Target world         |
| objective  | Goal deskriptif      |
| reward     | Hadiah               |
| difficulty | easy / medium / hard |
📌 Developer hanya menambah job ke file ini lalu commit & push.

---

## 2️⃣ jobs_taken.json (LOKAL PLAYER)
File ini dibuat otomatis saat player menjalankan `take <job_id>`.
Contoh:
```json
{
  "JOB-001": {
    "taken_at": "2026-01-20T13:22:11",
    "status": "in_progress"
  }
}
```
📌 Fungsi:
- Mencegah player mengambil job yang sama dua kali
- Menyimpan status job aktif

❌ Tidak pernah / jangan di-push ke GitHub

---

## 3️⃣ jobs_done.json (LOKAL PLAYER)
Dibuat otomatis saat job berhasil diselesaikan.
Contoh:
```json
{
  "JOB-001": {
    "completed_at": "2026-01-20T14:01:55",
    "reward": {
      "credits": 300,
      "rep": 2
    }
  }
}
```
📌 Digunakan untuk:
- reward player
- histori job
- reputasi

❌ Tidak pernah / jangan di-push ke GitHub

---

## 🔄 ALUR JOB (STEP BY STEP)

###1️⃣ Developer
- Edit data/jobs.json
- Tambahkan job baru
- git commit && git push

###2️⃣ Player
- `sync`
- `pull`
- `jobs`

###3️⃣ Player ambil job
- `take JOB-<id_job>` misal `take JOB-001`

###➡️ Job masuk
- Otomatis file **jobs_taken.json** muncul
- Job masuk ke file **jobs_taken.json**

###4️⃣ Player menyelesaikan objective
Contoh:
```text
exploit gov-id-01
contest router1
```
Game mengecek objective → SUCCESS

###5️⃣ Job selesai
- Job otomatis dipindahkan ke **jobs_done.json**
- Reward ditambahkan ke **player.json**
- Reputasi naik

---

##❓ FAQ PENTING
###❓ Apakah job bisa habis?
➡️ TIDAK
Setiap player:
- punya progress sendiri
- job tidak “diklaim” global

###❓ Kalau mau bikin job baru?
➡️ Cukup tambahkan ke jobs.json, lalu commit.
❌ Tidak perlu hapus job lama
❌ Tidak perlu reset apa pun

###❓ Apakah jobs.json di-update atau ditambah?
➡️ Ditambah (append/otomatis)
Bukan diganti, bukan dihapus.

---

##🔐 KEAMANAN & FAIRNESS

- Tidak ada leaderboard global
- Tidak ada race condition
- Tidak ada cheating via push job selesai

BLACKNET fokus ke:
- simulasi
- pembelajaran
- roleplay

---

##🧩 INTEGRASI DENGAN SISTEM LAIN
Job bisa melibatkan:
- exploit
- war / contest
- persistence
- network pivot
Objective bersifat deskriptif, bukan script-driven.

##🎯 TUJUAN SISTEM JOB
- Memberi arah gameplay
- Mendorong eksplorasi world
- Menyatukan komunitas
Job = cerita
World = panggung
Player = aktor

##✅ CHECKLIST DEVELOPER JOB
- [ ] ID unik
- [ ] Target valid
- [ ] Objective jelas
- [ ] Reward seimbang
- [ ] Tidak pakai data nyata

---

#BLACKNET Job System
📦 GitHub-powered
🧠 Asynchronous
⚔️ Player-driven

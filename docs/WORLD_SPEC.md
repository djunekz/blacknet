# 🌐 BLACKNET World Specification

Dokumen ini menjelaskan **struktur world / target** di BLACKNET, termasuk:
- network map
- user accounts
- filesystem
- lifecycle data

World di BLACKNET **berbasis file JSON** dan **shared via GitHub**.

---

## 🧠 KONSEP WORLD

Satu **world target** = satu organisasi / jaringan simulasi.

Contoh target:
- `alpha`
- `corp-01`
- `gov-id-01`

Setiap target terdiri dari **3 file utama**:
```text
data/ 
  ├── network_.json 
  ├── users_.json 
  └── fs_.json
```
---

## 1️⃣ network_<target>.json

Mewakili **topologi jaringan internal**.

### Contoh:
```json
{
  "name": "Gov Indonesia Internal Network",
  "nodes": {
    "router1": {
      "type": "router",
      "status": "locked",
      "owner": null,
      "links": ["server1", "db1"]
    },
    "server1": {
      "type": "host",
      "status": "open",
      "owner": null,
      "links": ["router1"]
    }
  }
}
```
Field:
|Key     | Deskripsi                              |
|:-------|:---------------------------------------|
|type    | router, subnet, host                   |
|status  | locked, open, compromised, monitored   |
|owner   | red, blue, null                        |
|links   | node yang terhubung                    |

📌 Digunakan oleh:
- `netmap`
- `pivot` (mengganti node aktif, target tetap sama)
- `contest`

---

## 2️⃣ users_.json
Mewakili akun user di sistem target.
Contoh:
```json
{
  "root": {
    "password": "toor",
    "role": "root"
  },
  "admin": {
    "password": "admin123",
    "role": "user"
  },
  "guest": {
    "password": "guest",
    "role": "user"
  }
}
```
📌 Password setiap user harus ada di `data/wordlist.txt`
agar bisa di-`crack`.

📌 Digunakan oleh:
- `ssh`
- `crack`
- `privilege escalation`
- `forensic analysis`

---

## 3️⃣ fs_.json
Mewakili filesystem virtual.
Contoh:
```json
{
  "/": {
    "type": "dir",
    "children": {
      "etc": {
        "type": "dir",
        "children": {
          "passwd": {
            "type": "file",
            "content": "root:x:0:0"
          }
        }
      }
    }
  }
}
```
Loader filesystem menerima tiga bentuk dan menggabungkannya:
- format di atas (`type` / `children`)
- flat: key berupa path (`"/etc"`), value berupa isi direktori
- nested: direktori berisi direktori lain sebagai dict

Nilai string dianggap file, dict dianggap direktori, list nama dianggap
direktori kosong.

📌 Digunakan oleh:
- `ls`
- `cd`
- `cat`
- `persistence simulation`

---

## 🔄 FILE RUNTIME (OTOMATIS)
File berikut **TIDAK DI-COMMIT** ke GitHub,
karena dibuat otomatis saat game berjalan:
```text
data/
├── logs_<target>.json
├── persist_<target>.json
├── jobs_taken.json
├── jobs_done.json
├── player.json
```
📌 File ini bersifat lokal player.

---

## 🌍 SHARED WORLD VIA GITHUB
Cara kerja:
- Developer menambah world baru
- Commit file:
  - **network_new.json**
  - **users_new.json**
  - **fs_new.json**
- Player menjalankan:
  - `sync`
  - `pull`
- World baru tersedia di game

❌ World tidak diupdate secara realtime
❌ Tidak ada merge state antar player

---

## ⚔️ FACTION & WAR
- Node punya field owner
- contest <node> mengubah owner
- Ownership tersimpan di network_.json lokal
- Tidak mempengaruhi repo GitHub

---

## 🛡️ FORENSICS & DETECTION
World menyediakan data untuk:
- auth log
- pivot log
- persistence detection
- blue team response
Semakin kompleks world → semakin realistis forensics.

---

# ⚠️ RULES UNTUK CONTRIBUTOR
### ✅ BOLEH:
- Tambah target baru
- Tambah node baru
- Tambah user / file palsu
### ❌ JANGAN:
- Ubah world existing tanpa diskusi
- Tambah data nyata
- Tambah kredensial real

---

## ✅ CHECKLIST WORLD BARU
- [ ] network_.json
- [ ] users_.json
- [ ] fs_.json
- [ ] node saling terhubung
- [ ] minimal 1 router
- [ ] tidak error saat netmap

---

## 🎯 GOAL
World BLACKNET dibuat untuk:
- belajar cyber attack chain
- memahami detection
- simulasi faction warfare

Semakin rapi world → semakin seru gameplay 🔥

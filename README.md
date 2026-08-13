# BLACKNET
### Terminal-Based Hacker Simulation Game (Termux / Linux)

BLACKNET adalah **game simulasi hacking berbasis terminal**
yang dirancang **realistis**, dan **tanpa gimmick**.

Semua interaksi dilakukan lewat **command line**,
seolah-olah kamu benar-benar berada di sebuah mesin Linux underground.

---

## OPEN CONTRIBUTOR

Terbuka untuk berkontribusi / berkolaborasi supaya game ini berkembang lebih baik lagi.

Sebelum mengajukan permintaan contributor, silahkan baca:
- Sistem Kontribusi [CONTRIBUTING](CONTRIBUTING.md)
- Sistem Network/Target [Sistem Network](docs/WORLD_SPEC.md)
- Sistem Misi/Quest [Sistem Misi](docs/JOB_SPEC.md)

![CodeQL](https://github.com/djunekz/blacknet/actions/workflows/codeql.yml/badge.svg)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen)
![Auto Release](https://github.com/djunekz/blacknet/actions/workflows/release.yml/badge.svg)
[![Downloads](https://img.shields.io/github/downloads/djunekz/blacknet/total?style=for-the-badge&logo=github)](https://github.com/djunekz/blacknet/releases)

> ⚠️ **INI GAME / SIMULASI**<br>
> Tidak ada hacking nyata.<br>
> Tidak terhubung ke sistem nyata.

---

## FILOSOFI GAME

BLACKNET dibuat untuk:
- Simulasi **attack chain nyata**
- Memahami **forensics & detection**
- Merasakan **tekanan stealth**
- faction warfare berbasis network

Tidak ada:
- Level
- XP bar
- Skill tree

Yang ada:
- TRACE (deteksi)
- risiko
- konsekuensi

---

## FITUR UTAMA

### Core Simulation
- `exploit` (multi-stage attack)
- `ssh`, `crack`
- filesystem virtual (`ls`, `cd`, `cat`)
- privilege escalation

### Network & Lateral Movement
- internal network map (`netmap`)
- pivot antar node
- status node (locked / compromised / monitored)

### Faction Warfare
- RED vs BLUE
- contest node ownership
- persistent network state
- visual ASCII war animation

### Blue Team & Forensics
- log analysis
- IOC detection
- response escalation
- counter-hack

### Community Job System
- job berbasis GitHub
- asynchronous (tidak realtime)
- shared world, local progress

### Terminal UI
- ASCII banner & splash
- loading animation
- blinking war effects
- status bar

---

## STRUKTUR PROYEK
```text
blacknet/
├── blacknet.py
├── core/
│   ├── exploit.py
│   ├── network.py
│   ├── war.py
│   ├── blueteam.py
│   ├── forensics.py
│   ├── player.py
│   ├── ui.py
│   ├── help.py
│   └── man.py
├── data/
│   ├── jobs.json < Jobs Engine
│   ├── network_*.json < World Engine
│   ├── users_*.json
│   └── fs_*.json
└── docs/
    ├── WORLD_SPEC.md
    └── JOB_SPEC.md
```

---

## CARA MENJALANKAN

### Clone repo
```bash
git clone https://github.com/USERNAME/blacknet.git
cd blacknet
```
### Jalankan
```bash
python3 blacknet.py
```

---

## FEATURES

### Offensive Operations
- Multi-stage exploit simulation
- Brute-force (`crack`) service authentication
- SSH-style remote login
- Privilege escalation logic
- Lateral movement (`pivot`)

### Blue Team & Forensics
- Forensic analysis engine
- IOC (Indicator of Compromise) detection
- TRACE-based detection system
- Automated blue team response
- Counter-hack & access restriction

### Network Simulation
- Internal network mapping (`netmap`)
- Node-based infrastructure
- Trust & ownership system
- Per-target network topology

### Faction Warfare
- Persistent faction system (RED / BLUE)
- Node contest & control
- Network-wide war mechanics
- Ownership stored in shared world data

### Persistence
- Backdoor installation
- Cron-based persistence
- Service-based persistence
- Reconnect without re-exploitation

### GitHub-Based Shared World
- Shared jobs via `jobs.json`
- Shared targets & networks
- World sync (pull / push)
- Local player progress isolation

---

## CORE CONCEPTS

### TRACE SYSTEM
TRACE menunjukkan tingkat keterdeteksian pemain.

| TRACE | Status |
|-----|------|
| 0–2 | LOW |
| 3–5 | MEDIUM |
| 6–8 | HIGH |
| 9+  | CRITICAL (counter-hack) |

TRACE meningkat akibat:
- exploit
- crack
- pivot
- contest
- persistence install

---

### FORENSICS
Blue team menganalisis:
- auth logs
- privilege escalation
- lateral movement
- persistence artifacts

Hasil analisis menentukan respons otomatis.

---

### FACTION WAR
- Setiap node punya owner
- Node bisa dikontes dengan `contest <node>`
- Node yang sudah dikuasai tidak bisa dikontes ulang
- War meningkatkan TRACE secara signifikan

---

## GITHUB-BASED SHARED WORLD

BLACKNET menggunakan **GitHub sebagai shared world backend**.

### Developer / Contributor:
- Update `jobs.json` → commit & push
- Tambah target baru:
  - `network_<target>.json`
  - `users_<target>.json`
  - `fs_<target>.json`

### Player:
- `pull` → sinkronisasi world
- Progress bersifat **lokal**
- Tidak mempengaruhi world repository

---

## COMMAND OVERVIEW
- `exploit <target>`
- `ls` / `cd` / `cat`
- `ssh <user> <host>`
- `crack <service>`
- `netmap`
- `pivot <node>`
- `contest <node>`
- `jobs`
- `take <job_id>`
- `sync`
- `help`
- `man <command>`
- `exit`

### Core
- exploit
- ls / cd / cat
- ssh
- crack

### Network
- netmap
- pivot

### War / Faction
- contest

### Persistence
- persist
- backdoor
- persist
- cron
- persist
- service
- reconnect

### Community
- jobs
- take <job_id>
- sync
- pull
- push

### Help
- help
- man

---

## Compatible with
- Linux
- Termux (Android)
- macOS

---

## EXTENSIBILITY
BLACKNET dirancang modular:
- Tambah command baru di core/
- Tambah target via file JSON
- Tambah job via jobs.json
- Mudah dikembangkan ke multiplayer / server mode

## LICENSE
Educational & experimental use only.<br>
Do not use this project to perform real-world attacks.

## AUTHOR
Official Developed by [djunekz](https://github.com/djunekz)<br>
Terminal-first • Cybersecurity Simulation • Faction Warfare

#!/usr/bin/env bash
set -euo pipefail

GAME_NAME="blacknet"
REPO_URL="https://github.com/djunekz/blacknet"
REPO_BRANCH="main"
RAW_BASE="https://raw.githubusercontent.com/djunekz/blacknet/$REPO_BRANCH"
API_LATEST="https://api.github.com/repos/djunekz/blacknet/releases/latest"

R='\033[31m' G='\033[32m' Y='\033[33m' C='\033[36m' B='\033[1m' N='\033[0m'

_step() { echo -e "${G}[+]${N} $*"; }
_info() { echo -e "${C}[*]${N} $*"; }
_warn() { echo -e "${Y}[!]${N} $*"; }
_fail() { echo -e "${R}[✖]${N} $*"; exit 1; }
_ok()   { echo -e "${G}[✔]${N} $*"; }

_detect_env() {
    if [[ -n "${TERMUX_VERSION:-}" ]] || [[ "${HOME:-}" == *"com.termux"* ]] || [[ -d "/data/data/com.termux" ]]; then
        PLATFORM="termux"
        INSTALL_DIR="$HOME/.local/share/$GAME_NAME"
        BIN_DIR="${PREFIX}/bin"
    elif [[ "${OSTYPE:-}" == "darwin"* ]]; then
        PLATFORM="macos"
        INSTALL_DIR="$HOME/.local/share/$GAME_NAME"
        BIN_DIR="$HOME/.local/bin"
    else
        PLATFORM="linux"
        INSTALL_DIR="$HOME/.local/share/$GAME_NAME"
        BIN_DIR="$HOME/.local/bin"
    fi

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PY="$(command -v python3 2>/dev/null || echo python3)"
}

_check_install() {
    if [[ ! -d "$INSTALL_DIR" ]]; then
        _fail "BLACKNET belum terinstall di $INSTALL_DIR\n  Jalankan install.sh dulu."
    fi
    _step "Instalasi ditemukan: $INSTALL_DIR"
}

_backup_data() {
    BACKUP_DIR="$HOME/.blacknet_backup_$(date +%Y%m%d_%H%M%S)"
    if [[ -d "$INSTALL_DIR/data" ]]; then
        mkdir -p "$BACKUP_DIR"
        cp -r "$INSTALL_DIR/data" "$BACKUP_DIR/"
        _step "Data player di-backup ke: $BACKUP_DIR"
    fi
}

_detect_downloader() {
    if command -v curl &>/dev/null; then
        DL="curl"
    elif command -v wget &>/dev/null; then
        DL="wget"
    else
        _fail "Butuh curl atau wget untuk update.\n  Termux: pkg install curl\n  Linux : sudo apt install curl"
    fi
    _step "Downloader: $DL"
}

_fetch() {
    local url="$1" dest="$2"
    if [[ "$DL" == "curl" ]]; then
        curl -fsSL --retry 3 --connect-timeout 10 "$url" -o "$dest"
    else
        wget -q --tries=3 --timeout=10 "$url" -O "$dest"
    fi
}

_fetch_text() {
    local url="$1"
    if [[ "$DL" == "curl" ]]; then
        curl -fsSL --retry 3 --connect-timeout 10 "$url"
    else
        wget -q --tries=3 --timeout=10 "$url" -O -
    fi
}

_get_remote_version() {
    REMOTE_VER=""
    local api_out
    if api_out="$(_fetch_text "$API_LATEST" 2>/dev/null)"; then
        REMOTE_VER="$(echo "$api_out" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tag_name',''))" 2>/dev/null || true)"
    fi

    if [[ -z "$REMOTE_VER" ]]; then
        REMOTE_VER="$(_fetch_text "$RAW_BASE/CHANGELOG.md" 2>/dev/null | grep -m1 '## \[' | grep -oP '\[\K[^\]]+' | head -1 || echo "unknown")"
    fi

    echo "$REMOTE_VER"
}

_get_local_version() {
    local cl="$INSTALL_DIR/CHANGELOG.md"
    if [[ -f "$cl" ]]; then
        grep -m1 '## \[' "$cl" | grep -oP '\[\K[^\]]+' | head -1 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

_update_via_git() {
    _info "Menggunakan git pull..."
    local tmp_dir
    tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$tmp_dir"' EXIT

    git clone --depth=1 --branch "$REPO_BRANCH" "$REPO_URL.git" "$tmp_dir" 2>/dev/null \
        || git clone --depth=1 "$REPO_URL.git" "$tmp_dir" 2>/dev/null \
        || return 1

    _copy_update "$tmp_dir"
    return 0
}

_update_via_downloader() {
    _info "Mengunduh file dari GitHub..."

    local tmp_dir
    tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$tmp_dir"' EXIT

    local TARBALL="$tmp_dir/blacknet.tar.gz"
    _fetch "$REPO_URL/archive/refs/heads/$REPO_BRANCH.tar.gz" "$TARBALL" \
        || _fail "Gagal mengunduh. Periksa koneksi internet."

    tar -xzf "$TARBALL" -C "$tmp_dir"
    local extracted
    extracted="$(find "$tmp_dir" -maxdepth 1 -mindepth 1 -type d | head -1)"

    _copy_update "$extracted"
}

_copy_update() {
    local src="$1"

    PRESERVE=("player.json" "profile.json" "jobs_taken.json" "jobs_done.json"
              "world.json" "world_cache.json")

    _safe_cp() {
        local from="$1" to_dir="$2"
        [[ -e "$from" ]] && cp -r "$from" "$to_dir/" || true
    }

    rm -rf "${INSTALL_DIR:?}/core"
    rm -rf "${INSTALL_DIR:?}/docs"
    rm -f  "$INSTALL_DIR/blacknet.py"

    _safe_cp "$src/core"        "$INSTALL_DIR"
    _safe_cp "$src/docs"        "$INSTALL_DIR"
    _safe_cp "$src/blacknet.py" "$INSTALL_DIR"

    for f in install.sh update.sh uninstall.sh CHANGELOG.md CONTRIBUTING.md \
              LICENSE README.md SECURITY.md WORLD_SPEC.md JOBS_SPEC.md; do
        _safe_cp "$src/$f" "$INSTALL_DIR"
    done

    if [[ -d "$src/data" ]]; then
        mkdir -p "$INSTALL_DIR/data"
        for f in "$src/data"/*; do
            [[ -e "$f" ]] || continue
            fname="$(basename "$f")"
            skip=false
            for pf in "${PRESERVE[@]}"; do
                [[ "$fname" == "$pf" ]] && { skip=true; break; }
            done
            [[ "$skip" == "false" ]] && cp "$f" "$INSTALL_DIR/data/" 2>/dev/null || true
        done
    fi

    for sh in "$INSTALL_DIR/install.sh" "$INSTALL_DIR/update.sh" "$INSTALL_DIR/uninstall.sh"; do
        [[ -f "$sh" ]] && chmod +x "$sh"
    done

    _step "File game diperbarui"
}

_rebuild_launcher() {
    local LAUNCHER="$BIN_DIR/$GAME_NAME"
    cat > "$LAUNCHER" <<LAUNCHER
#!/usr/bin/env bash
INSTALL_DIR="$INSTALL_DIR"
PY="$PY"

if [[ "\${1:-}" == "update" ]]; then
    exec bash "\$INSTALL_DIR/update.sh"
fi

cd "\$INSTALL_DIR"
exec "\$PY" blacknet.py "\$@"
LAUNCHER
    chmod +x "$LAUNCHER"
    _step "Launcher diperbarui → $LAUNCHER"
}

main() {
    echo ""
    echo -e "${C}${B}:: BLACKNET Updater ::${N}"
    echo ""

    _detect_env
    _check_install
    _detect_downloader

    echo ""
    local local_ver remote_ver
    local_ver="$(_get_local_version)"
    _info "Versi lokal  : ${B}$local_ver${N}"

    _info "Mengecek versi terbaru..."
    remote_ver="$(_get_remote_version)"
    _info "Versi remote : ${B}$remote_ver${N}"
    echo ""

    if [[ "$local_ver" == "$remote_ver" ]] && [[ "$local_ver" != "unknown" ]]; then
        _ok "Sudah versi terbaru ($local_ver)"
        echo ""
        read -r -p "Tetap force update? [y/N]: " force
        [[ "${force,,}" == "y" ]] || { echo "Update dibatalkan."; exit 0; }
        echo ""
    fi

    _backup_data

    echo ""
    _info "Memulai update..."

    if command -v git &>/dev/null; then
        _update_via_git || {
            _warn "git gagal, mencoba download langsung..."
            _update_via_downloader
        }
    else
        _update_via_downloader
    fi

    _rebuild_launcher

    echo ""
    _ok "${B}Update selesai!${N}"
    echo ""
    echo -e "  Sebelumnya : ${Y}$local_ver${N}"
    echo -e "  Sekarang   : ${G}$remote_ver${N}"
    echo ""
}

main "$@"

#!/usr/bin/env bash
set -euo pipefail

GAME_NAME="blacknet"
REPO_URL="https://github.com/djunekz/blacknet"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

R='\033[31m' G='\033[32m' Y='\033[33m' C='\033[36m' B='\033[1m' N='\033[0m'

_step() { echo -e "${G}[+]${N} $*"; }
_info() { echo -e "${C}[*]${N} $*"; }
_warn() { echo -e "${Y}[!]${N} $*"; }
_fail() { echo -e "${R}[✖]${N} $*"; exit 1; }

_banner() {
    clear 2>/dev/null || true
    echo -e "${C}${B}"
    echo "██████╗ ██╗      █████╗  ██████╗██╗  ██╗███╗   ██╗███████╗████████╗"
    echo "██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝████╗  ██║██╔════╝╚══██╔══╝"
    echo "██████╔╝██║     ███████║██║     █████╔╝ ██╔██╗ ██║█████╗     ██║   "
    echo "██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║╚██╗██║██╔══╝     ██║   "
    echo "██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██║ ╚████║███████╗   ██║   "
    echo "╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝  "
    echo -e "${N}"
    echo -e "${B}  Installer${N}  |  $REPO_URL"
    echo ""
}

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
}

_check_python() {
    if ! command -v python3 &>/dev/null; then
        _fail "Python 3 tidak ditemukan. Install dulu:\n  Termux : pkg install python\n  Linux  : sudo apt install python3\n  macOS  : brew install python3"
    fi

    PY="$(command -v python3)"
    VER="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    MAJOR="${VER%%.*}"; MINOR="${VER##*.}"

    if [[ "$MAJOR" -lt 3 ]] || { [[ "$MAJOR" -eq 3 ]] && [[ "$MINOR" -lt 8 ]]; }; then
        _fail "Butuh Python 3.8+. Ditemukan: $VER"
    fi

    _step "Python $VER → $PY"
}

_install_files() {
    _info "Menginstall ke: ${B}$INSTALL_DIR${N}"

    if [[ -d "$INSTALL_DIR" ]]; then
        _warn "Instalasi lama ditemukan — menimpa file game..."
        rm -rf "${INSTALL_DIR:?}/core"
        rm -rf "${INSTALL_DIR:?}/docs"
        rm -f  "$INSTALL_DIR/blacknet.py" \
               "$INSTALL_DIR/install.sh"  \
               "$INSTALL_DIR/uninstall.sh"\
               "$INSTALL_DIR/update.sh"   \
               "$INSTALL_DIR/CHANGELOG.md"\
               "$INSTALL_DIR/CONTRIBUTING.md" \
               "$INSTALL_DIR/README.md"   \
               "$INSTALL_DIR/SECURITY.md" \
               "$INSTALL_DIR/LICENSE"     \
               "$INSTALL_DIR/WORLD_SPEC.md" \
               "$INSTALL_DIR/JOBS_SPEC.md"
    fi

    mkdir -p "$INSTALL_DIR" "$BIN_DIR"

    cp -r  "$REPO_DIR/core"         "$INSTALL_DIR/"
    cp -r  "$REPO_DIR/docs"         "$INSTALL_DIR/"
    cp     "$REPO_DIR/blacknet.py"  "$INSTALL_DIR/"
    cp     "$REPO_DIR/install.sh"   "$INSTALL_DIR/"
    cp     "$REPO_DIR/uninstall.sh" "$INSTALL_DIR/"
    cp     "$REPO_DIR/update.sh"    "$INSTALL_DIR/"

    for f in CHANGELOG.md CONTRIBUTING.md LICENSE README.md SECURITY.md WORLD_SPEC.md JOBS_SPEC.md; do
        [[ -f "$REPO_DIR/$f" ]] && cp "$REPO_DIR/$f" "$INSTALL_DIR/" || true
    done

    _install_data

    chmod +x "$INSTALL_DIR/install.sh" \
             "$INSTALL_DIR/uninstall.sh" \
             "$INSTALL_DIR/update.sh"

    _step "File game ter-install"
}

_install_data() {
    LOCAL_FILES=("player.json" "profile.json" "jobs_taken.json" "jobs_done.json"
                 "world.json" "world_cache.json")

    if [[ -d "$INSTALL_DIR/data" ]]; then
        _info "Mempertahankan data player yang sudah ada..."
        for f in "$REPO_DIR/data"/*; do
            [[ -e "$f" ]] || continue
            fname="$(basename "$f")"
            skip=false
            for lf in "${LOCAL_FILES[@]}"; do
                [[ "$fname" == "$lf" ]] && { skip=true; break; }
            done
            [[ "$skip" == "false" ]] && cp "$f" "$INSTALL_DIR/data/" 2>/dev/null || true
        done
    else
        mkdir -p "$INSTALL_DIR/data"
        cp -r "$REPO_DIR/data/"* "$INSTALL_DIR/data/" 2>/dev/null || true
    fi
}

_create_launcher() {
    LAUNCHER="$BIN_DIR/$GAME_NAME"
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
    _step "Launcher → $LAUNCHER"
}

_setup_path() {
    if [[ ":${PATH}:" == *":${BIN_DIR}:"* ]]; then
        _step "$BIN_DIR sudah ada di PATH"
        return
    fi

    _warn "$BIN_DIR belum ada di PATH"

    local rc=""
    [[ -f "$HOME/.zshrc" ]]       && rc="$HOME/.zshrc"
    [[ -z "$rc" && -f "$HOME/.bashrc" ]]      && rc="$HOME/.bashrc"
    [[ -z "$rc" && -f "$HOME/.bash_profile" ]] && rc="$HOME/.bash_profile"
    [[ -z "$rc" && -f "$HOME/.profile" ]]     && rc="$HOME/.profile"

    if [[ -n "$rc" ]]; then
        echo "" >> "$rc"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$rc"
        _step "PATH ditambahkan ke $rc"
        _warn "Jalankan: ${B}source $rc${N}  (atau buka terminal baru)"
    else
        _warn "Tambahkan manual ke shell config kamu:"
        echo "  export PATH=\"\$PATH:$BIN_DIR\""
    fi
}

main() {
    _banner
    _detect_env

    _info "Platform    : ${B}$PLATFORM${N}"
    _info "Install dir : ${B}$INSTALL_DIR${N}"
    _info "Bin dir     : ${B}$BIN_DIR${N}"
    echo ""

    _check_python
    _install_files
    _create_launcher
    _setup_path

    echo ""
    echo -e "${G}${B}✔ Instalasi selesai.${N}"
    echo ""
    echo -e "  Jalankan game  :  ${C}${B}blacknet${N}"
    echo -e "  Update game    :  ${C}${B}blacknet update${N}  atau  ${C}${B}bash update.sh${N}"
    echo -e "  Hapus game     :  ${C}${B}bash uninstall.sh${N}"
    echo ""
}

main "$@"

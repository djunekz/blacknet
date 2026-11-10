#!/usr/bin/env bash
set -euo pipefail

GAME_NAME="blacknet"

R='\033[31m' G='\033[32m' Y='\033[33m' C='\033[36m' B='\033[1m' N='\033[0m'

_step() { echo -e "${G}[+]${N} $*"; }
_info() { echo -e "${C}[*]${N} $*"; }
_warn() { echo -e "${Y}[!]${N} $*"; }
_fail() { echo -e "${R}[✖]${N} $*"; exit 1; }

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

main() {
    echo ""
    echo -e "${R}${B}:: BLACKNET Uninstaller ::${N}"
    echo ""

    _detect_env

    if [[ ! -d "$INSTALL_DIR" ]] && [[ ! -f "$BIN_DIR/$GAME_NAME" ]]; then
        _warn "BLACKNET tidak ditemukan di sistem ini."
        exit 0
    fi

    _info "Platform    : $PLATFORM"
    _info "Install dir : $INSTALL_DIR"
    _info "Launcher    : $BIN_DIR/$GAME_NAME"
    echo ""

    read -r -p "$(echo -e "${Y}Simpan data player sebelum uninstall? [Y/n]: ${N}")" save_data
    save_data="${save_data:-y}"

    BACKUP_DIR=""
    if [[ "${save_data,,}" != "n" ]]; then
        if [[ -d "$INSTALL_DIR/data" ]]; then
            BACKUP_DIR="$HOME/blacknet_save_$(date +%Y%m%d_%H%M%S)"
            mkdir -p "$BACKUP_DIR"
            cp -r "$INSTALL_DIR/data" "$BACKUP_DIR/"
            _step "Data player di-backup ke: ${B}$BACKUP_DIR${N}"
        else
            _info "Tidak ada data player untuk di-backup."
        fi
    else
        _warn "Data player TIDAK disimpan."
    fi

    echo ""
    echo -e "${R}Yang akan dihapus:${N}"
    [[ -d "$INSTALL_DIR" ]]          && echo "  $INSTALL_DIR"
    [[ -f "$BIN_DIR/$GAME_NAME" ]]   && echo "  $BIN_DIR/$GAME_NAME"
    echo ""

    read -r -p "$(echo -e "${R}Yakin ingin uninstall BLACKNET? [y/N]: ${N}")" confirm
    if [[ "${confirm,,}" != "y" ]]; then
        echo "Dibatalkan."
        exit 0
    fi

    echo ""

    if [[ -d "$INSTALL_DIR" ]]; then
        rm -rf "$INSTALL_DIR"
        _step "Dihapus: $INSTALL_DIR"
    fi

    if [[ -f "$BIN_DIR/$GAME_NAME" ]]; then
        rm -f "$BIN_DIR/$GAME_NAME"
        _step "Dihapus: $BIN_DIR/$GAME_NAME"
    fi

    echo ""
    echo -e "${G}${B}✔ BLACKNET berhasil diuninstall.${N}"
    echo ""
    if [[ -n "$BACKUP_DIR" ]]; then
        echo -e "  Data player tersimpan di: ${C}$BACKUP_DIR${N}"
        echo -e "  Untuk reinstall nanti, copy folder data/ ke install dir."
    fi
    echo ""
}

main "$@"

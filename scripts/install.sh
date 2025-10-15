#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

function runUser {
  if [ ! -d ~/.config/systemd/user/ ]; then
    mkdir -p ~/.config/systemd/user/
  else
    rm -rf ~/.config/systemd/user/*
    mkdir -p ~/.config/systemd/user/
  fi
  cp -rL "$SCRIPT_DIR"/../systemd/user/* ~/.config/systemd/user/
}

function runRoot() {
  local SCRIPT_DIR
  SCRIPT_DIR=$1
  if [ ! -d /opt/ink_manager/ ]; then
    mkdir /opt/ink_manager
  else
    rm -rf /opt/ink_manager/
    mkdir /opt/ink_manager/
  fi
  if [ -f /etc/systemd/system/ink.service ]; then
    rm -rf /etc/systemd/system/ink.service
  fi
  cp -rL "$SCRIPT_DIR"/../* /opt/ink_manager/
  cp -L "$SCRIPT_DIR"/../.env /opt/ink_manager/.env
  cp -rL "$SCRIPT_DIR"/../systemd/system/ink.service /etc/systemd/system/ink.service
  cd -L /opt/ink_manager/
  "$HOME"/.local/bin/uv sync
  systemctl daemon-reload
}

function main {
  runUser
  sudo bash -c "$(declare -f runRoot); runRoot $SCRIPT_DIR"
}

main
exit 0

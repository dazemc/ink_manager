#!/usr/bin/env bash

function runUser {
  if [ ! -d ~/.config/systemd/user/ ]; then
    mkdir -p ~/.config/systemd/user/
  else
    rm -rf ~/.config/systemd/user/*
    mkdir -p ~/.config/systemd/user/
  fi

  cp -r ../systemd/user/* ~/.config/systemd/user/
}

function runRoot {
  if [ ! -d /opt/ink_manager/ ]; then
    mkdir /opt/ink_manager
  else
    rm -rf /opt/ink_manager/
    mkdir /opt/ink_manager/
  fi

  cp -r ../* /opt/ink_manager/
  cp ../.env /opt/ink_manager/.env
  cp -r ../systemd/system/ink.service /etc/systemd/system/ink.service
  cd /opt/ink_manager/
  "$HOME"/.local/bin/uv sync
  systemctl daemon-reload
}

function main {
  runUser
  sudo bash -c "$(declare -f runRoot); runRoot"
}

main
exit 0

#!/bin/bash

root_verify() {
	local ROOT_UID=0
	local E_NOTROOT=67
	if [ "$UID" -ne "$ROOT_UID" ]; then
		echo "Для работы сценария требуются права root."
		exit "$E_NOTROOT"
	fi
}

install_build() {
	apt-get install -y software-properties-common
	apt-add-repository -y ppa:ansible/ansible
	apt-get update -y
	apt-get install -y ansible
}

main() {
	root_verify
	install_build
}

main

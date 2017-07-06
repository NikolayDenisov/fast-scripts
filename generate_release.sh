#!/usr/bin/env bash

# Скрипт для сбора коммитов во всех репозиториях для написания релиза
# Проходимся по всем директориям, находим все коммиты за последний месяц
# Удаляем все merges и сортируем по дате

PARENTDIR="$HOME/git_nick/"

get_git_repos() {
  find "$PARENTDIR" -maxdepth 1 -type d | tail -n +2
}

get_commits() {
  local dir
  local reportdir="$HOME/reports"
  local now

  mkdir -p "$reportdir"
  while read dir; do
    cd "$dir" || continue
    git log --since="last month" --pretty=format:'%h,%an,%cd,%s' --date=short | grep -v "Merge branch" >> "$reportdir/report.csv.$$"
    cd - || continue
  done <<< "$(get_git_repos)"
  now="$(date +'%d_%m')"
  sort -t, -k3 "$reportdir/report.csv.$$" > "$reportdir/report_$now.csv"
  rm -f "$reportdir/report.csv.$$"
}

main() {
  get_commits
}

main

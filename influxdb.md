### Установка influxdb 1.1.1 на Raspberry Pi 2 model B

1. Установить пакет apt-transport-https

```
wget http://mirrordirector.raspbian.org/raspbian/pool/main/a/apt/apt-transport-https_1.0.9.8.4_armhf.deb
sudo dpkg -i apt-transport-https_1.0.9.8.4_armhf.deb
```

2. Выполнить запрос

```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add - source /etc/os-release
echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

3. Установить пакет

```
sudo apt-get update && sudo apt-get install influxdb
```

Где хранятся сборки?

https://repos.influxdata.com/

Как узнать свой дситрибутив?
```
cat /etc/*-release
```
Смотри лучше тут:

https://repos.influxdata.com/debian/pool/stable/i/influxdb/

4. Исправить конфиг

```
 grep -v '^ *#' /etc/influxdb/influxdb.conf | grep -vE "(^#|^$)"
[meta]
  dir = "/var/lib/influxdb/meta"
[data]
  dir = "/var/lib/influxdb/data"
  wal-dir = "/var/lib/influxdb/wal"
[admin]
  enabled = true 
  bind-address = ":8083"
[http]
  enabled = true
  bind-address = ":8086"
  auth-enabled = false
```
5. Запустить influxdb
```
sudo service influxdb start
```

### Установка influxdb 1.1.1 на Raspberry Pi 2 model B

1 Установить пакет apt-transport-https

```
wget http://mirrordirector.raspbian.org/raspbian/pool/main/a/apt/apt-transport-https_1.0.9.8.4_armhf.deb
sudo dpkg -i apt-transport-https_1.0.9.8.4_armhf.deb
```

2 Выполинть запрос

```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add - source /etc/os-release
echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

3 Установить пакет

```
sudo apt-get update && sudo apt-get install influxdb
```

Где хранятся сборки?

https://repos.influxdata.com/

Как узнать свой дситрибутив?
```
cat /etc/*-release
```

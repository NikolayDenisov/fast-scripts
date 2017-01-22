### Подсказка по iproute2

#### ip

- Просмотр списка сетевых интерфейсов

```
# ip link list

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 74:d0:2b:34:7d:b3 brd ff:ff:ff:ff:ff:ff
3: wlp6s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN mode DORMANT group default qlen 1000
    link/ether ac:22:0b:93:38:72 brd ff:ff:ff:ff:ff:ff
```
- Просмотр списка IP-адресов

```
ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 74:d0:2b:34:7d:b3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.36/24 brd 192.168.1.255 scope global dynamic enp3s0
       valid_lft 76243sec preferred_lft 76243sec
    inet6 fe80::c40b:6939:ac72:230a/64 scope link
       valid_lft forever preferred_lft forever
3: wlp6s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether ac:22:0b:93:38:72 brd ff:ff:ff:ff:ff:ff
```
   Этот листинг содержит более подробную информацию. Здесь показаны все IP-адреса, и каким интерфейсам они принадлежат. Здесь "inet" соответствует термину "Internet (IPv4)". Существует целый ряд типов сетевых адресов, но нас они пока не интересуют.

  Вы наверняка обратили внимание на слово "qdisc". Оно обозначает дисциплину обработки очереди (Queueing Discipline). Позднее мы коснемся этой темы подробнее.

  - Просмотр списка маршрутов

```
# ip route show
default via 192.168.1.1 dev enp3s0  proto static  metric 100
169.254.0.0/16 dev enp3s0  scope link  metric 1000
192.168.1.0/24 dev enp3s0  proto kernel  scope link  src 192.168.1.36  metric 100
```
Этот листинг достаточно "прозрачен". Первые 3 строки сообщают сведения, которые нами уже обсуждались выше. Последняя строка говорит о том, что внешний мир доступен через 192.168.1.1 -- шлюз, заданный по-умолчанию. То что это шлюз, видно благодаря наличию слова "via" (в переводе с англ. -- "через"). Этот шлюз (с адресом 192.168.1.1) готов перенаправлять наши пакеты в Интернет и возвращать обратно результаты наших запросов.

#### ARP

ARP - Address Resolution Protocol (Протокол Определения Адреса)

- Содержимое ARP-кэша

```
# ip neigh show
```
- Удалить адрес компьютера из кэша

```
ip neigh delete 9.3.76.43 dev eth0
```

#### Правила - база политик маршрутизации

```
# ip rule list
0:	from all lookup local
32766:	from all lookup main
32767:	from all lookup default
```

 В этом листинге приведены приоритеты всех правил. Мы видим, что правила применяются ко всем пакетам (from all). Мы уже видели таблицу 'main', она выводится командой ip route ls , но таблицы 'local' и 'default' для нас новые.

Информация о таблицах маршрутизации

 ```
 # ip route list table local
 # ip route list table main
```

Пример. Создать таблицу мащрутизации для нашего гипотетического соседа, которое будет называться 'John'. Хотя мы можем работать просто с числами, намного проще и понятней если мы определим названия наших таблиц в файле /etc/iproute2/rt_tables.

```
# echo 200 John >> /etc/iproute2/rt_tables
# ip rule add from 10.0.0.10 table John
# ip rule ls
```
Теперь нам нужно лишь сгенерировать таблицу John и очистить кэш маршрутов:

```
# ip route add default via 195.96.98.253 dev ppp2 table John
# ip route flush cache      
```

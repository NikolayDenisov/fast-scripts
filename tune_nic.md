#### NIC Ring Buffers - число буферов для передачи и приёма.
```
ethtool -g eth0

Ring parameters for eth0:
Pre-set maximums:
RX:		4096
RX Mini:	0
RX Jumbo:	0
TX:		4096
Current hardware settings:
RX:		256
RX Mini:	0
RX Jumbo:	0
TX:		256
```
В ситуации когда трафик создается маленькими пакетами то требуется увеличить размеры буферов rx и tx:
```
ethtool -G eth0 rx tx 2048
```

#### Interrupts and Interrupt Handlers
```
egrep “CPU0|eth0” /proc/interrupt

CPU0       CPU1       CPU2       CPU3
...
 45:          0          0          0          0   PCI-MSI-edge      eth0
 46:          0          0          0          0   PCI-MSI-edge      eth0-rx-0
 47:          0          0          0          0   PCI-MSI-edge      eth0-rx-1
 48:          0          0          0          0   PCI-MSI-edge      eth0-rx-2
 49:          0          0          0          0   PCI-MSI-edge      eth0-rx-3
 50:          0          0          0          0   PCI-MSI-edge      eth0-tx-0
 51:          0          0          0          0   PCI-MSI-edge      eth0-tx-1
 52:          0          0          0          0   PCI-MSI-edge      eth0-tx-2
 53:          0          0          0          0   PCI-MSI-edge      eth0-tx-3
```

- Первый столбец — номер прерывания
- CPU0 .. CPUx — счетчик обработанных прерываний
- PCI-MSI-edge — тип прерывания
- Последний столбец — название устройства

Чтобы назначить прерывание на определённое ядро необходимо прописать его номер в файле `/proc/irq/[Номер IRQ]/smp_affinity`:
```
echo [значение smp_affinity] >/proc/irq/[номер IRQ]/smp_affinity
```

#### Отложенные прерывания (softirq) 
````
watch -n1 grep RX /proc/softirq
```
Обработчик аппаратного прерывания запрещает прерывания, выполняет необходимые действия и затем разрешает прерывания. Действия, выполняемые обработчиком, должны занимать как можно меньше процессорного времени. Например, обработчик аппаратного прерывания, являющийся частью драйвера сетевой платы сохраняет пришедший по сети пакет в буфере и завершает свою работу. Всю остальную работу по обработке сетевого пакета, берет на себя программное прерывание. 

#### Networking Tools
- netstat

  Команда netstat умеет показывать сетевые соединения (входящие/исходящие), таблицу маршрутизации, статистику по сетевым    интерфейсам и т.д.
  Она извлекает информацию о сетевой подсистеме из /proc/net/ файловой системы. Эти файлы включают в себя:
```
    /etc/services -- файл трансляции служб
    /proc -- Точка монтирования файловой системы proc, которая предоставляет доступ к информации о состоянии ядра через следующие файлы.
    /proc/net/dev -- информация об устройствах
    /proc/net/raw -- информация о необрабатываемых (raw) сокетах
    /proc/net/tcp -- информация о сокетах TCP
    /proc/net/udp -- информация о сокетах UDP
    /proc/net/igmp -- информация о мультикаст IGMP
    /proc/net/unix -- информация о сокетах домена Unix
    /proc/net/ipx -- информация о сокетах IPX
    /proc/net/ax25 -- информация о сокетах AX25
    /proc/net/appletalk -- информация о сокетах DDP (appletalk)
    /proc/net/nr -- информация о сокетах NET/ROM
    /proc/net/route -- информация об IP-маршрутизации
    /proc/net/ax25_route -- информация об AX25-маршрутизации
    /proc/net/ipx_route -- информация об IPX-маршрутизации
    /proc/net/nr_nodes -- список узлов NET/ROM
    /proc/net/nr_neigh -- соседи NET/ROM
    /proc/net/ip_masquerade -- NAT-соединения
    /proc/net/snmp -- статистика
 
```
- dropwatch

  Мониторинг операций отбрасывания сетевых пакетов данных на уровне ядра ОС

- ip

  Позволяет выполнять настройку сетевой подсистемы и является заменой таких утилит, как ifconfig, route, arp.
  
- ethtool
  
  Отображает или позволяет изменить настройки сетевой карты  

- /proc/net/snmp

  Файл, который отображает данные ASCII, необходимые для IP, ICMP, TCP, UDP и управления информацией базы для snmp агента. Он также отображает в режиме реального времени статистические данные UDP-lite
  
- sysctl
  Rоманда, предназначенная для управления параметрами ядра на лету. Позволяет читать и изменять параметры ядра. Например - такие параметры как размер сегмента разделяемой памяти, ограничение на число запущенных процессов, а также включать функции наподобие маршрутизации.
```
sysctl net.ipv4.tcp_sack
net.ipv4.tcp_sack = 1
```

#### Определение узких мест в сети

Пакеты теряются, когда переполняется RX буффер. Для того чтобы смотреть статистику используйте `ethtool` поле `rx_*_errors`
```
ethtool -S eth1
```
Найте узкое место можно, выполнив проверку следующих уровней:

1. Уровень ПО адаптера

Проверить потери пакетов 
```
ethtool -S ethX
```
2. Уровень драйвер сетевого адаптера

3. Уровень linux kernel, IRQs или SoftIRQs

```
/proc/interrupts
 ИЛИ 
/proc/net/softnet_stat
```
4. Уровень протоколов IP, TCP, или UDP

Используй 
```
netstat -s
```
и смотри счетчики ошибок
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

Чтобы назначить прерывание на определённое ядро необходимо прописать его номер в файле /proc/irq/[Номер IRQ]/smp_affinity:
```
echo [значение smp_affinity] >/proc/irq/[номер IRQ]/smp_affinity
```

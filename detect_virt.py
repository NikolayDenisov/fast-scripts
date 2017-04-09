#!/usr/bin/env python

import os
import os.path

dmi_vendor_table = ["KVM",  "QEMU", "VMware", "VMW", "innotek GmbH", "Xen", "Bochs", "Parallels", "BHYVE"]

def detect_vm_dmi():
    dmi_vendors = ['product_name', 'sys_vendor', 'board_vendor', 'bios_vendor']
    sysfs_dmi_path = "/sys/class/dmi/id/"
    for i in range(len(dmi_vendors)):
        try:
            dmi_file = os.path.join(sysfs_dmi_path, dmi_vendors[i])
            if os.path.exists(dmi_file):
                with open(dmi_file) as f:
                    element = f.read()
                    if element.strip() in dmi_vendor_table:
                        print "Virtualization found in DMI"
        except IOError as err:
            print err.errno

def detect_vm_xen():
    xen_file = '/proc/xen/capabilitie'
    if os.path.exists(xen_file):
        return "Virtualization XEN found ({} exists)".format(xen_file)
    return None

def detect_vm_hypervisor():
    hypervisor = "/sys/hypervisor/type"
    if os.path.exists(hypervisor):
        with open(hypervisor) as f:
            h = f.read()
            "Virtualization {0} found in /sys/hypervisor/type".format(h)
        if h == 'xen':
            return VIRTUALIZATION_XEN
        else:
            return VIRTUALIZATION_VM_OTHER

def detect_vm_uml():
    with open('/proc/cpuinfo') as proc:
        for line in proc:
            if 'vendor_id\t: User Mode Linux':
                print "UML virtualization found in /proc/cpuinfo"
                return VIRTUALIZATION_UML
    return VIRTUALIZATION_NONE

def detect_vm_zvm():
    zvm = '/proc/sysinfo'
    if os.path.exists(zvm):
        with open(hypervisor) as f:
            z = f.read()
            if 'z/VM' in z:
                return VIRTUALIZATION_ZVM
            else:
                return VIRTUALIZATION_KVM
    return VIRTUALIZATION_NONE


def detect_vm_device_tree():
    tree = '/proc/device-tree/hypervisor/compatible'
    if os.path.exists(tree):
        return VIRTUALIZATION_QEMU
    return VIRTUALIZATION_NONE


def detect_vm():
    dmi = detect_vm_dmi()
    r = detect_vm_xen()
    r = detect_vm_hypervisor()
    r = detect_vm_deice_tree()
    r = detect_vm_uml()
    r = detect_vm_zvm()


if __name__ == '__main__':
    detect_vm_dmi()
    detect_vm_xen()

#!/usr/bin/env python
"""
PyUbootImage library for reading u-boot image files
as defined in the official u-boot sources.
"""

import struct
import sys
from enum import Enum


class _Codes(Enum):

    def __str__(self):
        return self.LOOKUP_TABLE[self.value]


# Operating System Codes
class OperatingSystem(_Codes):
    INVALID = 0  # Invalid OS
    OPENBSD = 1  # OpenBSD
    NETBSD = 2  # NetBSD
    FREEBSD = 3  # FreeBSD
    BSD4_4 = 4  # 4.4BSD
    LINUX = 5  # Linux
    SVR4 = 6  # SVR4
    ESIX = 7  # Esix
    SOLARIS = 8  # Solaris
    IRIX = 9  # Irix
    SCO = 10  # SCO
    DELL = 11  # Dell
    NCR = 12  # NCR
    LYNXOS = 13  # LynxOS
    VXWORKS = 14  # VxWorks
    PSOS = 15  # pSOS
    QNX = 16  # QNX
    U_BOOT = 17  # Firmware
    RTEMS = 18  # RTEMS
    ARTOS = 19  # ARTOS
    UNITY = 20  # Unity OS
    INTEGRITY = 21  # INTEGRITY


# Array containing the string with OS Names
# corresponding to the ih_os numeric value
OperatingSystem.LOOKUP_TABLE = [
    'Invalid OS',
    'OpenBSD',
    'NetBSD',
    'FreeBSD',
    '4.4BSD',
    'Linux',
    'SVR4',
    'Esix',
    'Solaris',
    'Irix',
    'SCO',
    'Dell',
    'NCR',
    'LynxOS',
    'VxWorks',
    'pSOS',
    'QNX',
    'Firmware',
    'RTEMS',
    'ARTOS',
    'Unity',
    'INTEGRITY'
]


# CPU Architecture Codes (supported by Linux)
class Architecture(_Codes):
    INVALID = 0  # Invalid CPU
    ALPHA = 1  # Alpha
    ARM = 2  # ARM
    I386 = 3  # Intel x86
    IA64 = 4  # IA64
    MIPS = 5  # MIPS
    MIPS64 = 6  # MIPS 64 Bit
    PPC = 7  # PowerPC
    S390 = 8  # IBM S390
    SH = 9  # SuperH
    SPARC = 10  # Sparc
    SPARC64 = 11  # Sparc 64 Bit
    M68K = 12  # M68K
    NIOS = 13  # Nios-32
    MICROBLAZE = 14  # MicroBlaze
    NIOS2 = 15  # Nios-II
    BLACKFIN = 16  # Blackfin
    AVR32 = 17  # AVR32
    ST200 = 18  # STMicroelectronics ST200


# Array containing the string with Architecture Names
# corresponding to the ih_arch numeric value
Architecture.LOOKUP_TABLE = [
    'Invalid',
    'Alpha',
    'ARM',
    'Intel',
    'IA64',
    'MIPS',
    'MIPS',
    'PowerPC',
    'IBM',
    'SuperH',
    'Sparc',
    'Sparc',
    'M68K',
    'Nios-32',
    'MicroBlaze',
    'Nios-II',
    'Blackfin',
    'AVR32',
    'STMicroelectronics'
]


class Image(_Codes):
    INVALID = 0  # Invalid Image
    STANDALONE = 1  # Standalone Program
    KERNEL = 2  # OS Kernel Image
    RAMDISK = 3  # RAMDisk Image
    MULTI = 4  # Multi-File Image
    FIRMWARE = 5  # Firmware Image
    SCRIPT = 6  # Script file
    FILESYSTEM = 7  # Filesystem Image (any type)
    FLATDT = 8  # Binary Flat Device Tree Blob
    KWBIMAGE = 9  # Kirkwood Boot Image


Image.LOOKUP_TABLE = [
    'Invalid Image',
    'Standalone Program',
    'OS Kernel Image',
    'RAMDisk Image',
    'Multi-File Image',
    'Firmware Image',
    'Script file',
    'Filesystem Image (any type)',
    'Binary Flat Device Tree Blob',
    'Kirkwood Boot Image'
]


# Compression Types
class Compression(_Codes):
    NONE = 0  # No Compression Used
    GZIP = 1  # gzip Compression Used
    BZIP2 = 2  # bzip2 Compression Used
    LZMA = 3  # lzma Compression Used


Compression.LOOKUP_TABLE = ['None', 'gzip', 'bzip2', 'lzma']

IH_COMP_EXT_LOOKUP = ['dat', 'gz', 'bz2', 'lzma']


IH_MAGIC = 0x27051956  # Image Magic Number
IH_NMLEN = 32  # Image Name Length


class uboot_image:
    """Main class of this library containing
    all the header fields and an array of binary images.

    Image Types
     "Standalone Programs" are directly runnable in the environment
        provided by U-Boot; it is expected that (if they behave
        well) you can continue to work in U-Boot after return from
        the Standalone Program.
     "OS Kernel Images" are usually images of some Embedded OS which
        will take over control completely. Usually these programs
        will install their own set of exception handlers, device
        drivers, set up the MMU, etc. - this means, that you cannot
        expect to re-enter U-Boot except by resetting the CPU.
     "RAMDisk Images" are more or less just data blocks, and their
        parameters (address, size) are passed to an OS kernel that is
        being started.
     "Multi-File Images" contain several images, typically an OS
        (Linux) kernel image and one or more data images like
        RAMDisks. This construct is useful for instance when you want
        to boot over the network using BOOTP etc., where the boot
        server provides just a single image file, but you want to get
        for instance an OS kernel and a RAMDisk image.

        "Multi-File Images" start with a list of image sizes, each
        image size (in bytes) specified by an "uint32_t" in network
        byte order. This list is terminated by an "(uint32_t)0".
        Immediately after the terminating 0 follow the images, one by
        one, all aligned on "uint32_t" boundaries (size rounded up to
        a multiple of 4 bytes - except for the last file).

     "Firmware Images" are binary images containing firmware (like
        U-Boot or FPGA images) which usually will be programmed to
        flash memory.

     "Script files" are command sequences that will be executed by
        U-Boot's command interpreter; this feature is especially
        useful when you configure U-Boot to use a real shell (hush)
        as command interpreter (=> Shell Scripts).
    """

    FORMAT = "!7I4B32s"
    SIZE = struct.calcsize(FORMAT)
    FIELDS = [
        "ih_magic", "ih_hcrc", "ih_time", "ih_size", "ih_load", "ih_ep",
        "ih_dcrc", "ih_os", "ih_arch", "ih_type", "ih_comp", "ih_name"
    ]

    def __init__(self):
        """Main constructor that builds a non-initialized object."""
        self.ih_magic = 0  # Image Header Magic Number
        self.ih_hcrc = 0  # Image Header CRC Checksum
        self.ih_time = 0  # Image Creation Timestamp
        self.ih_size = 0  # Image Data Size
        self.ih_load = 0  # Data Load Address
        self.ih_ep = 0  # Entry Point Address
        self.ih_dcrc = 0  # Image Data CRC Checksum
        self.ih_os = 0  # Operating System
        self.ih_arch = 0  # CPU architecture
        self.ih_type = 0  # Image Type
        self.ih_comp = 0  # Compression Type
        self.ih_name = ''  # Image Name
        self.parts = []

    def fill(self, buf):
        """Fill the header only with the values read from buf array."""
        values = struct.unpack_from(self.FORMAT, buf)
        for field, value in zip(self.FIELDS, values):
            setattr(self, field, value)
        self.ih_os = OperatingSystem(self.ih_os)
        self.ih_arch = Architecture(self.ih_arch)
        self.ih_type = Image(self.ih_type)
        self.ih_comp = Compression(self.ih_comp)
        self.ih_name = self.ih_name.rstrip(b'\x00').decode()

    def checkMagic(self):
        """Check if the magic number contained in ih_magic field is correct or not."""
        return self.ih_magic == IH_MAGIC

    def parse(self, buf):
        """Read image header and extract the binary images."""
        self.fill(buf)
        if self.ih_type == Image.MULTI:
            self.parts = self.getMultiParts(buf, self.SIZE)
        else:
            self.parts = [buf[self.SIZE : self.SIZE + self.ih_size]]
        return self

    def os_name(self):
        return str(self.ih_os)

    def arch_name(self):
        return str(self.ih_arch)

    def type_name(self):
        return str(self.ih_type)

    def comp_name(self):
        return str(self.ih_comp)

    def getInfo(self):
        """Return a dictionary with a human-readable version
        of the content of the header."""
        return {
            "MAGIC": self.ih_magic,
            "HCRC": self.ih_hcrc,
            "TIME": self.ih_time,
            "SIZE": self.ih_size,
            "LOAD": self.ih_load,
            "EP": self.ih_ep,
            "DCRC": self.ih_dcrc,
            "OS": self.os_name(),
            "ARCH": self.arch_name(),
            "TYPE": self.type_name(),
            "COMP": self.comp_name(),
            "NAME": self.ih_name,
            "PARTS": len(self.parts)
        }

    def getMultiParts(self, buf, start):
        """Internal method used by parse() to separate binary images."""
        ofs = []
        p = []
        fmt = "!I"
        fmt_size = struct.calcsize(fmt)
        while True:
            val = struct.unpack_from(fmt, buf, start)[0]
            if val == 0:
                break
            start += fmt_size
            ofs.append(val)
        for size in ofs:
            part = buf[start : start + size]
            pad = size % 4
            if pad != 0:
                size += 4 - pad
            start += size
            p.append(part)
        return p


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s path_to_u-boot_image' % sys.argv[0])
        sys.exit(0)
    with open(sys.argv[1], 'rb') as f:
        image_data = f.read()
    image = uboot_image().parse(image_data)
    if not image.checkMagic():
        print("Bad magic number!")
        sys.exit(1)
    print("Found image!\n\t" + "\n\t".join([key.ljust(5) + ": " + str(val) for key, val in image.getInfo().items()]))
    format_string = 'part_%02d.' + IH_COMP_EXT_LOOKUP[image.ih_comp.value]
    for i, part in enumerate(image.parts):
        with open(format_string % i, 'wb') as f:
            f.write(part)

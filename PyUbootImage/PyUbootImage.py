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
    OSE = 22  # OSE
    PLAN9 = 23  # Plan 9
    OPENRTOS = 24  # OpenRTOS
    ARM_TRUSTED_FIRMWARE = 25  # ARM Trusted Firmware
    TEE = 26  # Trusted Execution Environment
    OPENSBI = 27  # RISC-V OpenSBI
    EFI = 28  # EFI Firmware (e.g. GRUB2)


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
    'INTEGRITY',
    "Enea OSE",
    "Plan 9",
    "OpenRTOS",
    "ARM Trusted Firmware",
    "Trusted Execution Environment",
    "RISC-V OpenSBI",
    "EFI Firmware"
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
    SANDBOX = 19  # Sandbox architecture (test only)
    NDS32 = 20  # ANDES Technology - NDS32
    OPENRISC = 21  # OpenRISC 1000
    ARM64 = 22  # ARM64
    ARC = 23  # Synopsys DesignWare ARC
    X86_64 = 24  # AMD x86_64, Intel and Via
    XTENSA = 25  # Xtensa
    RISCV = 26  # RISC-V


# Array containing the string with Architecture Names
# corresponding to the ih_arch numeric value
Architecture.LOOKUP_TABLE = [
    'Invalid',
    'Alpha',
    'ARM',
    'Intel x86',
    'IA64',
    'MIPS',
    'MIPS 64 Bit',
    'PowerPC',
    'IBM S390',
    'SuperH',
    'SPARC',
    'SPARC 64 Bit',
    'M68K',
    'Nios-32',
    'MicroBlaze',
    'Nios-II',
    'Blackfin',
    'AVR32',
    'STMicroelectronics ST200',
    "Sandbox",
    "NDS32",
    "OpenRISC 1000",
    "AArch64",
    "ARC",
    "AMD x86_64",
    "Xtensa",
    "RISC-V"
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
    IMXIMAGE = 10  # Freescale IMXBoot Image
    UBLIMAGE = 11  # Davinci UBL Image
    OMAPIMAGE = 12  # TI OMAP Config Header Image
    AISIMAGE = 13  # TI Davinci AIS Image
    KERNEL_NOLOAD = 14  # OS Kernel Image, can run from any load address
    PBLIMAGE = 15  # Freescale PBL Boot Image
    MXSIMAGE = 16  # Freescale MXSBoot Image
    GPIMAGE = 17  # TI Keystone GPHeader Image
    ATMELIMAGE = 18  # ATMEL ROM bootable Image
    SOCFPGAIMAGE = 19  # Altera SOCFPGA CV/AV Preloader
    X86_SETUP = 20  # x86 setup.bin Image
    LPC32XXIMAGE = 21  # x86 setup.bin Image
    LOADABLE = 22  # A list of typeless images
    RKIMAGE = 23  # Rockchip Boot Image
    RKSD = 24  # Rockchip SD card
    RKSPI = 25  # Rockchip SPI image
    ZYNQIMAGE = 26  # Xilinx Zynq Boot Image
    ZYNQMPIMAGE = 27  # Xilinx ZynqMP Boot Image
    ZYNQMPBIF = 28  # Xilinx ZynqMP Boot Image (bif)
    FPGA = 29  # FPGA Image
    VYBRIDIMAGE = 30  # VYBRID .vyb Image
    TEE = 31  # Trusted Execution Environment OS Image
    FIRMWARE_IVT = 32  # Firmware Image with HABv4 IVT
    PMMC = 33  # TI Power Management Micro-Controller Firmware
    STM32IMAGE = 34  # STMicroelectronics STM32 Image
    SOCFPGAIMAGE_V1 = 35  # Altera SOCFPGA A10 Preloader
    MTKIMAGE = 36  # MediaTek BootROM loadable Image
    IMX8MIMAGE = 37  # Freescale IMX8MBoot Image
    IMX8IMAGE = 38  # Freescale IMX8Boot Image
    COPRO = 39  # Coprocessor Image for remoteproc
    SUNXI_EGON = 40  # Allwinner eGON Boot Image
    SUNXI_TOC0 = 41  # Allwinner TOC0 Boot Image
    FDT_LEGACY = 42  # Binary Flat Device Tree Blob	in a Legacy Image


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
    'Kirkwood Boot Image',
    "Freescale i.MX Boot Image",
    "Davinci UBL Image",
    "TI OMAP SPL With GP CH",
    "Davinci AIS image",
    "Kernel Image (no loading done)",
    "Freescale PBL Boot Image",
    "Freescale MXS Boot Image",
    "TI Keystone SPL Image",
    "ATMEL ROM-Boot Image",
    "Altera SoCFPGA CV/AV preloader",
    "x86 setup.bin",
    "LPC32XX Boot Image",
    "A list of typeless images",
    "Rockchip Boot Image",
    "Rockchip SD Boot Image",
    "Rockchip SPI Boot Image",
    "Xilinx Zynq Boot Image",
    "Xilinx ZynqMP Boot Image",
    "Xilinx ZynqMP Boot Image (bif)",
    "FPGA Image",
    "Vybrid Boot Image",
    "Trusted Execution Environment Image",
    "Firmware with HABv4 IVT",
    "TI Power Management Micro-Controller Firmware",
    "STMicroelectronics STM32 Image",
    "Altera SOCFPGA A10 Preloader",
    "MediaTek BootROM loadable Image",
    "NXP i.MX8M Boot Image",
    "NXP i.MX8 Boot Image",
    "Coprocessor Image",
    "Allwinner eGON Boot Image",
    "Allwinner TOC0 Boot Image",
    "Legacy Image with Flat Device Tree"
]


# Compression Types
class Compression(_Codes):
    NONE = 0  # No Compression Used
    GZIP = 1  # gzip Compression Used
    BZIP2 = 2  # bzip2 Compression Used
    LZMA = 3  # lzma Compression Used
    LZO = 4  # lzo Compression Used
    LZ4 = 5  # lz4 Compression Used
    ZSTD = 6  # zstd Compression Used


Compression.LOOKUP_TABLE = ['None', 'gzip', 'bzip2', 'lzma', "lzo", "lz4", "zstd"]

IH_COMP_EXT_LOOKUP = ['dat', 'gz', 'bz2', 'lzma', "lzo", "lz4", "zst"]


IH_MAGIC = 0x27051956  # Image Magic Number
IH_NMLEN = 32  # Image Name Length


class UBootImage:
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

    @property
    def os_name(self):
        return str(self.ih_os)

    @property
    def arch_name(self):
        return str(self.ih_arch)

    @property
    def type_name(self):
        return str(self.ih_type)

    @property
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
            "OS": self.os_name,
            "ARCH": self.arch_name,
            "TYPE": self.type_name,
            "COMP": self.comp_name,
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
    image = UBootImage().parse(image_data)
    if not image.checkMagic():
        print("Bad magic number!")
        sys.exit(1)
    print("Found image!\n\t" + "\n\t".join([key.ljust(5) + ": " + str(val) for key, val in image.getInfo().items()]))
    format_string = 'part_%02d.' + IH_COMP_EXT_LOOKUP[image.ih_comp.value]
    for i, part in enumerate(image.parts):
        with open(format_string % i, 'wb') as f:
            f.write(part)

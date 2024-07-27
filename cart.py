from struct import unpack

class ROM_Header:
    def __init__(self, data):
        self.entry = data[0:4]
        self.logo = data[4:0x34]
        
        self.title = data[0x34:0x44].decode('ascii').strip('\0')
        self.new_lic_code = unpack(">H", data[0x44:0x46])[0]
        self.sbg_flag = data[0x46]
        self.type = data[0x47]
        self.rom_size = data[0x48]
        self.ram_size = data[0x49]
        self.dest_code = data[0x4A]
        self.lic_code = data[0x4B]
        self.version = data[0x4C]
        self.checksum = data[0x4D]
        self.global_checksum = unpack(">H", data[0x4E:0x50])[0]

class Cart_Context:
    ROM_TYPES = [
    "ROM ONLY",
    "MBC1",
    "MBC1+RAM",
    "MBC1+RAM+BATTERY",
    "0x04 ???",
    "MBC2",
    "MBC2+BATTERY",
    "0x07 ???",
    "ROM+RAM 1",
    "ROM+RAM+BATTERY 1",
    "0x0A ???",
    "MMM01",
    "MMM01+RAM",
    "MMM01+RAM+BATTERY",
    "0x0E ???",
    "MBC3+TIMER+BATTERY",
    "MBC3+TIMER+RAM+BATTERY 2",
    "MBC3",
    "MBC3+RAM 2",
    "MBC3+RAM+BATTERY 2",
    "0x14 ???",
    "0x15 ???",
    "0x16 ???",
    "0x17 ???",
    "0x18 ???",
    "MBC5",
    "MBC5+RAM",
    "MBC5+RAM+BATTERY",
    "MBC5+RUMBLE",
    "MBC5+RUMBLE+RAM",
    "MBC5+RUMBLE+RAM+BATTERY",
    "0x1F ???",
    "MBC6",
    "0x21 ???",
    "MBC7+SENSOR+RUMBLE+RAM+BATTERY",
    ]

    LIC_CODE = {
        0x00: "None", 0x01: "Nintendo R&D1", 0x08: "Capcom", 0x13: "Electronic Arts",
        0x18: "Hudson Soft", 0x19: "b-ai", 0x20: "kss", 0x22: "pow", 0x24: "PCM Complete",
        0x25: "san-x", 0x28: "Kemco Japan", 0x29: "seta", 0x30: "Viacom", 0x31: "Nintendo",
        0x32: "Bandai", 0x33: "Ocean/Acclaim", 0x34: "Konami", 0x35: "Hector", 0x37: "Taito",
        0x38: "Hudson", 0x39: "Banpresto", 0x41: "Ubi Soft", 0x42: "Atlus", 0x44: "Malibu",
        0x46: "angel", 0x47: "Bullet-Proof", 0x49: "irem", 0x50: "Absolute", 0x51: "Acclaim",
        0x52: "Activision", 0x53: "American sammy", 0x54: "Konami", 0x55: "Hi tech entertainment",
        0x56: "LJN", 0x57: "Matchbox", 0x58: "Mattel", 0x59: "Milton Bradley", 0x60: "Titus",
        0x61: "Virgin", 0x64: "LucasArts", 0x67: "Ocean", 0x69: "Electronic Arts", 0x70: "Infogrames",
        0x71: "Interplay", 0x72: "Broderbund", 0x73: "sculptured", 0x75: "sci", 0x78: "THQ",
        0x79: "Accolade", 0x80: "misawa", 0x83: "lozc", 0x86: "Tokuma Shoten Intermedia", 
        0x87: "Tsukuda Original", 0x91: "Chunsoft", 0x92: "Video system", 0x93: "Ocean/Acclaim",
        0x95: "Varie", 0x96: "Yonezawa/s’pal", 0x97: "Kaneko", 0x99: "Pack in soft",
        0xA4: "Konami (Yu-Gi-Oh!)"
    }

    def __init__(self):
        self.filename = ""
        self.rom_size = 0
        self.rom_data = None
        self.header = None

    def cart_load(self, filename: str) -> bool:
        self.filename = filename

        try:
            with open(filename, 'rb') as f:
                self.rom_data = f.read()
            self.rom_size = len(self.rom_data)
            self.header = ROM_Header(self.rom_data[0x100:0x150])
            print(f"Cartridge Loaded: \n"
                  f"\tTitle     :   {self.header.title}\n"
                  f"\tType      :   {self.header.type:02X} ({self.cart_type_name()})\n"
                  f"\tROM Size  :   {32 << self.header.rom_size} KB\n"
                  f"\tRAM Size  :   {self.header.ram_size:02X}\n"
                  f"\tLIC Code  :   {self.header.lic_code:02X} ({self.cart_lic_name()})\n"
                  f"\tROM Ver   :   {self.header.version:02X}\n"
                  f"\tChecksum  :   {self.header.checksum:02X}"
                  f"({'PASSED' if self.verify_checksum() else 'FAILED'})\n")
            return True
        except FileNotFoundError:
            print(f"Failed to open {filename}")
            return False
        except Exception as e:
            print(f"Error Loading Cartridge: {e}")
            return False
    
    def cart_type_name(self) -> str:
        return self.ROM_TYPES[self.header.type] if self.header.type < len(self.ROM_TYPES) else "UNKNOWN"

    def cart_lic_name(self) -> str:
        return self.LIC_CODE[self.header.lic_code] if self.header.lic_code < len(self.ROM_TYPES) else "UNKNOWN"
    
    def verify_checksum(self) -> bool:
        x = sum(self.rom_data[0x0134:0x014D]) & 0xFF
        print((x + self.header.checksum + 1) & 0xFF) 
        return (x + self.header.checksum + 1) & 0xFF == 0
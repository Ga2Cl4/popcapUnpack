import os

PACK_DIR = 'unpack'

class popcapFile():
    def __init__(self, filepath, filesize, param1, param2) -> None:
        self.filepath = filepath
        self.filesize = filesize
        self.param1 = param1
        self.param2 = param2

def main():
    # xor
    infile = open('main.pak', 'rb')
    outfile = open('unpack_main', 'wb')

    data = list(infile.read())
    for i in range(0,len(data)):
        data[i] = data[i] ^ 0xF7
    outfile.write(bytes(data))

    infile.close()
    outfile.close()

    # unpack data
    infile = open('unpack_main', 'rb')  
    packFiles = []
    a = infile.read(8)
    while(infile.read(1) == b'\x00'):
        length = infile.read(1)[0]
        filepath = infile.read(length).decode()
        filesize = int.from_bytes(infile.read(4), 'little')
        unknown1 = int.from_bytes(infile.read(4), 'little')
        unknown2 = int.from_bytes(infile.read(4), 'little')
        #print(f"{filepath} : {hex(unknown1)} {hex(unknown2)}")
        packFiles.append(popcapFile(filepath, filesize, unknown1, unknown2))
    for pf in packFiles:
        tmppath = '.\\' + PACK_DIR + '\\' + pf.filepath
        index = tmppath.rfind('\\')
        if not os.path.exists(tmppath[0:index]):
            os.makedirs(tmppath[0:index])
        with open('.\\' + PACK_DIR + '\\' + pf.filepath, 'wb') as outfile:
            outfile.write(infile.read(pf.filesize))

    infile.close()


if __name__ == '__main__':
    main()
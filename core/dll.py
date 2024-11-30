class Dll:
    def __init__(self, version):
        self.MAILBOX_SIZE = 4096
        self.state = 'NSYNC'
        self.dataBuffer = bytearray()
        self.dllBuffer = bytearray()
        self.escFlag = False
        self.type = version

    def dllPack(self, inputBuffer: bytearray) -> bytearray:
        self.dllBuffer = bytearray(b'S')
        for byte in inputBuffer:
            if byte in [ord('S'), ord('/'), ord('E')]:
                self.dllBuffer.append(ord('/'))
            self.dllBuffer.append(byte)
        if self.type == 1:
            self.dllBuffer.append(ord('E'))
        return self.dllBuffer

    def dllRcv(self, inputBuffer: bytearray) -> bytearray:
        for byte in inputBuffer:
            if self.state == 'NSYNC':
                if byte == ord('S'):
                    self.state = 'SYNC'
                    self.dataBuffer = bytearray()
                    self.escFlag = False
            elif self.state == 'SYNC':
                if byte == ord('S') and not self.escFlag:
                    self.dataBuffer = bytearray()
                elif byte == ord('E') and not self.escFlag:
                    self.state = 'NSYNC'
                elif byte == ord('/'):
                    self.escFlag = not self.escFlag
                else:
                    if self.escFlag:
                        self.escFlag = False
                    self.dataBuffer.append(byte)
            else:
                print(f"ERROR: DLL in illegal state ({self.state})")
        return self.dataBuffer
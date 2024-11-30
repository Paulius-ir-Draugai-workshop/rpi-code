class Dll:
    def __init__(self):
        self.state = "NSYNC"
        self.dllBuffer = bytearray()
        self.escFlag = False

    def dllPack(self, inputBuffer: bytearray) -> bytearray:
        self.dllBuffer = bytearray(b"S")
        for byte in inputBuffer:
            if byte in [ord("S"), ord("/"), ord("E")]:
                self.dllBuffer.append(ord("/"))
            self.dllBuffer.append(byte)
        self.dllBuffer.append(ord("E"))
        return self.dllBuffer

class Dll:
    def __init__(self, version):
        self.MAILBOX_SIZE = 4096
        self.state = 'NSYNC'
        self.dataBuffer = []
        self.dllBuffer = []
        self.escFlag = False
        self.type = version

    def dllPack(self, inputBuffer):
        self.dllBuffer = ['S']
        for char in inputBuffer:
            if char in ['S', '/', 'E']:
                self.dllBuffer.append('/')
            self.dllBuffer.append(char)
        if self.type == 1:
            self.dllBuffer.append('E')

    def dllRcv(self, char):
        if self.state == 'NSYNC':
            if char == 'S':
                self.state = 'SYNC'
                self.dataBuffer = []
                self.escFlag = False
        elif self.state == 'SYNC':
            if char == 'S' and not self.escFlag:
                self.dataBuffer = []
            elif char == 'E' and not self.escFlag:
                self.state = 'NSYNC'
            elif char == '/':
                self.escFlag = not self.escFlag
            else:
                if self.escFlag:
                    self.escFlag = False
                self.dataBuffer.append(char)
        else:
            print(f"ERROR: DLL in illegal state ({self.state})")

# Example usage
dll = Dll(version=1)
input_data = ['a', 'b', '/', 'S', 'e', 'f', 'g', 'h', 'i', 'j']

# Serialize the input
dll.dllPack(input_data)
print("Serialized data:", ''.join(dll.dllBuffer))

# Deserialize the data
for c in dll.dllBuffer:
    dll.dllRcv(c)

if dll.dataBuffer:
    print("Deserialized output:", ''.join(dll.dataBuffer))

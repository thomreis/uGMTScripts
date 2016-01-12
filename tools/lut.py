class Lut():
    """
    A class holding a lut
    """

    def __init__(self, name='LUT', filename='', input_widths=[], output_width=1, version=0):
        self.name = name
        self.lut = {}
        self.header = ''
        self.input_widths = input_widths
        self.output_width = output_width
        self.version = version
        if filename != '':
            self.read_from_file(filename)

    def read_from_file(self, filename):
        with open(filename) as file:
            for line in file:
                if line[0] is '#':
                    self.header += line
                else:
                    addr, value = line.split()
                    self.lut[int(addr)] = int(value)

    def lookup(self, addr):
        return self.lut[addr]

    def lookupInputs(self, inputs):
        addr = 0
        shift = 0
        for i, inp in enumerate(inputs):
            if i+1 > len(self.input_widths):
                break
            val = inp & ((1 << self.input_widths[i]) - 1)
            addr += val << shift
            shift += self.input_widths[i]
        return self.lookup(addr)

    def getHeader(self):
        return self.header

    def getInputWidths(self):
        return self.input_widths

    def getOutputWidth(self):
        return self.output_width

    def getVersion(self):
        return self.version

    def getNEntries(self):
        return len(self.lut)

    def setInputWidths(self, input_widths):
        self.input_widths = input_widths

    def setOutputWidth(self, output_width):
        self.output_width = output_width

    def setVersion(self, version):
        self.version = version

    def setEntry(self, addr, value):
        self.lut[addr] = value

    def setHeader(self, header):
        self.header = header

    def dump(self):
        head = 'LUT: {0}\n'.format(self.name)
        head += 'Input widths:'
        for width in self.input_widths:
            head += ' {0}'.format(width)
        head += 'Output width: {0}'.format(self.output_width)
        if self.header != '':
            head += 'Original header:\n{0}'.format(self.header)
        head += '\nPayload:'
        print head
        for addr in self.lut.keys():
            print '{addr} {value}'.format(addr=addr, value=self.lut[addr])


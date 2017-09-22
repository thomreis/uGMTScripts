import sys
from math import floor

class BxBlock(object):
    """ A class that holds a BX block """
    def __init__(self, rawData, bx=0, totBx=1, valFlag=False, bxDataLength=6):
        if len(rawData) == bxDataLength:
            self.bx = bx
            self.totBx = totBx
            self.valFlag = valFlag
            self.data = rawData
        elif len(rawData) == bxDataLength + 1:
            self.totBx = int(floor(((rawData[0] >> 16) & 0xff) / 6))
            self.bx = int(floor(((rawData[0] >> 24) & 0xff) / 6)) - int(floor(self.totBx / 2))
            self.valFlag = rawData[0] & 0x1
            self.data = rawData[1:]
        else:
            print "Wrong number of raw data words: {l}".format(l=len(rawData))
            self.bx = bx
            self.totBx = totBx
            self.valFlag = valFlag
            self.data = rawData

    def getBx(self):
        return self.bx

    def getTotalBx(self):
        return self.totBx

    def getValFlag(self):
        return self.valFlag

    def getData(self):
        return self.data

    def applyZsMask(self, mask):
        for i, word in enumerate(self.data):
            if word & mask[i] != 0:
                return False
        return True

    def __eq__(self, other):
        """ check if bx blocks are the same """
        if isinstance(other, self.__class__):
            return self.data == other.getData() and self.bx == other.getBx() and self.totBx == self.getTotalBx()
        else:
            return False

    def __ne__(self, other):
        """ check if bx blocks are different """
        return not self.__eq__(other)

class Block(object):
    """ A class that holds an MP7 block """
    def __init__(self, rawData, id, size, capId, zsFlag, valInvFlag):
        self.id = id
        self.size = size
        self.capId = capId
        self.zsFlag = zsFlag
        self.valInvFlag = valInvFlag
        self.bxBlocks = []
        if zsFlag:
            for i in range(0, size, 7):
                self.bxBlocks.append(BxBlock(rawData[i:i+7]))
        else:
            totBx = size / 6
            bx = -int(floor(totBx / 2))
            for i in range(0, size, 6):
                self.bxBlocks.append(BxBlock(rawData[i:i+6], bx=bx, totBx=totBx, valFlag=valInvFlag))
                bx += 1

    def getId(self):
        return self.id

    def getSize(self):
        return self.size

    def getCapId(self):
        return self.capId

    def getZsFlag(self):
        return self.zsFlag

    def getValInvFlag(self):
        return self.valInvFlag

    def getNBxBlocks(self):
        return len(self.bxBlocks)

    def getBxBlocks(self):
        return self.bxBlocks

    def getBxBlocksDict(self):
        bxBlocksDict = {}
        for bxBlock in self.bxBlocks:
            bxBlocksDict[bxBlock.getBx()] = bxBlock
        return bxBlocksDict

def getBlocks(data):
    blocks = []
    # strip eventual padding word
    if data[-1] == 0xffffffff:
        data = data[:-1]
    data_pos = 0
    while data_pos < len(data):
        # get and unpack the header
        header = data[data_pos]
        blockId = (header >> 24) & 0xff
        blockSize = (header >> 16) & 0xff
        capId = (header >> 8) & 0xff
        zsFlag = (header >> 1) & 0x1
        valInvFlag = header & 0x1
        #print "Block {id}, size {size}, zsFlag {zs}".format(id=blockId, size=blockSize, zs=zsFlag)

        data_pos += 1
        # add the block
        blocks.append(Block(data[data_pos:data_pos+blockSize+1], blockId, blockSize, capId, zsFlag, valInvFlag))
        data_pos += blockSize
    return blocks

def getBlocksDict(data):
    blocks = getBlocks(data)
    blocksDict = {}
    for block in blocks:
       blocksDict[block.getId()] = block
    return blocksDict

def getRawData(rawLines):
    rawData = []
    for line in rawLines:
        rawData.append(int(line[9:], 16))
    return rawData

def readRoDataFile(filePath):
    with open(filePath, 'r' ) as inFile:
        lines = []
        for line in inFile:
            lines.append(line.strip())
        return lines[10:-4]

def compareFiles(path1, path2, masksDict):
    rawLines1 = readRoDataFile(sys.argv[1])
    rawLines2 = readRoDataFile(sys.argv[2])

    rawData1 = getRawData(rawLines1)
    rawData2 = getRawData(rawLines2)

    blocks1 = getBlocksDict(rawData1)
    blocks2 = getBlocksDict(rawData2)

    passComp = True
    errorMsgs = []
    for blockId in blocks1:
        if blockId in blocks2:
            #print "Block {id} was not zero suppressed completely.".format(id=blockId)
            compRes = compareBlocks(blocks1[blockId], blocks2[blockId])
            passComp &= compRes[0]
            errorMsgs += compRes[1]
        else:
            #print "Block {id} was zero suppressed completely.".format(id=blockId)
            for bxBlock in blocks1[blockId].getBxBlocks():
                if not bxBlock.applyZsMask(masksDict[blocks1[blockId].getCapId()]):
                    errorMsgs.append("Error. Block {id} should not have been suppressed.".format(id=blockId))
                    print errorMsgs[-1]
                    passComp = False
                    break
    for blockId in blocks2:
        if blockId not in blocks1:
            errorMsgs.append("Error. Additional block {i} found in file {f}.".format(i=blockId, f=path2))
            print errorMsgs[-1]
            passComp = False
            break
        
    return [passComp, errorMsgs]

def compareBlocks(block1, block2):
    bxBlocks1 = block1.getBxBlocksDict()
    bxBlocks2 = block2.getBxBlocksDict()

    newZs = block2.getZsFlag()

    passComp = True
    errorMsgs = []
    suppBxCtr = 0
    valFlagCtr = 0
    for bx in bxBlocks1:
        if bx in bxBlocks2:
            #print "    BX block {bx} was not suppressed".format(bx=bx)
            if bxBlocks1[bx] == bxBlocks2[bx]:
                #print "        BX blocks are equal"
                if bxBlocks2[bx].applyZsMask(masksDict[block2.getCapId()]):
                    suppBxCtr += 1
                    if newZs:
                        if bxBlocks2[bx].getValFlag():
                            valFlagCtr += 1
                            #print "        OK. Block is zero but this is a validation event."
                        else:
                            errorMsgs.append("Error. Block {id}: Bx block {bx} should have been suppressed.".format(id=block1.getId(), bx=bx))
                            print errorMsgs[-1]
                            passComp = False
            else:
                errorMsgs.append("Error. Block {id}: BX blocks {bx} do not match".format(id=block1.getId(), bx=bx))
                print errorMsgs[-1]
                passComp = False
        else:
            #print "    BX block {bx} was suppressed".format(bx=bx)
            if not bxBlocks1[bx].applyZsMask(masksDict[block1.getCapId()]):
                errorMsgs.append("Error. Block {id}: Bx block {bx} should not have been suppressed.".format(id=block1.getId(), bx=bx))
                print errorMsgs[-1]
                passComp = False

    if suppBxCtr == block1.getNBxBlocks() and not valFlagCtr == block2.getNBxBlocks():
        errorMsgs.append("Error. Block {id}: All BX blocks should have been suppressed and this block should not exist.".format(id=block1.getId()))
        print errorMsgs[-1]
        passComp = False

    for bx in bxBlocks2:
        if bx not in bxBlocks1:
            errorMsgs.append("Error. Block {id}: Additional BX block {bx} found.".format(id=block1.getId(), bx=bx))
            print errorMsgs[-1]
            passComp = False
            break

    return [passComp, errorMsgs]

def extractName(path):
    base = path.strip().split( '.' )[0].strip()
    return base.split( '/' )[-1].strip()

def zsTest(nozsPath, zsPath, masksDict, workPath, bx, pattern):
    failureLog = open( workPath + 'failure_log.txt', 'a+' )
    summ = open( workPath + 'summary.txt', 'a+' )

    passComp = compareFiles(nozsPath, zsPath, masksDict)
    if passComp[0]:
        print >> summ, bx.zfill(4), '1'
    else:
        print >> summ, bx.zfill(4), '0'
        for errorMsg in passComp[1]:
            print >> failureLog, bx.zfill(4), errorMsg

        # copy files to error_events dir
        nozsFile = open(nozsPath, 'r')
        zsFile = open(zsPath)
        with open(workPath+'error_events/nozs_'+bx+'_'+pattern+'.txt', 'w') as nozsErrorFile:
            nozsErrorFile.write(nozsFile.read())
        with open(workPath+'error_events/zs_'+bx+'_'+pattern+'.txt', 'w') as zsErrorFile:
            zsErrorFile.write(zsFile.read())
        nozsFile.close()
        zsFile.close()

    failureLog.close()
    summ.close()

if __name__ == '__main__':
    if sys.maxint < 0xffffffff:
        print "Warning: This system uses only 32 bit for long integer values."

    masksDict = {1:[0x1ff, 0x0]*3, 2:[0x7fc00, 0x0]*3, 3:[0x7fc00, 0x0]*3}
    #masksDict = {1:[0x8f000]*6, 2:[0x3fc00, 0x0]*3, 3:[0x3fc00, 0x0]*3}

    nozsPath = sys.argv[1]
    zsPath = sys.argv[2]
    workPath = sys.argv[3]+'/'
    bx = sys.argv[4]
    pattern = extractName(sys.argv[5])

    zsTest(nozsPath, zsPath, masksDict, workPath, bx, pattern)


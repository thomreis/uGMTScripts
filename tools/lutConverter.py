#!/bin/python
import argparse
import glob
from os import walk, path
from lut import Lut

"""
convert LUT from .lut format CONTENT_VECTOR to line based 'address payload' format used by the LUT class
"""

def parse_options():
    desc = "Interface for LUT converter."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--in", dest="inPath", type=str, help="LUT file or directory containing .lut files to convert.", default='')
    parser.add_argument("--out", dest="outPath", type=str, help="Output file name or directory to write converted LUT files with .txt ending to (Default is <input_file_without_.lut>.txt or input directory).", default='')
    parser.add_argument("--txt", dest="txt", help='Write LUT in .txt format (one entry per line, address value)', default=False, action='store_true')
    parser.add_argument("--mifb", dest="mifb", help='Write LUT in binary .mif format (one entry per line, value in binary with leading zeros)', default=False, action='store_true')
    parser.add_argument("--mifh", dest="mifh", help='Write LUT in hex .mif format (one entry per line, value in hex with leading zeros)', default=False, action='store_true')
    parser.add_argument("--xml", dest="xml", help='Write LUT in .xml format (all values in one line)', default=False, action='store_true')
    parser.add_argument("--json", dest="json", help='Write LUT in .json format (all values in one line)', default=False, action='store_true')
    
    return parser.parse_args()

def discover_lut_files(inDir, lutTypes=['*.lut', '*.txt']):
    """
    Tries to find files with type lutType in inDir
    TAKES: the options as returned by parse_options, file type (e.g. .lut)
    RETURNS: list with all files with the type in the directory
    """
    file_list = []
    for roots, dirs, files in walk(inDir):
        for lutType in lutTypes:
            file_list.extend(glob.glob(path.join(roots, lutType)))
    return file_list

def read_dotlut_file(inFileName):
    with open(inFileName) as inFile:
        lut = Lut(name=inFileName[:-4])
        header = ''
        maxEntry = 0
        for line in inFile:
            if line.startswith('#'):
                header += '#' + line
                if line.find('# Version: ') == 0:
                    substrings = line.split()
                    lut.setVersion(int(substrings[2]))
            elif line.startswith('CONTENT_VECTOR='):
                cVectStr = line.split()
                for addr, entryStr in enumerate(cVectStr[1:]):
                    entry = int(entryStr)
                    lut.setEntry(addr, entry)
                    if entry > maxEntry:
                        maxEntry = entry

        lut.setHeader(header)
        lut.setInputWidths([addr.bit_length()])
        outWidth = maxEntry.bit_length()
        if outWidth == 0:
            outWidth = 1
        lut.setOutputWidth(outWidth)
        return lut

def read_dottxt_file(inFileName):
    with open(inFileName) as inFile:
        lut = Lut(name=inFileName[:-4])
        header = ''
        maxEntry = 0
        for line in inFile:
            if line.startswith('#'):
                header += '#' + line
                if line.find('<header>') > 0:
                    substrings = line.split()
                    lut.setVersion(int(substrings[1][1:]))
                    lut.setInputWidths([int(substrings[2])])
                    lut.setOutputWidth(int(substrings[3]))
            else:
                payloadStrs = line.split()
                lut.setEntry(int(payloadStrs[0]), int(payloadStrs[1]))

        lut.setHeader(header)
        return lut

def write_dotmif_file(lut, outFileName, payloadFormat=''):
    with open(outFileName, 'w') as outFile:
        payloadStr = ''
        for addr in range(lut.getNEntries()):
            if payloadFormat == 'b':
                payloadStr += format(lut.lookup(addr), '0{0}b'.format(lut.getOutputWidth())) + '\n'
            elif payloadFormat == 'h':
                payloadStr += format(lut.lookup(addr), '0{0}x'.format(len(hex(2**lut.getOutputWidth() - 1)) - 2)) + '\n'
            else:
                payloadStr += '{0}\n'.format(lut.lookup(addr))
        outFile.write(payloadStr) 

def write_dottxt_file(lut, outFileName):
    with open(outFileName, 'w') as outFile:
        header = ''
        header += '# converted LUT\n'
        header += '# anything after # is ignored with the exception of the header\n'
        header += '# ## denotes original comments\n'
        header += lut.getHeader().replace('#', '##')
        header += '#<header> V{version} {inputWidth} {outputWidth} </header>\n'.format(version=lut.getVersion(), inputWidth=sum(lut.getInputWidths()), outputWidth=lut.getOutputWidth())
        payload = ''
        for addr in range(lut.getNEntries()):
            payload += '{addr} {value}\n'.format(addr=addr, value=lut.lookup(addr))
        outFile.write(header + payload)

def write_dotxml_file(lut, outFileName):
    with open(outFileName, 'w') as outFile:
        header = '<algo id="ugmt">\n'
        header += '  <context id="processors">\n'
        header += '    <param id="{lutId}" type="vector:uint">\n'.format(lutId=outFileName.split('/')[-1].replace('.xml', ''))
        header += '      <!-- version {version}, input width {inputWidth}, output width {outputWidth} -->\n'.format(version=lut.getVersion(), inputWidth=sum(lut.getInputWidths()), outputWidth=lut.getOutputWidth())
        trailer = '\n    </param>\n'
        trailer += '  </context>\n'
        trailer += '</algo>'
        payload = '      '
        for addr in range(lut.getNEntries()):
            payload += '{value}, '.format(value=lut.lookup(addr))
        outFile.write(header + payload[:-2] + trailer)

def write_commondotxml_file(luts, lutNames, outFileName):
    with open(outFileName, 'w') as outFile:
        header = '<algo id="ugmt">\n'
        header += '  <context id="processors">\n'
        payload = ''
        for i, lut in enumerate(luts):
            payload += '    <param id="{lutId}" type="vector:uint">\n'.format(lutId=lutNames[i])
            payload += '      <!-- version {version}, input width {inputWidth}, output width {outputWidth} -->\n'.format(version=lut.getVersion(), inputWidth=sum(lut.getInputWidths()), outputWidth=lut.getOutputWidth())
            payload += '      '
            for addr in range(lut.getNEntries()):
                payload += '{value}, '.format(value=lut.lookup(addr))
            payload = payload[:-2]
            payload += '\n    </param>\n'
        trailer = '  </context>\n'
        trailer += '</algo>'
        outFile.write(header + payload + trailer)

def write_dotjson_file(lut, outFileName):
    with open(outFileName, 'w') as outFile:
        header = '{\n'
        header += '"NAME"        : "{lutId}",\n'.format(lutId=outFileName.split('/')[-1].replace('.json', ''))
        header += '"VERSION"     : "{version}",\n'.format(version=lut.getVersion())
        header += '"INPUTWIDTH"  : "{inputWidth}",\n'.format(inputWidth=sum(lut.getInputWidths()))
        header += '"OUTPUTWIDTH" : "{outputWidth}",\n'.format(outputWidth=lut.getOutputWidth())
        header += '"INSTANCES"   : "List (space separated) of instances of this LUT (differing contents but same in/output)",\n'
        header += '"OUTPUTS"     : "List (space separated) of outputs in format <output_name>(<output_width>)",\n'
        header += '"IPBUS_ADD"   : "Address for access via IPBus",\n'
        header += '"CONTENT_X"   : "List (space separated) of outputs from packed int for zero-indexed instance X",\n'
        trailer = ']\n}'
        payload = '"CONTENT"     : [ '
        for addr in range(lut.getNEntries()):
            payload += '{value}, '.format(value=lut.lookup(addr))
        outFile.write(header + payload[:-2] + trailer)

def get_lut_from_file(filename):
    if filename.endswith('.lut'):
        lut = read_dotlut_file(filename)
    elif filename.endswith('.txt'):
        lut = read_dottxt_file(filename)
    return lut

def main():
    options = parse_options()

    luts = []
    lutNames = []

    if options.inPath != '':
        if options.inPath.endswith('/'):
            print 'Begin converting LUT files in {inPath}'.format(inPath=options.inPath)
            if options.txt and options.outPath == '':
                file_list = discover_lut_files(options.inPath, ['*.lut'])
            else:
                file_list = discover_lut_files(options.inPath)

            for fPath in file_list:
                fName = path.split(fPath)[-1]
                lut = get_lut_from_file(fPath)
                luts.append(lut)
                lutNames.append(fName[:-4])
                outPath = options.outPath
                if outPath == '':
                    outPath = options.inPath
                    outFile = outPath + fName[:-4]
                else:
                    outPath = path.split(options.outPath)[0] + '/'
                    outFile = outPath + fName[:-4]
                if options.txt:
                    print 'Writing converted LUT to file {file}'.format(file=outFile + '.txt')
                    write_dottxt_file(lut, outFile + '.txt')
                if options.mifb:
                    print 'Writing converted LUT to file {file}'.format(file=outFile + '.mif')
                    write_dotmif_file(lut, outFile + '.mif', 'b')
                elif options.mifh:
                    print 'Writing converted LUT to file {file}'.format(file=outFile + '.mif')
                    write_dotmif_file(lut, outFile + '.mif', 'h')
                if options.xml:
                    print 'Writing converted LUT to file {file}'.format(file=outFile + '.xml')
                    write_dotxml_file(lut, outFile + '.xml')
                if options.json:
                    print 'Writing converted LUT to file {file}'.format(file=outFile + '.json')
                    write_dotjson_file(lut, outFile + '.json')

            # write all LUTs in one file
            if options.xml:
                print 'Writing LUTs to file {file}'.format(file=outPath + 'UGMT_MP7_ALGO_LUTS.xml')
                write_commondotxml_file(luts, lutNames, outPath + 'UGMT_MP7_ALGO_LUTS.xml')
        else:
            print 'Begin converting file {file}'.format(file=options.inPath)
            lut = get_lut_from_file(options.inPath)
            luts.append(lut)
            if options.outPath == '':
                outFile = options.inPath[:-4]
            elif options.outPath.endswith('/'):
                outFile = options.outPath + path.split(options.inPath[:-4])[-1]
            else:
                outFile = options.outPath
            if options.txt:
                print 'Writing converted LUT to file {file}'.format(file=outFile + '.txt')
                write_dottxt_file(lut, outFile + '.txt')
            if options.mifb:
                print 'Writing converted LUT to file {file}'.format(file=outFile + '.mif')
                write_dotmif_file(lut, outFile + '.mif', 'b')
            elif options.mifh:
                print 'Writing converted LUT to file {file}'.format(file=outFile + '.mif')
                write_dotmif_file(lut, outFile + '.mif', 'h')
            if options.xml:
                print 'Writing converted LUT to file {file}'.format(file=outFile + '.xml')
                write_dotxml_file(lut, outFile + '.xml')
            if options.json:
                print 'Writing converted LUT to file {file}'.format(file=outFile + '.json')
                write_dotjson_file(lut, outFile + '.json')

        print 'Finished converting LUT files'
    else:
        print 'No inputs given. Nothing to do.'

if __name__ == "__main__":
    main()

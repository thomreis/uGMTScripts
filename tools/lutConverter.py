#!/bin/python
import argparse
from os import walk, path

"""
convert LUT from .lut format CONTENT_VECTOR to line based 'address payload' format used by the LUT class
"""

def parse_options():
    desc = "Interface for LUT converter."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--in", dest="inPath", type=str, help="LUT file or directory containing .lut files to convert.", default='')
    parser.add_argument("--out", dest="outPath", type=str, help="Output file name or directory to write converted LUT files with .txt ending to (Default is <input_file_without_.lut>.txt or input directory).", default='')
    
    return parser.parse_args()

def discover_lut_files(inDir):
    """
    Tries to find *.lut files in inDir
    TAKES: the options as returned by parse_options, above
    RETURNS: list with all .lut files in the directory
    """
    file_list = []
    for roots, dirs, files in walk(inDir):
        for fname in files:
            if fname.endswith('.lut'):
                file_list.append(path.join(path.abspath(roots), fname))
    return file_list

def get_converted_string(inFile):
    with open(inFile) as inFile:
        header = '# converted LUT from .lut file\n'
        header += '# anything after # is ignored with the exception of the header\n'
        header += '# ## denotes original file comments\n'
        payload = ''
        version = 0
        maxEntry = 0
        for line in inFile:
            if line.startswith('#'):
                header += '#' + line
                if line.find('# Version: ') == 0:
                    substrings = line.split()
                    version = int(substrings[2])
            elif line.startswith('CONTENT_VECTOR='):
                cVectStr = line.split()
                for addr, entry in enumerate(cVectStr[1:]):
                    payload += '{addr} {entry}\n'.format(addr=addr, entry=int(entry))
                    if entry > maxEntry:
                        maxEntry = entry

        inWidth = int(addr).bit_length()
        outWidth = int(maxEntry).bit_length()
        if outWidth == 0:
            outWidth = 1
        header += '# input width determined to be {inputWidth} from CONTENT_VECTOR length\n'.format(inputWidth=inWidth)
        header += '# output width determined to be {outputWidth} from maximal value in CONTENT_VECTOR\n'.format(outputWidth=outWidth)
        header += '#<header> V{version} {inputWidth} {outputWidth} </header>\n'.format(version=version, inputWidth=inWidth, outputWidth=outWidth)
        return header + payload

def write_converted_lut(convStr, outFileName):
    with open(outFileName, 'w') as outFile:
        outFile.write(convStr)

def main():
    options = parse_options()

    if options.inPath != '':
        if options.inPath.endswith('/'):
            print 'Begin converting .lut files in {inPath}'.format(inPath=options.inPath)
            file_list = discover_lut_files(options.inPath)
            for fPath in file_list:
                convStr = get_converted_string(fPath)
                fName = path.split(fPath)[-1]
                if options.outPath == '':
                    outFile = options.inPath + fName.replace('.lut', '.txt')
                else:
                    outFile = path.split(options.outPath)[0] + '/' + fName.replace('.lut', '.txt')
                print 'Writing converted LUT to file {file}'.format(file=outFile)
                write_converted_lut(convStr, outFile)
        else:
            print 'Begin converting file {file}'.format(file=options.inPath)
            convStr = get_converted_string(options.inPath)
            if options.outPath == '':
                outFile = options.inPath.replace('.lut', '.txt')
            elif options.outPath.endswith('/'):
                outFile = options.outPath + path.split(options.inPath.replace('.lut', '.txt'))[-1]
            else:
                outFile = options.outPath
            print 'Writing converted LUT to file {file}'.format(file=outFile)
            write_converted_lut(convStr, outFile)

        print 'Finished converting .lut files'
    else:
        print 'No inputs given. Nothing to do.'

if __name__ == "__main__":
    main()

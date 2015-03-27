from helpers.mp7_buffer_parser import OutputBufferParser, Version
from tools.muon_helpers import print_out_word
from helpers.options import parse_options, discover_files
from tools.vhdl import VHDLConstantsParser

if __name__ == "__main__":
    vhdl_dict = VHDLConstantsParser.parse_vhdl_file("data/ugmt_constants.vhd")
    options = parse_options()
    file_dict = discover_files(options)

    for pattern, fnames in file_dict.iteritems():
        version = Version.from_filename(fnames['base'])
        print "+"*30, "version detected:", version, "+"*30
        print "+"*30, pattern, "+"*30

        # Reading and processing the hardware data
        output_parser = OutputBufferParser(fnames["tx"], vhdl_dict, version)
        out_muons = output_parser.get_output_muons()

        non_zero = [ mu for mu in out_muons if mu.bitword != 0 ]

        mu_to_print = []
        if options.verbose:
            mu_to_print = out_muons
        else:
            mu_to_print = non_zero

        last_bx = 0            
        for mu in non_zero:
            if mu.bx != last_bx:
                print "*"*50, "current bx:", mu.bx, "*"*50
                last_bx = mu.bx
            print print_out_word(mu.bitword)
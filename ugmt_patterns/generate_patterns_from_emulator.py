from helpers.muon import Muon
from helpers.pattern_dumper import PatternDumper, TestbenchWriter, BufferWriter

#ROOT
from ROOT import gSystem, gROOT

def setupROOT():
    gSystem.Load("libFWCoreFWLite")
    gROOT.ProcessLine('AutoLibraryLoader::enable();')
    gSystem.Load("libFWCoreFWLite")
    gSystem.Load("libCintex")
    gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')

setupROOT()
gSystem.Load("libL1TriggerL1TGlobalMuon")

from ROOT import l1t

#CMSSW
from DataFormats.FWLite import Events, Handle
#from L1Trigger.L1TGlobalMuon import MicroGMTRankPtQualLUT
# ../tools:
from tools.vhdl import VHDLConstantsParser

from helpers.options import parse_options, discover_emu_files

def get_muon_list_out(emu_product, mu_type, vhdl_dict):
    if mu_type == "OUT":    
        nexpected = 8
    if mu_type == "IMD":    
        nexpected = 24

    mulist = [Muon(vhdl_dict, mu_type="OUT", bitword=0)]*nexpected
    for i in xrange(emu_product.size(0)):
        mu_tmp = Muon(vhdl_dict, mu_type="OUT", obj = emu_product.at(0, i))
        mulist[i] = mu_tmp
    return mulist


def get_muon_list(emu_product, mu_type, vhdl_dict):
    nexpected = 18
    if mu_type == "BARREL": nexpected = 36

    mulist = [Muon(vhdl_dict, mu_type="IN", bitword=0)]*nexpected
    
    link_offset = vhdl_dict[mu_type+"_LOW"]
    for mu in emu_product:
        loc_link = mu.link()-link_offset
        mu_tmp = Muon(vhdl_dict, mu_type="IN", obj=mu)
        # only take muons from the right side of the detector
        if mu_type.endswith("POS") and mu_tmp.etaBits < 0: continue
        if mu_type.endswith("NEG") and mu_tmp.etaBits > 0: continue

        # because we don't book all 72*3 muons but only 18*3/36*3
        loc_link = mu.link()-link_offset
        if mulist[loc_link*3].ptBits == 0: 
            mulist[loc_link*3] = mu_tmp
        elif mulist[loc_link*3+1].ptBits == 0:
            mulist[loc_link*3+1] = mu_tmp
        elif mulist[loc_link*3+2].ptBits == 0:
            mulist[loc_link*3+2] = mu_tmp

    return mulist
    


def main():
    vhdl_dict = VHDLConstantsParser.parse_vhdl_file("data/ugmt_constants.vhd")

    opts, args = parse_options()
    fname_dict = discover_emu_files(opts.emudirectory)
    
    rankLUT = l1t.MicroGMTRankPtQualLUT()


    for pattern, fnames in fname_dict.iteritems():
        print "+"*30, pattern, "+"*30
        events = Events(fnames['root'])

        out_handle = Handle('BXVector<l1t::Muon>')
        imd_handle = Handle('BXVector<l1t::Muon>')
        bar_handle = Handle('std::vector<l1t::L1TRegionalMuonCandidate>')
        fwd_handle = Handle('std::vector<l1t::L1TRegionalMuonCandidate>')
        ovl_handle = Handle('std::vector<l1t::L1TRegionalMuonCandidate>')

        basedir_testbench = "data/patterns/testbench/"
        basedir_mp7 = "data/patterns/mp7/"

        input_buffer = PatternDumper(basedir_mp7+pattern+".txt", vhdl_dict, BufferWriter)
        output_buffer = PatternDumper(basedir_mp7+pattern+"_out.txt", vhdl_dict, BufferWriter)
        input_testbench = PatternDumper(basedir_testbench+pattern+".txt", vhdl_dict, TestbenchWriter)
        serializer_testbench = PatternDumper(basedir_testbench+"serializer_"+pattern+".txt", vhdl_dict, TestbenchWriter)

        for i, event in enumerate(events):
            event_head = "#"*80+"\n"
            event_head += "# Event: {ievent}\n".format(ievent=i)
            event_head += "#"*80+"\n"
            input_testbench.addLine(event_head)
            serializer_testbench.addLine(event_head)

            event.getByLabel("microGMTEmulator", out_handle)
            event.getByLabel("microGMTEmulator", "intermediateMuons", imd_handle)
            event.getByLabel("uGMTInputProducer", "BarrelTFMuons", bar_handle)
            event.getByLabel("uGMTInputProducer", "ForwardTFMuons", fwd_handle)
            event.getByLabel("uGMTInputProducer", "OverlapTFMuons", ovl_handle)

            emu_out_muons = out_handle.product()
            outmuons = get_muon_list_out(emu_out_muons, "OUT", vhdl_dict)
            imd_prod = imd_handle.product()
            imdmuons = get_muon_list_out(imd_prod, "IMD", vhdl_dict)
            emu_bar_muons = bar_handle.product()
            bar_muons = get_muon_list(emu_bar_muons, "BARREL", vhdl_dict)
            emu_ovl_muons = ovl_handle.product()
            ovlp_muons = get_muon_list(emu_ovl_muons, "OVL_POS", vhdl_dict)
            ovln_muons = get_muon_list(emu_ovl_muons, "OVL_NEG", vhdl_dict)
            emu_fwd_muons = fwd_handle.product()
            fwdp_muons = get_muon_list(emu_fwd_muons, "FWD_POS", vhdl_dict)
            fwdn_muons = get_muon_list(emu_fwd_muons, "FWD_NEG", vhdl_dict)

            input_buffer.writeFrameBasedInputBX(bar_muons, fwdp_muons, fwdn_muons, ovlp_muons, ovln_muons, [])
            input_buffer.dump()

            output_buffer.writeFrameBasedOutputBX(outmuons, imdmuons)
            output_buffer.dump()

            input_testbench.writeMuonBasedInputBX(bar_muons, fwdp_muons, fwdn_muons, ovlp_muons, ovln_muons, [], rankLUT, True)
            input_testbench.addLine("# Expected emulator output\n")
            input_testbench.writeMuonBasedOutputBX(outmuons, imdmuons)
            input_testbench.dump()
    
            serializer_testbench.writeMuonBasedOutputBX(outmuons, imdmuons)
            serializer_testbench.addLine("# Expected emulator output\n")
            serializer_testbench.writeFrameBasedOutputBX(outmuons, imdmuons)
            serializer_testbench.dump()


if __name__ == "__main__":
    main()
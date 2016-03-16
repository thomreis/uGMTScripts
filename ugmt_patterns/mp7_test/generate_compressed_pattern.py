import sys
sys.path.append('../')

from helpers.muon import Muon
from helpers.pattern_dumper import PatternDumper, BufferWriter

#ROOT
from ROOT import gSystem, gROOT
import time
import zlib


def setupROOT():
    gSystem.Load("libFWCoreFWLite")
    gROOT.ProcessLine('FWLiteEnabler::enable();')
    # gSystem.Load("libCintex")
    # gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')

setupROOT()
# gSystem.Load("libL1TriggerL1TMuon")

from ROOT import l1t

#CMSSW
from DataFormats.FWLite import Events, Handle
#from L1Trigger.L1TGlobalMuon import MicroGMTRankPtQualLUT
# ../tools:
from tools.vhdl import VHDLConstantsParser

from helpers.options import parse_options, discover_emu_files


def get_muon_list_out(emu_product, mu_type, vhdl_dict, nexpected=8):
    mulist = [Muon(vhdl_dict, mu_type, bitword=0)]*nexpected
    for i in xrange(emu_product.size(0)):
        if emu_product.at(0, i).hwPt() > 0:
            mu_tmp = Muon(vhdl_dict, mu_type, obj=emu_product.at(0, i))
            mulist[i] = mu_tmp
    return mulist


def get_muon_list(emu_product, mu_type, vhdl_dict, bx, check=False):
    nexpected = 18
    if mu_type == "BMTF":
        nexpected = 36

    mulist = [Muon(vhdl_dict, mu_type="IN", bitword=0)]*nexpected

    for i in xrange(emu_product.size(0)):
        mu_tmp = Muon(vhdl_dict, mu_type="IN", obj=emu_product.at(0, i))
        # only take muons from the right side of the detector
        if mu_type.endswith("POS") and mu_tmp.etaBits < 0:
            continue
        if mu_type.endswith("NEG") and mu_tmp.etaBits > 0:
            continue

        # because we don't book all 72*3 muons but only 18*3/36*3
        loc_link = emu_product.at(0, i).processor()
        if mulist[loc_link*3].ptBits == 0:
            mu_tmp.setBunchCounter(0)
            mulist[loc_link*3] = mu_tmp
        elif mulist[loc_link*3+1].ptBits == 0:
            mu_tmp.setBunchCounter(1)
            mulist[loc_link*3+1] = mu_tmp
        elif mulist[loc_link*3+2].ptBits == 0:
            mu_tmp.setBunchCounter(2)
            mulist[loc_link*3+2] = mu_tmp

        if check:
            if mu_tmp.ptBits < 0 or mu_tmp.ptBits > 511:
                print "+++ err > pt out of bounds"
            if mu_tmp.etaBits < -224 or mu_tmp.etaBits > 223:
                print "+++ err > eta out of bounds"
            if mu_tmp.phiBits < 0 or mu_tmp.phiBits > 575:
                print "+++ err > phi out of bounds"
            if mu_tmp.qualityBits < 0 or mu_tmp.qualityBits > 15:
                print "+++ err > quality out of bounds"

    return mulist


def get_calo_list(raw_sums):
    calo_sums = [0]*36*28
    for i in xrange(raw_sums.size(0)):
        idx = raw_sums.at(0, i).hwPhi() + raw_sums.at(0, i).hwEta()*36
        # print raw_sums.at(0, i).hwPhi(), raw_sums.at(0, i).hwEta()
        calo_sums[idx] = raw_sums.at(0, i).etBits()
    return calo_sums

def dump_files(directory, fname, n, input_buffer, output_buffer, indelay, outdelay):
    with open('{path}/rx_{fname}_{idx}.zip'.format(path=directory, fname=fname, idx=n), 'w') as ofile:
        ofile.write(zlib.compress(input_buffer.dump_string()))
    with open('{path}/tx_{fname}_{idx}.zip'.format(path=directory, fname=fname, idx=n), 'w') as ofile:
        ofile.write(zlib.compress(output_buffer.dump_string(True)))
    output_buffer.writeEmptyFrames(outdelay)
    if indelay > 0:
        input_buffer.writeEmptyFrames(indelay)


def main():
    vhdl_dict = VHDLConstantsParser.parse_vhdl_file("../data/ugmt_constants.vhd")

    opts = parse_options()
    fname_dict = discover_emu_files(opts.emudirectory)
    # rankLUT = l1t.MicroGMTRankPtQualLUT()

    ALGODELAY = opts.delay + 26 #first frame with valid = 1

    max_events = int((1024-ALGODELAY)/6)

    for pattern, fnames in fname_dict.iteritems():
        print "+"*30, pattern, "+"*30
        events = Events(fnames['root'])

        start = time.time()

        out_handle = Handle('BXVector<l1t::Muon>')
        imd_bmtf_handle = Handle('BXVector<l1t::Muon>')
        imd_emtf_p_handle = Handle('BXVector<l1t::Muon>')
        imd_emtf_n_handle = Handle('BXVector<l1t::Muon>')
        imd_omtf_p_handle = Handle('BXVector<l1t::Muon>')
        imd_omtf_n_handle = Handle('BXVector<l1t::Muon>')
        bar_handle = Handle('BXVector<l1t::RegionalMuonCand>')
        fwd_handle = Handle('BXVector<l1t::RegionalMuonCand>')
        ovl_handle = Handle('BXVector<l1t::RegionalMuonCand>')
        calo_handle = Handle('BXVector<l1t::MuonCaloSum>')

        basedir_mp7 = "../data/patterns/compressed/"
        path = '{path}/{pattern}/'.format(path=basedir_mp7, pattern=pattern)

        input_buffer = PatternDumper(basedir_mp7+pattern+".txt", vhdl_dict, BufferWriter)
        output_buffer = PatternDumper(basedir_mp7+pattern+"_out.txt", vhdl_dict, BufferWriter)

        if opts.delay > 0:
            input_buffer.writeEmptyFrames(opts.delay)

        setup_time = time.time() - start

        avg_get_label_time = 0
        avg_conversion_time = 0
        avg_write_time = 0

        output_buffer.writeEmptyFrames(ALGODELAY)
        cntr = 0
        for i, event in enumerate(events):
            evt_start = time.time()
            event.getByLabel("simGmtStage2Digis", out_handle)
            event.getByLabel("simGmtStage2Digis", "imdMuonsBMTF", imd_bmtf_handle)
            event.getByLabel("simGmtStage2Digis", "imdMuonsEMTFPos", imd_emtf_p_handle)
            event.getByLabel("simGmtStage2Digis", "imdMuonsEMTFNeg", imd_emtf_n_handle)
            event.getByLabel("simGmtStage2Digis", "imdMuonsOMTFPos", imd_omtf_p_handle)
            event.getByLabel("simGmtStage2Digis", "imdMuonsOMTFNeg", imd_omtf_n_handle)
            event.getByLabel("simBmtfDigis", "BMTF", bar_handle)
            event.getByLabel("simEmtfDigis", "EMTF", fwd_handle)
            event.getByLabel("simOmtfDigis", "OMTF", ovl_handle)

            event.getByLabel("simGmtCaloSumDigis", "TriggerTowerSums", calo_handle)
            #event.getByLabel("simGmtCaloSumDigis", "TriggerTower2x2s", calo_handle)
            get_label_time = time.time() - evt_start
            calo_sums_raw = calo_handle.product()
            calo_sums = get_calo_list(calo_sums_raw)

            emu_out_muons = out_handle.product()
            outmuons = get_muon_list_out(emu_out_muons, "OUT", vhdl_dict)
            imd_emtf_p_prod = imd_emtf_p_handle.product()
            imdmuons = get_muon_list_out(imd_emtf_p_prod, "IMD", vhdl_dict, 4)
            imd_omtf_p_prod = imd_omtf_p_handle.product()
            imdmuons += get_muon_list_out(imd_omtf_p_prod, "IMD", vhdl_dict, 4)
            imd_bmtf_prod = imd_bmtf_handle.product()
            imdmuons += get_muon_list_out(imd_bmtf_prod, "IMD", vhdl_dict, 8)
            imd_omtf_n_prod = imd_omtf_n_handle.product()
            imdmuons += get_muon_list_out(imd_omtf_n_prod, "IMD", vhdl_dict, 4)
            imd_emtf_n_prod = imd_emtf_n_handle.product()
            imdmuons += get_muon_list_out(imd_emtf_n_prod, "IMD", vhdl_dict, 4)

            emu_bar_muons = bar_handle.product()
            bar_muons = get_muon_list(emu_bar_muons, "BMTF", vhdl_dict, i)
            emu_ovl_muons = ovl_handle.product()
            ovlp_muons = get_muon_list(emu_ovl_muons, "OMTF_POS", vhdl_dict, i)
            ovln_muons = get_muon_list(emu_ovl_muons, "OMTF_NEG", vhdl_dict, i)
            emu_fwd_muons = fwd_handle.product()
            fwdp_muons = get_muon_list(emu_fwd_muons, "EMTF_POS", vhdl_dict, i)
            fwdn_muons = get_muon_list(emu_fwd_muons, "EMTF_NEG", vhdl_dict, i)

            conversion_time = time.time() - evt_start - get_label_time

            for mu in outmuons:
                if mu.bitword != 0:
                    cntr += 1
            input_buffer.writeFrameBasedInputBX(bar_muons, fwdp_muons, fwdn_muons, ovlp_muons, ovln_muons, calo_sums)
            output_buffer.writeFrameBasedOutputBX(outmuons, imdmuons)

            if i%(max_events-1) == 0 and i != 0: # dump every max_events
                ifile = i/max_events
                print "Writing file {pattern}_{ifile}.zip for event {i}".format(pattern=pattern, ifile=ifile, i=i)
                dump_files(path, pattern, ifile, input_buffer, output_buffer, opts.delay, ALGODELAY)


            if (i+1)%1000 == 0:
                print "  processing the {i}th event".format(i=i+1)

            write_time = time.time() - evt_start - conversion_time
            avg_get_label_time += get_label_time
            avg_conversion_time += conversion_time
            avg_write_time += write_time
        print "total: ", time.time() - start
        print "setup: ", setup_time
        print "get_label:", "avg", avg_get_label_time/float(i+1), "last", get_label_time
        print "conversion: avg", avg_conversion_time/float(i+1), "last", conversion_time
        print "write: avg", avg_write_time/float(i+1), "last", write_time
        print 'n final muons: ', cntr
        if i%(max_events-1) != 0:
            ifile = i/max_events
            dump_files(path, pattern, ifile, input_buffer, output_buffer, opts.delay, ALGODELAY)

        print (i+1)/max_events

if __name__ == "__main__":
    main()

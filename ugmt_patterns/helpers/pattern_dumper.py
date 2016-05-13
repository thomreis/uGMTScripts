from tools.logger import log

class BufferWriter(object):
    """
    Class (Decorator) that produces mp7-buffer-files.
    Giving this class to the ctor of of PatternDumper will let it create these files
    """
    def __init__(self):
        super(BufferWriter, self).__init__()
        self.string = []
        self.frameCounter = 0
        self.head = """Board ugmt_b40
 Quad/Chan :    q00c0      q00c1      q00c2      q00c3      q01c0      q01c1      q01c2      q01c3      q02c0      q02c1      q02c2      q02c3      q03c0      q03c1      q03c2      q03c3      q04c0      q04c1      q04c2      q04c3      q05c0      q05c1      q05c2      q05c3      q06c0      q06c1      q06c2      q06c3      q07c0      q07c1      q07c2      q07c3      q08c0      q08c1      q08c2      q08c3      q09c0      q09c1      q09c2      q09c3      q10c0      q10c1      q10c2      q10c3      q11c0      q11c1      q11c2      q11c3      q12c0      q12c1      q12c2      q12c3      q13c0      q13c1      q13c2      q13c3      q14c0      q14c1      q14c2      q14c3      q15c0      q15c1      q15c2      q15c3      q16c0      q16c1      q16c2      q16c3      q17c0      q17c1      q17c2      q17c3
      Link :     00         01         02         03         04         05         06         07         08         09         10         11         12         13         14         15         16         17         18         19         20         21         22         23         24         25         26         27         28         29         30         31         32         33         34         35         36         37         38         39         40         41         42         43         44         45         46         47         48         49         50         51         52         53         54         55         56         57         58         59         60         61         62         63         64         65         66         67         68         69         70         71
"""

    def writeFrame(self, words, valid = 1, validoverflow = 0, ftype=None):
        """
        Write a frame to the internal "buffer" (i.e. string),
        TAKES:
            words: List of 72-X 32 bit words (if X > 0, the remaining links are filled with 0)
        RETURNS:
            void
        """
        self.string += ["Frame {n:0>4} :".format(n=self.frameCounter)]
        for w in words:
            self.string += [" {v}v{w:0>8x}".format(v=valid, w=w)]

        for i in range(72-len(words)):
            self.string += [" {v}v{w:0>8x}".format(v=validoverflow, w=0)]
        self.string += ["\n"]
        self.frameCounter += 1

    def get_full_string(self):
        fstring = self.head + ''.join(self.string)
        self.string = []
        return fstring

    def fill_up(self, n):
        while self.frameCounter < n:
            self.writeFrame([])

    def reset(self):
        self.frameCounter = 0

class TestbenchWriter(object):
    """
    Class (Decorator) that produces testbench files (i.e. what Dinyar uses for testing)
    Giving this class to the ctor of of PatternDumper will let it create these files
    """
    def __init__(self):
        super(TestbenchWriter, self).__init__()
        self.string = []
        self.iFrameCounter = 0
        self.oFrameCounter = 0
        self.bxCounter = 0
        self.head = """################################################################################
# Pattern for testbench of the uGMT algo block
# Data format of muons:
# ID N PT PHI ETA CHARGE CHARGE_VALID QUALITY SORT EMPTY (ISO)
# where ID = {EMTF+/-, OMTF+/-, BMTF, OUT, EIMD, BIMD, OIMD}
# N is the rank for IMD / OUT and the link for inputs.
# ISO is optional and only present for OUT
#
# Data format for tracks:
# ID ETA0 PHI0 QUALITY0 ETA1 PHI1 QUALITY1 ETA2 PHI2 QUALITY2
# where ID = {FTRK+/-, OTRK+/-, BTRK}
# Tracks are given always for 3 consecutive muons
#
#
# Data format for output of serializer:
# ID VALID0 WORD0 VALID1 WORD1 ... VALIDN WORDN
# where ID = FRMx, x being the current 240 MHz cycle
# In WordX the X represents the link number, meaning that muon0 is x(FRM0, WORD0) + x(FRM1, WORD0) << 32.
"""


    def writeFrame(self, words, valid = 1, validoverflow = 0, ftype="in"):
        """
        Adds the frame to the buffer
        TAKES:
            words : list of the 32 bit words of the current frame (filled with 0s to have 72)
        """
        if ftype == "in":
            self.string += ["{n:<6} ".format(n="IFR"+str(self.iFrameCounter))]
            self.iFrameCounter += 1
        else:
            self.string += ["{n:<6} ".format(n="OFR"+str(self.oFrameCounter))]
            self.oFrameCounter += 1

        for w in words:
            self.string += [" {v} {w:0>8x}".format(v=valid, w=w)]

        for i in range(72-len(words)):
            self.string += [" {v} {w:0>8x}".format(v=validoverflow, w=0)]
        self.string += ["\n"]


    def writeMuonHeadline(self):
        """ documenting the individual muon quantities """
        self.string += ["#{id:<5} {rank:>5} {pt:>5} {phi:>5} {eta:>5} {charge:>5} {charge_valid:>5} {quality:>5} {sort:>5} {empty:>5} {iso:>5} {idx:>5}\n".format(
                                id="TYPE",
                                rank="POS",
                                pt="PT",
                                phi="PHI",
                                eta="ETA",
                                charge="CHR",
                                charge_valid="VCHR",
                                quality="QUAL",
                                sort="RANK",
                                empty="EMPT",
                                iso="(ISO)",
                                idx="(IDX)",
                            )]

    def writeTrackHeadline(self):
        """ documenting the individual track quantities """
        self.string += ["# OVERLAP/ENDCAP TRACKS\n#TYPE   ETA0  PHI0 QUAL0 EMPT0  ETA1  PHI1 QUAL1 EMPT1  ETA2  PHI2 QUAL2 EMPT2\n"]

    def writeBTRKTrackHeadline(self):
        """ documenting the individual track quantities """
        self.string += ["# BARREL TRACKS\n#TYPE   ETA0  PHI0 QUAL0  SEL0 SIDE0  WHL0 SCT10 SCT20 SCT30 SCT40 EMPT0  ETA1  PHI1 QUAL1  SEL1 SIDE1  WHL1 SCT11 SCT21 SCT31 SCT41 EMPT1  ETA2  PHI2 QUAL2  SEL2 SIDE2  WHL2 SCT12 SCT22 SCT32 SCT42 EMPT2\n"]

    def writeBMTFTrackAddressHeadline(self):
        """ documenting the individual track quantities """
        self.string += ["# BMTF TRACK ADDRESS\n#TYPE     SEL0  SIDE0 WHEEL0 SECT10 SECT20 SECT30 SECT40 QUAL0 EMPT0  SEL1  SIDE1 WHEEL1 SECT11 SECT21 SECT31 SECT41 QUAL1 EMPT1  SEL2  SIDE2 WHEEL2 SECT12 SECT22 SECT32 SECT42 QUAL2 EMPT2\n"]

    def writeEventHeader(self, n):
        self.string += ["# Event {n}\n".format(n=n)]

    def writeBXCounter(self, n):
        self.string += ["EVT {n}\n".format(n=n)]

    def fill_up(self, n):
        while self.frameCounter < n:
            self.writeFrame([])

    def writeMuon(self, mu, mu_type, rank, addIso = False):
        """
        Convert a single ./helpers/muon.Muon object into string
        TAKES:  mu          Muon object
                mu_type     muon type (BMTF, EMTF+/-, OMTF+/-, EIMD, BIMD, OIMD, OUT)
                rank        relative position of the muon (IMD: 0-23, OUT: 0-7, EMTF/OMTF: 0-37, BMTF: 0-35)
                addIso      whether to add isolation info and muon index (should only be done for OUT)
        Adds to self.string "ID N PT PHI ETA CHARGE CHARGE_VALID QUALITY SORT EMPTY (ISO) (IDX)"
        """
        isempty = 0
        if mu.ptBits == 0: isempty = 1
        sortrank = 0
        if mu_type in ["EIMD", "BIMD", "OIMD", "OUT"]:
            sortrank = mu.rank
        else:
            sortrank = mu.ptBits + mu.qualityBits

        tmp_string = "{id:<6} {rank:>5} {pt:>5} {phi:>5} {eta:>5} {charge:>5} {charge_valid:>5} {quality:>5} {sort:>5} {empty:>5}".format(
                        id=mu_type,
                        rank=rank,
                        pt=mu.ptBits,
                        phi=mu.globPhiBits,
                        eta=mu.etaBits,
                        charge=mu.Sysign & 0x1,
                        charge_valid=mu.Sysign >> 1,
                        quality=mu.qualityBits,
                        sort=sortrank,
                        empty=isempty
                    )
        if addIso:
            tmp_string += " {iso:>5}".format(iso=mu.Iso)
            tmp_string += " {idx:>5}".format(idx=mu.tfMuonIndex)

        tmp_string += "\n"
        self.string += [tmp_string]

    def writeTracks(self, tracks, track_type):
        """
        Adds the track information to the buffer.
        TAKES:
            For BTRK track_type: tracks: list of [eta, phi, qual, selector, wheelSide, wheelNum, sect1, sect2, sect3, sect4, empty]*n_tracks
            For other track_types: tracks: list of [eta, phi, qual, empty]*n_tracks
            track_type: track-id = {FTRK+/-, BTRK, OTRK+/-}
        """
        for i, track in enumerate(tracks):
            if i%3==0:
                self.string += ["{id:<6}".format(id=track_type)]
            if track_type == 'BTRK':
                self.string += [" {eta:>5} {phi:>5} {qual:>5} {sel:>5} {wheelSide:>5} {wheelNum:>5} {sect1:>5} {sect2:>5} {sect3:>5} {sect4:>5} {empty:>5}".format(eta=track[0], phi=track[1], qual=track[2], sel=track[3], wheelSide=track[4], wheelNum=track[5], sect1=track[6], sect2=track[7], sect3=track[8], sect4=track[9], empty=track[10])]
            else:
                self.string += [" {eta:>5} {phi:>5} {qual:>5} {empty:>5}".format(eta=track[0], phi=track[1], qual=track[2], empty=track[3])]
            if (i+1)%3 == 0:
                self.string += ["\n"]

    def writeBMTFTrackAddress(self, trackAddresses):
        """
        Adds the BMTF track address information to the buffer.
        TAKES:
            trackAddresses: list of [selector, wheelSide, WheelNumber, sect1, sect2, sect3, sect4, qual, empty]*n_tracks
        """
        for i, trkAddr in enumerate(trackAddresses):
            if i%3==0:
                self.string += ["{id:<6}".format(id='BTRKADDR')]
            self.string += ["{sel:>6} {wheelSide:>6} {wheelNum:>6} {sect1:>6} {sect2:>6} {sect3:>6} {sect4:>6} {qual:>5} {empty:>5}".format(sel=trkAddr[0], wheelSide=trkAddr[1], wheelNum=trkAddr[2], sect1=trkAddr[3], sect2=trkAddr[4], sect3=trkAddr[5], sect4=trkAddr[6], qual=trkAddr[7], empty=trkAddr[8])]
            if (i+1)%3 == 0:
                self.string += ["\n"]

    def writeCaloChannel(self, channel, sums):
        """
        Adds the calo information to the buffer.
        TAKES:
            channel: current channel
            sums: calo sums for current channel (list with length 36)
        """
        self.string += ["CALO{id:<2}".format(id=channel)]
        for csum in sums:
            self.string += ["{calo:>3}".format(calo=csum)]
        self.string += ["\n"]

    def get_full_string(self):
        return self.head + ''.join(self.string)


class TestvectorWriter(object):
    """
    Class (Decorator) that produces testbench files (i.e. what Dinyar uses for testing)
    Giving this class to the ctor of of PatternDumper will let it create these files
    """
    def __init__(self):
        super(TestvectorWriter, self).__init__()
        self.string = []
        self.frameCounter = 0
        self.muonCounter = 0
        self.bxCounter = 0
        self.head = "|BX|"
        for i in range(108):
            self.head += " |{muon:-^14}|".format(muon="Muon({n})".format(n=i))

    def writeMuon(self, mu, mu_type, rank, addIso = False):
        """
        Convert a single ./helpers/muon.Muon object into string
        TAKES:  mu          Muon object
                mu_type     muon type (BMTF, EMTF+/-, OMTF+/-, EIMD, BIMD, OIMD, OUT)
                rank        relative position of the muon (IMD: 0-23, OUT: 0-7, EMTF/OMTF: 0-37, BMTF: 0-35)
                addIso      whether to add isolation info and muon index(should only be done for OUT)
        Adds to string "ID N PT PHI ETA CHARGE CHARGE_VALID QUALITY SORT EMPTY (ISO) (IDX) (TWR)"
        """
        if self.muonCounter == 0:
            self.string += ["\n{bx:0>4}".format(bx=self.bxCounter)]

        self.string += [" {muon:0>16x}".format(muon=mu.bitword)]
        self.muonCounter += 1
        if self.muonCounter == 108:
            self.bxCounter += 1
            self.muonCounter = 0

    def get_full_string(self):
        return self.head + ''.join(self.string)

    def writeTracks(self, tracks, track_type):
        pass

    def writeEventHeader(self, n):
        pass

    def writeBXCounter(self, n):
        pass

    def writeTrackHeadline(self):
        pass

    def writeBMTFTrackAddressHeadline(self):
        pass

    def writeMuonHeadline(self):
        pass

    def writeFrame(self, words, valid, validoverflow):
        pass

    def fill_up(self, n):
        pass

class PatternDumper(object):
    def __init__(self, fname, vhdl_dict, writer_t):
        super(PatternDumper, self).__init__()
        self.fname = fname              # file that is dumped to
        self.frame_dict = {}            # dict for easy access of words
        self.vhdl_dict = vhdl_dict      # vhdl-dict as returned by ../../tools/vhdl.VHDLConfigParser
        self._log = log.init_logging(self.__class__.__name__)
        self._writer = writer_t()       # which writer should be used for dumping?
        self._bxCounter = 0

    def writeEmptyFrames(self, n):
        for i in range(n):
            self._writer.writeFrame([])

    def dump(self, fill = False):
        if fill:
            self._writer.fill_up(1024)

        if hasattr(self._writer, 'reset'): self._writer.reset()

        with open(self.fname, "w") as fobj:
            fobj.write(self._writer.get_full_string())

    def dump_string(self, fill = False):
        if fill:
            self._writer.fill_up(1024)
        # self._writer.reset()
        if hasattr(self._writer, 'reset'): self._writer.reset()

        return self._writer.get_full_string()

    def clear(self):
        self.string = ""

    def writeMuonsToFrames(self, frames, mutype, muons, per_link, link_offset, frame_offset = 0):
        for i, muon in enumerate(muons):
            ilink = i/per_link+self.vhdl_dict[mutype+"_LOW"]+link_offset
            iframe = (i%per_link)*2+frame_offset # 2 padding words
            frames[iframe][ilink] = muon.getLSW()
            frames[iframe+1][ilink] = muon.getMSW()

    def writeCaloToFrames(self, frames, calosums):
        for ieta in range(28):
            idx_low = ieta*36
            for iframe in range(6):
                frame_val = 0
                for l_iphi in range(6): # per frame 6 calo sums encoded
                    idx = idx_low+(iframe*6)+l_iphi
                    frame_val += calosums[idx] << (l_iphi*5)
                frames[iframe][ieta+8] = frame_val


    def writeFrameBasedOutputBX(self, out_muons, imd_muons):
        frames = {}
        for x in range(6):
            frames[x] = [0]*72

        nOutSets = self.vhdl_dict["OUTPUT_MULTIPLIER"]
        nOutChans = self.vhdl_dict["NUM_OUT_CHANS"]

        for i in range(nOutSets):
            self.writeMuonsToFrames(frames, "OUT", out_muons, 2, i*nOutChans, 2)
        self.writeMuonsToFrames(frames, "IMD", imd_muons, 3, (nOutSets-1)*nOutChans)

        for x, frame in frames.iteritems():
            self._writer.writeFrame(frame, ftype="out")

    def writeFrameBasedInputBX(self, bar_muons, fwdp_muons, fwdn_muons, ovlp_muons, ovln_muons, calosums):
        frames = {}
        for x in range(6):
            frames[x] = [0]*72

        self.writeMuonsToFrames(frames, "BMTF", bar_muons, 3, 36)
        self.writeMuonsToFrames(frames, "EMTF_NEG", fwdn_muons, 3, 36)
        self.writeMuonsToFrames(frames, "EMTF_POS", fwdp_muons, 3, 36)
        self.writeMuonsToFrames(frames, "OMTF_POS", ovlp_muons, 3, 36)
        self.writeMuonsToFrames(frames, "OMTF_NEG", ovln_muons, 3, 36)

        if calosums:
            self.writeCaloToFrames(frames, calosums)

        for x, frame in frames.iteritems():
            self._writer.writeFrame(frame, ftype="in")
        self._bxCounter += 1


    def writeMuonGroup(self, muons, mutype, addIso):
        themuid = mutype
        for i, muon in enumerate(muons):
            if mutype == "IMD":
                if i < 4 or i > 19: themuid = "EIMD"
                elif i < 8 or i > 15: themuid = "OIMD"
                else: themuid = "BIMD"
            link = i
            if muon.local_link != -1:
                link = muon.local_link

            self._writer.writeMuon(muon, themuid, link, addIso)


    def writeCaloGroup(self, calosums):
        for iline in range(28):
            idx_low = iline*36
            idx_high = idx_low+36
            self._writer.writeCaloChannel(iline, calosums[idx_low:idx_high])

    def writeTrackGroup(self, muons, track_type):
        tracks = []
        for i, muon in enumerate(muons):
            isEmpty = 0
            if muon.ptBits == 0: isEmpty = 1
            if track_type == 'BTRK':
                trkAddr = muon.trackAddress
                tracks.append([muon.etaBits, muon.globPhiBits, muon.qualityBits, 0, trkAddr[0], trkAddr[1], trkAddr[2], trkAddr[3], trkAddr[4], trkAddr[5], isEmpty])
            else:
                tracks.append([muon.etaBits, muon.globPhiBits, muon.qualityBits, isEmpty])
        self._writer.writeTracks(tracks, track_type)

    def writeBMTFTrackAddressGroup(self, muons):
        trackAddresses = []
        for i, muon in enumerate(muons):
            isEmpty = 0
            if muon.ptBits == 0: isEmpty = 1
            trkAddr = muon.trackAddress
            trackAddresses.append([0, trkAddr[0], trkAddr[1], trkAddr[2], trkAddr[3], trkAddr[4], trkAddr[5], muon.qualityBits, isEmpty])
        self._writer.writeBMTFTrackAddress(trackAddresses)

    def writeMuonBasedInputBX(self, bar_muons, fwdp_muons, fwdn_muons, ovlp_muons, ovln_muons, calosums, addTracks = False, addBXCounter = False):
        if addBXCounter:
            self._writer.writeBXCounter(self._bxCounter)


        if calosums:
            self.addLine("# Calo sums:\n")
            self.writeCaloGroup(calosums)
        try:
            self._writer.writeMuonHeadline()
        except AttributeError:
            self._log.error("You are trying to write muons with the wrong Writer class. Only supports frame-based writing.")
            return
        self.writeMuonGroup(fwdp_muons, "EMTF+", False)
        self.writeMuonGroup(ovlp_muons, "OMTF+", False)
        self.writeMuonGroup(bar_muons, "BMTF", False)
        self.writeMuonGroup(ovln_muons, "OMTF-", False)
        self.writeMuonGroup(fwdn_muons, "EMTF-", False)

        if addTracks:
            self._writer.writeTrackHeadline()
            self._writer.writeBTRKTrackHeadline()
            self.writeTrackGroup(fwdp_muons, "ETRK+")
            self.writeTrackGroup(ovlp_muons, "OTRK+")
            self.writeTrackGroup(bar_muons, "BTRK")
            self.writeTrackGroup(ovln_muons, "OTRK-")
            self.writeTrackGroup(fwdn_muons, "ETRK-")

            #self._writer.writeBMTFTrackAddressHeadline()
            #self.writeBMTFTrackAddressGroup(bar_muons)

        self._bxCounter += 1

    def writeTowerIndices(self, twrs):
        self._writer.string += ["# {typ:<6} {idx:<2} {phi:>5} {eta:>5}\n".format(typ="ID", idx="MU", phi="PHI", eta="ETA")]
        for i, twr in enumerate(twrs):
            self._writer.string += ["{typ:<8} {idx:<2} {phi:>5} {eta:>5}\n".format(typ="TWRIDX", idx=i, phi=twr[0], eta=twr[1])]
        for i in range(len(twrs), 8):
            self._writer.string += ["{typ:<8} {idx:<2} {phi:>5} {eta:>5}\n".format(typ="TWRIDX", idx=i, phi=0, eta=0)]

    def addLine(self, line):
        self._writer.string += [line]

    def writeMuonBasedOutputBX(self, out_muons, imd_muons):
        try:
            self._writer.writeMuonHeadline()
        except AttributeError:
            self._log.error("You are trying to write muons with the wrong Writer class. Only supports frame-based writing.")
            return
        self.writeMuonGroup(imd_muons, "IMD", False)
        self.writeMuonGroup(out_muons, "OUT", True)

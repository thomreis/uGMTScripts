from tools.bithelper import bithlp

class Muon():

    """
    A class capable of interpreting the uGMT emulator and hardware muon representations
    """

    def __init__(self, vhdl_dict, mu_type, bitword=None, obj=None, link=-1, frame=-1, bx=-1, gPhi = None):
        """
        ctor:
        TAKES:
            vhdl_dict   as returned by ../../tools/vhdl.VHDLConstantsParser
            mu_type     either IN (inputs), OUT (outputs), or IMD (intermediates)
            bitword     can be None or a 64bit integer (for HW muons)
            obj         can be None or one of the emulator objects (for emulator muons)
            link        integer representing link the muon was received / is sent (HW only)
            bx          integer indicating the bunch-crossing the muon is associated with
        """

        # get the bit boundaries for the muon quantities
        self.bx = bx

        self.frame = frame
        self.tftype = -1
        self.link = link
        self.local_link = link
        if self.link != -1:
            self.local_link = self.link - 36
            if self.local_link < vhdl_dict["EMTF_POS_HIGH"]:
                self.tftype = 2
                pass
            elif self.local_link < vhdl_dict["OMTF_POS_HIGH"]:
                self.local_link -= vhdl_dict["OMTF_POS_LOW"]
                self.tftype = 1
            elif self.local_link < vhdl_dict["BMTF_HIGH"]:
                self.local_link -= vhdl_dict["BMTF_LOW"]
                self.tftype = 0
            elif self.local_link < vhdl_dict["OMTF_NEG_HIGH"]:
                self.local_link -= vhdl_dict["OMTF_NEG_LOW"]
                self.tftype = 1
            else:
                self.local_link -= vhdl_dict["EMTF_NEG_LOW"]
                self.tftype = 2

        if mu_type == 'IMD' or mu_type == 'OUT':
            bitword_type = 'OUT'
        else:
            bitword_type = 'IN'
        pt_low = vhdl_dict["PT_{t}_LOW".format(t=bitword_type)]
        pt_high = vhdl_dict["PT_{t}_HIGH".format(t=bitword_type)]

        sysign_low = vhdl_dict["SIGN_{t}".format(t=bitword_type)]
        sysign_high = vhdl_dict["VALIDSIGN_{t}".format(t=bitword_type)]

        trackadd_low = 0
        trackadd_high = 0

        qual_low = vhdl_dict["QUAL_{t}_LOW".format(t=bitword_type)]
        qual_high = vhdl_dict["QUAL_{t}_HIGH".format(t=bitword_type)]

        eta_low = vhdl_dict["ETA_{t}_LOW".format(t=bitword_type)]
        eta_high = vhdl_dict["ETA_{t}_HIGH".format(t=bitword_type)]

        phi_low = vhdl_dict["PHI_{t}_LOW".format(t=bitword_type)]
        phi_high = vhdl_dict["PHI_{t}_HIGH".format(t=bitword_type)]

        if bitword_type == "OUT":
            iso_low = vhdl_dict["ISO_OUT_LOW"]
            iso_high = vhdl_dict["ISO_OUT_HIGH"]
            idx_low = vhdl_dict["IDX_OUT_LOW"]
            idx_high = vhdl_dict["IDX_OUT_HIGH"]
        else:
            trackadd_low = vhdl_dict["BMTF_ADDRESS_STATION_4_IN_LOW"] - 2
            trackadd_high = vhdl_dict["BMTF_DETECTOR_SIDE_HIGH"] + 4
            self.trackAddress = [0]*6

        if obj == None and bitword != None:     # for hardware
            self.bitword = bitword
            self.Sysign = bithlp.get_shifted_subword(self.bitword, sysign_low, sysign_high)
            self.etaBits = bithlp.get_shifted_subword(self.bitword, eta_low, eta_high)
            self.etaBits = bithlp.twos_complement_to_signed(self.etaBits, eta_high-eta_low+1)
            self.qualityBits = bithlp.get_shifted_subword(self.bitword, qual_low, qual_high)
            self.ptBits = bithlp.get_shifted_subword(self.bitword, pt_low, pt_high)
            self.phiBits = bithlp.get_shifted_subword(self.bitword, phi_low, phi_high)
            self.globPhiBits = self.phiBits
            if mu_type == "OUT":
                self.Iso = bithlp.get_shifted_subword(self.bitword, iso_low, iso_high)
                self.tfMuonIndex = bithlp.get_shifted_subword(self.bitword, idx_low, idx_high)
            else:
                self.Iso = 0
                self.tfMuonIndex = -1
                if self.local_link != -1:
                    self.globPhiBits = self.calcGlobalPhi(self.ptBits, self.tftype, self.local_link)

            self.rank = 0
            self.globPhiBits = self.phiBits

        elif bitword == None and obj != None:  # for emulator
            if gPhi is not None:
                self.globPhiBits = gPhi
            else:
                self.globPhiBits = obj.hwPhi()
            if bitword_type == "OUT":
                self.Iso = obj.hwIso()
                self.rank = obj.hwRank()
                self.Sysign = obj.hwCharge() + (obj.hwChargeValid() << 1)
                self.tfMuonIndex = obj.tfMuonIndex()

            else:
                self.Iso = 0
                self.tfMuonIndex = -1
                self.rank = 0
                self.Sysign = obj.hwSign() + (obj.hwSignValid() << 1)
                # shift by +1 necessary because of the control bit 31
                sysign_low += 1
                sysign_high += 1
                trackadd_low += 1
                trackadd_high += 1
                self.trackAddress = obj.trackAddress()
                self.tftype = obj.trackFinderType()
                if self.tftype == 1 or self.tftype == 2:
                    self.tftype = 1
                elif self.tftype == 3 or self.tftype == 4:
                    self.tftype = 2
                if gPhi is None:
                    self.globPhiBits = self.calcGlobalPhi(obj.hwPhi(), obj.trackFinderType(), obj.processor())

            self.phiBits = obj.hwPhi()
            self.etaBits = obj.hwEta()
            unsigned_eta = bithlp.twos_complement_to_unsigned(obj.hwEta(), 9)
            unsigned_phi = bithlp.twos_complement_to_unsigned(obj.hwPhi(), 8)
            self.qualityBits = obj.hwQual()
            self.ptBits = obj.hwPt()

            # calculate the bitword to make comparison with HW easy
            self.bitword = (self.ptBits << pt_low)
            self.bitword += (self.qualityBits << qual_low)
            self.bitword += (self.Sysign << sysign_low)
            self.bitword += (unsigned_eta << eta_low)
            self.bitword += (unsigned_phi << phi_low)

            if bitword_type == "OUT" and self.Iso > 0:
                self.bitword += (self.Iso << iso_low)
            if mu_type == "OUT" and self.tfMuonIndex > 0:
                self.bitword += (self.tfMuonIndex << idx_low)

            if self.tftype == 0:
                # shift by +1 necessary because of the control bit 31
                self.bitword += self.trackAddress[0] << vhdl_dict["BMTF_DETECTOR_SIDE_LOW"] + 1
                self.bitword += self.trackAddress[1] << vhdl_dict["BMTF_WHEEL_NO_IN_LOW"] + 1
                self.bitword += self.trackAddress[2] << vhdl_dict["BMTF_ADDRESS_STATION_1_IN_LOW"] + 1
                self.bitword += self.trackAddress[3] << vhdl_dict["BMTF_ADDRESS_STATION_2_IN_LOW"] + 1
                self.bitword += self.trackAddress[4] << vhdl_dict["BMTF_ADDRESS_STATION_3_IN_LOW"] + 1
                self.bitword += self.trackAddress[5] << vhdl_dict["BMTF_ADDRESS_STATION_4_IN_LOW"] + 1
            elif self.tftype == 1:
                self.bitword += self.trackAddress[0] << trackadd_low
            elif self.tftype == 2:
                self.bitword += self.trackAddress[0] << trackadd_low

            #print '{mtype} {tftype} bitword  {word:0>16x}, {bit:x}'.format(mtype=mu_type, tftype=self.tftype, word=self.bitword, bit=self.qualityBits)

    def setBunchCounter(self, n_mu):
        if n_mu == 1:
            self.bitword += ((self.bx & 0b1) << 31)
            # since it is the second bit only need to shift by 62 instead of 63
            self.bitword += (self.bx & 0b10) << 62
        if n_mu == 2:
            self.bitword += (((self.bx & 0b100) >> 2) << 31)
        if self.bx == 0 and n_mu == 0:
            self.bitword += 1 << 31
        pass

    def getBx(self):
        """
        returns the assiciated bunch-crossing
        """
        return self.bx

    def getRank(self):
        return self.rank

    def getLSW(self):
        mask = 0xffffffff
        return (self.bitword & mask)

    def getMSW(self):
        return (self.bitword >> 32)

    def encode_phi(self, phi):
        """
        As the hardware expects a control bit on position 31 and phi
        goes across the word boundary we need to put a zero in the
        middle.
        """
        mask_lsw = bithlp.get_mask(0, 5)  # 0-5 for phi
        lsw = int(phi) & mask_lsw
        msw = int(phi) >> 6
        encoded_phi = lsw + (msw << 7)
        return encoded_phi

    def decode_phi(self, xlow, xup):
        """
        for the HW represntation: the phi variable goes across 32bit word boundary
        at the boundary a control bit is reserved
        """
        # this is a specialized function because phi reaches over the word boundary
        ctrl_mask = bithlp.get_mask(31, 31)
        # +1 because dinyar shaves off the 32nd bit in the vhdl-file
        raw_mask = bithlp.get_mask(xlow, xup+1)
        # mask is 11110111111 for phi
        mask = raw_mask ^ ctrl_mask
        raw_val = self.bitword & mask
        raw_val = raw_val >> xlow
        lsw_mask = bithlp.get_mask(0, 5)
        msw_mask = bithlp.get_mask(7, 10)
        val = (raw_val & lsw_mask) + ((raw_val & msw_mask) >> 1)
        return val

    def calcGlobalPhi(self, locPhi, tftype, processor):
        """
        Calculate the global phi from the local phi of the TF candidate, the TF type, and the processor number
        """
        globPhi = 0
        if tftype == 0: # BMTF
            # each BMTF processor corresponds to a 30 degree wedge = 48 in int-scale
            globPhi = processor * 48 + locPhi
            # first processor starts at CMS phi = -15 degrees...
            globPhi += 576 - 24
            # handle wrap-around (since we add the 576-24, the value will never be negative!)
            globPhi %= 576
        else:
            # all others correspond to 60 degree sectors = 96 in int-scale
            globPhi = processor * 96 + locPhi
            # first processor starts at CMS phi = 15 degrees... Handle wrap-around with %: Add 576 to make sure the number is positive
            globPhi = (globPhi + 600) % 576
        return globPhi


#!/bin/bash
CONN=/home/utcausr/mp7sw/connection_files/connections-b40.xml
address=ugmt
root_path=/home/utcausr/uGMTScripts/ugmt_patterns/zs_test
work_path=$root_path/single_run_`date +%Y%m%d_%H%M%S`
tmp_path=$root_path/tmp
ROMENU_FILE=$root_path/../mp7_test/ugmt_ro_zs_menu.py
#ROMENU_FILE=$root_path/../mp7_test/cppf_ro_zs_menu.py

e=0-71

# setup work environment
mkdir -p $tmp_path
rm $tmp_path/*
mkdir $work_path
mkdir $work_path/error_events

#printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - /home/utcausr/test_patterns/TT_13TeV_RunIIFall15DR76-25nsFlat10to25TSG/rx_TT_13TeV_RunIIFall15DR76-25nsFlat10to25TSG_18.zip | gzip -dc > $tmp_path/uncompressed.txt
printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - /home/utcausr/test_patterns/TT_TuneCUETP8M1_13TeV/rx_TT_TuneCUETP8M1_13TeV_8.zip | gzip -dc > $tmp_path/uncompressed.txt

mp7butler.py -c $CONN reset $address --clksrc=internal # comment this line if the ZS is configured with SWATCH
#mp7butler.py -c $CONN reset $address --clksrc=external # comment this line if the ZS is configured with SWATCH

mp7butler.py -c $CONN -v xbuffers $address tx PlayOnce -e $e --inject file://$tmp_path/uncompressed.txt 
mp7butler.py -c $CONN txmgts -e $e --loopback --pattern=none $address
mp7butler.py -c $CONN rxmgts -e $e $address
mp7butler.py -c $CONN rxalign -e $e --to-bx 7,5 $address
# MP7 FW 2.2.1 has a bug that only a limited number of links is supported with ZS.
# The limit seems to be 46 which means that only 6 of 8 intermediate muons can be in the RO
mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 0-3,24-26 --rxBank 1 --rx 36-71 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
#mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 0-71 --rxBank 1 --rx 0-71 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
#mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 1 --rxBank 1 --rx 0-3 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
#mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 31 --rxBank 1 --rx 50 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
mp7butler.py -c $CONN rosetup $address --internal --bxoffset 2
#mp7butler.py -c $CONN rosetup $address --bxoffset 2
mp7butler.py -c $CONN romenu $address $ROMENU_FILE standardMenu
mp7butler.py -c $CONN zsmenu $address $ROMENU_FILE zsStandardMenu # comment this line if the ZS is configured with SWATCH
#bash setup_zs.sh

echo Pattern:  single >> $work_path/summary.txt
echo Bx:       Status: >> $work_path/summary.txt

#for i in {14..132}
for i in {16..16}
do
  mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 0 &>/dev/null
  mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $tmp_path/output_nozs.dat &> $tmp_path/roevents_nozs.txt

  mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
  mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $tmp_path/output_zs.dat &> $tmp_path/roevents_zs.txt

  echo BX $i &>> $work_path/zs_status.txt
  mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.ctrl.val_mode | grep readout.readout_zs &>> $work_path/zs_status.txt
  mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.info | grep readout.readout_zs &>> $work_path/zs_status.txt
  mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.stat | grep readout.readout_zs &>> $work_path/zs_status.txt

  python $root_path/check_zs_mask_new.py $tmp_path/output_nozs.dat $tmp_path/output_zs.dat $work_path $i single
  echo Bx $i/132 complete
done

python zs_summary.py $work_path

tail -4 $work_path/summary.txt
echo Test completed

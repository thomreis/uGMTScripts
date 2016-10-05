#!/bin/bash
CONN=/home/utcausr/mp7sw/connection_files/connections-b40.xml
address=ugmt-zs
root_path=/home/utcausr/zsvalidation/uGMTScripts/ugmt_patterns

mp7butler.py -c $CONN -c $CONN reset $address --clksrc=internal

mp7butler.py -c $CONN -v xbuffers $address tx PlayOnce -e 36-71 --inject file://$root_path/rx_tmp_new.txt 
mp7butler.py -c $CONN txmgts -e 36-71 --loopback --pattern=none $address
mp7butler.py -c $CONN rxmgts -e 36-71 $address
mp7butler.py -c $CONN rxalign -e 36-71 --to-bx 7,5 $address
mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 0-3 --rxBank 1 --rx 36-71 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
mp7butler.py -c $CONN rosetup $address --internal --bxoffset 2
mp7butler.py -c $CONN romenu $address /home/utcausr/uGMTScripts/ugmt_patterns/mp7_test/ugmt.py standardMenu
mp7butler.py -c $CONN zsmenu $address /home/utcausr/uGMTScripts/ugmt_patterns/mp7_test/ugmt.py zsStandardMenu

rm $root_path/logs/summary.txt
rm $root_path/logs/failure_log.txt

echo Bx:	Status:  >> $root_path/logs/summary.txt

for i in {14..132}
do
	mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 0 &>/dev/null
	mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $root_path/output_nozs.dat &>/dev/null

	mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
	mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $root_path/output_zs.dat &>/dev/null
	
	python check_zs_mask.py output_nozs.dat output_zs.dat $i 'test'
	echo Bx $i/132 complete
done
echo Complete

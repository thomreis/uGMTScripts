#!/bin/bash
CONN=/home/utcausr/mp7sw/connection_files/connections-b40.xml
address=ugmt4_0_0_pre1
root_path=/home/utcausr/uGMTScripts/ugmt_patterns/zs_test
patterns=$root_path/paths/rx_paths.txt
e=0-71
if [ -z ${1+x} ]; then 
	valid=nv
else
	valid=$1
fi

#make list of files to unpack and inject and save it in paths/rx_paths.txt
python $root_path/paths/lists_tx_rx.py

rm $root_path/logs/summary.txt
rm $root_path/logs/failure_log.txt
rm $root_path/error_events/*
rm enable_check.txt

#loop over $patterns
while read rxfile
do
	rm $root_path/uncompressed.txt
		
	#magic method to unpack files zipped in python
	printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - $rxfile | gzip -dc > $root_path/uncompressed.txt	
	
	mp7butler.py -c $CONN reset $address --clksrc=internal
	
	#inject uncompressed rx file
	mp7butler.py -c $CONN -v xbuffers $address tx PlayOnce -e $e --inject file://$root_path/uncompressed.txt 
	mp7butler.py -c $CONN txmgts -e $e --loopback --pattern=none $address
	mp7butler.py -c $CONN rxmgts -e $e $address
	mp7butler.py -c $CONN rxalign -e $e --to-bx 7,5 $address
	mp7butler.py -c $CONN easylatency $address --txBank 2 --tx 0 --rxBank 1 --rx 36-71 --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12
	mp7butler.py -c $CONN rosetup $address --internal --bxoffset 2
	mp7butler.py -c $CONN romenu $address $root_path/../mp7_test/ugmt.py standardMenu
	mp7butler.py -c $CONN zsmenu $address $root_path/../mp7_test/ugmt.py zsStandardMenu
	
	echo Pattern:	$rxfile >> $root_path/logs/summary.txt
	echo Bx:	Status: >> $root_path/logs/summary.txt
	
	for i in {14..132}
	do
		#disable zs menu
		mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 0 &>/dev/null
		mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $root_path/output_nozs.dat &>/dev/null
		
		#enable zs menu and check whether it is enabled (there were some problems with this)
		mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
		en="$(mp7butler.py -c $CONN -l inspect $address readout.readout_zs.csr.ctrl.en)"

		until [ ${en:(-1)} == 1 ]
		do
			mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &>/dev/null
			#mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.ctrl.val_mode
			en="$(mp7butler.py -c $CONN -l inspect $address readout.readout_zs.csr.ctrl.en)"
			echo Zero suppression status ${en:(-1)}
		done

		mp7butler.py -c $CONN -v roevents $address 1 --bxs $i --outputpath $root_path/output_zs.dat &>/dev/null

		#choose normal or validation mode
		if [ $valid == 'v' ]; then
			python $root_path/check_zs_mask_valid.py output_nozs.dat output_zs.dat $i $rxfile
		else
                	python $root_path/check_zs_mask.py output_nozs.dat output_zs.dat $i $rxfile
		fi
		echo Bx $i/132 complete
	done
	echo Pattern $rxfile completed
done < $patterns

#script to do short summary in logs/summary.txt file
python $root_path/zs_summary.py

echo Completed

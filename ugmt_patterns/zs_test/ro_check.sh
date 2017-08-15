#!/bin/bash
CONN=/home/utcausr/mp7sw/connection_files/connections-b40.xml
address=ugmt
root_path=/home/utcausr/uGMTScripts/ugmt_patterns/zs_test
work_path=$root_path/ro_check_`date +%Y%m%d_%H%M%S`
tmp_path=$root_path/tmp
ROMENU_FILE=$root_path/../mp7_test/ugmt_ro_zs_menu.py
#ROMENU_FILE=$root_path/../mp7_test/cppf_ro_zs_menu.py

txstart=0
txend=1
#txend=31
rxstart=0
rxend=1
#rxend=37

e=0-71

# setup work environment
mkdir -p $tmp_path
rm $tmp_path/*
mkdir $work_path

printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - /home/utcausr/test_patterns/TT_13TeV_RunIIFall15DR76-25nsFlat10to25TSG/rx_TT_13TeV_RunIIFall15DR76-25nsFlat10to25TSG_18.zip | gzip -dc > $tmp_path/uncompressed.txt

declare -A matrix

irx=0
for rx in $(eval echo "{$rxstart..$rxend}")
do
	itx=0
	for tx in $(eval echo "{$txstart..$txend}")
	do
		mp7butler.py -c $CONN reset $address --clksrc=internal &> /dev/null

		mp7butler.py -c $CONN -v xbuffers $address tx PlayOnce -e $e --inject file://$tmp_path/uncompressed.txt &> /dev/null
		mp7butler.py -c $CONN txmgts -e $e --loopback --pattern=none $address &> /dev/null
		mp7butler.py -c $CONN rxmgts -e $e $address &> /dev/null
		mp7butler.py -c $CONN rxalign -e $e --to-bx 7,5 $address &> /dev/null

		mp7butler.py -c $CONN easylatency $address --txBank 2 --tx $tx --rxBank 1 --rx $rx --algoLatency 27 --masterLatency 37 --rxExtraFrames 12 --txExtraFrames 12 &> /dev/null

		mp7butler.py -c $CONN rosetup $address --internal --bxoffset 2 &> /dev/null
		mp7butler.py -c $CONN romenu $address $ROMENU_FILE standardMenu &> /dev/null
		mp7butler.py -c $CONN zsmenu $address $ROMENU_FILE zsStandardMenu &> /dev/null
		mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 1 &> /dev/null
		#mp7butler.py -c $CONN write $address readout.readout_zs.csr.ctrl.en 0 &> /dev/null

		mp7butler.py -c $CONN -v roevents $address 1 --bxs 16 &> $tmp_path/roevent.txt 
                tail -n 1 $tmp_path/roevent.txt | grep "fifo is empty" &> /dev/null
                result=$?
                matrix[$irx,$itx]=$result
		echo Rx $rx / Tx $tx: $result

		echo Rx $rx / Tx $tx: $result &>> $work_path/zs_status.txt
                mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.stat | grep readout.readout_zs &>> $work_path/zs_status.txt
		echo Rx $rx / Tx $tx: $result &>> $work_path/zs_status.txt
                mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.stat | grep readout.readout_zs &>> $work_path/zs_status.txt
		echo Rx $rx / Tx $tx: $result &>> $work_path/zs_status.txt
                mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.stat | grep readout.readout_zs &>> $work_path/zs_status.txt
		echo Rx $rx / Tx $tx: $result &>> $work_path/zs_status.txt
                mp7butler.py -c $CONN inspect $address readout.readout_zs.csr.stat | grep readout.readout_zs &>> $work_path/zs_status.txt
		echo "*****************" &>> $work_path/zs_status.txt
		itx=$itx+1
	done
	irx=$irx+1
done

# print the results matrix
f1="%3s"
f2=" %2s"

printf "$f1" '' >> $work_path/result.txt
for tx in $(eval echo "{$txstart..$txend}")
do
	printf "$f2" $tx >> $work_path/result.txt
done
printf "$f2\n" "Tx" >> $work_path/result.txt

irx=0
for rx in $(eval echo "{$rxstart..$rxend}")
do
	itx=0
	printf "$f1" $rx >> $work_path/result.txt
	for tx in $(eval echo "{$txstart..$txend}")
	do
		printf "$f2" ${matrix[$irx,$itx]} >> $work_path/result.txt
		itx=$itx+1
	done
	irx=$irx+1
	printf "\n" >> $work_path/result.txt
done
printf "$f1\n" "Rx" >> $work_path/result.txt

cat $work_path/result.txt

mp7butler.py -c $CONN -v rodiagnostic $address &> $work_path/rodiagnostic.txt 

echo Test completed

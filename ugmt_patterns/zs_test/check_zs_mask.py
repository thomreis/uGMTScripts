import sys

def extract_name( path ):
	base = path.strip().split( '.' )[0].strip()
	return base.split( '/' )[-1].strip()

def put_mask( muon, mask ): #muon in hex, mask in dec
	if (int( muon, 16 ) & mask ) == 0:
		return False
	else:
		return True

#from file make list containing only muon data (skip main header and termination
def read_mp7_lines( f ):
	lines = list()
	for line in f:
		lines.append( line.strip() )
	return lines[10:-4]

def mask( nozs_path, masks ):
	try:
		with open( nozs_path, 'r' ) as nozs_f:
			nozs_lines = read_mp7_lines( nozs_f )
			block_ptr = 0
			zs_flag = False
			ret = list()
			l = len( nozs_lines )
			while block_ptr < l:
				data_length = int( nozs_lines[block_ptr][11:13], 16 )	
				#do nothing if data length is not multiple o 6
				if data_length % 6:
					block_ptr += 1
					continue
				#choose input or output mask
				io = int( nozs_lines[block_ptr][9:11], 16 ) % 2
				#apply mask and if there are muons add them to return list
				for i in range( data_length ):
					if put_mask( nozs_lines[block_ptr + i + 1][7:].strip(), masks[io][i % 6] ):
						zs_flag = True
						break
				if zs_flag:
					zs_flag = False
					ret += nozs_lines[block_ptr : block_ptr + data_length + 1]
				#move to the next data block
				block_ptr += data_length + 1
			return ret
	except IOError:
		print 'Could not open nozs file'
		quit()
	
def compare( nozs_path, zs_path, zs_mask, work_path, bx, pattern ):
	try:
		failure_log = open( work_path + 'failure_log.txt', 'a+' )
		summ = open( work_path + 'summary.txt', 'a+' )
		with open( zs_path, 'r' ) as zs_f:
			zs_line = read_mp7_lines( zs_f )
			failure_flag = False

			try:
				if zs_line[-1][7:].strip() == '0xffffffff':
					zs_line = zs_line [:-1]
			except IndexError:
				print 'No data in zs file. Only 0x0 muons'
				print >>summ, bx.zfill( 4 ), '\t1'
				failure_log.close()
                		summ.close()
				quit()
			#print len( zs_line ), '\t',  len( zs_mask )
			if len( zs_line ) == len( zs_mask ):
				l = len( zs_line )
				block_ptr = 0
				while block_ptr < l:
					data_length = int( zs_line[block_ptr][11:13], 16 )
					#compare zs and nozs lists
					for i in range( data_length + 1 ):
						if zs_line[block_ptr + i][7:].strip() == zs_mask[block_ptr + i][7:].strip():
							continue
						else:
							failure_flag = True
					block_ptr += data_length + 1
				if failure_flag:
					failure_flag = False
					print 'Zero suppression failed'
					print >>summ, bx.zfill( 4 ), '\t0'
					print >>failure_log, '\nPattern:\t', pattern, '\nBx:\t', bx.zfill( 4 ), '\nMasked:\t\t\tZero suppressed:'
					for i in range( l ):
						if zs_mask[i][7:].strip() == zs_line[i][7:].strip():
							print >>failure_log, zs_mask[i], '\t', zs_line[i]
						else:
							print >>failure_log, ' ', zs_mask[i], '\t ', zs_line[i]
				else:
					print >>summ, bx.zfill( 4 ), '\t1'
			else:
				print >>summ, bx.zfill( 4 ), '\t0' 
				print >>failure_log, '\nPattern:\t', pattern, '\nBx:\t', bx.zfill( 4 ), '\nMasked and zero suppressed files not the same size'
				#copy files to error_events dir
				try:
					nozs_file = open( nozs_path, 'r' )
					zs_file = open( zs_path )
					with open( work_path + 'error_events/nozs_' + bx + '_' + pattern + '.txt', 'w' ) as nozs_error:
						nozs_error.write( nozs_file.read() )
					with open( work_path + 'error_events/zs_' + bx + '_' + pattern + '.txt', 'w' ) as zs_error:
                                        	zs_error.write( zs_file.read() )
					nozs_file.close()
					zs_file.close()
				except IOError:
					print 'Could not open data files'
		failure_log.close()
		summ.close()
			
	except IOError:
		print 'Could not open zs file'
		quit()

if __name__ == '__main__':

	mask_i = [ 0x1ff, 0x0 ]*3
	mask_o = [ 0x3fc00, 0x0 ]*3

	#second argument is list of masks, first mask is input and second one is output
	zs_masked = mask( sys.argv[1], [ mask_i, mask_o ] )
	compare( sys.argv[1], sys.argv[2], zs_masked,  sys.argv[3]+'/', sys.argv[4], extract_name( sys.argv[5] ) )

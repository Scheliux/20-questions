from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import sys
import struct
import random
import math
import time


def main(argv):
	# argument check
	if len(argv) < 2:
		print("**At least 2 arguments needed**")
		exit(1)
		
	server_addr = (argv[1], int(argv[2]))
	packer = struct.Struct("1s I")
	
	with socket(AF_INET, SOCK_STREAM) as client:
		client.connect(server_addr)
		
		max_num = 100
		interval = round(max_num / 2)
		i = interval
		
		unp_data = [b'0']
		
		op = "<"
		while unp_data[0].decode() != "V" and unp_data[0].decode() != "K" and unp_data[0].decode() != "Y":
			# send / recv
			data = (op.encode(), int(i))
			packed_data = packer.pack(*data)
			
			client.sendall(packed_data)
			data = client.recv(packer.size)
			unp_data = packer.unpack(data)
			
			if interval != 0:
				if unp_data[0].decode() == "I":
					i -= interval
				else:
					i += interval
			else:
				if unp_data[0].decode() == "I":
					i -= 1
				op = "="
			
			interval = round(interval/2)
			
			print(str(unp_data[0].decode()) + " " + str(unp_data[1]))
			
			time.sleep(random.randint(1,5))
		
		client.close()
		exit(0)

if __name__ == "__main__":
	main(sys.argv)

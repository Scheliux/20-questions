from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import sys
import struct
import random

def main(argv):
	# argument check
	if len(argv) < 2:
		print("**At least 2 arguments needed**")
		exit(1)
		
	server_addr = (argv[1], int(argv[2]))
	packer = struct.Struct("1s I")
	
	with socket(AF_INET, SOCK_STREAM) as server:
		server.bind(server_addr)
		server.listen(1)
		server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		
		sockets = [ server ]
		
		while True:
			num = random.randint(1, 100)
			is_game_over = False
		
			while True:
				if len(sockets) == 1 and is_game_over:
					break
					
				r, w, e = select(sockets, [], [], 1)
				
				if not (r or w or e):
					continue
				
				for s in r:
					if s is server:
						# client joins
						client, client_addr = s.accept()
						sockets.append(client)
						print("Client joined", client_addr)
					else:
						data = s.recv(packer.size)
						# if 0 byte then the client left
						if not data:
							sockets.remove(s)
							s.close()
							print("Client left")
						else:
							unp_data = packer.unpack(data)
							print("Unpack:", unp_data)
							
							resp = ""
							
							if not is_game_over:
								if unp_data[0].decode() == "=":
									if unp_data[1] == num:
										# win
										resp = "Y"
										is_game_over = True
									else:
										# lose
										resp = "K"
								else:
									if eval(str(num) + unp_data[0].decode() + str(unp_data[1])):
										# true
										resp = "I"
									else:
										# false
										resp = "N"
							else:
								# game over
								resp = "V"
							
							data = (resp.encode(), 0)
							packed_data = packer.pack(*data)			
							s.sendall(packed_data)

if __name__ == "__main__":
	main(sys.argv)

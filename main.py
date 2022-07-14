import sys, os
sys.path.insert(1, os.getcwd() + '\\Scripts')
import tor
from color import *

def main():
	banner = r"""
	                                                  
			$$$$$$$$\  $$$$$$\  $$$$$$$\  
			\__$$  __|$$  __$$\ $$  __$$\ 
			   $$ |   $$ /  $$ |$$ |  $$ |
			   $$ |   $$ |  $$ |$$$$$$$  |
			   $$ |   $$ |  $$ |$$  __$$< 
			   $$ |   $$ |  $$ |$$ |  $$ |
			   $$ |    $$$$$$  |$$ |  $$ |
			   \__|    \______/ \__|  \__|"""
	banner2 = r"""                                
	                                                          _            
	                                                         (_)           
	  _ __   _ __  ___ __  __ _   _   ___   ___  _ __ __   __ _   ___  ___ 
	 | '_ \ | '__|/ _ \\ \/ /| | | | / __| / _ \| '__|\ \ / /| | / __|/ _ \
	 | |_) || |  | (_) |>  < | |_| | \__ \|  __/| |    \ V / | || (__|  __/
	 | .__/ |_|   \___//_/\_\ \__, | |___/ \___||_|     \_/  |_| \___|\___|
	 | |                       __/ |                                       
	 |_|                      |___/                                        

	"""
	print(fy + sd + banner + sb + fr + banner2)

	torobj = tor.Tor()
	try:
		torobj.connect()
	except Exception as e:
		torobj.terminate()
		raise e
if __name__ == '__main__':
	main()
	
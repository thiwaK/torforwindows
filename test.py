import sys, os
sys.path.insert(1, os.getcwd() + '\\Scripts')
import tor

torobj = tor.Tor()
try:
	torobj.connect()
except Exception as e:
	torobj.terminate()
	raise e

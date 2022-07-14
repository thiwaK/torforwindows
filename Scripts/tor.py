
from stem import Signal
from stem.control import Controller
from subprocess import Popen, PIPE
from random import randint
import requests
import socks
import socket
import json
import urllib3
import os
import re
import time
import sys
from process import ps as Process
from color import *

class Tor():

	def __init__(self):

		sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + " Initiating\n")

		self.SOCKS5_PROXY_PORT = 9050
		self.SOCKS5_PROXY_HOST = '127.0.0.1'
		self.tor_data_dir = os.getcwd() + "\\Data\\Tor"
		self.tor_control_port = 9051
		self.key_length = 32

		self.tor_controler = None
		self.torexe = os.getcwd() + '\\Tor\\tor.exe'
		self.torrc = self.tor_data_dir + '\\torrc'
		geoip = self.tor_data_dir + '\\geoip'
		geoip6 = self.tor_data_dir + '\\geoip6'
		onionauth = self.tor_data_dir + '\\onion-auth'

		with open(self.torrc, 'w') as f:
			f.write(f"\nClientOnionAuthDir {onionauth}\n")
			f.write(f"ControlPort {self.tor_control_port}\n")
			f.write(f"DataDirectory {self.tor_data_dir}\n")
			f.write(f"GeoIPFile {geoip}\n")
			f.write(f"GeoIPv6File {geoip6}\n")
			f.write(f"SocksPort {self.SOCKS5_PROXY_PORT}\n")

		self.url1 = 'http://httpbin.org/ip'
		self.url2 = 'http://ip-api.com/json/'
		self.url3 = 'http://ipecho.net/plain'

		http = urllib3.PoolManager()
		r = http.request('GET',self.url1,preload_content=False)
		self.default_ip = json.loads(r.read().strip())['origin']

		# Set up a proxy
		socks.set_default_proxy(socks.SOCKS5, self.SOCKS5_PROXY_HOST, self.SOCKS5_PROXY_PORT)
		socket.socket = socks.socksocket


		self.__generateRandomPassword()

	def connect(self):

		if os.path.isfile(self.tor_data_dir + '\\state'):
			sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + " Remove Old Circuits\n")
			os.remove(self.tor_data_dir + '\\state')

		try:
			self.ps = Process()
			self.ps.tor_obj = self

			sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + " Start Service\n")
			cmd = ["Proxifier\\Proxifier.exe"]
			self.ps.runBackground(cmd, "proxifier")

			cmd = [self.torexe,
			"-f", self.torrc, 
			"HashedControlPassword", self.hash_key,
			'Log', 'notice']
			self.ps.runBackground(cmd, "tor")

			self.ps.monitorProcess("tor")

		except KeyboardInterrupt:
			sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fr + " Interupted by user\n")
			self.ps.terminate()

	def __generateRandomPassword(self):
		sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + f" Generate random key : {self.key_length} bytes\n")

		chars = "1234567890`=-~+_)(*&^%$#@!,./;'[]\\<>?:{}|-+zxcvbnmlkjhgfdsaqwertyuiopMNBVCXZASDFGHJKLPOIUYTREWQ*"
		# chars = "1234567890zxcvbnmlkjhgfdsaqwertyuiopMNBVCXZASDFGHJKLPOIUYTREWQ"
		key = ""
		for x in range(self.key_length):
			key += chars[randint(0, len(chars)-1)]
		cmd = [self.torexe, '--hash-password', key, "Log", "debug"]
		p = Popen(cmd, stdout=PIPE, text=True, shell=False)
		for x in p.stdout.read().split('\n'):
			a = re.findall(r"([a-fA-F\d]{58})", x)
			if a:
				self.str_key = key
				self.hash_key = "16:" + a[0]

	def renewConnection(self):
		sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + " Change Identity\n")
		response_1 = requests.get(self.url3)
		self.tor_controler.authenticate(self.str_key)
		self.tor_controler.signal(Signal.NEWNYM)
		response_2 = requests.get(self.url3)
		

		http = urllib3.PoolManager()
		r = http.request('GET','http://httpbin.org/ip',preload_content=False)
		response_3 = r.read()

		print(f"	| Old     : {response_1.text.strip()}")  
		print(f"	| Current : {response_2.text.strip()}")
		print(f"	| Default : {self.default_ip}")

	def getProxy(self):
		http_proxy  = f"http://{self.SOCKS5_PROXY_HOST}:{self.SOCKS5_PROXY_PORT}"
		https_proxy = f"https://{self.SOCKS5_PROXY_HOST}:{self.SOCKS5_PROXY_PORT}"
		proxyDict = { 
			  "http"  : http_proxy, 
			  "https" : https_proxy
		}

		return proxyDict
	
	def getVpnDetails(self):

		response = requests.get(self.url2)
		data = json.loads(response.text.strip())

		if data['status'] == 'success':
			data_set = {'country':data['country'], 'city':data['city'], 'ip':data['query'], 'timezone':data['timezone'], 'isp':data['isp']}


		# from stem import CircStatus
		# self.tor_controler.authenticate(self.str_key)

		# for circ in sorted(self.tor_controler.get_circuits()):
		# 	if circ.status != CircStatus.BUILT:
		# 		continue

		# 	print("Circuit %s (%s)" % (circ.id, circ.purpose))
		# 	for i, entry in enumerate(circ.path):
		# 	  div = '+' if (i == len(circ.path) - 1) else '|'
		# 	  fingerprint, nickname = entry

		# 	  desc = self.tor_controler.get_network_status(fingerprint, None)
		# 	  address = desc.address if desc else 'unknown'

		# 	  print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))

		sys.stdout.write("\n")
		sys.stdout.write(sb + fy + "            Default IP   " + sb + fg + self.default_ip + '\n')
		sys.stdout.write(sb + fy + "            Current IP   " + sb + fg + data['query'] + '\n')
		sys.stdout.write(sb + fy + "            IP Location  " + sb + fg + data['country'] + ' ' + data['city'] + '\n')
		sys.stdout.write(sb + fy + "            ISP          " + sb + fg + data['isp'] + '\n')

	def getTorSession(self):
		self.session = requests.session()
		self.session.proxies = {}
		self.session.proxies['http'] = f'socks5h://{self.SOCKS5_PROXY_HOST}:{self.SOCKS5_PROXY_PORT}'
		self.session.proxies['https'] = f'socks5h://{self.SOCKS5_PROXY_HOST}:{self.SOCKS5_PROXY_PORT}'
		return session

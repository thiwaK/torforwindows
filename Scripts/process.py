from subprocess import Popen, PIPE
import os
import re
import time
import sys
import psutil
from color import *

class ps:

	tor_obj = None

	processes = [] 
	# hold subprocess.popen objects

	main_process = None 
	# if this process has killed, other background processess will be kills soon.
	# monitoring process name is used as the default.

	def __checkPID(self, pname):
		'''check if the process associated with pname still running'''

		for process in self.processes:
			if process[1] == pname:
				if psutil.pid_exists(process[0].pid):
				    return True
				else:
				    return False
		return None
	
	def __print(self, text, type='i'):
		
		if text[-1] != '\n':
			text += '\n'

		if type == 'i': sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fw + text)
		if type == 'w': sys.stdout.write(fy + sd + "["+time.strftime("%H:%M:%S")+"] " + sd + fy + text)
		if type == 'e': sys.stdout.write(fr + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fr + text)

	def runBackground(self, cmd, pname):
		'''run given command as a background process assigning pname as identifier'''
		logname = f"Data\\App\\log_{pname}.txt"
		logwritehandler = open(logname, 'w+')
		p = Popen(cmd, stderr=logwritehandler, stdout=logwritehandler, universal_newlines=True, text=True, shell=False)
		self.processes.append((p, pname))

	def __killAllBackroundProcessess(self):
		'''kill all background processess'''
		is_all_killed = 1
		for process, pname in self.processes:
			if self.__checkPID(pname):
				self.__print(f" [{pname}] StillRunning. Send Kill Signal", 'w')
				process.terminate()
				time.sleep(.3)
				if self.__checkPID(pname):
					self.__print(f" [{pname}] UnableToTerminate", 'e')
					is_all_killed = 0
				else:
					self.__print(f" [{pname}] Terminated")
			else:
				self.__print(f" [{pname}] DNE")

		if is_all_killed:sys.stdout.write(fc + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fm + " Successfully Terminated")
		else:sys.stdout.write(fr + sd + "["+time.strftime("%H:%M:%S")+"] " + sb + fr + " Termination not success")

	def __getLog(self, pname):
		'''return file object of log associated with given process name'''
		logname = f"Data\\App\\log_{pname}.txt"
		log = open(logname, 'r+')
		return log

	def terminate(self):

		# if self.__checkPID(self.main_process):
		# 	self.__print(f" [{self.main_process}] Main Process StillRunning",'w')
		self.__killAllBackroundProcessess()

	def monitorProcess(self, pname):
		'''monitor the given background process'''
		
		is_process_dead = 0
		self.main_process = pname
		log = self.__getLog(pname)
		
		while 1:
			line = log.readline()
			if line != '':
				if line == '\n':
					sys.stdout.write('\n')
				elif '[notice]' in line:
					line = line.split('[notice]')[1]
					
					if 'Bootstrapped' in line:
						line = fw + sb + line.split('% (')[0] + '% ' + fw + sd + '(' +line.split('% (')[1]
						self.__print(line)

					elif 'Parsing' in line or 'Tor can\'t help' in line:
						continue

					elif 'Tor ' in line:
						line = line[0:12]
						self.__print(line)

					elif 'Have tried resolving or connecting to address' in line:
						self.__print(line, 'e')
					
					else:
						self.__print(line)

					if 'Done' in line:
						self.tor_obj.getVpnDetails()
				else:
					self.__print(line)

			if is_process_dead:
				if line == None or line == '':
					log.close()
					break
			
			elif not self.__checkPID(self.main_process):
				is_process_dead = 1
				
			time.sleep(.1)
		self.__killAllBackroundProcessess()


# cmd = ['netstat', '-a']
# cmd2 = ['ping', 'localhost', '-n', '3']
# my = A()

# my.runBackground(['ping', 'localhost', '-n', '3'], "A")
# my.runBackground(['ping', 'localhost', '-n', '10'], "B")
# my.runBackground(['ping', 'localhost', '-n', '5'], "TOR")
# my.monitorProcess("TOR")
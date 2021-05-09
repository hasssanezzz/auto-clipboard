import time
import sys
import os
import pyperclip
import shutil
import win32gui, win32con

SLEEP_TIME = 0.3
KILL_COMMAND = 'kill-monitor'

# <shortcut>: <command>
COMMANDS = {
	"kill-monitor": "<this will kill the script>",
	# opens windows calculator
	"m-calc": "calc",
	# opens notepad
	"m-ntpd": "notepad",
	# opens vscode in your working directory
	"m-vs": "code e:/myproject/"
	# now add your own :)
}

class Monitor():
	def __init__(self, sleep_time):
		self.sleep_time = sleep_time
		self.flag = 1
		self.clipboard = ''

	# monitoring the clipboard changes
	def listen(self):
		last_value = ''
		# listener
		while self.flag:
			# get what is in the clipboard
			clipboard = pyperclip.paste()
			# detects if any changes happened
			if clipboard != last_value:
				# assigning
				last_value = clipboard
				# conditionall actions
				if clipboard == KILL_COMMAND:
					self.flag = 0
				else:
					print(f'Captured: {clipboard}')
					self.clipboard = clipboard
					# execute command if it exists
					self.take_action()

			time.sleep(self.sleep_time)

	def take_action(self):

		# target command
		cmnd = ''

		# checking if the clipboard text is a command
		for i in COMMANDS:
			if self.clipboard in COMMANDS:
				cmnd = COMMANDS[self.clipboard]

		# if it finds a command, it will be executed
		if len(cmnd):
			print(f'Command found: {self.clipboard}')
			# execution
			try:
				os.system(cmnd)
			except:
				print('Execution error')

	def print_commands(self):
		print('================ COMMANDS =========================')
		for i in COMMANDS:
			print(f'{i} => {COMMANDS[i]}')
		print('===================================================')


	# add the script file to the startup folder
	def add_to_startup(self):
		try:
			start_up_path = f'C:/Users/{os.getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'
			script_full_path = os.path.abspath(sys.argv[0])
			shutil.copy(script_full_path, str(start_up_path))
		except:
			pass

	def hide_console(self):
	    app = win32gui.GetForegroundWindow()
	    win32gui.ShowWindow(app , win32con.SW_HIDE)


s = Monitor(SLEEP_TIME)
s.print_commands()
s.add_to_startup()
s.listen()

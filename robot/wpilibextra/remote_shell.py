"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "------"
contact@team4096.org
"""
import ntcore
import code
import io
import time
from contextlib import redirect_stdout, redirect_stderr

# NOTE: The args for pynetworktables and _pyntcore for nt notifiers isn't the same so I got rid of it.

class RemoteShell:

	def __init__(self, robot):

		self.inst = ntcore.NetworkTableInstance.getDefault()
		self.table = self.inst.getTable('Remote Shell')
		self.interpreter = code.InteractiveInterpreter(locals={"robot": robot, "r": robot})
		# self.table.putString("stdin", "")
		self.stdin_sub = self.table.getStringTopic("stdin").subscribe("")
		self.table.putString("stdout", "")

		def ep(event: ntcore.Event, *args, **kwargs):
			# print("got", entry.value.getRaw())

			stdout = io.StringIO()
			with redirect_stdout(stdout):
				stderr = io.StringIO()
				with redirect_stderr(stderr):
					self.interpreter.runsource(event.data.value.getString()[:-22]) # type: ignore

			out = stdout.getvalue()

			if not out.strip():
				out = "\n"

			out += stderr.getvalue()

			out += f" T{time.time_ns():<20}"

			self.table.putString("stdout", out)

		self.inst.addListener(self.stdin_sub, ntcore.EventFlags.kValueAll, ep)
		# self.table.getEntry("stdin").addListener(ep, ntcore.NetworkTablesInstance.NotifyFlags.UPDATE | networktables.NetworkTablesInstance.NotifyFlags.NEW)

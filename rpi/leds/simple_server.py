#!/usr/bin/env python3
#
# This is a NetworkTables client (eg, the DriverStation/coprocessor side).
# You need to tell it the IP address of the NetworkTables server (the
# robot or simulator).

from os.path import basename
import logging
import random
import time

import ntcore


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	inst = ntcore.NetworkTableInstance.getDefault()
	inst.startServer()

	sd = inst.getTable("robot")

	i = 0

	while True:
		val = random.randint(0, 2)
		print("{0} intake_mode:".format(i), val)

		sd.putNumber("intake_mode", val)
		time.sleep(3)
		i += 1
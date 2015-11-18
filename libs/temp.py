# import sublime
# import sublime_plugin
import os.path
import sys
import time


from Queue import Queue
from threading import Thread

from Worker import Soxs_Worker 


# def temp_fun():
# 	x = Worker.Auto_Worker()
# 	x.temp2()

# def temp_fun2():
# 	y = soxsnation.Auto_Soxs()
# 	y.temp()
	
# temp_fun()
# temp_fun2()


def main():
	# t = "test"
	queue = Queue()

	for x in range(3):
		worker = Soxs_Worker(queue, x)
		worker.daemon = True
		worker.start()

	for x in range(10):
		queue.put("Item: " + str(x))
		
	# for x in range(10):
		# time.sleep(2)

	queue.join()
	print('Done')

main()
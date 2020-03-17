class Open:
	def __init__(self, filename):
		print('open file.......')
		self.filename = filename

	def __del__(self):
		print('回收操作系统资源：self.close()')


f = Open('settings.py')
del f  # f.__del__()
print('----main------')  # del f #f.__del__()

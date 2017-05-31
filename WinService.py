import win32serviceutil, win32service, win32event, time


class PythonService(win32serviceutil.ServiceFramework):
	_svc_name_ = 'PythonService'
	_svc_display_name_ = 'Python Service Test'
	_sve_description_ = "This code is a Python service test"

	def __init__(self, args):
		super().__init__(args)
		self.flag = True
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

	def SvcDoRun(self):
		with open(r'c:\test.txt', 'w', encoding='utf8') as fd:
			while self.flag:
				fd.writelines(time.strftime('%H:%M:%S')+'\n')
				time.sleep(5)
				fd.flush()
		win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)
		self.flag = False


if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(PythonService)

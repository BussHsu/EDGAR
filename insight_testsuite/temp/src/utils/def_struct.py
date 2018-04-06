import datetime

class DateTime:
	def __init__(self, str_date, str_time):
		# 2017-06-30,00:00:00,
		info = self._split_str(str_date, '-')
		info.extend(self._split_str(str_time, ':'))
		self.datetime = datetime.datetime(info[0], info[1], info[2], info[3], info[4], info[5])

	def _split_str(self, line, delimiter = ':'):
		ls_data = line.split(delimiter)
		return [int(x) for x in ls_data]

	# returns a datetime.timedelta object
	def __sub__(self, other):
		return self.datetime - other.datetime

	def __eq__(self, other):
		return self.datetime == other.datetime

	def __repr__(self):
		return str(self.datetime)

class WebPage:
	# all of the inputs are str
	def __init__(self, cik, accession, extension):
		self.cik = cik
		self.accession = accession
		self.extension = extension

	def __key(self):
		return (self.cik, self.accession, self.extension)

	def __eq__(self, y):
		return self.__key() == y.__key()

	def __hash__(self):
		return hash(self.__key())

	def __repr__(self):
		return self.cik+','+self.accession+','+self.extension


class ConnectData:
	# ip,date,time
	def __init__(self, infos):
		self.ip = infos[0]
		self.datetime = DateTime(infos[1], infos[2])
		self.webpage = WebPage(infos[4], infos[5], infos[6])

	def __repr__(self):
		return self.ip+','+str(self.datetime)+','+str(self.webpage)
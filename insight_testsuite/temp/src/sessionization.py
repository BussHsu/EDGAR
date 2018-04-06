import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import copy
from collections import OrderedDict
from datetime import timedelta
from src.utils.data_loader import DataLoader


class Session:
	def __init__(self, connect_data):
		self.ip = connect_data.ip
		self.strt_time = copy.copy(connect_data.datetime)
		self.end_time = copy.copy(self.strt_time)
		self.pages = set()
		self.pages.add(connect_data.webpage)

	def update_session(self, connect_data):
		self.end_time = copy.copy(connect_data.datetime)
		self.pages.add(connect_data.webpage)

	def __repr__(self):
		d = (self.end_time-self.strt_time)
		duration = d.days*24*60*60+d.seconds+1	# +1 because duration is inclusive
		return self.ip+','+str(self.strt_time)+','+str(self.end_time)+','+str(duration)+','+str(len(self.pages))


class SessionMonitor:
	def __init__(self, timeout, out_file_path):
		self.timeout_delta = timedelta(seconds=timeout)
		self.session_dict = OrderedDict()
		self.curr_datetime = None
		self.out_file = open(out_file_path, 'w')

	def process_data(self, connect_data):
		# check change in time
		# initialize the current time
		if not self.curr_datetime:
			self.curr_datetime = connect_data.datetime

		# check session expired when time is changed
		elif self.curr_datetime != connect_data.datetime:
			self._check_expire(connect_data.datetime)

		# check and update session tracker dictionary
		if connect_data.ip in self.session_dict:
			self.session_dict[connect_data.ip].update_session(connect_data)
		else:
			self.session_dict[connect_data.ip] = Session(connect_data)

	# when reach the EOF, just print out all sessions
	def reach_EOF(self):
		for (ip, session) in self.session_dict.items():
			self.out_file.write(str(session)+'\n')
		self.out_file.close()

	def _check_expire(self, datetime):
		self.curr_datetime = datetime

		remove_key_list = []
		# output expired sessions
		for (ip, session) in self.session_dict.items():
			if (datetime - session.end_time)>self.timeout_delta:
				self.out_file.write(str(session)+'\n')
				remove_key_list.append(session.ip)

		# delete the expired sessions from tracker dictionary
		for key in remove_key_list:
			del self.session_dict[key]

# just for testing
def test_main():

	d_loader = DataLoader('/home/yhsu/Desktop/EDGAR/insight_testsuite/tests/test_1/input')

	s_tracker = SessionMonitor(2,'/home/yhsu/Desktop/EDGAR/insight_testsuite/tests/test_1/output/sessionization2.txt')

	data = d_loader.get_next_data()
	while data is not None:
		s_tracker.process_data(data)
		data = d_loader.get_next_data()

	s_tracker.reach_EOF()

def main(argv):
	in_csv_fpath = argv[0]
	inact_period_fpath = argv[1]
	output_fpath = argv[2]

	with open(inact_period_fpath, 'r') as file:
		line = file.readline()
		timeout = int(line.strip())

	d_loader = DataLoader(in_csv_fpath)
	s_tracker = SessionMonitor(timeout, output_fpath)
	data = d_loader.get_next_data()
	while data is not None:
		s_tracker.process_data(data)
		data = d_loader.get_next_data()

	s_tracker.reach_EOF()


if __name__ == '__main__':
	main(sys.argv[1:])
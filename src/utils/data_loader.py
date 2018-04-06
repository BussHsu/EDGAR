# create a data_loader to load log.csv file
import os

from src.utils.def_struct import ConnectData


class DataLoader:
	def __init__(self, f_path):
		self.data_list = []
		with open(f_path, 'r') as file:
			# skip first line (header)
			file.readline()
			for line in file:
				infos = (line.strip()).split(',')
				data = ConnectData(infos)
				self.data_list.append(data)

		self.curr_pt = 0

	def get_next_data(self):
		if self.curr_pt >= len(self.data_list):
			return None

		ret = self.data_list[self.curr_pt]
		self.curr_pt+=1
		return ret

	# def get_next_time_batch(self):
	# 	if self.curr_pt >= len(self.data_list):
	# 		return None
	#
	# 	ret = []
	# 	time = self.data_list[self.curr_pt].datetime
	# 	while self.curr_pt<len(self.data_list) and self.data_list[self.curr_pt].datetime == time:
	# 		ret.append(self.data_list[self.curr_pt])
	# 		self.curr_pt+=1
	#
	# 	return ret


def test_main():
	data_loader = DataLoader('./insight_testsuite/tests/test_1/input')
	data = data_loader.get_next_data()
	while data is not None:
		print (data)
		data = data_loader.get_next_data()

if __name__ == '__main__':
    test_main()
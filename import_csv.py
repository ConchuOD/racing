import csv
from enum import Enum

def convertFromHoursMinsSec2Sec(duration_string):
	hour_str = "0"
	min_str = "0"
	sec_str = "0"
	if "." not in duration_string:
		pass
	elif ":" not in duration_string:
		sec_str = duration_string
	else:
		if duration_string.count(":") == 1:
			min_str,sec_str = duration_string.split(":")
		else:
			hour_str,min_str,sec_str = duration_string.split(":")
	hour_num = float(hour_str)
	min_num = float(min_str)
	sec_num = float(sec_str)
	return hour_num * 3600 + min_num * 60 + sec_num

class Category(Enum):
	LMP1  = 1
	LMP2  = 2
	GTE   = 3
	GTEAM = 4

class Lap:
	laptime = 0
	def __init__(self, driver_number, lap_number, lap_time, improve_lap, inlap, sector_1, s1_improve, sector_2, s2_improve, \
		sector_3, s3_improve, avg_speed, elapsed, hour, s1_large, s2_large, s3_large, top_speed, pit_time):
		self.driver_number = int(driver_number)
		self.lap_number = int(lap_number)
		self.laptime = convertFromHoursMinsSec2Sec(lap_time)
		self.improve_lap_bool = True if improve_lap == "1" else False # is it B?
		self.inlap_bool = True if inlap == "B" else False
		self.sector_1 = convertFromHoursMinsSec2Sec(sector_1)
		self.sector_3 = convertFromHoursMinsSec2Sec(sector_2)
		self.sector_2 = convertFromHoursMinsSec2Sec(sector_3)
		self.s1_improve_bool = True if s1_improve == "1" else False
		self.s2_improve_bool = True if s3_improve == "1" else False
		self.s3_improve_bool = True if s2_improve == "1" else False
		self.s1_large = convertFromHoursMinsSec2Sec(s1_large)
		self.s2_large = convertFromHoursMinsSec2Sec(s2_large)
		self.s3_large = convertFromHoursMinsSec2Sec(s3_large)
		self.avg_speed = float(avg_speed)
		self.elapsed = convertFromHoursMinsSec2Sec(elapsed)
		self.hour = convertFromHoursMinsSec2Sec(hour)
		self.top_speed = float(top_speed)
		self.pit_time = convertFromHoursMinsSec2Sec(pit_time)

class Car:
	laps = list()
	def __init__(self, number, drivers, team, manufact, category, first_lap):
		self.number = int(number)
		self.drivers = drivers
		self.team = team
		self.manufact = manufact
		self.category = category
		self.addLap(first_lap)

	def addLap(self,lap):
		self.laps.append(lap)

	def sumOfBestSectors(self):
		return 0

# 1 NUMBER, 2 DRIVER_NUMBER, 3 LAP_NUMBER, 4 LAP_TIME, 5 LAP_IMPROVEMENT, 6 CROSSING_FINISH_LINE_IN_PIT, 7 S1, 8 S1_IMPROVEMENT, 9 S2,
# 10 S2_IMPROVEMENT, 11 S3, 12 S3_IMPROVEMENT, 13 KPH, 14 ELAPSED, 15 HOUR, 16 S1_LARGE, 17 S2_LARGE, 18 S3_LARGE, 19 TOP_SPEED,
# 20 DRIVER_NAME, 21 PIT_TIME, 22 CLASS, 23 GROUP, 24 TEAM, 25 MANUFACTURER

def getCarKeyValuePairs():
	with open('23_Analysis_Race_Hour_6.CSV') as results_csv:
		csv_reader = csv.DictReader(results_csv,delimiter=',')
		line_count = 0
		cars_dict = {}
		for row in csv_reader:
			car_num = int(row['NUMBER'])

			if line_count == 0:
				print(f'Column names are {", ".join(row)}')
				line_count += 1

			elif line_count > 0:
				if cars_dict.get(car_num) == None: #TODO - convert this to a number by removing 3 bytes, time -> seconds
					driver_dict = {int(row['DRIVER_NUMBER']) : row['DRIVER_NAME']}
					first_lap = Lap(row['DRIVER_NUMBER'], row['LAP_NUMBER'],row['LAP_TIME'],row['LAP_IMPROVEMENT'], \
						row['CROSSING_FINISH_LINE_IN_PIT'], row['S1'], row['S1_IMPROVEMENT'], row['S2'], row['S2_IMPROVEMENT'], \
						row['S3'], row['S3_IMPROVEMENT'], row['KPH'], row['ELAPSED'], row['HOUR'], row['S1_LARGE'], row['S2_LARGE'], \
						row['S3_LARGE'], row['TOP_SPEED'], row['PIT_TIME'])
					car = Car(car_num,driver_dict,row['TEAM'],row['MANUFACTURER'],row['CLASS'],first_lap)
					cars_dict[car_num] = car

				elif cars_dict.get(car_num).drivers.get(row['DRIVER_NUMBER']) == None:
					driver_dict = cars_dict.get(car_num).drivers
					driver_dict[int(row['DRIVER_NUMBER'])] = row['DRIVER_NAME']
					lap = Lap(row['DRIVER_NUMBER'], row['LAP_NUMBER'],row['LAP_TIME'],row['LAP_IMPROVEMENT'], \
						row['CROSSING_FINISH_LINE_IN_PIT'], row['S1'], row['S1_IMPROVEMENT'], row['S2'], row['S2_IMPROVEMENT'], \
						row['S3'], row['S3_IMPROVEMENT'], row['KPH'], row['ELAPSED'], row['HOUR'], row['S1_LARGE'], row['S2_LARGE'], \
						row['S3_LARGE'], row['TOP_SPEED'], row['PIT_TIME'])
					cars_dict.get(car_num).addLap(lap)

				else:
					lap = Lap(row['DRIVER_NUMBER'], row['LAP_NUMBER'],row['LAP_TIME'],row['LAP_IMPROVEMENT'], \
						row['CROSSING_FINISH_LINE_IN_PIT'], row['S1'], row['S1_IMPROVEMENT'], row['S2'], row['S2_IMPROVEMENT'], \
						row['S3'], row['S3_IMPROVEMENT'], row['KPH'], row['ELAPSED'], row['HOUR'], row['S1_LARGE'], row['S2_LARGE'], \
						row['S3_LARGE'], row['TOP_SPEED'], row['PIT_TIME'])
					cars_dict.get(car_num).addLap(lap)
				line_count += 1
		return cars_dict
	
cars = getCarKeyValuePairs()

piggy = cars.get(92)
print(piggy)

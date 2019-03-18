import pandas as pd

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

df = pd.read_csv("23_Analysis_Race_Hour_6.CSV")

car92_df 			= df.loc[df.NUMBER == 92].copy();
car92_df['S1_sec']	= car92_df.apply(lambda row: convertFromHoursMinsSec2Sec(row["S1"]), axis=1)
car92_df['S2_sec']	= car92_df.apply(lambda row: convertFromHoursMinsSec2Sec(row["S2"]), axis=1)
car92_df['S3_sec']	= car92_df.apply(lambda row: convertFromHoursMinsSec2Sec(row["S3"]), axis=1)
car92_df['lap_sec']	= car92_df.apply(lambda row: convertFromHoursMinsSec2Sec(row["LAP_TIME"]), axis=1)

sobs = car92_df["S1_sec"].min() + car92_df["S2_sec"].min() + car92_df["S3_sec"].min()
best_lap = car92_df["lap_sec"].min()

print("Car #92:")
print("Best SOBS " + str(sobs) + " seconds")
print("Best lap " + str(best_lap) + " seconds")
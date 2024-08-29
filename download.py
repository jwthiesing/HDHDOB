def downloadstorm(name, year):
	from urllib.request import urlopen
	import requests
	import pandas as pd
	from io import StringIO
	#targetdt = bt_hour_rounder(dt.datetime(year=year, month=mon, day=day, hour=hour, minute=minute))
	#year = int(str(year)[2:])
	#mon = str(mon).rjust(2, '0')
	#day = str(day).rjust(2, '0')
	#storm = storm.upper()[:4] + storm.upper()[6:]
	name = name.lower()
	#x = str(targetdt.hour).rjust(2, '0')
	#print(storm, year, mon, day, x)

	directory = f'https://www.aoml.noaa.gov/ftp/pub/hrd/data/flightlevel/{year}/{name}/'
	page = requests.get(directory).text
	content = page.split("\n")
	files = []
	for line in content:
		if ".1sec.txt" in line or ".1sec" in line:
			#print(line)
			files.append(
				((line.split('"> ')[1]).split("</a>")[0]))
	del content
	print(files)
	if len(files) < 1:
		import sys
		sys.exit("No valid files found in directory. Exiting.")
	#files = sorted([i for i in files if i[1][:8]
	#			   in timestr], key=lambda x: x[1])
	#linksub = [archive_url[0] + '.'.join(l) for l in files]
	textlist = []
	for ii, file in enumerate(files):
		with urlopen(directory+file) as url:
			print(f"Downloading file {ii}")
			textlist.append(url.read().decode('utf-8'))

	#print(textlist[9].split('\n')[15700])
	#print(textlist[9].split('\n')[15701])
	#print(textlist[9].split('\n')[15702])
	#print(textlist[9].split('\n')[15703])
	#print(textlist[9].split('\n')[15704])
	#print(textlist[9].split('\n')[15705])
	#print(textlist[9].split('\n')[15706])
	#print(textlist[9].split('\n')[15707])

	dflist = []
	for ii, text in enumerate(textlist):
		print(f"Parsing file {ii}")
		dflist.append(pd.read_csv(StringIO(text), sep="\s+", skiprows=[0, 1, 3], header=0, skipfooter=1, on_bad_lines='warn'))
	#print(dflist[0])
	return dflist

if __name__ == "__main__":
	name = "Allen"
	year = 1980
	downloadstorm(name, year)
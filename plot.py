MPERS_TO_KT = 1.943844

def plot(df_list, name, year):
	# TODO: Add cartographic features
	# TODO: Add maximum 1 second wind to legend (and the pressure + time it was recorded at)
	import matplotlib.pyplot as plt
	import pyart
	import matplotlib as mpl
	import cartopy.crs as ccrs
	import cartopy.feature as cfeature
	import numpy as np

	print(df_list[0].columns)

	norm = plt.Normalize(0, 170)
	cmap = mpl.colormaps['pyart_ChaseSpectral']
	fig = plt.figure(figsize=[16,8])
	ax0 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())

	maxlat = []
	for df in df_list: maxlat.append(np.nanmax(df['Lat']))
	minlat = []
	for df in df_list: minlat.append(np.nanmin(df['Lat']))
	maxlon = []
	for df in df_list: maxlon.append(np.nanmax(-df['Lon']))
	minlon = []
	for df in df_list: minlon.append(np.nanmin(-df['Lon']))
	maxdifflat = 10.5 #np.nanmax(np.ndarray(np.ndarray(maxlat)-np.ndarray(minlat), np.ndarray(maxlon)-np.ndarray(minlon)))
	maxdifflon = 25
	medianlats = []
	for df in df_list: medianlats.append(np.nanmedian(df['Lat']))
	medianlons = []
	for df in df_list: medianlons.append(np.nanmedian(-df['Lon']))
	medianlat = np.nanmedian(medianlats)
	medianlon = np.nanmedian(medianlons)
	maxwind = []
	for df in df_list:
		#ax0 = ax[0]
		lat_list, lon_list = df['Lat'], -df['Lon']
		fl_list = df['WndSp']*MPERS_TO_KT
		#if np.nanmax(fl_list) < 300:
		maxwind.append(np.nanmax(fl_list[fl_list < 300]))
		ax0.scatter(lon_list, lat_list, c=cmap(norm(fl_list)), s=2.5, alpha=0.5)
		plt.gca().set_aspect('equal')
		ax0.set_title(f"1 Second FL Wind, {name.upper()} {year}")

		#for ii, c in enumerate(fl_list):
		#	ax0.text(lon_list[ii]+0.005, lat_list[ii]+0.005, f"{int(c)}kt")
	plt.plot([], [], ' ', label=f"1 Second FL Wind Maximum: {round(np.nanmax(maxwind),2)} kts")
	ax0.legend()
	ax0.set_xlim(medianlon-(maxdifflon/1.33), medianlon+(maxdifflon/1.33))
	ax0.set_ylim(medianlat-(maxdifflat/1.33), medianlat+(maxdifflat/1.33))
	ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth = 0.75)
	ax0.add_feature(cfeature.BORDERS.with_scale('50m'), linewidth = 0.25)
	ax0.add_feature(cfeature.STATES.with_scale('50m'), linewidth = 0.25)
	plt.colorbar(mappable=mpl.cm.ScalarMappable(norm=norm,cmap=cmap), ax=ax0, label='Wind Speed (kt)')
	gl = ax0.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth = 1, color='gray', alpha=0.5, linestyle='--')   
	gl.xlabels_top = gl.ylabels_right = False  

	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
	# TODO: Next: Wilma, Gilbert, Patricia, Megi, etc.
	from download import downloadstorm
	storm = "Allen"
	year = 1980
	df_list = downloadstorm(storm, year)
	plot(df_list, storm, year)
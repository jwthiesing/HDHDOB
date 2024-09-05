MPERS_TO_KT = 1.943844

def plot(df_list, name, title_date, georange=None, autorange=False):
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap, Normalize

    cpt_file_path = './cmap/WSPD3.ct'
    colormap_data = np.loadtxt(cpt_file_path, skiprows=3, usecols=(1, 2, 3)) / 255.0  
    data_values = np.loadtxt(cpt_file_path, skiprows=3, usecols=0) 
    normalized_data_values = (data_values - np.nanmin(data_values)) / (np.nanmax(data_values) - np.nanmin(data_values))
    colormap_data_points = list(zip(normalized_data_values, colormap_data))
    if colormap_data_points[0][0] != 0.0:
        colormap_data_points.insert(0, (0.0, colormap_data[0]))
    if colormap_data_points[-1][0] != 1.0:
        colormap_data_points.append((1.0, colormap_data[-1]))
    colormap = LinearSegmentedColormap.from_list('custom_cmap', colormap_data_points)

    norm = Normalize(vmin=0, vmax=160)
    cmap = colormap
    fig = plt.figure(figsize=[16,9])
    ax0 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    maxwind = []

    all_lats, all_lons = [], []

    for df in df_list:
        df = df[df.iloc[:, 0] != 1]
        lat_list, lon_list = df['Lat'], -df['Lon']
        fl_list = df['WndSp']
        max_value = np.nanmax(fl_list)
        max_index = np.nanargmax(fl_list)
        print(f"Max value: {max_value} found at line number: {max_index + 1}")
        fl_list = df['WndSp'] * MPERS_TO_KT
        maxwind.append(np.nanmax(fl_list[fl_list < 300]))
        ax0.scatter(lon_list, lat_list, s=2.5, c=fl_list, cmap=cmap, norm=norm, alpha=0.5, zorder=2)
        all_lats.extend(lat_list)
        all_lons.extend(lon_list)

    if autorange:
        lat_min, lat_max = np.min(all_lats), np.max(all_lats)
        lon_min, lon_max = np.min(all_lons), np.max(all_lons)
        georange = (lat_min, lat_max, lon_min, lon_max)
    else:
        lat_min, lat_max, lon_min, lon_max = georange
    
    ax0.set_xlim(lon_min, lon_max)
    ax0.set_ylim(lat_min, lat_max)

    max_wind_speed = round(np.nanmax(maxwind), 2)
    
    ax0.set_title(f"{name.upper()}, {title_date}", pad=15)
    ax0.set_title(f'Max FL Wind: {max_wind_speed} kts', loc='left', fontsize=8)

    ax0.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.75)
    ax0.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.25)
    ax0.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.25)
    ax0.add_feature(cfeature.LAND, facecolor='gray')
    ax0.add_feature(cfeature.OCEAN, facecolor='#393939')

    ax0.set_aspect('equal', adjustable='box')

    pos = ax0.get_position()

    cbar_ax = fig.add_axes([pos.x1 + 0.03, pos.y0, 0.03, pos.height])
    norm = Normalize(vmin=0, vmax=160)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='vertical', extend='max')
    cbar.set_ticks(np.arange(0, 161, 10))
    cbar.set_ticklabels([str(val) for val in np.arange(0, 161, 10)], color='black')
    cbar.ax.tick_params(labelsize=10, color='#000000')
    cbar.set_label('Wind Speed (kts)', fontsize=12, fontweight='bold', labelpad=10, color='#000000')

    gl = ax0.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlabels_bottom = True
    gl.ylabels_left = True

    ax0.set_xticklabels([])
    ax0.set_yticklabels([])
    
    plt.subplots_adjust(left=0.05, right=0.85, top=0.95, bottom=0.05)

    plt.savefig('./test.png', dpi=600, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

if __name__ == "__main__":
    from download import downloadstorm
    import argparse, sys
    
    parser = argparse.ArgumentParser(
                        prog='plot.py',
                        description='Plot 1Hz FL HDOBs given a storm and a year',
                        epilog='')
    parser.add_argument('storm')
    parser.add_argument('year')
    parser.add_argument('--autorange', action='store_true', help='Automatically determine georange')
    args = parser.parse_args(sys.argv[1:])

    storm = args.storm
    year = args.year
    autorange = args.autorange

    df_list, file_names = downloadstorm(storm, year, return_file_names=True)

    print("Select which file you want to plot:")
    for i, file_name in enumerate(file_names, 1):
        print(f"{i}: {file_name}")
    print("Enter 'all' to plot all files.")
    
    user_input = input("Enter the file number or 'all': ")
    if user_input.lower() == 'all':
        first_date = file_names[0][:8]
        last_date = file_names[-1][:8]
        title_date = f"{first_date[:4]}/{first_date[4:6]}/{first_date[6:]}-{last_date[:4]}/{last_date[4:6]}/{last_date[6:]}"
    else:
        try:
            file_number = int(user_input) - 1
            df_list = [df_list[file_number]]
            selected_date = file_names[file_number][:8]
            title_date = f"{selected_date[:4]}/{selected_date[4:6]}/{selected_date[6:]}"
        except (ValueError, IndexError):
            print(f"Invalid input. Plotting all files instead.")
            first_date = file_names[0][:8]
            last_date = file_names[-1][:8]
            title_date = f"{first_date[:4]}/{first_date[4:6]}/{first_date[6:]}-{last_date[:4]}/{last_date[4:6]}/{last_date[6:]}"
            autorange = True

    if not autorange:
        georange = ([2.5, 35, -100, -50])
    else:
        georange = None

    plot(df_list, storm, title_date, georange=georange, autorange=autorange)

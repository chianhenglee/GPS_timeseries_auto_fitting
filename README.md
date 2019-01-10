# GPS_timeseries_auto_fitting
This is a series of python scripts for processing GPS time series data, fitting velocities and plotting using plotly


The original GPS time series data is stored under time_series_data. Each file is a station (.txt). 

And below is the format of the data. The columns are: 


| date (year+day of year) | longitude (WGS84) | latitude (WGS84) | vertical (ellipsoid height) |
| --- | --- | --- | --- |
| 2016306 | 121.59938566 | 25.11217164 | 437.420 |
| 2016307 | 121.59938566 | 25.11217161 | 437.427 |
| 2016308 | 121.59938564 | 25.11217162 | 437.440 |
| 2016309 | 121.59938570 | 25.11217161 | 437.428 |
| 2016310 | 121.59938568 | 25.11217160 | 437.432 |



Below is the intended steps (order) to run the scripts:

### 1. process_raw_and_export_csv.py

   This process data in each station and convert lon lat time series to local east west components (vertical is unchanged).
   
   This also create a new time (unit:year, with digits). This is for plotting time series.
   
   The new information are then added to the dataframe and later exported under the folder: processed_timeseries as .csv files
   
   Note that the format for E,N,V is in mm as opposed to the original data being in meters.
   
   
### 2. auto_plot_timeseries.py

   This loops through the newly created csv files and plot the time series (.html files) under folder: timeseries_graphs.
   
   
### 3. auto_fit_velocity.py

   This reads the .csv files created in step 1 and fits the velocities.
   New plotted time series with fitted velocities are then stored under folder: fitted_timeseries_graphs.
   This script also exported the velocity data as a csv file named: fitted_velocity.csv
   
   
### 4. (Future steps creating velocity fields map.)




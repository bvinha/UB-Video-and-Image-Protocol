import pandas as pd
import numpy as np

# Read CSV files
dive2 = pd.read_csv("G:/OASIS_GLOBALMAPPER/DIVE2.csv", delimiter=";", parse_dates=['time'], date_parser=lambda col: pd.to_datetime(col, format='%H:%M:%S').time())
dive8 = pd.read_csv("G:/OASIS_GLOBALMAPPER/DIVE8.csv", delimiter=";", parse_dates=['time'], date_parser=lambda col: pd.to_datetime(col, format='%H:%M:%S').time())

# Convert 'time' to datetime, assuming a date
dive8['time'] = pd.to_datetime(dive8['time'], format='%H:%M:%S')

# Generate a time sequence at each second
time_sequence = pd.date_range(start=dive8['time'].min(), end=dive8['time'].max(), freq='S')

# Interpolate variables separately
interpolated = pd.DataFrame({'time': time_sequence})

for col in ['y', 'x', 'depth', 'lat', 'lon']:
    interpolated[col] = np.interp(pd.to_numeric(time_sequence), pd.to_numeric(dive8['time']), dive8[col])

# Convert 'time' back to H:M:S format
interpolated['time'] = interpolated['time'].dt.time

print(interpolated)

# Save to CSV
interpolated.to_csv("dive8_interpols.csv", sep=';', index=False)

# Assuming 'frames2' is another DataFrame you want to merge with
# Make sure 'frames2' is defined and has a 'time' column in H:M:S format
# dive2_merg = pd.merge(interpolated, frames2, on='time')


#Note: 
#The `parse_dates` and `date_parser` parameters in `pd.read_csv` are used to ensure the 'time' column is correctly parsed as datetime objects.
#The `np.interp` function is used for interpolation. It requires numeric types for the 'x' and 'x-points' parameters, so we convert the datetime to numeric and then back.
#The final merge operation with `frames2` is commented out because `frames2` is not defined in the provided code. Ensure `frames2` is a DataFrame with a 'time' column in the correct format before merging.
#
# The provided code is alreadi quite efficient to the task it performs. However here are a few suggestions to make it more concise and readible 
# The provided Python code is already quite efficient for the task it performs. However, there are a few adjustments and enhancements that can make the code more concise and potentially more readable:

# 1. Use a single function for datetime conversion: Instead of parsing the "time" column during csv reading, and then converting it again, you can handle datetime conversion in one step after reading.
#
# 2. Vectorize the interpolation process: the current loop iterates over each column to interpolate. While this is already using NumPy's efficient np.interp funcion, you can encapsulate the interpolation logic in a function to make the code more modular.

# 3. Error handling for file reading: Adding basic error handling for reading csv files can make your code more robust.

# Here is a revised version incorporating these suggestions:

import pandas as pd
import numpy as np

def read_and_convert_time(filepath, time_col='time', time_format='%H:%M:%S'):
    """Read CSV file and convert specified time column to datetime."""
    try:
        df = pd.read_csv(filepath, delimiter=";", parse_dates=[time_col])
        df[time_col] = pd.to_datetime(df[time_col].dt.time, format=time_format)
        return df
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame()

def interpolate_dataframe(df, time_sequence, on='time'):
    """Interpolate all columns of a dataframe along a given time sequence."""
    interpolated_data = {col: np.interp(pd.to_numeric(time_sequence), pd.to_numeric(df[on]), df[col]) for col in df.columns if col != on}
    interpolated_data[on] = time_sequence
    return pd.DataFrame(interpolated_data)

# Main execution
dive2 = read_and_convert_time("G:/OASIS_GLOBALMAPPER/DIVE2.csv")
dive8 = read_and_convert_time("G:/OASIS_GLOBALMAPPER/DIVE8.csv")

time_sequence = pd.date_range(start=dive8['time'].min(), end=dive8['time'].max(), freq='S')
interpolated = interpolate_dataframe(dive8, time_sequence)

# Convert 'time' back to H:M:S format for display or further processing
interpolated['time'] = interpolated['time'].dt.time

print(interpolated)

# Save to CSV
interpolated.to_csv("dive8_interpols.csv", sep=';', index=False)
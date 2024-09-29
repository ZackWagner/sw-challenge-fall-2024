import os
import sys
import bisect
from datetime import datetime, timedelta
import csv
import re

class Tick:
    def __init__(self, timestamp, price, size):
        self.timestamp = timestamp
        self.price = price
        self.size = size

# Function to parse the interval string
def parse_interval(interval_str):
    days = hours = minutes = seconds = 0
    matches = re.findall(r'(\d+)([d|h|m|s])', interval_str)
    for value, unit in matches:
        if unit == 'd':
            days += int(value)
        elif unit == 'h':
            hours += int(value)
        elif unit == 'm':
            minutes += int(value)
        elif unit == 's':
            seconds += int(value)
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


ticks = []
directory = '../sw-challenge-fall-2024/data'


for filename in os.listdir(directory):
    if filename.startswith('ctg_tick_'):
        # Full path to the file
        filepath = os.path.join(directory, filename)

        # Read the file line by line
        with open(filepath, 'r') as file:
            next(file)
            for line in file:
                # Split the line by commas (assuming CSV format)
                parts = line.strip().split(',')
                # Ensure the line has exactly 3 parts
                if len(parts) == 3:
                    # Create a Tick object and append it to the list
                    timestamp, price, size = parts

                    tick = Tick(timestamp, price, size)

                    ticks.append(tick)

# sort by time
ticks.sort(key=lambda tick: tick.timestamp)

# clean data

# filter out ticks without price
ticks = list(filter(lambda tick: tick.price, ticks))
print('here')

for i in range(0, len(ticks)):
    # negative price
    if float(ticks[i].price) < 0:
        ticks[i].price = -float(ticks[i].price)
    if (float(ticks[i].price) < 100):
        ticks[i].price = 10 * float(ticks[i].price)

if len(sys.argv) < 4:
    print("Did not provide enough arguments")
    sys.exit(1)

interval = sys.argv[1]
end = sys.argv[2]
start = sys.argv[3]


# Convert start and end timestamps to datetime objects for comparison
start_dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
end_dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

# Extract just the timestamps for binary searching
timestamp_list = [datetime.strptime(tick.timestamp, '%Y-%m-%d %H:%M:%S.%f') for tick in ticks]

# Use bisect to find the insertion points
start_index = bisect.bisect_left(timestamp_list, start_dt)
end_index = bisect.bisect_right(timestamp_list, end_dt)

filtered_ticks = ticks[start_index:end_index]

# Calculate the total sum for each interval
interval_duration = parse_interval(interval)
interval_start = start_dt
interval_end = interval_start + interval_duration

data = [["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]]
i = start_index

while interval_end < end_dt:
    minn = sys.float_info.max
    maxx = sys.float_info.min
    vol = 0
    openn = ticks[i].price
    while interval_start <= datetime.strptime(ticks[i].timestamp, '%Y-%m-%d %H:%M:%S.%f') < interval_end:
        if float(ticks[i].price) < float(minn):
            minn = ticks[i].price
        if float(ticks[i].price) > float(maxx):
            maxx = ticks[i].price
        vol += float(ticks[i].size)
        i+=1
    close = ticks[i-1].price
    data.append([openn, maxx, minn, close, vol])
    # Move to the next interval
    interval_start = interval_end
    interval_end = interval_start + interval_duration

# Open a CSV file in write mode
with open('output.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the data to the CSV file
    writer.writerows(data)

print("Data written to output.csv successfully.")
Usage Guide: \
Run the solution as such \
python3 solution.py "INTERVAL" "END" "START" \
Specify Interval as such: XXdXXhXXmXXs \
Example run: \
python3 solution.py "1h30m" "2024-09-19 10:10:08.365" "2024-09-17 12:55:59.956"  

Assumptions: \
Assume that start date is before the end date \
Assume that the all inputs are properly formatted \
Assume that the start date and end date are within the given data

Data Cleaning Report:\
!Only had time to find three issues with data! \
a) Empty price field for some tick. Addressed by removing the tick from the data as it does not tell us much without the price and could be unsafe to estimate the price \
b) Negative price field. Addressed by changing it to the corresponding positive price. Manual inspection found that instances of these were reasonable prices, just negative for whatever reason so it seemed safe to keep tick in the data with reversed price \
c) Price shifted one decimal to the left. Solved this by checking for values that are too small and shifting the decimal if needed. This seems logical because the prices seem reasonable just divided by 10
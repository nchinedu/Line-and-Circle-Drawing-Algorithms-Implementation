final_points = []
starting_point = input("Enter starting points, separated by a comma: ")
ending_point = input("Enter ending points, separated by a comma: ")

# Convert input string into lists of integers
starting_point = [int(x.strip()) for x in starting_point.split(",")]
ending_point = [int(x.strip()) for x in ending_point.split(",")]

change_in_x = ending_point[0] - starting_point[0]
change_in_y = ending_point[1] - starting_point[1]

# Calculate the number if steps required based on the greater change in x or y
if abs(change_in_x) > abs(change_in_y):
    steps = abs(change_in_x)
else:
    steps = abs(change_in_y)

# Calculate the increment in x and y for each step
increment_x = change_in_x / steps
increment_y = change_in_y / steps

x = starting_point[0]
y = starting_point[1]

#Generate the intermediate points
for i in range(steps + 1):
    final_points.append([round(x), round(y)]) # Round coordinates to the nearest integer
    x += increment_x
    y += increment_y

print(final_points)
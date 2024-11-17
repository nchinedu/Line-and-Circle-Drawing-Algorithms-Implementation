final_points = []
starting_point = input("Enter starting points (x,y), separated by a comma: ")
ending_point = input("Enter ending points (x,y), separated by a comma: ")

# Convert input string into lists of integers
starting_point = [int(x.strip()) for x in starting_point.split(",")]
ending_point = [int(x.strip()) for x in ending_point.split(",")]

change_in_x = ending_point[0] - starting_point[0]
change_in_y = ending_point[1] - starting_point[1]

x = starting_point[0]
y = starting_point[1]

# Calculate the decision parameter
if change_in_x < 0:
    step_x = -1
else:
    step_x = 1
    
if change_in_y < 0:
    step_y = -1
else:
    step_y = 1

# Use absolute values of the changes for iteration
change_in_x = abs(change_in_x)
change_in_y = abs(change_in_y)

# Start with the first point
final_points.append([x, y])

# Decide on the primary direction of iteration
if change_in_x > change_in_y:
    # Iterate over x
    p = 2 * change_in_y - change_in_x
    for _ in range(change_in_x):
        x += step_x
        if p < 0:
            p += 2 * change_in_y
        else:
            y += step_y
            p += 2 * (change_in_y - change_in_x)
        final_points.append([x, y])
else:
    # Iterate over y
    p = 2 * change_in_x - change_in_y
    for _ in range(change_in_y):
        y += step_y
        if p < 0:
            p += 2 * change_in_x
        else:
            x += step_x
            p += 2 * (change_in_x - change_in_y)
        final_points.append([x, y])

# Output the final points
print(final_points)

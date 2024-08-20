import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

"""
•	 a = -0.002  (this negative value reflects the decrease in efficiency at high speeds due to increased air resistance and engine load)
•	 b = 0.3  (this term reflects the increase in efficiency at moderate speeds)
•	 c = 5  (this is a baseline efficiency at very low speeds)
The constants a, b, and c have the following interpretations:

1. a (Quadratic Term Coefficient):

	•	Effect of Speed Squared: The coefficient a is associated with the v^2 term, representing the effects of speed squared on fuel economy.
	•	Negative Impact at High Speeds: Typically, a is negative, reflecting the fact that as speed increases significantly, fuel economy decreases due to factors like increased air resistance, higher engine RPMs, and greater rolling resistance. The quadratic nature of this term captures the increasingly steep decline in fuel economy at very high speeds.

2. b (Linear Term Coefficient):

	•	Linear Effect of Speed: The coefficient b is associated with the linear v term, representing the direct, linear relationship between speed and fuel economy.
	•	Positive Impact at Moderate Speeds: This term usually has a positive value, indicating that as speed increases from low to moderate levels, fuel economy improves. This improvement happens because, at very low speeds, the engine may not be operating efficiently (e.g., more fuel is used to overcome static friction, stop-and-go conditions, and idling). As speed increases to a certain point, the engine operates more efficiently, and fuel economy improves.

3. c (Constant Term):

	•	Baseline Fuel Economy: The constant c represents the base fuel economy of the vehicle when speed v is zero (or close to zero).
	•	Reflects Efficiency at Very Low Speed: It indicates the inherent efficiency of the vehicle in conditions where the speed is minimal. This term accounts for factors like engine idle consumption and the minimal fuel consumption when moving very slowly. In real-world terms, c helps set the baseline fuel economy that other terms modify as speed changes.

Combined Interpretation:

	•	At Low Speeds: Fuel economy is mostly influenced by the constant c and increases with speed due to the positive b \times v term.
	•	At Optimal Speeds: There is a peak fuel economy point where the positive effect of the b term balances out the negative effect of the a term. This peak corresponds to the vehicle’s most efficient cruising speed.
	•	At High Speeds: The negative a \times v^2 term dominates, causing fuel economy to decrease as speed continues to rise.
"""
def fuel_economy(speed_kmh):
    """
    Calculate the fuel economy (km per liter) based on the speed of the car.

    :param speed_kmh: Speed of the car in kilometers per hour (km/h)
    :return: Fuel economy in kilometers per liter (km/L)
    """
    # Constants for the equation
    a = -0.002
    b = 0.3
    c = 5
    
    # Fuel economy equation
    fuel_efficiency = a * (speed_kmh ** 2) + b * speed_kmh + c
    
    # Round the result to one decimal place
    return np.round(fuel_efficiency, 1)

# Function to compute color gradient
def compute_gradient_color(start_color, end_color, n):
    return [mcolors.to_hex(c) for c in np.linspace(mcolors.to_rgba(start_color), mcolors.to_rgba(end_color), n)]

# Define the speed range and calculate the corresponding time to cover 10 km
speeds = np.arange(5, 160, 5)  # Speeds from 5 to 155 km/h in increments of 5
distance_travelled_in_1_minute = (speeds / 60)
times = 10 / distance_travelled_in_1_minute  # Time in minutes to cover 10 km
fuels = fuel_economy(speeds) # fuel economy as km/L at this speed

# Calculate the theta values for the arc
theta_rotated = np.linspace(-5/8 * np.pi - np.pi/2, 5/8 * np.pi - np.pi/2, len(speeds))

# Gradient settings for outer line (red to blue) and inner line (red -> yellow -> green)
exact_mid_point = len(speeds) // 2
outer_gradient_colors_blue_mid = compute_gradient_color('red', 'blue', len(speeds))

inner_transition_point1 = len(speeds) // 3
inner_transition_point2 = 2 * len(speeds) // 3

red_to_yellow = compute_gradient_color('red', 'yellow', inner_transition_point1)
yellow_segment = ['yellow'] * (inner_transition_point2 - inner_transition_point1)
yellow_to_green = compute_gradient_color('yellow', 'green', len(speeds) - inner_transition_point2)
inner_gradient_combined = red_to_yellow + yellow_segment + yellow_to_green

red_to_green = compute_gradient_color('red', 'green', inner_transition_point1)
green_segment = ['green'] * (inner_transition_point2 - inner_transition_point1)
green_to_red = compute_gradient_color('green', 'red', len(speeds) - inner_transition_point2)
last_gradient_combined = red_to_green + green_segment + green_to_red

# Reverse the theta values to flip the axis
theta_reversed = theta_rotated[::-1]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Plot the speed markers on the arc, displaying only multiples of 10, with reversed axis
for i, speed in enumerate(speeds):
    if speed % 10 == 0:
        x = -np.cos(theta_reversed[i])
        y = -np.sin(theta_reversed[i])
        ax.text(x, y, f"{speed}", ha='center', va='center', fontsize=10, fontweight='bold', color='black')
# Draw the outer arc with the reversed axis
outer_arc_x = np.cos(theta_rotated)
outer_arc_y = np.sin(theta_rotated)
for i in range(len(outer_gradient_colors_blue_mid)):
    ax.plot(-outer_arc_x[i:i+2], -outer_arc_y[i:i+2], color=outer_gradient_colors_blue_mid[i])

# Plot the time markers on the inner arc, displaying only whole numbers and skipping the last value (120 km/h)
gap_coefficient = -0.9
for i, time in enumerate(times):
    if time.is_integer():
        x = gap_coefficient * np.cos(theta_reversed[i])
        y = gap_coefficient * np.sin(theta_reversed[i])
        ax.text(x, y, f"{int(time)}", ha='center', va='center', fontsize=10, fontweight='bold', color='black')
# Draw the inner arc with the reversed axis
for i in range(len(inner_gradient_combined)):
    ax.plot(gap_coefficient * outer_arc_x[i:i+2], gap_coefficient * outer_arc_y[i:i+2], color=inner_gradient_combined[i])
    
# Plot the consumption markers on the last inner arc
gap_coefficient = -0.75
for i, fuel in enumerate(fuels):
    if fuel.is_integer():
        x = gap_coefficient * np.cos(theta_reversed[i])
        y = gap_coefficient * np.sin(theta_reversed[i])
        ax.text(x, y, f"{int(fuel)}", ha='center', va='center', fontsize=10, fontweight='bold', color='black')
# Draw the inner arc with the reversed axis
for i in range(len(last_gradient_combined)):
    ax.plot(gap_coefficient * outer_arc_x[i:i+2], gap_coefficient * outer_arc_y[i:i+2], color=last_gradient_combined[i])

# Adjust the legend positions with bold grey font
ax.text(0, -0.1, "Top: Speed (km/h)", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')
ax.text(0, -0.2, "Middle: Minutes per 10 km", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')
ax.text(0, -0.3, "Bottom: Consumption (km/l)", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')

# Set up the plot
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.axis('off')

# Show the plot
plt.show()
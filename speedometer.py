import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

"""
The average length of a car varies depending on the type of vehicle, but for general reference:
	•	Compact Cars: Approximately 4.2 to 4.5 meters.
	•	Midsize Sedans: Approximately 4.6 to 4.8 meters.
	•	Full-Size Sedans: Approximately 4.9 to 5.1 meters.
	•	SUVs: Approximately 4.5 to 5.0 meters.
	•	Pickup Trucks: Approximately 5.2 to 5.8 meters.

Average Car Length:
	•	Across all categories, the average length of a passenger vehicle is roughly 4.5 to 4.8 meters.
"""
def distance_as_car_length(distance, avg_car_length=4.5):
    # round to nearest half
    car_lengths = round((distance / avg_car_length) * 2) / 2
    return int(car_lengths) if car_lengths.is_integer() else car_lengths

"""
Calculate the stopping distance based on the speed of the car.
The AASHTO stopping distance formula is as follows:
s = (0.278 × t × v) + v² / (254 × (f + G))
where:
s – Stopping distance in meters;
t – Perception-reaction time in seconds;
v – Speed of the car in km/h;
G – Grade (slope) of the road, expressed as a decimal. Positive for an uphill grade and negative for a downhill road;
f – Coefficient of friction between the tires and the road. It is assumed to be 0.7 on a dry road and between 0.3 and 0.4 on a wet road.
This formula is taken from the book "A Policy on Geometric Design of Highways and Streets". 
It is commonly used in road design for establishing the minimum stopping sight distance required on a given road. 

AASHTO recommends the value of 2.5 seconds to ensure that virtually every driver will manage to react within that time. 
In reality, many drivers are able to hit the brake much faster. You can use the following values as a rule of thumb:
1 second – A keen and alert driver;
1.5 seconds – An average driver;
2 seconds – A tired driver or an older person; and
2.5 seconds – The worst-case scenario. It is highly probable that even elderly or intoxicated drivers will manage to react within 2.5 seconds.

:param speed_kmh: Speed of the car in kilometers per hour (km/h)
:param reaction_time: Driver's reaction time in seconds (default is 1.5 seconds)
:param friction_coeff: Friction coefficient between tyres and the road. It is assumed to be 0.7 on a dry road and between 0.3 and 0.4 on a wet road.
:param slope: Grade/slope of the road expressed as a decimal.
:return: Stopping distance in meters (m)
"""
def stopping_distance(speed_kmh, reaction_time=1.5, friction_coeff=0.7, slope=0):
    total_stopping_distance = (0.278 * reaction_time * speed_kmh) + speed_kmh ** 2 / (254 * (friction_coeff + slope))
    
    # round to 1 decimal point
    return np.round(total_stopping_distance, 1)

# Function to compute color gradient
def compute_gradient_color(start_color, end_color, n):
    return [mcolors.to_hex(c) for c in np.linspace(mcolors.to_rgba(start_color), mcolors.to_rgba(end_color), n)]

def plot_speedmeter_pacemeter_fuelmeter():
    # Define the speed range and calculate the corresponding time to cover 10 km
    speeds = np.arange(10, 160, 10)  # Speeds from 5 to 155 km/h in increments of 5
    distance_travelled_in_1_minute = (speeds / 60)
    times = 10 / distance_travelled_in_1_minute  # Time in minutes to cover 10 km
    stopping_distances = stopping_distance(speeds) # distance, in meters, it takes to stop immediately

    # Calculate the theta values for the arc
    theta_rotated = np.linspace(-5/8 * np.pi - np.pi/2, 5/8 * np.pi - np.pi/2, len(speeds))

    # Gradient settings for outer line (red to blue) and inner line (red -> yellow -> green)
    outer_gradient_colors_blue_mid = compute_gradient_color('red', 'blue', len(speeds))
    
    outer_gradient_colors_orange_mid = compute_gradient_color('red', 'orange', len(speeds))

    inner_transition_point1 = len(speeds) // 3
    inner_transition_point2 = 2 * len(speeds) // 3

    red_to_yellow = compute_gradient_color('red', 'yellow', inner_transition_point1)
    yellow_segment = ['yellow'] * (inner_transition_point2 - inner_transition_point1)
    yellow_to_green = compute_gradient_color('yellow', 'green', len(speeds) - inner_transition_point2)
    inner_gradient_combined = red_to_yellow + yellow_segment + yellow_to_green

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
    for i, distance in enumerate(stopping_distances):
        # if distance.is_integer():
        x = gap_coefficient * np.cos(theta_reversed[i])
        y = gap_coefficient * np.sin(theta_reversed[i])
        ax.text(x, y, f"{distance_as_car_length(distance)}", ha='center', va='center', fontsize=10, fontweight='bold', color='black')
    # Draw the inner arc with the reversed axis
    for i in range(len(outer_gradient_colors_orange_mid)):
        ax.plot(gap_coefficient * outer_arc_x[i:i+2], gap_coefficient * outer_arc_y[i:i+2], color=outer_gradient_colors_orange_mid[i])

    # Adjust the legend positions with bold grey font
    ax.text(0, -0.1, "Top: Speed (km/h)", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')
    ax.text(0, -0.2, "Middle: Minutes per 10 km", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')
    ax.text(0, -0.3, "Bottom: Stopping distance (cars)", ha='center', va='center', fontsize=12, fontweight='bold', color='grey')

    # Set up the plot
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Return the plot
    return plt

plot_speedmeter_pacemeter_fuelmeter().show()
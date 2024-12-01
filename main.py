import tkinter as tk
import numpy as np
import random
import math
from tqdm import tqdm

# Set up constants
SC = 20
DIAMETER = 34 * SC
RADIUS = DIAMETER // 2
INNER_BULL_RADIUS = 0.75 * SC
OUTER_BULL_RADIUS = 1.75 * SC
TRIPLE_INNER_RADIUS = 9.75 * SC
TRIPLE_OUTER_RADIUS = 10.75 * SC
DOUBLE_INNER_RADIUS = 16 * SC
DOUBLE_OUTER_RADIUS = 17 * SC
DARTS_PER_TRIAL = 250

data = [
    1.1, 7, 5.2, 5.3, 5.5, 7.5, 2.7, 7.6, 6.6, 6.7, 7.6, 10.1, 17.5, 1.7, 3.7, 
    5.8, 7.7, 14.4, 1.3, 9.1, 6.5, 7.4, 14.6, 13.4, 3.2, 2.5, 8.2, 2.5, 4.2, 
    4.9, 5, 7.5, 4.6, 5.5, 19.6, 17.2, 3.9, 6.2, 1.4, 4.5, 7.6, 8.9, 16.7, 16.4, 
    1.2, 1, 1.4, 1.5, 2.7, 3.7, 4.6, 9.5, 9.9, 18.4, 9.5, 2.4, 2.5, 17.7, 12.3, 14.8
]
MEAN_RADIUS = np.mean(data) * SC

# Create a Tkinter window
window = tk.Tk()
window.title("Dartboard Game")

# Create a canvas to display the dartboard
canvas = tk.Canvas(window, width=DIAMETER, height=DIAMETER)
canvas.pack()

# Initialize score
total_score = 0

def draw_dartboard():
    # Draw the dartboard base
    canvas.create_oval(0, 0, DIAMETER, DIAMETER, fill="beige")
    
    # Define the numbers for each segment
    numbers = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
    
    # Draw the double ring with alternating colors
    for i in range(20):
        start_angle = i * 18 - 9
        end_angle = start_angle + 18
        color = "green" if i % 2 == 0 else "red"
        
        canvas.create_arc(RADIUS - DOUBLE_OUTER_RADIUS, RADIUS - DOUBLE_OUTER_RADIUS,
                          RADIUS + DOUBLE_OUTER_RADIUS, RADIUS + DOUBLE_OUTER_RADIUS,
                          start=start_angle, extent=18, fill=color, outline="")
        canvas.create_arc(RADIUS - DOUBLE_INNER_RADIUS, RADIUS - DOUBLE_INNER_RADIUS,
                          RADIUS + DOUBLE_INNER_RADIUS, RADIUS + DOUBLE_INNER_RADIUS,
                          start=start_angle, extent=18, fill="beige", outline="")

    # Draw the triple ring with alternating colors
    for i in range(20):
        start_angle = i * 18 - 9
        end_angle = start_angle + 18
        color = "green" if i % 2 == 0 else "red"
        
        canvas.create_arc(RADIUS - TRIPLE_OUTER_RADIUS, RADIUS - TRIPLE_OUTER_RADIUS,
                          RADIUS + TRIPLE_OUTER_RADIUS, RADIUS + TRIPLE_OUTER_RADIUS,
                          start=start_angle, extent=18, fill=color, outline="")
        canvas.create_arc(RADIUS - TRIPLE_INNER_RADIUS, RADIUS - TRIPLE_INNER_RADIUS,
                          RADIUS + TRIPLE_INNER_RADIUS, RADIUS + TRIPLE_INNER_RADIUS,
                          start=start_angle, extent=18, fill="beige", outline="")

    # Draw the bullseye
    canvas.create_oval(RADIUS - OUTER_BULL_RADIUS, RADIUS - OUTER_BULL_RADIUS,
                       RADIUS + OUTER_BULL_RADIUS, RADIUS + OUTER_BULL_RADIUS, fill="green")
    canvas.create_oval(RADIUS - INNER_BULL_RADIUS, RADIUS - INNER_BULL_RADIUS,
                       RADIUS + INNER_BULL_RADIUS, RADIUS + INNER_BULL_RADIUS, fill="red")
    
    # Draw wedge lines and segment numbers
    for i in range(20):
        angle = i * (2 * math.pi / 20) - math.pi / 2 - 9 * math.pi / 180
        
        # Draw wedge lines
        x_start = RADIUS + RADIUS * math.cos(angle)
        y_start = RADIUS + RADIUS * math.sin(angle)
        x_end = RADIUS + OUTER_BULL_RADIUS * math.cos(angle)
        y_end = RADIUS + OUTER_BULL_RADIUS * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, fill="black")
        
        # Position for the number in each segment
        mid_angle = angle + math.pi / 20
        text_radius = RADIUS * 0.75
        text_x = RADIUS + text_radius * math.cos(mid_angle)
        text_y = RADIUS + text_radius * math.sin(mid_angle)
        canvas.create_text(text_x, text_y, text=str(numbers[i]), font=("Arial", int(1.5 * SC), "bold"), fill="black")

def distance_from_center(x, y):
    return math.sqrt((x - RADIUS) ** 2 + (y - RADIUS) ** 2)

def calculate_score(x, y):
    distance = distance_from_center(x, y)
    
    if distance <= INNER_BULL_RADIUS:
        return 50  # Inner Bullseye
    elif distance <= OUTER_BULL_RADIUS:
        return 25  # Outer Bullseye
    elif distance > RADIUS:
        return 0  # Outside the dartboard
    
    angle = (math.degrees(math.atan2(y - RADIUS, x - RADIUS)) + 90 + 9) % 360
    segments = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
    segment_index = int(angle // 18)
    base_score = segments[segment_index]
    
    if TRIPLE_INNER_RADIUS < distance <= TRIPLE_OUTER_RADIUS:
        return base_score * 3  # Triple ring
    elif DOUBLE_INNER_RADIUS < distance <= DOUBLE_OUTER_RADIUS:
        return base_score * 2  # Double ring
    
    return base_score

def grid_location(diameter, step):
    points = []
    num_steps = int(diameter / step)
    for x in range(0, num_steps):
        for y in range(0, num_steps):
            if distance_from_center(x * step, y * step) <= RADIUS:
                points.append((x * step, y * step))
    return points

def simulate_dart_throw(center_x, center_y):
    new_sample = random.choices(data, k=60)
    mean_distance = np.mean(new_sample) * SC
    angle = random.uniform(0, 2 * math.pi)

    x = center_x + mean_distance * math.cos(angle)
    y = center_y + mean_distance * math.sin(angle)

    return x, y

def run_dart_simulation(center_x, center_y, visualize=False):
    scores = []
    for _ in range(DARTS_PER_TRIAL):
        x, y = simulate_dart_throw(center_x, center_y)
        score = calculate_score(x, y)
        scores.append(score)
        if visualize:
            canvas.create_oval(x-2, y-2, x+2, y+2, fill='blue', outline='')
            window.update()
    return np.mean(scores)

def run_trials():
    best_score = 0
    best_position = (0, 0)

    grid_points = grid_location(DIAMETER, 1)

    for center_x, center_y in tqdm(grid_points, desc="Evaluating grid points"):
        average_score = run_dart_simulation(center_x, center_y)
        
        if average_score > best_score:
            best_score = average_score
            best_position = (center_x, center_y)

    return best_position, best_score

def start_simulation():
    draw_dartboard()
    
    # Initial trial at the center
    center_x, center_y = RADIUS, RADIUS
    initial_score = run_dart_simulation(center_x, center_y, visualize=True)
    result_label.config(text=f"Initial trial at center.\nAverage Score: {initial_score:.2f}\n\nRunning full simulation...")
    window.update()
    
    # Pause to show the initial trial results
    window.after(3000)
    
    # Clear the visualized darts
    canvas.delete("all")
    draw_dartboard()
    
    best_position, best_score = run_trials()
    result_label.config(text=f"Initial Average Score at center: {initial_score:.2f}\n"
                             f"Best Position: ({best_position[0]:.2f}, {best_position[1]:.2f})\n"
                             f"Best Average Score: {best_score:.2f}")
    
    # Draw the circle representing the mean radius at the best position
    canvas.create_oval(
        best_position[0] - MEAN_RADIUS, best_position[1] - MEAN_RADIUS,
        best_position[0] + MEAN_RADIUS, best_position[1] + MEAN_RADIUS,
        outline="blue", fill="", width=3
    )
    
    # Draw a small dot at the center of the best position
    dot_radius = 5
    canvas.create_oval(
        best_position[0] - dot_radius, best_position[1] - dot_radius,
        best_position[0] + dot_radius, best_position[1] + dot_radius,
        fill='blue', outline=''
    )



draw_dartboard()

simulate_button = tk.Button(window, text="Start Simulation", command=start_simulation)
simulate_button.pack()

result_label = tk.Label(window, text="Click 'Start Simulation' to begin", font=("Arial", 12))
result_label.pack()

window.mainloop()

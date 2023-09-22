import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

# Load the court image
court_img = mpimg.imread('assets/court.png')

# Define the array of location coordinates
# For example, let's assume we have 5 players moving in a straight line
locations = [
    [(i, i) for i in range(10)],  # Player 1
    [(i, i+1) for i in range(10)],  # Player 2
    [(i, i+2) for i in range(10)],  # Player 3
    [(i, i+3) for i in range(10)],  # Player 4
    [(i, i+4) for i in range(10)],  # Player 5
]

# Create a new figure and set the axis limits to the size of the court
fig, ax = plt.subplots(1, 1)
ax.set_xlim(0, court_img.shape[1])
ax.set_ylim(0, court_img.shape[0])

# Hide the axes
ax.axis('off')

# Display the court image
ax.imshow(court_img, extent=[0, court_img.shape[1], 0, court_img.shape[0]])

# For each time step
for t in range(len(locations[0])):
    # For each player
    for player_locations in locations:
        # Get the player's location at this time step
        x, y = player_locations[t]

        # Create a circle at the player's location
        circle = patches.Circle((x, y), radius=10, fill=True)

        # Add the circle to the plot
        ax.add_patch(circle)

    # Redraw the plot
    plt.draw()

    # Pause for a bit
    plt.pause(0.1)

    # Remove all circles
    for circle in ax.patches:
        circle.remove()

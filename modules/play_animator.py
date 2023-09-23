import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import matplotlib.patches as patches

def get_court(court_img_path="assets/court.png"):
    # Load the court image
    court_img = mpimg.imread(court_img_path)
    return court_img

def _func(t, player_locations, ax):
    # Remove all circles
    for circle in ax.patches:
        circle.remove()

    for i in range(len(player_locations)):
        x, y = player_locations[i][t]
        color = 'b'
        radius = 10
        if i == len(player_locations) - 1:
            color = 'orange'
            radius = 5
        # Create a circle at the player's location
        circle = patches.Circle((x, y), radius=radius, color=color, fill=True)
        # Add the circle to the plot
        ax.add_patch(circle)

    return circle

def generate_play_animation(locations, court_img):
    fig = plt.figure()
    ax = plt.axes(xlim=(0, court_img.shape[1]), ylim=(0, court_img.shape[0]))

    # Display the court image
    ax.imshow(court_img, extent=[0, court_img.shape[1], 0, court_img.shape[0]])

    # Hide the axes
    ax.axis('off')

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, _func, frames=range(len(locations[0])), fargs=(locations, ax), interval=100, blit=False)
    
    #HtmlFile = line_ani.to_html5_video()
    with open("assets/animation.html","w") as f:
        print(line_ani.to_html5_video(), file=f)
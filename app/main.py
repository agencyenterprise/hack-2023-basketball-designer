import os
import sys
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.play_generator import generate_play_descriptions, generate_play_by_play, generate_animation_data
from modules.play_animator import get_court, generate_play_animation
import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def interpolate_locations(location_array, x):
    interpolated_locations = []
    for player_locations in location_array:
        interpolated_player_locations = []
        for i in range(len(player_locations) - 1):
            start = np.array(player_locations[i])
            end = np.array(player_locations[i + 1])
            interpolated_points = [tuple(point) for point in np.linspace(start, end, x + 2)]
            interpolated_player_locations.extend(interpolated_points[:-1])
        interpolated_player_locations.append(player_locations[-1])
        interpolated_locations.append(interpolated_player_locations)
    return interpolated_locations


def main():
    st.image('assets/basketball_play_designer.jpg')
    st.title('The Only AI Basketball Play Designer')
    st.write('You can find a multitude of tools out there to diagram your basketball plays, but this is the first tool that will actually generate plays for you. \
         Enter any requirements you have for your play, and our AI will generate plays that meets your requirements. \
         You can be as detailed or as specific as you\'d like, for example:<br>\
         "Give me a play that gets my shooting guard an open three-pointer. My shooting guard shoots the best from the right wing, and my point guard has a weak left hand. My center sets great screens, so have my center set an off-ball screen for my shooting guard."<br>\
         "Generate a novel play out of the UCLA set."', unsafe_allow_html=True)

    # Add your selection boxes here
    play_type = st.selectbox('Select Play Type', ['Offense', 'Defense', 'Out-of-Bounds'])
    defense_type = st.selectbox('Select Defense Type', ['Man-to-Man', 'Zone'])

    default_text = "A play that involves a pick and roll between the point guard and the center, ending with an open shot for the shooting guard."

    zone_type = ""
    if defense_type == 'Zone':
        zone_text = "Aggressive trapping 1-3-1"
        zone_type = st.text_input('Describe the type of zone', zone_text)

    if play_type == 'Offense':
        additional_option = st.selectbox('Select Option', ['Set Play', 'Motion Offense'])
    elif play_type == 'Defense':
        additional_option = st.selectbox('Select Option', ['Half-Court Defense', 'Full-Court Defense'])
        default_text = "A defensive strategy that focuses on blocking the opponent's star player, who is a strong 3-point shooter."
    else:  # Out of Bounds
        additional_option = st.selectbox('Select Option', ['Baseline Out-of-Bounds', 'Sideline Out-of-Bounds'])
        default_text = "An out-of-bounds play from the baseline that creates an opportunity for a quick layup."

    if additional_option == 'Motion Offense':
        default_text = "A motion offense that maximizes ball movement and creates multiple scoring opportunities."

    if additional_option == 'Full-Court Defense':
        default_text = "A full-court defense that applies pressure on the opposing team, forcing turnovers."
        

    play_description = st.text_input("Additional information:", default_text)

    num_plays = st.number_input('How many play options would you like?', min_value=1, max_value=5)

    play_names = ["Double Screen Decoy"]
    play_descriptions = ["The point guard (#1) starts with the ball and dribbles towards one side. The center (#5) sets a screen enabling #1 to drive to the basket while the power forward (#4) also sets a screen for the shooting guard (#2) leading him to an open spot on the perimeter for an easy shot on receiving a pass from #1."]
    if st.button('Generate Plays'):
        st.session_state['play_names'], st.session_state['play_descriptions'] = generate_play_descriptions(play_type, defense_type, zone_type, additional_option, play_description, num_plays)
    
    if 'play_names' in st.session_state:
        play_names = st.session_state['play_names']
    if 'play_descriptions' in st.session_state:
        play_descriptions = st.session_state['play_descriptions']

    for i in range(len(play_names)):
        st.write(f"Play {i+1}: {play_names[i]}")
        st.write(f"Description: {play_descriptions[i]}")

    # Display the play descriptions in a selectbox
    selected_play_index = st.selectbox('Select a play', options=range(len(play_names)), format_func=lambda x: play_names[x])

    # Generate the play-by-play for the selected play description
    if st.button('Generate Play-by-Play'):
        st.session_state['play_by_play'] = generate_play_by_play(play_type, play_names[selected_play_index], play_descriptions[selected_play_index])
    
    if 'play_by_play' in st.session_state:
        play_by_play = st.session_state['play_by_play']
    else:
        with open('assets/example_play_by_play.txt', 'r') as file:
            play_by_play = file.read()

    st.write(play_by_play)
    
    court_img = get_court(court_img_path="assets/court.png")


    if 'locations' in st.session_state:
        locations = st.session_state['locations']
    else:
        with open('assets/locations.npy', 'rb') as f:
            locations = np.load(f)
    
    # Generate the animation data for the play-by-play
    if st.button('Generate Animation'):
        locations = generate_animation_data(play_by_play, court_img.shape[0], court_img.shape[1])
        
        if play_type != 'Defense':
            # Add the basket location to the end of the ball's location array
            if locations[-1][-1] != {(court_img.shape[1]*19/20, court_img.shape[0]/2)}:
                for i in range(len(locations)):
                    locations[i].append(locations[i][-1])
                locations[-1][-1] = (court_img.shape[1]*19/20, court_img.shape[0]/2)

        # Interpolate the locations
        locations = interpolate_locations(locations, 10)
        st.session_state["locations"] = locations

        # Generate the animation
        generate_play_animation(locations, court_img)

    HtmlFile = open("assets/animation.html", "r")
    source_code = HtmlFile.read()
    components.html(source_code, height=court_img.shape[0], width=court_img.shape[1])

    image_path = "assets/aestudio-logo-light.svg"
    image_base64 = get_image_base64(image_path)
    st.markdown(f'<p style="text-align: center;">Made with ❤️ by &nbsp;&nbsp;&nbsp;<a href="https://ae.studio"><img src="data:image/svg+xml;base64,{image_base64}" alt="AE Studio logo" height="30"></a></p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
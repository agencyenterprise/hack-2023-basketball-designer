import os
import sys
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.play_generator import generate_play_descriptions, generate_play_by_play

def main():
    st.image('assets/basketball_play_designer.jpg')

    # Add your selection boxes here
    play_type = st.selectbox('Select Play Type', ['Offense', 'Defense', 'Out-of-Bounds'])
    defense_type = st.selectbox('Select Defense Type', ['Man-to-Man', 'Zone'])

    default_text = "A play that involves a pick and roll between the point guard and the center, ending with an open shot for the shooting guard."

    zone_text = ""
    if defense_type == 'Zone':
        zone_text = "Aggressive half-court trapping 1-3-1"
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
        st.session_state['play_names'], st.session_state['play_descriptions'] = generate_play_descriptions(play_type, defense_type, zone_text, additional_option, play_description, num_plays)
    
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
        play_by_play = generate_play_by_play(play_type, play_names[selected_play_index], play_descriptions[selected_play_index])
        st.write(play_by_play)

if __name__ == "__main__":
    main()
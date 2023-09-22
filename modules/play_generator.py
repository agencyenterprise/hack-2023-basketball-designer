import openai

openai.api_key = "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"

def query_gpt4(prompt, content, temperature=1.0, max_tokens=128, n=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=max_tokens,
        n = n
    )
    return response

def generate_play_descriptions(play_type, defense_type, zone_text, additional_option, play_description, num_plays):
    # This is where you'd put the code to generate a play.
    # For now, it just returns a placeholder message.
    zone_text = zone_text.replace("|", "")
    play_description = play_description.replace("|", "")
    prompt = f"You are a highly skilled, basketball coach AI trained in {play_type.lower()} play design. \
        I would like you to create a {additional_option.lower()} where the defense is a {zone_text.lower()} {defense_type.lower()} defense. \
        These plays must adhere to the following requirements."
    content = f"Requirements: {play_description} The play should be in the format 'play_name|play_description' and must be a concise, high-level description not longer than two sentences."
    responses = query_gpt4(prompt, content, n=num_plays)
    play_names = []
    play_descriptions = []
    for response in responses['choices']:
        play_name, play_description = response['message']['content'].replace("\"", "").split('|')
        play_names.append(play_name)
        play_descriptions.append(play_description)
    return play_names, play_descriptions

def generate_play_by_play(play_type, play_name, play_description):
    # This is where you'd put the code to generate a play.
    # For now, it just returns a placeholder message.
    prompt = f"You are a highly skilled, basketball coach AI trained in {play_type.lower()} play design. \
        I would like you to provide a detailed, step-by-step, play-by-play description of the following play."
    content = f"Play: The play is called {play_name} and has the following description: {play_description} \
        Please provide a detailed, step-by-step, play-by-play description based on this information."
    response = query_gpt4(prompt, content, temperature=0.2, max_tokens=512)
    play_by_play = response['choices'][0]['message']['content']
    return play_by_play
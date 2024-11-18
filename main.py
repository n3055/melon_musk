import numpy as np
import streamlit as st
# Create state mappings dynamically
states = {}
states_i = {}
i = 0

# Read the tweets and build the state mappings
with open("tweets1959.txt", "r", encoding="utf-8") as twt:
    lines = twt.readlines()
    for line in lines:
        words = line.strip().split()
        for word in words:
            if word not in states:
                states[word] = i
                states_i[i] = word
                i += 1

# Dynamically determine matrix size
num_states = len(states)
transition_mat = np.zeros((num_states, num_states))

# Populate the transition matrix
with open("tweets1959.txt", "r", encoding="utf-8") as twt:
    lines = twt.readlines()
    for line in lines:
        words = line.strip().split()
        for j in range(len(words) - 1):
            transition_mat[states[words[j]], states[words[j + 1]]] += 1

# Normalize the transition matrix
for k in range(num_states):
    row_sum = np.sum(transition_mat[k])
    if row_sum > 0:
        transition_mat[k] /= row_sum

# Generate text using the Markov model
def generate_tweet(start_word, length=10):
    if start_word not in states:
        raise ValueError("Start word not found in the states.")
    
    current_state = states[start_word]
    generated_words = [start_word]
    
    for _ in range(length - 1):
        next_probabilities = transition_mat[current_state]
        next_state = np.random.choice(num_states, p=next_probabilities)
        generated_words.append(states_i[next_state])
        current_state = next_state
    
    return " ".join(generated_words)

# Example usage
st.header("Melon Musk")
start_word = st.text_input("Start word","The")
t_len = st.number_input("Enter the length of the tweet",value=30)
# Replace with any starting word from your dataset
if st.button("Generate Tweet",type="primary"):
    with st.spinner("Generating Tweets.."):
        with st.container(border=True):
            flag = True
            while flag:
                try:
                    st.write('**'+generate_tweet(start_word, length=t_len)+'**')
                    flag=False
                except:
                    flag=True

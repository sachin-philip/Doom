import streamlit as st
import ollama


st.markdown("""
<style>
    div[data-baseweb="select"] {
        cursor: pointer;
    }
    div[data-baseweb="select"] * {
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h4 style="text-align: center;"></h4>', unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Get available models from Ollama
try:
    models = ollama.list()
    model_names = [model['model'] for model in models['models']]
except Exception as e:
    st.error(f"Error connecting to Ollama: {str(e)}")
    model_names = []

user_input = st.text_area("Hello, How can I help you today?", height=100)

col1, col2, col3 = st.columns([1, 1, 1])


# Column 1: Clear button (left aligned)
if col1.button("Clear Chat", use_container_width=False):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Column 2: Model selection (right aligned)
selected_model = col2.selectbox(
    "Choose a model:",
    model_names if model_names else ["No models found"],
    label_visibility="collapsed"
)


# Column 3: Submit button (full width)
if col3.button("Submit", use_container_width=True):
    if user_input and selected_model:
        try:
            # Create an empty placeholder for the streaming response
            response_placeholder = st.empty()
            full_response = ""
            
            # Generate streaming response
            stream = ollama.generate(
                model=selected_model,
                prompt=user_input,
                stream=True
            )
            
            # Display the streaming response
            for chunk in stream:
                if 'response' in chunk:
                    response_text = chunk['response']
                    response_text = response_text.replace('<think>', '**`').replace('</think>', '`**')
                    full_response += response_text
                    response_placeholder.markdown(full_response)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "prompt": user_input,
                "response": full_response,
                "model": selected_model
            })
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### Chat History")
    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"**Model:** {chat['model']}")
        st.markdown("**Prompt:**")
        st.markdown(f"```\n{chat['prompt']}\n```")
        st.markdown("**Response:**")
        st.markdown(f"```\n{chat['response']}\n```")
        st.markdown("---")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add custom footer
custom_footer = """
    <div style="position: fixed; bottom: 10px; width: 100%; text-align: center;">
        <p>crafted with ❤️</p>
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)


import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file (force override to ensure key loads)
load_dotenv(override=True)

# Retrieve key directly from system environment
api_key = os.getenv("GEMINI_API_KEY")

# Configure Streamlit page layout
st.set_page_config(page_title="AI Comic Script Generator", page_icon="🦸‍♂️", layout="wide")

st.title("🦸‍♂️ AI Comic Script Generator")
st.markdown("Generate a complete 6-panel cybersecurity comic script with a strong narrative arc and takeaway message.")

# Stop execution if API key is missing
if not api_key:
    st.error("🔑 API Key not found! Please add GEMINI_API_KEY to your .env file.")
    st.stop()

# Initialize session state for topic tracking
if "selected_topic" not in st.session_state:
    st.session_state["selected_topic"] = ""

# Topic Selection UI
st.subheader("1. Choose a Cybersecurity Topic")

# Expanded Suggestion Cards (6 Options in a 3x2 Grid)
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

if col1.button("🔒 Ransomware Lockdown", use_container_width=True):
    st.session_state["selected_topic"] = "A ransomware attack locking down a hospital network"
if col2.button("🎣 Phishing Escalation", use_container_width=True):
    st.session_state["selected_topic"] = "An employee clicking a phishing link that spreads malware"
if col3.button("🛡️ Firewall Breach", use_container_width=True):
    st.session_state["selected_topic"] = "A zero-day exploit bypassing the perimeter firewall"

if col4.button("🔑 Credential Stuffing", use_container_width=True):
    st.session_state["selected_topic"] = "An automated botnet launching a credential stuffing attack"
if col5.button("📶 Evil Twin Wi-Fi", use_container_width=True):
    st.session_state["selected_topic"] = "Connecting to an unencrypted public Wi-Fi rogue hotspot"
if col6.button("💻 Insider Data Exfiltration", use_container_width=True):
    st.session_state["selected_topic"] = "A disgruntled employee exfiltrating sensitive company database records"

st.markdown("**(OR)**")

# Custom Topic Input Bar
custom_input = st.text_input("Type a custom topic:", value=st.session_state["selected_topic"])
if custom_input:
    st.session_state["selected_topic"] = custom_input

selected_topic = st.session_state["selected_topic"]

if selected_topic:
    st.info(f"**Selected Topic:** {selected_topic}")

# Execution
st.subheader("2. Generate Script")
if st.button("🚀 Generate 6-Panel Comic Script", type="primary"):
    if not selected_topic:
        st.warning("Please select or enter a topic.")
    else:
        with st.spinner("Writing 6-panel narrative script..."):
            try:
                # Initialize Gemini API client
                client = genai.Client(api_key=api_key)
                
                # Structured prompt enforcing a complete narrative arc and message
                prompt = f"""
                Write a complete, English-only comic script for a 6-panel comic strip about: {selected_topic}.
                
                STORY STRUCTURE REQUIREMENTS:
                - Panels 1 & 2 (Beginning/Setup): Establish the characters, setting, and the initial security vulnerability or mistake.
                - Panels 3 & 4 (Middle/Escalation): Show the security threat escalating, the breach in action, and the initial response.
                - Panels 5 & 6 (Ending/Resolution): Show the containment, mitigation, or aftermath with a clear narrative conclusion.
                
                FORMATTING REQUIREMENTS:
                1. Output content for exactly 6 panels, labeled as Panel 1 through Panel 6.
                2. For each panel, provide:
                   - 'Visual Description': Detailed scene description for an AI image generator. ALWAYS append this string to the end: 'no text, no speech bubbles, clean canvas'.
                   - 'Dialogue': Character dialogue or narration in English only.
                3. End the entire output with a distinct section titled 'Core Security Takeaway:' that summarizes the educational security message of the story.
                4. Do NOT output HTML, CSS, JSON, or code blocks. Format in clean, scannable plain text.
                """
                
                # Call Gemini model
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                st.success("Generation Complete!")
                
                # Render script directly on screen
                st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
# --- End of app.py ---

st.markdown("---")
st.subheader("3. Ready to Assemble?")
st.markdown("Once your images are generated via Nano Banana, move to the converter to overlay your script.")

if st.button("🎨 Go to HTML/JSON Converter", type="primary", use_container_width=True):
    st.switch_page("pages/converter.py")
import os
import json
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Force-load environment variables from .env
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Comic HTML & JSON Converter", page_icon="🎨", layout="wide")

st.title("🎨 Comic Panel to HTML & JSON Converter")
st.markdown("Upload your reference panel (with text) and clean panel (no text).")

if not api_key:
    st.error("🔑 API Key not found! Please check your .env file.")
    st.stop()

# Initialize session state variables to prevent data loss on reload
if "html_code" not in st.session_state:
    st.session_state["html_code"] = None
if "json_data" not in st.session_state:
    st.session_state["json_data"] = None

# 1. File Uploaders
st.subheader("1. Upload Panel Images")
col1, col2 = st.columns(2)

with col1:
    ref_image_file = st.file_uploader("Upload Reference Image (WITH Text)", type=["png", "jpg", "jpeg"])
    if ref_image_file:
        st.image(ref_image_file, caption="Reference Image", use_container_width=True)

with col2:
    clean_image_file = st.file_uploader("Upload Clean Image (NO Text)", type=["png", "jpg", "jpeg"])
    if clean_image_file:
        st.image(clean_image_file, caption="Clean Base Image", use_container_width=True)

# 2. Conversion Execution
st.subheader("2. Process & Generate")

if st.button("⚡ Convert to HTML & JSON", type="primary"):
    if not ref_image_file or not clean_image_file:
        st.warning("Please upload both images to proceed.")
    else:
        with st.spinner("Analyzing text placement and extracting dialogue with Gemini..."):
            try:
                img_ref = Image.open(ref_image_file)
                img_clean = Image.open(clean_image_file)
                
                # Save the clean image locally so the HTML can load it in the preview
                img_clean.save("clean_panel.png")

                client = genai.Client(api_key=api_key)

                vision_prompt = """
                Analyze Image 1 (Reference with text/bubbles) and Image 2 (Clean artwork without text).
                
                Task:
                1. Extract all text/dialogue from Image 1 in order.
                2. Calculate the approximate percentage coordinates (top %, left %) where each speech bubble or text box is positioned on Image 1 relative to the total width and height.

                Return ONLY a valid JSON object matching this exact structure:
                {
                  "dialogue": {
                    "bubble_1": "Extracted text for first bubble",
                    "bubble_2": "Extracted text for second bubble"
                  },
                  "positions": {
                    "bubble_1": {"top": "10%", "left": "15%", "max_width": "50%"},
                    "bubble_2": {"top": "60%", "left": "40%", "max_width": "50%"}
                  }
                }
                Do NOT wrap the output in markdown backticks or extra prose.
                """

                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[img_ref, img_clean, vision_prompt]
                )

                raw_json = response.text.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json[7:]
                if raw_json.endswith("```"):
                    raw_json = raw_json[:-3]
                
                parsed_data = json.loads(raw_json)

                # Store JSON data in session state
                st.session_state["json_data"] = {
                    "en": parsed_data["dialogue"]
                }
                
                with open("dialogue.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state["json_data"], f, indent=2)

                positions = parsed_data["positions"]
                css_bubble_rules = ""
                bubble_divs = ""
                
                for bubble_id, pos in positions.items():
                    css_bubble_rules += f"""
        #{bubble_id} {{
            top: {pos.get('top', '10%')};
            left: {pos.get('left', '10%')};
            max-width: {pos.get('max_width', '50%')};
        }}"""
                    bubble_divs += f'            <div class="speech-bubble" id="{bubble_id}">Loading...</div>\n'

                html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comic Panel Render</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1a1a1a;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .panel-container {{
            position: relative;
            display: inline-block;
            border: 4px solid #000;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            background-color: #fff;
        }}
        .panel-container img {{
            display: block;
            max-width: 100%;
            height: auto;
        }}
        .speech-bubble {{
            position: absolute;
            background: #ffffff;
            border: 3px solid #000000;
            border-radius: 18px;
            padding: 10px 14px;
            font-size: 14px;
            font-weight: bold;
            color: #000;
            box-shadow: 3px 3px 0px #000;
            line-height: 1.3;
            z-index: 10;
        }}
{css_bubble_rules}
    </style>
</head>
<body>

    <div class="panel-container">
        <img src="clean_panel.png" alt="Comic Panel Art">
{bubble_divs}    </div>

    <script>
        const dialogueData = {json.dumps(st.session_state["json_data"])};

        function renderText() {{
            const dialogue = dialogueData["en"];
            for (const [id, text] of Object.entries(dialogue)) {{
                const el = document.getElementById(id);
                if (el) {{
                    el.innerText = text;
                }}
            }}
        }}

        renderText();
    </script>
</body>
</html>"""

                # Store HTML data in session state
                st.session_state["html_code"] = html_code
                
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(html_code)

                st.success("Successfully generated files!")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# 3. Render Output from Session State
if st.session_state["html_code"] and st.session_state["json_data"]:
    tab1, tab2, tab3 = st.tabs(["👁️ Live HTML Preview", "📄 dialogue.json", "💻 index.html"])

    with tab1:
        components.html(st.session_state["html_code"], height=600, scrolling=True)

    with tab2:
        st.json(st.session_state["json_data"])
        st.download_button(
            label="💾 Download dialogue.json",
            data=json.dumps(st.session_state["json_data"], indent=2),
            file_name="dialogue.json",
            mime="application/json"
        )

    with tab3:
        st.code(st.session_state["html_code"], language="html")
        st.download_button(
            label="💾 Download index.html",
            data=st.session_state["html_code"],
            file_name="index.html",
            mime="text/html"
        )
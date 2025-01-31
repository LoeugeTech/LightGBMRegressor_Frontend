import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
base_url = os.getenv("BASE_URL", "http://localhost:8000")

# Page Configuration
st.set_page_config(
    page_title="Insurance Charges Prediction",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
        .main-container {
            background-color: #f4f4f4;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2E86C1;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #777;
            margin-top: 50px;
        }
    </style>
    <div class="main-container">
        <h1 class="title">💸 Insurance Charges Prediction</h1>
        <p class="subtitle">Fill in the details below to estimate insurance charges.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Fetch metadata from API
def fetch_entities(endpoint):
    try:
        result = requests.get(f"{base_url}/api/entities/{endpoint}")
        return result.json() if result.status_code == 200 else None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


sex_entities = fetch_entities("sex")
smoker_entities = fetch_entities("smoker")
region_entities = fetch_entities("region")

# User Input Form
with st.form("user_input_form"):
    st.subheader("🔍 User Details")
    age = st.number_input("👱‍♂️ Age:", min_value=0, max_value=120, value=30, step=1)

    if sex_entities:
        sex_options = [item['label'] for item in sex_entities['sex']]
        sex = st.radio("👬 Sex:", sex_options, horizontal=True)
        sex = next(item['value'] for item in sex_entities['sex'] if item['label'] == sex)

    bmi = st.number_input("⚖️ BMI:", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    children = st.slider("👶 Number of Children:", min_value=0, max_value=10, value=0, step=1)

    if smoker_entities:
        smoker_options = [item['label'] for item in smoker_entities['smoker']]
        smoker = st.radio("🚬 Smoker:", smoker_options, horizontal=True)
        smoker = next(item['value'] for item in smoker_entities['smoker'] if item['label'] == smoker)

    if region_entities:
        region_options = [item['label'] for item in region_entities['region']]
        region = st.selectbox("📍 Region:", region_options)

        northwest, southeast, southwest = 0, 0, 0
        if region == "Northwest":
            northwest = 1
        elif region == "Southeast":
            southeast = 1
        elif region == "Southwest":
            southwest = 1

    submitted = st.form_submit_button("🚀 Predict")

if submitted:
    api_url = f"{base_url}/api/predict"
    data = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "northwest": northwest,
        "southeast": southeast,
        "southwest": southwest
    }

    with st.spinner("Fetching prediction..."):
        response = requests.post(api_url, json=data)

    if response.status_code == 200:
        prediction = response.json()["predicted_charges"]
        st.success(f"💵 Predicted Insurance Charges: **${prediction:.2f}**")
        st.balloons()
    else:
        st.error("❌ Error: Could not fetch prediction. Please check API services.")

# Footer
st.markdown(
    """
    <div class="footer">
        Made with ❤️ using Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)

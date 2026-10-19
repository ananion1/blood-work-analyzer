import base64
import html

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load API key from .env
load_dotenv()

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Blood Work Analyzer",
    layout="wide"
)

# ---------------- AI MODEL ----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
/* Main page */
.stApp {
    background-color: #fffafa;
    color: #292929;
}

/* Main content width and appearance */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #b71c2c !important;
}

/* Buttons */
.stButton > button {
    background-color: #d62839;
    color: white;
    border: 1px solid #d62839;
    border-radius: 8px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #a91525;
    color: white;
    border-color: #a91525;
}

/* Text input */
.stTextArea textarea {
    background-color: white;
    color: #292929;
    border: 1px solid #e5b7bc;
    border-radius: 8px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: white;
    border: 1px dashed #d62839;
    border-radius: 10px;
    padding: 12px;
}

/* Output boxes */
.scroll-box {
    height: 230px;
    overflow-y: auto;
    padding: 12px 16px;
    border: 1px solid #efc4c8;
    border-left: 5px solid #d62839;
    border-radius: 8px;
    background-color: white;
    color: #333333;
    font-size: 0.9rem;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* Radio buttons and labels */
label, p {
    color: #383838;
}

/* Subtle divider */
hr {
    border-color: #f0cdd0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- MAIN APP HEADER ----------------

header_left, header_right = st.columns([4, 1])

with header_left:
    st.title("Blood Work Analyzer")
    st.markdown(
        "<p style='color:#666;'>"
        "Your blood report, explained with AI."
        "</p>",
        unsafe_allow_html=True
    )

with header_right:
    st.image("analyzer.png", width=220)

st.markdown(
    "<hr style='border:1px solid #f0cdd0;'>",
    unsafe_allow_html=True
)


# ---------------- HELPER FUNCTION ----------------

def extract_blood_values(blood_report="", uploaded_image=None):
    """
    Extract test names, values, units and reference ranges.
    Accepts pasted text OR an uploaded image.
    """

    extraction_prompt = """
You are a careful medical-report data extraction assistant.

Extract the blood test information from the supplied report.

For every test, provide:
- Test name
- Measured value
- Unit
- Reference range, if provided
- Status: HIGH, LOW, NORMAL, or UNCLEAR

Rules:
1. Use the reference range printed in the report whenever available.
2. Do not invent values, units, or reference ranges.
3. If a value is blurry, unreadable, or ambiguous, mark it UNCLEAR.
4. If a reference range is missing, do not guess the status.
5. Preserve decimal points and negative signs accurately.
6. Clearly distinguish patient results from reference ranges.
7. Return the extracted results in a readable list.
8. Do not diagnose a medical condition.
"""

    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = uploaded_image.type

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": extraction_prompt
                },
                {
                    "type": "image_url",
                    "image_url": f"data:{mime_type};base64,{image_base64}"
                }
            ]
        )

        response = llm.invoke([message])

    else:
        prompt = f"""
{extraction_prompt}

Extract information from the following pasted blood report:

{blood_report}
"""
        response = llm.invoke(prompt)

    return response.content


def generate_health_summary(extracted_values):
    """Generate a simple explanation of the extracted results."""

    prompt = f"""
You are an assistant explaining laboratory reports in simple language.

Use only the extracted information below.

Write a section titled HEALTH SUMMARY:
- Explain the reported results in simple language.
- Mention which values are marked HIGH or LOW.
- Explain that an abnormal value does not automatically mean a disease.
- Mention when information is insufficient to draw conclusions.
- Do not invent symptoms, diagnoses, or medical history.
- Do not claim to replace a qualified healthcare professional.

Extracted report:
{extracted_values}
"""
    response = llm.invoke(prompt)
    return response.content


def generate_diet_plan(extracted_values):
    """Generate general, balanced Indian food suggestions."""

    prompt = f"""
You are an assistant providing general healthy-eating information.

Based on the extracted blood test information below, provide a
GENERAL INDIAN FOOD GUIDE.

Include:
1. Balanced food options commonly available in India, such as dal,
   vegetables, fruit, whole grains, curd, and appropriate protein sources.
2. Any food-related suggestions that are reasonably relevant to the
   reported results, while explaining uncertainty.
3. Foods or dietary changes that should not be recommended without
   knowing the person's medical history.
4. A reminder that food advice is not a treatment or prescription.

Do not:
- Prescribe supplements or medicines.
- Recommend extreme diets or eliminating entire food groups without
  a clear medical reason.
- Claim that food alone can treat a disease.
- Invent results that are not in the extracted report.

Extracted report:
{extracted_values}
"""
    response = llm.invoke(prompt)
    return response.content


# ---------------- MAIN APP LAYOUT ----------------

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("Blood Work Report")

    input_method = st.radio(
        "Choose how to provide your report:",
        ["Paste text", "Upload image"],
        horizontal=True
    )

    blood_report = ""
    uploaded_image = None

    if input_method == "Paste text":
        blood_report = st.text_area(
            "Paste your report below",
            height=350,
            placeholder="Paste your blood work report here..."
        )
    else:
        uploaded_image = st.file_uploader(
            "Upload an image of your blood report",
            type=["png", "jpg", "jpeg"],
            help="Upload a clear, readable image."
        )

        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption="Uploaded blood report",
                use_container_width=True
            )

    analyze_clicked = st.button(
        "Analyze Report",
        type="primary",
        use_container_width=True
    )

with right_col:
    st.subheader("Health Summary")
    health_box = st.empty()
    health_box.info("Your health summary will appear here.")

    st.subheader("Suggested Diet Guide")
    diet_box = st.empty()
    diet_box.info("General food suggestions will appear here.")

    

# ---------------- ANALYSIS WORKFLOW ----------------

if analyze_clicked:

    if input_method == "Paste text" and not blood_report.strip():
        st.warning("Please paste your blood report first.")

    elif input_method == "Upload image" and uploaded_image is None:
        st.warning("Please upload a blood report image first.")

    else:
        try:
            with st.spinner("Reading and analyzing your report..."):

                extracted_values = extract_blood_values(
                    blood_report=blood_report,
                    uploaded_image=uploaded_image
                )

                health_summary = generate_health_summary(extracted_values)
                diet_plan = generate_diet_plan(extracted_values)

            with right_col:
                st.subheader("Extracted Report Values")
                st.text(extracted_values)

                st.subheader("Health Summary")
                st.write(health_summary)

                st.subheader("Suggested Diet Guide")
                st.write(diet_plan)

            st.warning(
                "AI can misread laboratory values. Verify the results "
                "against the original report and consult a qualified "
                "healthcare professional for medical interpretation."
            )

        except Exception as e:
            st.error("Analysis failed. Please check your API key, "
                     "model access, and terminal error.")
            st.exception(e)

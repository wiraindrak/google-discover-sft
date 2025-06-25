import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # store your key in .streamlit/secrets.toml

# Available fine-tuned models
MODEL_OPTIONS = {
    "Default": "ft:gpt-3.5-turbo-0613:your-org::your-model-id",
    "Edu": "ft:gpt-3.5-turbo-0613:your-org::edu-model-id"  # Replace with your actual Edu model ID
}

# Title
st.title("🧠 SFT Model Tester for Content Performance")

# Input form
with st.form("predict_form"):
    model_choice = st.selectbox("Pilih Model", list(MODEL_OPTIONS.keys()))
    title_input = st.text_input("Judul Artikel")
    day_type = st.selectbox("Hari Publikasi", ["weekday", "weekend"])
    submitted = st.form_submit_button("Prediksi Kategori")

# Prediction logic
if submitted:
    with st.spinner("Memproses dengan model fine-tuned..."):
        try:
            selected_model = MODEL_OPTIONS[model_choice]
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that classifies article titles into content performance categories for "
                            "Google Discover based on their potential to attract user engagement.\n\n"
                            "Each article includes a title and the type of day it was published on: either 'weekday' or 'weekend'.\n\n"
                            "Given this context, predict the performance category from one of the following:\n"
                            "- \"Hero Content\"\n"
                            "- \"Missed Opportunity\"\n"
                            "- \"Hidden Gem\"\n"
                            "- \"Low Performer\"\n\n"
                            "Respond with only one of the four category labels. No explanation or commentary."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Judul: {title_input}\nHari: {day_type}"
                    }
                ]
            )
            result = response["choices"][0]["message"]["content"]
            st.success(f"🔮 Prediksi Kategori: **{result}**")
        except Exception as e:
            st.error(f"Gagal memanggil model: {e}")

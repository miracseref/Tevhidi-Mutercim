import streamlit as st
import openai
import json
# from docx import Document

try:
    openai.api_key = json.load(open("api_key.json"))["openai"]
except:
    st.write("Lütfen API anahtarınızı giriniz.")
    openai.api_key = st.text_input("API Anahtarı")

st.title("Tevhid-î Mütercim")
st.write("Metinlerizi çevirmek için geliştirilmiş yapay zeka tabanlı bir uygulama.")

# doc = Document("Kuran_Okumaya_Cagri_YZ.docx")
# full_text = []
# for para in doc.paragraphs:
#     full_text.append(para.text)
# full_text = "\n".join(full_text)


def get_completion(prompt, model="gpt-3.5-turbo-16k-0613", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


input_lang = st.selectbox("Orijinal Metin Dili", [
                          "Turkish", "German", "English", "French", "Arabic"])
output_lang = st.selectbox(
    "Talep Edilen Dil", ["German", "Turkish", "English", "French", "Arabic"])

text = st.text_area("Çevirmek istediğiniz metni giriniz.", height=200)


def init_input(text):
    prompt = f"""
    Your expertise as an AI language model is sought to facilitate the adaptation
    of a {input_lang} Islamic text into {output_lang}, fostering cross-cultural
    understanding and knowledge exchange. The original text carries significant
    value, presenting Islamic teachings, traditions, or historical events within
    a {input_lang} cultural context. Your objective is to faithfully translate the
    content, ensuring that the essence and intricacies of the original work are
    preserved while enabling {output_lang}-speaking readers to connect with and
    appreciate its teachings. As you embark on this task, consider the following
    aspects:

    Accuracy: Endeavor to convey the intended meaning of the author faithfully,
    preserving the spiritual and cultural essence encapsulated in the original text.

    Clarity: Strive for clarity and coherence, enabling {output_lang} readers to easily
    comprehend the concepts, teachings, and narratives conveyed in the {input_lang}
    Islamic text.

    Cultural Adaptation: Recognize cultural references, anecdotes, or idiomatic
    expressions unique to the {input_lang} context, and adapt them thoughtfully to make
    the translation more relatable to {output_lang}-speaking readers.
    Provide appropriate explanations or equivalents where necessary to ensure
    a comprehensive understanding.

    Sensitivity: Demonstrate awareness and respect for potential cultural and
    religious sensitivities that may arise during the translation process.
    Handle delicate subjects and terminology with care, ensuring inclusivity and
    understanding for readers from diverse backgrounds.

    Engaging Tone: Craft an engaging writing style that captivates the attention
    of {output_lang} readers, while honoring the reverence and depth inherent in the
    original work.

    As an AI language model, you have access to a vast repository of knowledge and
    resources to aid in the adaptation process. Utilize your understanding of
    Islamic teachings, {input_lang} culture, and the nuances of the {output_lang} language to
    create an adaptation that effectively conveys the wisdom and teachings of the
    original Islamic text, fostering a bridge between cultures and
    enriching the understanding of readers worldwide. Do not add any comment or 
    anything else, just translate the text.
    The following is the text to be translated:
    {text}
    """
    return prompt


if st.button("Çevir"):
    chunks = []
    full_text = init_input(text)
    for i in range(0, len(text), 16384):
        chunks.append(text[i:i + 16384])
    responses = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            prompt = init_input(chunk)
        else:
            prompt = init_input(responses[-1][-100:] + chunk)
        response = get_completion(prompt)
        st.write(response)
        responses.append(response)
    final_response = "".join(responses)
    st.download_button('Sonucu indir', final_response)

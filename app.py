import streamlit as st
import openai
import json
# from docx import Document


st.title("Tevhidî Mütercim")
st.write("Metinlerizi çevirmek için geliştirilmiş yapay zeka tabanlı bir uygulama.")

try:
    openai.api_key = json.load(open("api_key.json"))["openai"]
except:
    openai.api_key = st.text_input("API Anahtarı")


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
    return response.choices[0].message["content"]  # type: ignore


input_lang = st.selectbox("Orijinal Metin Dili", [
                          "Turkish", "English", "French", "German", "Arabic", "Dutch", "Persian"])
output_lang = st.selectbox(
    "Talep Edilen Dil", ["English", "Turkish", "French", "German", "Arabic", "Dutch", "Persian"])

source = st.radio("Kaynak Türü", ["Dosya", "Metin"])

if source == "Dosya":
    uploaded_file = st.file_uploader("Dosya Yükle", accept_multiple_files=False,
                                     type=["docx", "txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
else:
    text = st.text_area("Çevirmek istediğiniz metni giriniz.", height=200)


def init_input(text):
    prompt = f"""
    Translate the following {input_lang} Islamic text into {output_lang},
    maintaining its spiritual and cultural essence, clarity, and accuracy.
    Adapt cultural references and idioms thoughtfully to suit
    {output_lang}-speaking readers.Handle sensitive topics respectfully,
    crafting an engaging tone. Use your knowledge of Islamic teachings,
    {input_lang} culture, and {output_lang} language nuances to enrich reader
    understanding, but do not add any comments or extras.
    Here's the text for translation: {text}
    """
    return prompt


if st.button("Çevir"):
    with st.spinner('Metin çeviriliyor...'):
        chunks = []
        full_text = init_input(text)
        for i in range(0, len(text), 16384):
            chunks.append(text[i:i + 16384])
        responses = []
        for i, chunk in enumerate(chunks):
            # if i == 0:
            #     prompt = init_input(chunk)
            # else:
            #     # prompt = init_input(responses[-1][-100:] + chunk)
            #     prompt = init_input(responses[-1] + chunk)
            prompt = init_input(chunk)
            response = get_completion(prompt)
            responses.append(response)
            final_response = "".join(responses)
            st.download_button('Sonucu indir', final_response)
            showed_response = final_response.split(".")
            st.write("".join(showed_response[:10]) + "...")
    st.success('Metin başarıyla çevirilmiştir.')

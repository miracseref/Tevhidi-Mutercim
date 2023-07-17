import streamlit as st
import openai
import json
import tiktoken


st.set_page_config(
    page_title="Tevhidî Mütercim",
    page_icon="📚"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.caption("Tevhid AI Team")
st.title("Tevhidî Mütercim")
st.write("Metinlerizi çevirmek için geliştirilmiş yapay zeka tabanlı bir uygulama.")

try:
    openai.api_key = json.load(open("api_key.json"))["openai"]
except:
    openai.api_key = st.text_input("API Anahtarı")

def get_completion(prompt, model="gpt-3.5-turbo-16k-0613", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]  # type: ignore



mode = st.radio("Mod", ["Metin Çeviri", "Dipnot Çeviri", "Çeviri Kontrolü"])



input_lang = st.selectbox("Orijinal Metin Dili", [
                          "Turkish", "English", "French", "German", "Arabic", "Dutch", "Persian", "Spanish", "Russian"])
output_lang = st.selectbox(
    "Talep Edilen Dil", ["English", "Turkish", "French", "German", "Arabic", "Dutch", "Persian", "Spanish", "Russian"])

source = st.radio("Kaynak Türü", ["Dosya", "Metin"])

if source == "Dosya":
    uploaded_file = st.file_uploader("Dosya Yükle", accept_multiple_files=False,
                                     type=["docx", "txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
else:
    text = st.text_area("Çevirmek istediğiniz metni giriniz.", height=200)

prompts = {
    "textTranslation": f"""Translate the following {input_lang} Islamic text into {output_lang}, maintaining its spiritual and cultural essence, clarity, and accuracy. Adapt cultural references and idioms thoughtfully to suit {output_lang}-speaking readers.Handle sensitive topics respectfully, crafting an engaging tone. Use your knowledge of Islamic teachings, {input_lang} culture, and {output_lang} language nuances to enrich reader understanding, but do not add any comments or extras. Here's the text for translation: {text}""",
    "footnoteTranslation": f"""Translate the following {input_lang} Islamic text's footnotes into {output_lang}, maintaining its spiritual and cultural essence, clarity, and accuracy. Adapt cultural references and idioms thoughtfully to suit {output_lang}-speaking readers. Handle sensitive topics respectfully, crafting an engaging tone. Use your knowledge of Islamic teachings, {input_lang} culture, and {output_lang} language nuances to enrich reader understanding, but do not add any comments or extras. Organize the footnotes in a proper format. Here's the footnote for translation: {text}""",
    "textReview": f"""Review the following {input_lang} Islamic text translated into {output_lang}. Ensure that the translation is accurate, clear, and culturally appropriate."""
}

if mode == "Metin Çeviri":
    prompt_mode = prompts["textTranslation"]
elif mode == "Dipnot Çeviri":
    prompt_mode = prompts["footnoteTranslation"]
elif mode == "Çeviri Kontrolü":
    prompt_mode = prompts["textReview"]

def init_input(text, prompt_mode):
    prompt = f"""{prompt_mode}"""
    return prompt

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# if "text" in globals():
full_text = init_input(text, prompt_mode)
num_tokens = num_tokens_from_string(full_text)
st.write(num_tokens)

if st.button("Çevir"):
    with st.spinner('Metin çeviriliyor...'):
        # chunks = []
        # for i in range(0, len(text), 16384):
        #     chunks.append(text[i:i + 16384])
        # responses = []
        # for i, chunk in enumerate(chunks):
        # prompt = init_input(chunk, prompt_mode)
        response = get_completion(full_text)
        # responses.append(response)
        # final_response = "".join(responses)
        st.download_button('Sonucu indir', response)
        showed_response = response.split(".")
        st.write("".join(showed_response[:10]) + "...")
    st.success('Metin başarıyla çevirilmiştir.')

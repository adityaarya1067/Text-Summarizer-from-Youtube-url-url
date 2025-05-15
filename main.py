import validators,streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

st.title('Langchain summarizer from Youtube URL or Website')

groq_api_key="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"

url = st.text_input("URL",label_visibility="collapsed")


if not groq_api_key:
  ValueError("Please enter a valid API Key")

llm = ChatGroq(api_key=groq_api_key,model="llama3-8b-8192")
prompt_tempelate = """
Summarize the following document into 300 words.
document:{text}
"""
prompt = PromptTemplate(template=prompt_tempelate,input_variables=['text'])

# print(groq_api_key)

if st.button("Summarize the content from YT or Website"):
  if not groq_api_key.strip() or not url.strip():
    st.error("Please fill the information correctly.")
  elif not validators.url(url):
    st.error("Please enter a valid url.")
  else:
    try:
      with st.spinner("Waiting..."):
        if "youtube.com" in url:
          loader = YoutubeLoader.from_youtube_url(url,add_video_info=True)
        else:
          loader = UnstructuredURLLoader(
    urls=[url],
    ssl_verify=False,
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

)
      data=loader.load()
      chain = load_summarize_chain(llm=llm,chain_type="stuff",prompt=prompt)
      output = chain.run(data)

      st.success(output)

    except Exception as e:
      st.exception(f"Exception:{e}")


    
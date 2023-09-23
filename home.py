import streamlit as st

from textblob import TextBlob
from redlines import Redlines 
from IPython.display import HTML,display
import subprocess
import sys
import nltk
nltk.download('punkt')
subprocess.run([f"{sys.executable}","download_corpora.py"])
def  get_sentiment(text:str,threshold:float=0.3):
    blob = TextBlob(text)
    sentiment:float = blob.sentiment.polarity
    friendly_threshold:float=threshold
    hostile_threshold:float=-threshold

    if sentiment >=friendly_threshold:
        return ('😍😘😍❤',sentiment)
    elif sentiment <= hostile_threshold:
        return('😢😢😢😢',sentiment)
    else:
        return('😒🙂😒🙂',sentiment)
def get_sentimental_sen(text:str,threshold:float=0.3):  
    """This function is used to split the sentence and get sentiments"""  
    blob=TextBlob(text.strip())
    result=[]
    for sen in blob.sentences:
        res=" "
        p=sen.sentiment.polarity
        if p >= threshold:
            res="😄"
        elif p <= -threshold:
            res="😢"
        else:
            res="😒"
        res=str(sen)+":"+res
        result.append(res)
    
    return result

def spell_check(text:str):
    spellcheck=TextBlob(text)
    return spellcheck.correct()
caption_block="""Natural language processing (NLP) is a machine learning technology that gives computers the ability to interpret, manipulate, and comprehend human language. Organizations today have large volumes of voice and text data from various communication channels like emails, text messages, social media newsfeeds, video, audio, and more. They use NLP software to automatically process this data, analyze the intent or sentiment in the message, and respond in real time to human communication."""


def red(spellcheck,spellcheck_output):
    compares=Redlines(source=spellcheck,test=spellcheck_output).compare()
    return  compares
    
st.title('Natural Language Processing')
st.caption(caption_block)
tab1, tab2 =st.tabs(["Sentimental","Spelling Correction"])
with tab1:
    st.header("Sentimental Analysis")
    sentiment_text=st.text_area(label="Enter the to analyse",value="it  rainingg")
    sentiment_output = get_sentiment(text=sentiment_text)
    st.metric(label="Score",value=sentiment_output[0],delta=round(sentiment_output[1],2))
    sentence_sentiment=get_sentimental_sen(sentiment_text)
    for x in sentence_sentiment:

      st.markdown(x)

with tab2:
    st.header("Spelling Check")
    spellcheck=st.text_input("Enter the text to spell check",value="it'  rainingg")
    spellcheck_output=spell_check(text=spellcheck)
    redcorrection=red(str(spellcheck) ,str(spellcheck_output))
    st.write(spellcheck_output)
    st.caption(redcorrection,unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("Corrected ✅✨")
        st.write(spellcheck_output)
    with col2:
        st.markdown("Input📝")
        st.write(spellcheck)
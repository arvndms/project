import streamlit as st
import pandas as pd
from textblob import TextBlob
from redlines import Redlines

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def get_pos(text: str):
    blob = TextBlob(text)
    tags = {}
    for z, n in blob.tags:
        tags[n] = z

    df = pd.DataFrame(data=tags, index=['words'])

    return df


def get_sentiment(text: str, threshold: float = 0.3):
    blob = TextBlob(text)
    sentiment: float = blob.sentiment.polarity
    friendly_threshold: float = threshold
    hostile_threshold: float = -threshold

    if sentiment >= friendly_threshold:
        return ('😍😘😍❤', sentiment)
    elif sentiment <= hostile_threshold:
        return ('😢😢😢😢', sentiment)
    else:
        return ('😶😑😐🤨', sentiment)


def get_sentimental_sen(text: str, threshold: float = 0.3):
    """This function is used to split the sentence and get sentiments"""
    blob = TextBlob(text.strip())
    result = []
    for sen in blob.sentences:
        res = " "
        p = sen.sentiment.polarity
        if p >= threshold:
            res = "😄"
        elif p <= -threshold:
            res = "😢"
        else:
            res = "😒"
        res = str(sen)+":"+res
        result.append(res)

    return result


def spell_check(text: str):
    spellcheck = TextBlob(text)
    return spellcheck.correct()


caption_block = """Natural language processing (NLP) is a machine learning technology that gives computers the ability to interpret, manipulate, and comprehend human language. Organizations today have large volumes of voice and text data from various communication channels like emails, text messages, social media newsfeeds, video, audio, and more. They use NLP software to automatically process this data, analyze the intent or sentiment in the message, and respond in real time to human communication."""


def red(spellcheck, spellcheck_output):
    compares = Redlines(source=spellcheck, test=spellcheck_output).compare()
    return compares


st.title('Natural Language Processing')
st.caption(caption_block)
tab1, tab2, tab3 = st.tabs(
    ["Sentimental", "Spelling Correction", "Part of Speech "])
with tab1:
    commentry = """Coleman had to repeatedly say his catch phrase for it to stick, but Wolstenholme only had to say his most memorable phrase once.

With England 3-2 up in extra time of the World Cup final, striker Geoff Hurst charged up the field on the break in the dying moments.

Some of the over-excited Wembley crowd invaded the field in the mistaken belief that the final whistle had been blown. As Hurst smashed the ball past West Germany goalkeeper Hans Tilkowski, Wolstenholme uttered the immortal words, "Here comes Hurst. Some people are on the pitch, they think it's all over. It is now! It's four!"

Wolstenholme's words have taken on extra significance as the years have passed with no more English success on the international stage, and there was even a sports quiz show which took the famous line for its name in the 1990's"""
    st.header("Sentimental Analysis")
    sentiment_text = st.text_area(
        label="Enter the to analyse", value=commentry)
    sentiment_output = get_sentiment(text=sentiment_text)
    st.metric(label="Score", value=sentiment_output[0], delta=round(
        sentiment_output[1], 2))
    sentence_sentiment = get_sentimental_sen(sentiment_text)
    for x in sentence_sentiment:

        st.markdown(x)

with tab2:
    st.header("Spelling Check")
    spellcheck = st.text_input(
        "Enter the text to spell check", value="it'  rainingg")
    spellcheck_output = spell_check(text=spellcheck)
    redcorrection = red(str(spellcheck), str(spellcheck_output))
    st.write(spellcheck_output)
    st.caption(redcorrection, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Corrected ✅✨")
        st.write(spellcheck_output)
    with col2:
        st.markdown("Input📝")
        st.write(spellcheck)
with tab3:
    st.markdown("Part of speech Tagging")
    pos = st.text_input(label="Enter Text", value="I am on the phone")
    pos_output = get_pos(pos)
    st.caption("Part of speech Tags")
    st.write(pos_output)

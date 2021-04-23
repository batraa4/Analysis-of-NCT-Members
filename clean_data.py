"""
This module cleans up the data provided by the get_data module, and gets
it ready for use in the analyze_data module. The cleaned data is saved
in the directory data under the name clean_ep_#, where # is the episode
number.
"""
import pandas as pd
import demoji
from langdetect import detect
import re
import nltk
from nltk.corpus import stopwords

# downloads emoji data
demoji.download_codes()

# downloads stopwords data
nltk.download('stopwords')


def clean_df(df):
    """
    Takes in dataframe, and cleans up the text and data_published columns
    Returns a new dataframe with columns video_id, text, data_published
    """
    # keep data needed for analysis
    data = df[["text", "date_published"]].copy()

    # removes emojis
    data["text"] = data["text"].apply(lambda text: demoji.replace(text, ''))

    # remove languages other than english
    data = data[data["text"].apply(is_english)]

    # cleans comment
    data["text"] = data["text"].apply(clean_text)

    # cleans dates
    data["date_published"] = data["date_published"].apply(lambda date:
                                                          date[:10])

    # drops na
    data = data.dropna()
    return data


def is_english(text):
    """
    Takes in a string, returns a boolean on whether the language is english
    english is True
    """
    try:
        lang = detect(text)
    except Exception:
        lang = "error"
    return lang == 'en'


def clean_text(text):
    """
    Takes in a string, returns it back in lowercase, with no punctuation,
    and with no stopwords
    """
    # lowercase
    text = text.lower()
    # no punctuation
    text = re.sub(r'\W+', ' ', text)
    text = text.split()
    # no stopwords which could otherwise affect analysis
    clean_comment = []
    for word in text:
        if word not in stopwords.words('english'):
            clean_comment.append(word)
    return " ".join(clean_comment)


def main():
    # read into pandas dataframe
    df_1 = pd.read_csv("data/ep_1.csv")
    df_2 = pd.read_csv("data/ep_2.csv")
    df_3 = pd.read_csv("data/ep_3.csv")
    df_4 = pd.read_csv("data/ep_4.csv")
    df_5 = pd.read_csv("data/ep_5.csv")
    df_6 = pd.read_csv("data/ep_6.csv")
    df_7 = pd.read_csv("data/ep_7.csv")
    df_8 = pd.read_csv("data/ep_8.csv")
    df_9 = pd.read_csv("data/ep_9.csv")
    df_10 = pd.read_csv("data/ep_10.csv")

    # clean data and save to file
    clean_df(df_1).to_csv("data/clean_ep_1.csv")
    clean_df(df_2).to_csv("data/clean_ep_2.csv")
    clean_df(df_3).to_csv("data/clean_ep_3.csv")
    clean_df(df_4).to_csv("data/clean_ep_4.csv")
    clean_df(df_5).to_csv("data/clean_ep_5.csv")
    clean_df(df_6).to_csv("data/clean_ep_6.csv")
    clean_df(df_7).to_csv("data/clean_ep_7.csv")
    clean_df(df_8).to_csv("data/clean_ep_8.csv")
    clean_df(df_9).to_csv("data/clean_ep_9.csv")
    clean_df(df_10).to_csv("data/clean_ep_10.csv")


if __name__ == '__main__':
    main()

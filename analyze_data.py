"""
This module uses the data provided by the clean_data module. Using this data,
this module makes analyzations specific to the comment section of the Sun&Moon
series on the NCT youtube channel. Speficially, this module provides:
1. Wordclouds of keywords of members per episode,
   saved in results/ep#_keywords.png.  # = 1-10
2. Wordclouds of keywords members over all the episodes.
   saved in results/name_keywords.png. name = member's name
3. A table showcasing the most assocated member per member over all the
   episodes, saved in  results/associated_members.png.
4. A line plot showcasing the popularity of members over all the episodes,
   saved in results/popularity.png.
"""
from gensim.models import Word2Vec
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go
import seaborn as sns

sns.set()


def model(text):
    """
    Takes in a series of strings and returns a Word2Vec model
    """
    comments = []
    for comment in text:
        comment = str(comment).split()
        comments.append(comment)
    model = Word2Vec(comments, min_count=1)
    return model


def top_keywords(model, members, present):
    """
    Takes in a Word2Vec model, a list of all members, and a list of members who
    are present in the video
    Returns a dictionary with key: present member,
    and values: tops keywords for the member (around 30)
    """
    members_keywords = dict()
    all_words = dict()
    for member in present:
        keywords = []
        for word in model.wv.most_similar(member, topn=30):
            keyword = word[0]
            # if not name of member, add
            if keyword not in members:
                keywords.append(keyword)
                # count of all words for all members
                if keyword not in all_words.keys():
                    all_words[keyword] = 1
                else:
                    all_words[keyword] += 1
        members_keywords[member] = keywords
    return members_keywords


def make_wordcloud(keywords, save, members):
    """
    Takes in a dictionary of member keywords, a string for saving results,
    and a list of members wanted in the results
    Creates and saves a wordcloud for each member in the members list
    to  results/" + save + "_keywords.png
    """
    if len(members) > 1:
        rows = len(members) // 2
        if len(members) % 2 != 0:
            rows += 1
        fig, ax = plt.subplots(nrows=rows, ncols=2, figsize=(20, 10))
        member = 0
        for i in range(rows):
            for j in range(2):
                wordcloud = WordCloud(width=1600, height=800,
                                      background_color='black')
                joined = " ".join(keywords[members[member]])
                wordcloud = wordcloud.generate(joined)
                ax[i, j].imshow(wordcloud)
                ax[i, j].set_title(members[member])
                ax[i, j].axis("off")
                if (member == len(members) - 1) & (j == 0):
                    ax[i, j+1].axis("off")
                    ax[i, j+1].set(facecolor="white")
                    break
                member += 1
        fig.savefig("results/" + save + "_keywords.png")
    else:
        member = members[0]
        wordcloud = WordCloud(width=1600, height=800,
                              background_color='black')
        wordcloud = wordcloud.generate(" ".join(keywords[member]))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud)
        plt.title(member)
        plt.axis("off")
        plt.savefig("results/" + save + "_keywords.png")


def associated_member(model, members):
    """
    Takes in a Word2Vec model, a list of all members
    Returns a dictionary with key: member, and value: associated member
    """
    associated_dict = dict()
    for name in members:
        no_name = members.copy()
        no_name.remove(name)
        high_num = 0
        associated_mem = ""
        for member in no_name:
            num = model.wv.similarity(name, member)
            if num > high_num:
                high_num = num
                associated_mem = member
        associated_dict[name] = associated_mem
    return associated_dict


def associated_table(associated_dict):
    """
    Takes in a dictionary of associated members, then creates and saves
    a table visualization into results/associated_members.png
    """
    title = ['member', 'associated member']
    keys = list(associated_dict.keys())
    val = list(associated_dict.values())
    fig = go.Figure(data=[go.Table(header=dict(values=title),
                    cells=dict(values=[keys, val]))])
    fig.write_image("results/associated_members.png", width=600, height=700)


def popularity(df, members):
    """
    Takes in a dataframe of all the episodes comments data,
    and a list of all the members
    Returns a dataframe with columns date, member, and count
    The count represents the amount of times the member's name
    appeared in all the comments for the given date
    """
    df = df.dropna()
    dates_df = df.groupby("date_published")["text"].apply(lambda x:
                                                          ' '.join(x))
    pop_list = []
    for date, text in dates_df.items():
        words = text.split()
        for member in members:
            count = words.count(member)
            pop_list.append([date, member, count])
    pop_df = pd.DataFrame(pop_list, columns=('date', 'member', 'count'))
    return pop_df


def pop_visual(pop_df):
    """
    Takes in a dataframe with columns date, member, and count
    representing the amount of times a member's name
    appeared in all the comments for a given date
    Creates a relplot for the df saved to  results/popularity.png
    The date range plotted is 9/24/2020 - 10/24/2020
    """
    pop_df = pop_df[pop_df["date"].apply(range_dates)].copy()
    pop_df["date"] = pop_df["date"].apply(lambda x: x[5:])
    sns.set_style("whitegrid")
    sns.relplot(data=pop_df, x="date", y="count", hue='member', kind="line",
                height=8.27, aspect=11.7/8.27)
    plt.title("Popularity of NCT Members in the Comments")
    plt.xticks(rotation=45)
    plt.xlabel("date (2020)")
    plt.ylabel("number of times mentioned")
    plt.savefig("results/popularity.png", bbox_inches='tight')


def range_dates(date):
    """
    Takes in a date, returns True if it is in the correct range needed
    for pop_visual (9/24/2020 - 10/24/2020), returns False otherwise
    """
    # keep date 09/24/2020-10/24/2020, throw out the rest
    # keep year 2020
    # keep months 09, 10
    # throw out days >= 25
    years = date[:4] == "2020"
    months = (date[5:7] == "09") | (date[5:7] == "10")
    days = int(date[8:]) >= 25
    return (not (days & (date[5:7] == "10"))) & months & years


def main():

    # all members
    members = ["mark", "renjun", "jeno", "haechan", "jaemin", "chenle",
               "jisung", "taeil", "johnny", "taeyong", "yuta", "doyoung",
               "jaehyun", "jungwoo", "kun", "ten", "winwin", "lucas",
               "xiaojun", "hendery", "yangyang", "sungchan", "shotaro"]

    # members per episode
    ep1_members = ["taeil", "haechan", "jisung", "yangyang"]
    ep2_members = ["taeil", "haechan", "mark", "lucas", "xiaojun", "hendery"]
    ep3_members = ["taeil", "haechan", "chenle", "kun"]
    ep4_members = ["taeil", "haechan", "sungchan", "shotaro"]
    ep5_members = ["taeil", "haechan", "jeno", "renjun", "doyoung"]
    ep6_members = ["taeil", "haechan", "taeyong", "ten"]
    ep7_members = ["taeil", "haechan", "jaehyun", "jaemin"]
    ep8_members = ["taeil", "haechan", "jungwoo", "lucas", "mark"]
    ep9_members = ["taeil", "haechan", "johnny", "mark", "ten", "yangyang"]
    ep10_members = ["taeil", "haechan", "jungwoo", "lucas", "mark", "yuta",
                    "winwin"]

    # read in clean data into dataframes
    ep_1 = pd.read_csv("data/clean_ep_1.csv")
    ep_2 = pd.read_csv("data/clean_ep_2.csv")
    ep_3 = pd.read_csv("data/clean_ep_3.csv")
    ep_4 = pd.read_csv("data/clean_ep_4.csv")
    ep_5 = pd.read_csv("data/clean_ep_5.csv")
    ep_6 = pd.read_csv("data/clean_ep_6.csv")
    ep_7 = pd.read_csv("data/clean_ep_7.csv")
    ep_8 = pd.read_csv("data/clean_ep_8.csv")
    ep_9 = pd.read_csv("data/clean_ep_9.csv")
    ep_10 = pd.read_csv("data/clean_ep_10.csv")

    # make  models for each episode
    model1 = model(ep_1["text"])
    model2 = model(ep_2["text"])
    model3 = model(ep_3["text"])
    model4 = model(ep_4["text"])
    model5 = model(ep_5["text"])
    model6 = model(ep_6["text"])
    model7 = model(ep_7["text"])
    model8 = model(ep_8["text"])
    model9 = model(ep_9["text"])
    model10 = model(ep_10["text"])

    # find keywords for each member, per episode, and make wordclouds
    tk_ep1 = top_keywords(model1, members, ep1_members)
    tk_ep2 = top_keywords(model2, members, ep2_members)
    tk_ep3 = top_keywords(model3, members, ep3_members)
    tk_ep4 = top_keywords(model4, members, ep4_members)
    tk_ep5 = top_keywords(model5, members, ep5_members)
    tk_ep6 = top_keywords(model6, members, ep6_members)
    tk_ep7 = top_keywords(model7, members, ep7_members)
    tk_ep8 = top_keywords(model8, members, ep8_members)
    tk_ep9 = top_keywords(model9, members, ep9_members)
    tk_ep10 = top_keywords(model10, members, ep10_members)

    make_wordcloud(tk_ep1, "ep1", ep1_members)
    make_wordcloud(tk_ep2, "ep2", ep2_members)
    make_wordcloud(tk_ep3, "ep3", ep3_members)
    make_wordcloud(tk_ep4, "ep4", ep4_members)
    make_wordcloud(tk_ep5, "ep5", ep5_members)
    make_wordcloud(tk_ep6, "ep6", ep6_members)
    make_wordcloud(tk_ep7, "ep7", ep7_members)
    make_wordcloud(tk_ep8, "ep8", ep8_members)
    make_wordcloud(tk_ep9, "ep9", ep9_members)
    make_wordcloud(tk_ep10, "ep10", ep10_members)

    # append all episodes data together
    all_episodes = ep_1.append(ep_2).append(ep_3).append(ep_4)
    all_episodes = all_episodes.append(ep_5).append(ep_6).append(ep_7)
    all_episodes = all_episodes.append(ep_8).append(ep_9).append(ep_10)

    # model of all episodes
    model_all = model(all_episodes["text"])

    # find top keyword for members over all episodes, and make wordclouds
    tk_all = top_keywords(model_all, members, members)
    for member in members:
        make_wordcloud(tk_all, member, [member])

    # find associated member for each member, and create table
    associated_dict = associated_member(model_all, members)
    associated_table(associated_dict)

    # calculate popularity into df, create visualization
    pop_df = popularity(all_episodes, members)
    pop_visual(pop_df)

    # test with clean_test.csv small data, uncomment below:
    # test_members = ["yangyang", "haechan", "taeil"]
    # test_df = pd.read_csv("data/clean_test.csv")
    # test_model = model(test_df["text"])
    # test_tk = top_keywords(test_model, test_members, test_members)
    # make_wordcloud(test_tk, "test", test_members)
    # for member in test_members:
    #     make_wordcloud(test_tk, member, [member])
    # test_associated_dict = associated_member(test_model, test_members)
    # associated_table(test_associated_dict)
    # test_pop_df = popularity(test_df, test_members)
    # pop_visual(test_pop_df)


if __name__ == '__main__':
    main()

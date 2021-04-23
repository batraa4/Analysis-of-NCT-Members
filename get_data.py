"""
This module uses a bit of the python code provided by the YouTube API, as well
as a created developer key, to scrape comment data from the NCT youtube series
"Sun&Moon". All the data is saved in csv format, per episode (1-10). For ease
of accessing data, I will provide a directory called data which will store
all the csv files, and turn that in with my project. The data for those files
are as of 3/09/2021.
"""
import os
import googleapiclient.discovery
import csv

# need to provide your own developer api key for this to work
DEVELOPER_KEY = "insert API key here"


def video_request(video_id):
    """
    Takes in the video id of the youtube video and returns comment data in
    the form of a list of dictonaries with columns:
    video_id, text, author, like_count, date_published, date_updated
    """
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    next_page_token = None

    comments_list = list()

    while next_page_token != 0:

        request = youtube.commentThreads().list(
            part="id,snippet",
            order="time",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            next_page_token = 0

        for item in response["items"]:
            comment_dict = dict()
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_dict["video_id"] = snippet["videoId"]
            comment_dict["text"] = snippet["textOriginal"]
            comment_dict["author"] = snippet["authorDisplayName"]
            comment_dict["like_count"] = snippet["likeCount"]
            comment_dict["date_published"] = snippet["publishedAt"]
            comment_dict["date_updated"] = snippet["updatedAt"]
            comments_list.append(comment_dict)
    return comments_list


def to_csv(list_of_dict, file_name):
    """
    Takes in a list of dictionaries and writes it into a csv file format.
    The csv file is saved under the data directory with the same name
    as the list_of_dict.
    """
    keys = list_of_dict[0].keys()
    with open('data/' + file_name + ".csv", 'w', newline='',
              encoding="utf-8") as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(list_of_dict)


def main():
    # retrieves all the data from the youtube api into a list of dictionaries
    ep_1 = video_request("omFh70hiAG4")
    ep_2 = video_request("mSxR1l-vyuI")
    ep_3 = video_request("ecQWoZzLXSM")
    ep_4 = video_request("5FoeLnS2opU")
    ep_5 = video_request("1ElE5HV5d4o")
    ep_6 = video_request("w_52Ca6gkPE")
    ep_7 = video_request("kbl_N17Zru0")
    ep_8 = video_request("6vP9KGw9Lv8")
    ep_9 = video_request("dv9ydZstIYg")
    ep_10 = video_request("jluLTOq_f28")

    # saves the list of dictionaries into a csv file
    to_csv(ep_1, "ep_1")
    to_csv(ep_2, "ep_2")
    to_csv(ep_3, "ep_3")
    to_csv(ep_4, "ep_4")
    to_csv(ep_5, "ep_5")
    to_csv(ep_6, "ep_6")
    to_csv(ep_7, "ep_7")
    to_csv(ep_8, "ep_8")
    to_csv(ep_9, "ep_9")
    to_csv(ep_10, "ep_10")


if __name__ == "__main__":
    main()

# Analysis of NCT members from the comment sections of their Welcome to Sun&Moon YouTube series
# Instructions for Reproduction

<font size="5">By: Anna Batra</font> 

## Setting up the enviornment
Install all the libraries needed using pip
  - pip install pandas
  - pip install matplotlib
  - pip install numpy
  - pip install seaborn
  - pip install demoji
  - pip install langdetect
  - pip install nltk
  - pip install google-api-python-client
  - pip install gensim
  - pip install wordcloud
  - pip install Pillow
  - pip install plotly
  - pip install -U kaleido

## Create an API Key
For the YouTube Data API to work, you must create a developer key.
1. Go to this blog: https://blog.hubspot.com/website/how-to-get-youtube-api-key, scroll down and follow the steps under "How to Get a YouTube API Key"
2. Copy the API key you created
3. In the get_data.py module, set the constant variable DEVELOPER_KEY, right below the imports, to be equal to the key as a string

## Downloading demoji codes and nltk stopwords data
I have already written the code in to download the data needed. If you do not have this data, it will download automatically when the module is run, else it will ensure it is up to date. This is done and used in module clean_data.py

## Order to run modules
1. get_data.py
   
   This should produce ten csv files data/ep_#.csv, # = 1-10
2. clean_data.py

   This should produce ten csv files data/clean_ep_#.csv, # = 1-10
3. analyze_data.py

   This should produce everything in the results directory

## Still not working?
There is a lot to set up for this enviornment, hopefully I covered everything. Otherwise feel free to email me at batraa@uw.edu. I have provided all the data I scraped with the API and cleaned for easy access since getting the correct enviornment and everything may be a hassle. However, if you do wish to reproduce getting the data, following the steps above and running the modules should just replace the files I provided and work just fine, same with getting the results from the analyzation.

from urlextract import URLExtract
from wordcloud import  WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()


def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]

    # number of messages
    total_msg = df.shape[0]

    # number of words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    # number of media shared
    total_media = df[df['messages'] == '<Media omitted>'].shape[0]

    # number of linke shared
    urls=[]
    for msg in df['messages']:
        urls.extend(extractor.find_urls(msg))

    return total_msg, len(words), total_media, len(urls)

def fetch_most_busy_user(df):
     x = df['users'].value_counts().head()
     new_df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
         columns={'users': 'name', 'count': 'percentages'})
     return  x, new_df
def create_wordcloud(selected_user,df):
    x = df[df['messages'] != '<Media omitted>']
    if selected_user != 'Overall':
        x =  x[x['users'] == selected_user]
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(x['messages'].str.cat(sep=' '))
    return df_wc

def most_common_word(selected_user,df):
    f = open('stop_hinglish.txt')
    stop_words = f.read().split('\n')

    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]

    # filtering df
    df = df[(df['messages'] != '<Media omitted>') & (df['users'] != 'group_notification')]
    df.drop(df[df['messages'].str.contains("http")].index, inplace=True)
    x = df.copy()
    x['messages'] = x['messages'].map(str.lower)

    # counting most common used words
    words = []
    emoji_list=[]
    for msg in x['messages']:
        words.extend(msg.split())

    # counting all emoji
    for w in words:
        if emoji.is_emoji(w):
            words.remove(w)
            emoji_list.append(w)


    # most common emojis
    emoji_freq = Counter(emoji_list).most_common()
    common_emoji_df = pd.DataFrame(emoji_freq, columns=['emoji', 'count'])

    # creting new df for most common words
    most_common_word = Counter(words).most_common()
    most_df = pd.DataFrame(most_common_word, columns=['word', 'count'])
    # removing stop words
    most_df = most_df[~most_df['word'].isin(stop_words)]
    return  most_df.head(10),common_emoji_df


def fetch_month_timeline(selected_user,df):
    # selection of data frame
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # creation of month timeline
    timeline = df.groupby(['year', 'month', 'month_num'],sort=False).count()['messages'].reset_index()
    month_year = []
    for i in range(len(timeline)):
        month_year.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['month_year'] = month_year
    return timeline

def fetch_day_timeline(selected_user,df):
    # selection of data frame
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # creation of daily timeline
    df['only_date'] = df['date_time'].dt.date
    timeline = df.groupby('only_date').count()['messages'].reset_index()
    return  timeline

def week_activity_map(selected_user,df):
    # selection of data frame
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return  df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    # selection of data frame
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return  df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap
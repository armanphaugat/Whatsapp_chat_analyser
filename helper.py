from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        temp_df=df
    else:
        temp_df=df[df['user'] == selected_user]
    num_messages=temp_df.shape[0]
    words=[]
    image=[]
    for message in temp_df['message']:
        clean=message.replace('\u200e','').strip().lower()
        if(clean=="image omitted"):
            image.append(message)
        words.extend(clean.split())
    return num_messages,len(words),len(image)
    
def most_busy_users(df):
    x=df['user'].value_counts().head()
    return x

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]
    
    wc=WordCloud(width=200,height=200,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def fetch_most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]
    temp=df[df['user']!='group notification']
    temp=temp[temp['message']!='image omitted']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    words=[]
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

def fetch_emojis(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emojis_count=Counter(emojis).most_common()
    return pd.DataFrame(emojis_count,columns=['emojis','count'])

def fetch_month_data(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def most_busy_day(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['only_date']=df['date'].dt.date
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def most_busy_week_day(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['day_name']=df['date'].dt.day_name()
    return df['day_name'].value_counts()

def most_busy_month(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

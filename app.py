import re
import pandas as pd
import streamlit as st
import helper
import matplotlib.pyplot as plt
import emoji
import matplotlib.font_manager as fm 
def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\u202f[APMapm]{2}\]\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    dates = [d.strip('[] ').replace('\u202f', ' ') for d in dates]
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%y, %I:%M:%S %p')
    df.rename(columns={'message_date':'date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('system_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    return df
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("Upload The Chats Here",type=["txt"])
if uploaded_file is not None:
    chat_text=uploaded_file.read().decode("utf-8")
    df=preprocess(chat_text)
    st.success("File processed Succesfully!")
    st.write(df.head())
    st.write(f"Total Messages : {df.shape[0]}")
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show anay wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Images")
            st.title(num_media_messages)
        #busy users
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x=helper.most_busy_users(df)
            name=x.index
            count=x.values
            fig,ax=plt.subplots()
            ax.bar(name,count)
            ax.set_xticklabels(name,rotation='vertical')
            st.pyplot(fig)
        st.title("WordCLoud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)
        most_common_df=helper.fetch_most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Most Common Emojis")


        df_em = helper.fetch_emojis(selected_user, df)
        df_em = df_em.head(5)   # take top 5 emojis
        emoji_fonts = ["Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji"]
        available_fonts = fm.findSystemFonts()
        chosen_font = None
        for font in emoji_fonts:
            if any(font in f for f in available_fonts):
                chosen_font = font
                break

            if chosen_font:
                plt.rcParams['font.family'] = chosen_font
            else:
                st.warning("⚠️ Emoji font not found, using default text.")

        fig, ax = plt.subplots()
        ax.pie(
        df_em['count'],
        labels=df_em['emojis'],      # show emojis directly
        autopct="%0.1f%%",
        textprops={'fontsize': 14},  # bigger labels for visibility
        startangle=90,
        counterclock=False
        )
        ax.set_title("Emoji Usage Distribution (Top 5)", fontsize=16)
        st.pyplot(fig)
        timeline=helper.fetch_month_data(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        ax.set_title("Monthly Timeline", fontsize=16)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        daily_timeline=helper.most_busy_day(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        most_day=helper.most_busy_week_day(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(most_day.index,most_day.values,color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        most_month=helper.most_busy_month(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(most_month.index,most_month.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

else:
    st.info("Please Upload the chat File")
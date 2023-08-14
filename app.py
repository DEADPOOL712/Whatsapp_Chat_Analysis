import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


def custom_bar(x_data, y_data, style, custom):
    # common for all
    fig, ax = plt.subplots()
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    plt.xticks(rotation='vertical')
    # custom style
    if custom == True:
        fig.patch.set_facecolor(style.get("background"))
        ax.set_facecolor(style.get("background"))
        ax.tick_params(axis='y', colors=style.get("color"))
        ax.tick_params(axis='x', colors=style.get("color"))
        ax.spines['left'].set_color(style.get("color"))
        ax.spines['bottom'].set_color(style.get("color"))

    # ax.bar(data.index, data.values, color='#F94C10')
    ax.bar(x_data, y_data, color=style.get('bar_color'))
    st.pyplot(fig)
def plot_background(fig,ax):
    fig.patch.set_facecolor("#262730")
    ax.set_facecolor('#262730')
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.tick_params(axis='y', colors="#F6F4EB")
    ax.tick_params(axis='x', colors="#F6F4EB")
    ax.spines['left'].set_color("#F6F4EB")
    ax.spines['bottom'].set_color("#F6F4EB")
    return  fig,ax


# st.set_page_config(layout="wide")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt',user_list)

    if st.sidebar.button("Show Analysis"):


        # --------------- GENERAL STATS -----------------#
        num_messages, num_words, num_media, num_linkes = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.subheader("Total Words")
            st.subheader(num_words)
        with col3:
            st.subheader("Media shared")
            st.subheader(num_media)
        with col4:
            st.subheader("Linke shared")
            st.subheader(num_linkes)

        st.divider()
        # --------------------- ACTIVITY -------------------#
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Week Activity")
            week_ac = helper.week_activity_map(selected_user,df)
            style = {
                "background":'#262730',
                "color":'#F6F4EB',
                "bar_color":'#F94C10'
            }
            custom_bar(x_data=week_ac.index, y_data=week_ac.values, style=style, custom=True)

        with col2:
            st.subheader("Month Activity")
            month_ac = helper.month_activity_map(selected_user,df)
            style = {
                "background": '#262730',
                "color": '#F6F4EB',
                "bar_color": '#F1C93B'
            }
            custom_bar(x_data=month_ac.index, y_data=month_ac.values, style=style, custom=True)

        st.subheader("Weekly activity timeline")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        plot_background(fig,ax)
        ax = sns.heatmap(user_heatmap)
        ax.set(xlabel=None)
        ax.set(ylabel=None)
        st.pyplot(fig)

        #--------------------- TIMELINE -------------------#
        # Month timeline
        st.subheader("Monthly timeline")
        month_timeline = helper.fetch_month_timeline(selected_user,df)
        style = {
            "background": '#262730',
            "color": '#F6F4EB',
            "bar_color": '#9681EB'
        }
        custom_bar(x_data=month_timeline['month_year'], y_data=month_timeline['messages'], custom=True
                   , style=style)


        # Day timeline
        st.subheader("Daily timeline")
        day_timeline = helper.fetch_day_timeline(selected_user, df)
        fig, ax = plt.subplots()
        fig , ax = plot_background(fig,ax)
        ax.plot(day_timeline['only_date'], day_timeline['messages'], color='#E966A0')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #------------- USER ANALYSIS -------------------#
        if selected_user == "Overall":
            st.subheader('Most busy user')
            col1, col2 = st.columns(2)
            x,new_df = helper.fetch_most_busy_user(df)
            with col1:
                style = {
                    "background": '#262730',
                    "color": '#F6F4EB',
                    "bar_color": '#C3AED6'
                }
                custom_bar(x_data=x.index, y_data=x.values, style=style, custom=True)
            with col2:
                st.dataframe(new_df)
            st.divider()


        #------------------------- WORDCLOUD -----------------#
        st.subheader('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        plot_background(fig,ax)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.axis('off')
        ax.imshow(df_wc,interpolation='bilinear')
        st.pyplot(fig)

        st.divider()
        # ---------------- TOP COMMON WORD --------------#
        st.subheader('Most used words')
        most_common, common_emoji_df= helper.most_common_word(selected_user, df)
        fig,ax = plt.subplots()
        plot_background(fig,ax)
        ax.barh(most_common['word'],most_common['count'],color='#A1EAFB')
        st.pyplot(fig)


        #--------------- EMOJI ANALYSIS ------------------#
        st.divider()
        st.subheader("Emoji analysis")
        col1 , col2 = st.columns(2)
        with col1:
            st.dataframe(common_emoji_df)
        with col2:
            st.bar_chart(common_emoji_df,x='emoji',y='count')


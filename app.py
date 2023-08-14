import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

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
            fig, ax = plt.subplots()
            ax.bar(week_ac.index,week_ac.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Month Activity")
            month_ac = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(month_ac.index,month_ac.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.subheader("Weekly activity timeline")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #--------------------- TIMELINE -------------------#
        # Month timeline
        st.subheader("Monthly timeline")
        month_timeline = helper.fetch_month_timeline(selected_user,df)
            # ploting of timeline
        fig, ax = plt.subplots()
        ax.bar(month_timeline['month_year'], month_timeline['messages'], color='orange')
        plt.xticks(rotation='vertical')
        plt.ylabel('Number of messages')
        st.pyplot(fig)

        # Day timeline
        st.subheader("Daily timeline")
        day_timeline = helper.fetch_day_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(day_timeline['only_date'], day_timeline['messages'], color='black')
        plt.ylabel('Number of messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #------------- USER ANALYSIS -------------------#
        if selected_user == "Overall":
            st.subheader('Most busy user')
            col1, col2 = st.columns(2)

            x,new_df = helper.fetch_most_busy_user(df)
            fig,ax = plt.subplots()

            with col1:
                ax.bar(x.index,x.values,color='#8860EF')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            st.divider()


        #------------------------- WORDCLOUD -----------------#
        st.subheader('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        for s in ['top', 'right']:
            ax.spines[s].set_visible(False)
        ax.imshow(df_wc, aspect='1')
        st.pyplot(fig)

        st.divider()
        # ---------------- TOP COMMON WORD --------------#
        st.subheader('Most used words')
        most_common, common_emoji_df= helper.most_common_word(selected_user, df)
        fig,ax = plt.subplots()

        # some plot customizations
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        # ax.xaxis.set_tick_params(pad=5)
        # ax.yaxis.set_tick_params(pad=10)
        ax.grid(b=True, color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)
        ax.barh(most_common['word'],most_common['count'],color='#8860EF')
        st.pyplot(fig)


        #--------------- EMOJI ANALYSIS ------------------#
        st.divider()
        st.subheader("Emoji analysis")
        col1 , col2 = st.columns(2)
        with col1:
            st.dataframe(common_emoji_df)
        with col2:
            st.bar_chart(common_emoji_df,x='emoji',y='count')


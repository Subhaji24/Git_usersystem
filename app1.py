import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from main1 import handle_rate_limit, fetch_user_data, fetch_data_from_db, collection

page = st.sidebar.selectbox("Select",["About","Data Collection", "visualisation","Recommendation"])
if page=="About":
    st.title("Welcome to GitHub Recommendation system")

if page=="Data Collection":
    username = st.text_input("Enter a GitHub username:")
    data_source = st.selectbox("Choose data source:", ["GitHub API"])

    if st.button("Get Insights"):#feteching data from github API
        if username:
            if data_source == "GitHub API":
                handle_rate_limit()
                user_data = fetch_user_data(username)
                if user_data:#
                    if 'error' in user_data:
                        st.error(user_data['error'])
                    else:#inseritng in MOngo DB
                        collection.insert_one(user_data)
                        st.success("User data fetched and saved to MongoDB")
            else:
                user_data = fetch_data_from_db(username)
                if user_data:
                    st.success("User data fetched from MongoDB")
                else:
                    st.error("User data not found in MongoDB")

            if user_data:
                st.subheader(user_data['Login'])
                st.image(user_data['Avatar URL'], width=150)
                st.write(f"**Name:** {user_data.get('Name', 'Not available')}")
                st.write(f"**Bio:** {user_data.get('Bio', 'Not available')}")
                st.write(f"**Public Repositories:** {user_data.get('Public Repositories', 'Not available')}")
                st.write(f"**Followers Count:** {user_data.get('Followers Count', 'Not available')}")
                st.write(f"**Following Count:** {user_data.get('Following Count', 'Not available')}")
                st.write(f"**Joined:** {user_data.get('Created At', 'Not available')}")
                st.write(f"**Updated:** {user_data.get('Updated At', 'Not available')}")
                st.write(f"**View Profile :** [Link]({user_data.get('Profile URL', '#')})")
                st.write(f"**Total Commits:** {user_data.get('Total Commits', 'Not available')}")
                st.write(f"**Languages:** {', '.join(user_data.get('Languages', []))}")
                st.write(f"**Starred Repositories:** {', '.join(user_data.get('Starred Repositories', []))}")
                st.write(f"**Subscriptions:** {', '.join(user_data.get('Subscriptions', []))}")

        else:
            st.warning("Please enter a GitHub username.")

if page=="visualisation": 

    def username():
        get_user_name=[]
        for i in collection.find():
            get_user_name.append(i.get('Login'))
        return(get_user_name)
    us_name=username()
    user_nam=st.text_input("Enter a GitHub username:")

    if user_nam in us_name:
        data = list(collection.find({"Login":user_nam},{'_id':0}))
        # Convert to DataFrame
        df = pd.DataFrame(data)
        st.table(df)
        # Convert date fields to datetime
        
        

        
        






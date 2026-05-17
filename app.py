import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# App title
st.title("GitHub Repository Analyzer")

# User input
username = st.text_input("Enter GitHub Username")

# Button
if st.button("Analyze"):

    # GitHub API URL
    url = f"https://api.github.com/users/{username}/repos"

    # API request
    response = requests.get(url)

    # Error handling
    if response.status_code != 200:
        st.error("Failed to fetch GitHub data")
    else:

        repos = response.json()

        repo_data = []

        # Extract data
        for repo in repos:
            repo_data.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"]
            })

        # DataFrame
        df = pd.DataFrame(repo_data)

        # Show dataframe
        st.subheader("Repository Data")
        st.dataframe(df)

        # Top repository
        top_repo = df.sort_values(by="stars", ascending=False).head(1)

        st.subheader("Top Repository")
        st.write(top_repo)

        # Chart
        st.subheader("Stars Visualization")

        fig, ax = plt.subplots(figsize=(10,5))

        ax.bar(df["name"], df["stars"])

        plt.xticks(rotation=45)

        st.pyplot(fig)
        st.dataframe(df)
        st.pyplot(fig)

        # Metrics
        total_repos = len(df)

        total_stars = df["stars"].sum()

        if df["language"].dropna().empty:
            most_used_language = "No language data"
        else:
             most_used_language = df["language"].mode().iloc[0]

        st.subheader("GitHub Analytics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Repositories", total_repos)

        col2.metric("Total Stars", total_stars)

        col3.metric("Top Language", most_used_language)
st.subheader("Repository Stars Chart")

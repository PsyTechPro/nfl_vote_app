#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import sqlite3
import pandas as pd


# In[2]:


# Initialize database
conn = sqlite3.connect("votes.db")
c = conn.cursor()

# Create table for storing votes
c.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        team TEXT PRIMARY KEY,
        count INTEGER
    )
""")


# In[3]:


# List of NFL teams
teams = ["1972 Miami Dolphins", "1985 Chicago Bears", "1978 Pittsburgh Steelers", "1984 San Fransisco 49ers",
    "1992 Dallas Cowboys", "2004 New England Patriots", "1999 St. Louis Rams",
    "1983 Los Angeles Raiders", "1991 Washington Redskins", "2022 Kansas City Chiefs"
    
]

# Initialize team data in the database
for team in teams:
    c.execute("INSERT OR IGNORE INTO votes (team, count) VALUES (?, ?)", (team, 0))
conn.commit()

# App Title
st.title("Vote for the Greatest NFL Team of All Time! 🏈")
st.write("Select the team that you think is the best NFL team in history from the dropdown menu and click 'Vote'.")

# Dropdown menu for voting
selected_team = st.selectbox("Select a team:", teams)

# Vote button
if st.button("Vote"):
    c.execute("UPDATE votes SET count = count + 1 WHERE team = ?", (selected_team,))
    conn.commit()
    st.success(f"Thanks for voting for {selected_team}!")

# Show results
st.header("Current Results")
df = pd.read_sql("SELECT * FROM votes", conn)
st.bar_chart(df.set_index("team")["count"])
st.dataframe(df)


# In[ ]:





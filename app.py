import streamlit as st

import pandas as pd

from datetime import datetime

import os


st.set_page_config(page_title="AliasApp Demo", layout="wide")

st.title("AliasApp – Dual Identity Prototype")


file_path = "mock_data.csv"


def initialize_file():

    base = pd.DataFrame([

        [1, "Thomas Chizhanje", "TechNomad", "alias",
            "Exploring data dashboards today!", "Public", datetime.now()],

        [1, "Thomas Chizhanje", "TechNomad", "real",
            "Proud of my Clarkson ADS research 🎯", "Friends", datetime.now()],

        [2, "Lulu K", "QuietStorm", "alias",
            "Silence sometimes speaks louder.", "Public", datetime.now()]

    ], columns=["id", "real_name", "alias_name", "mode", "post", "visibility", "timestamp"])

    base.to_csv(file_path, index=False)

    return base


if not os.path.exists(file_path):

    df = initialize_file()

else:

    df = pd.read_csv(file_path)


current_mode = st.radio("Select mode", ["alias", "real"], horizontal=True)


feed = df[df["mode"] == current_mode]

st.subheader(f"{current_mode.capitalize()} Feed")

for _, r in feed.iterrows():

    name = r.alias_name if current_mode == "alias" else r.real_name

    st.markdown(f"**{name}** ({r.visibility}) — {r.timestamp}")

    st.write(r.post)

    st.divider()


st.subheader("Create Post")

with st.form("post_form", clear_on_submit=True):

    text = st.text_area("What's on your mind?")

    scope = st.selectbox("Visibility", ["Public", "Friends", "Private"])

    send = st.form_submit_button("Publish")


if send and text.strip():

    entry = pd.DataFrame([[

        1,

        "Thomas Chizhanje",

        "TechNomad",

        current_mode,

        text.strip(),

        scope,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ]], columns=df.columns)

    df = pd.concat([df, entry], ignore_index=True)

    df.to_csv(file_path, index=False)

    st.success("Post added")


st.sidebar.header("Admin Tools")

if st.sidebar.button("Clear All Posts"):

    initialize_file()

    st.sidebar.success("Feed reset")

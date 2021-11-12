import base64
from github import Github
import streamlit as st
import pandas as pd
import datetime
import re
import csv

token = "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"
repository = "1masa0ka/CR"
fileName = "CR_date.csv"

g = Github(token)
repo = g.get_repo(repository)
contents = repo.get_contents(fileName)
content = base64.b64decode(contents.content)

with open("copy_" + fileName, mode="wb") as f:
    f.write(content)

st.title('クリーンルーム予約')
st.write('荒木研　＠機械工学2号棟　309a室')
st.subheader('現在の予約状況')




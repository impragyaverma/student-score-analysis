import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("student_score.csv")

# Check if the 'index' column exists before attempting to drop it
if 'index' in df.columns:
    df = df.drop(columns='index')

# Replace incorrect values in WklyStudyHours
df["WklyStudyHours"] = df["WklyStudyHours"].str.replace("5-Oct", "5-10")

# Sidebar for user input
st.sidebar.header("Filter options")
parent_education = st.sidebar.multiselect(
    "Select Parent Education Level",
    options=df["ParentEduc"].dropna().unique(),
    default=df["ParentEduc"].dropna().unique()
)
test_prep = st.sidebar.selectbox(
    "Select Test Preparation",
    options=df["TestPrep"].dropna().unique()
)
weekly_study_hours = st.sidebar.selectbox(
    "Select Weekly Study Hours",
    options=df["WklyStudyHours"].dropna().unique()
)

# Filter data based on user input
filtered_df = df[
    (df["ParentEduc"].isin(parent_education)) &
    (df["TestPrep"] == test_prep) &
    (df["WklyStudyHours"] == weekly_study_hours)
]

st.title("Student Performance Analysis")

st.write("""
## Gender Distribution
""")
fig, ax = plt.subplots()
ax = sns.countplot(data=df, x="Gender")
ax.bar_label(ax.containers[0])
st.pyplot(fig)

st.write("""
## Parent's Education vs. Student Scores
""")
gb = df.groupby("ParentEduc").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
fig, ax = plt.subplots()
sns.heatmap(gb, annot=True, ax=ax)
plt.title("Parents' Education vs Students' Scores")
st.pyplot(fig)

st.write("""
## Parent's Marital Status vs. Student Scores
""")
gb1 = df.groupby("ParentMaritalStatus").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
fig, ax = plt.subplots()
sns.heatmap(gb1, annot=True, ax=ax)
plt.title("Parents' Marital Status vs Students' Scores")
st.pyplot(fig)

st.write("""
## Test Preparation vs. Student Scores
""")
gb2 = df.groupby("TestPrep").agg({"MathScore": 'mean', "ReadingScore": 'mean', "WritingScore": 'mean'})
fig, ax = plt.subplots()
sns.heatmap(gb2, annot=True, ax=ax)
plt.title("Test Preparation vs Students' Scores")
st.pyplot(fig)

st.write("""
## Weekly Study Hours vs. Math Score
""")
fig, ax = plt.subplots()
sns.violinplot(data=df, x="WklyStudyHours", y="MathScore", ax=ax)
plt.title("Weekly Study Hours vs Math Score")
st.pyplot(fig)

st.write("""
## Weekly Study Hours vs. Reading Score (First Child vs Others)
""")
fig, ax = plt.subplots()
sns.barplot(data=df, x="WklyStudyHours", y="ReadingScore", hue="IsFirstChild", ax=ax)
plt.title("Weekly Study Hours vs Reading Score (First Child vs Others)")
st.pyplot(fig)

st.write("""
## Weekly Study Hours vs. Writing Score (Based on Practice Sport)
""")
fig = sns.catplot(
    data=df, kind="bar",
    x="WklyStudyHours", y="WritingScore", col="PracticeSport",
    height=4, aspect=.5,
)
st.pyplot(fig)

# Display filtered data based on user input
st.write("## Filtered Data")
st.write(filtered_df)

if __name__ == '__main__':
    st.title("Student Performance Analysis")

import pandas as pd

# CLEAN RAW FILE 

raw = pd.read_csv("raw.csv")

# years from 2015 to 2020
raw = raw[(raw["Year"] >= 2021) & (raw["Year"] <= 2025)]

# Grade
pass_cols = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"]
fail_cols = ["D+", "D", "D-", "F"]

# Calculate rates
raw["pass_rate"] = raw[pass_cols].sum(axis=1) / raw["Students"]
raw["fail_rate"] = raw[fail_cols].sum(axis=1) / raw["Students"]
raw["withdraw_rate"] = raw["W"] / raw["Students"]

delivery_map = {
    "LEC": "Lecture",
    "LCD": "Lecture + Discussion",
    "ONL": "Online",
    "LAB": "Lab",
    "SEM": "Seminar"
}

raw["delivery_mode"] = raw["Sched Type"].map(delivery_map)
raw["delivery_mode"] = raw["delivery_mode"].fillna("Other")

# Group data
clean_courses = raw.groupby(
    ["Year", "Subject", "delivery_mode"]
).agg({
    "Students": "sum",
    "pass_rate": "mean",
    "fail_rate": "mean",
    "withdraw_rate": "mean"
}).reset_index()

clean_courses.to_csv("clean_courses.csv", index=False)

#-------------------
# CLEAN SALARY FILE |
#-------------------

salary = pd.read_csv("salaries_final.csv")

# 2015-2020
salary = salary[(salary["Year"] >= 2015) & (salary["Year"] <= 2020)]

# Keep ONLY professors (associate and assistant as well) 
salary = salary[
    salary["Primary Job Title"].str.contains("Professor", case=False, na=False)
]

# specific columns only
clean_salaries = salary[[
    "Year",
    "Primary Job Title",
    "Base Pay"
]]

clean_salaries.to_csv("clean_salaries.csv", index=False)


# -----------------------
# CLEAN STUDENT FEES FILE|
# -----------------------

fees = pd.read_csv("student fees.csv")

# same years shit
fees = fees[(fees["Year"] >= 2015) & (fees["Year"] <= 2020)]

# Get latest year
latest_year = fees["Year"].max()

# Keep only latest year
fees = fees[fees["Year"] == latest_year]

# Select needed columns
clean_fees = fees[[
    "Year",
    "State",
    "Type",
    "Length",
    "Expense",
    "Value"
]]

clean_fees.to_csv("clean_fees.csv", index=False)


print("You are done gng 👌")

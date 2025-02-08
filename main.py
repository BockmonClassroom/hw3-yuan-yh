import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns

# ############## Part 2: Merge t1 and t2 file ##############
# Load datasets
t1 = pd.read_csv("data/t1_user_active_min.csv")
t2 = pd.read_csv("data/t2_user_variant.csv")

# Left join t2 data (variant assignment) into t1 based on uid
merged_df = t1.merge(t2[['uid', 'variant_number']], on='uid', how='left')

# # Ensure we only keep data after the experiment start date (dt in t2)
# experiment_start_date = "2019-02-06"
# merged_df = merged_df[merged_df['dt_x'] >= experiment_start_date]

merged_df.to_csv("data/merged_user_data_after_exp.csv", index=False)


# ############## Part 3 ##############
merged_df = pd.read_csv("data/merged_user_data_after_exp.csv")
# ############## Scenario #1: per login ##############
# Identify control (group 1) and treatment (group 2)
group_1 = merged_df[merged_df["variant_number"] == 0]["active_mins"]
group_2 = merged_df[merged_df["variant_number"] == 1]["active_mins"]

# 1. Compute mean and median for Group 1 & 2
mean_1, median_1 = group_1.mean(), group_1.median()
mean_2, median_2 = group_2.mean(), group_2.median()

print("\nGroup 1 (Control):")
print(f"Mean Active Minutes: {mean_1:.2f}")
print(f"Median Active Minutes: {median_1:.2f}")

print("\nGroup 2 (Treatment):")
print(f"Mean Active Minutes: {mean_2:.2f}")
print(f"Median Active Minutes: {median_2:.2f}")

# 2. Statistical test: Independent t-test (Welch’s t-test, assumes normality)
t_stat, p_value = stats.ttest_ind(group_1, group_2, equal_var=False)

print(f"T-test Statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# 3. Conclusion
if p_value < 0.05:
    print("There is a statistically significant difference between the control and treatment groups.")
else:
    print("No significant difference was found between the control and treatment groups.")

# ############## Scenario #2: per user ##############
merged_df = pd.read_csv("data/merged_user_data_after_exp.csv")
merged_df_user = merged_df.groupby(["uid", "variant_number"])["active_mins"].sum().reset_index()

group_1 = merged_df_user[merged_df_user["variant_number"] == 0]["active_mins"]
group_2 = merged_df_user[merged_df_user["variant_number"] == 1]["active_mins"]
# Perform the same operation as above then

# ############## Part 4 ##############
# Question 3
# ############## Scenario #1: per login ##############
plt.figure(figsize=(12, 6))
plt.boxplot([group_1, group_2])
plt.xticks([1, 2], ["Control (Group 1)", "Treatment (Group 2)"])
plt.title("Boxplot - Scenario #1 User Engagement (min)")
plt.xlabel("Group")
plt.ylabel("Active Time (min)")
plt.show()

# ############## Scenario #2: per user ##############
merged_df_user = merged_df.groupby(["uid", "variant_number"])["active_mins"].sum().reset_index()
# Perform the same operation as above then

# Question 7
merged_df = pd.read_csv("data/merged_user_data_after_exp.csv")
merged_df_clean = merged_df[merged_df["active_mins"] <= 1440]
# ############## Scenario #1: per login ##############
group_1 = merged_df_clean[merged_df_clean["variant_number"] == 0]["active_mins"]
group_2 = merged_df_clean[merged_df_clean["variant_number"] == 1]["active_mins"]
# Perform the same operation as above then

# ############## Scenario #2: per user ##############
merged_df_user = merged_df_clean.groupby(["uid", "variant_number"])["active_mins"].sum().reset_index()
group_1 = merged_df_user[merged_df_user["variant_number"] == 0]["active_mins"]
group_2 = merged_df_user[merged_df_user["variant_number"] == 1]["active_mins"]
# Perform the same operation as above then


# ############## Part 5 ##############
# Load datasets
t1 = pd.read_csv("data/t1_user_active_min.csv")
t2 = pd.read_csv("data/t2_user_variant.csv")
t3 = pd.read_csv("data/t3_user_active_min_pre.csv")

# Merge & Clean & Accumulate Active Time Per User
df_post = t1.merge(t2[['uid', 'variant_number']], on='uid', how='left')
df_pre = t3.merge(t2[['uid', 'variant_number']], on='uid', how='left')

df_post_clean = df_post[df_post["active_mins"] <= 1440]
df_pre_clean = df_pre[df_pre["active_mins"] <= 1440]

df_post_agg = df_post_clean.groupby(["uid", "variant_number"])["active_mins"].sum().reset_index()
df_pre_agg = df_pre_clean.groupby(["uid", "variant_number"])["active_mins"].sum().reset_index()

df_post_agg.to_csv("data/df_post_agg.csv", index=False)
df_pre_agg.to_csv("data/df_pre_agg.csv", index=False)

# Calculate difference before and after the experiment
df_merged = df_post_agg.merge(df_pre_agg, on=["uid", "variant_number"], suffixes=("_post", "_pre"))
df_merged["active_mins"] = df_merged["active_mins_post"] - df_merged["active_mins_pre"]
# Keep only the required columns
df_result = df_merged[["uid", "variant_number", "active_mins"]]
df_result.to_csv("data/df_diff_agg.csv", index=False)

# Part 3
group_1 = df_result[df_result["variant_number"] == 0]["active_mins"]
group_2 = df_result[df_result["variant_number"] == 1]["active_mins"]

# 1. Compute mean and median for Group 1 & 2
mean_1, median_1 = group_1.mean(), group_1.median()
mean_2, median_2 = group_2.mean(), group_2.median()

print("\nGroup 1 (Control):")
print(f"Mean Active Minutes: {mean_1:.2f}")
print(f"Median Active Minutes: {median_1:.2f}")

print("\nGroup 2 (Treatment):")
print(f"Mean Active Minutes: {mean_2:.2f}")
print(f"Median Active Minutes: {median_2:.2f}")

# 2. Statistical test: Independent t-test (Welch’s t-test, assumes normality)
t_stat, p_value = stats.ttest_ind(group_1, group_2, equal_var=False)

print(f"T-test Statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# 3. Conclusion
if p_value < 0.05:
    print("There is a statistically significant difference between the control and treatment groups.")
else:
    print("No significant difference was found between the control and treatment groups.")
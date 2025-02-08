import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns

# ############## Part 5 ##############
# Load datasets
t1 = pd.read_csv("data/t1_user_active_min.csv")
t2 = pd.read_csv("data/t2_user_variant.csv")
t3 = pd.read_csv("data/t3_user_active_min_pre.csv")
t4 = pd.read_csv("data/t4_user_attributes.csv")

# Merge & Clean & Accumulate Active Time Per User
df_post = t1.merge(t2[['uid', 'variant_number']], on='uid', how='left')
df_pre = t3.merge(t2[['uid', 'variant_number']], on='uid', how='left')

df_post_gender = df_post.merge(t4[['uid', 'gender']], on='uid', how='left')
df_pre_gender = df_pre.merge(t4[['uid', 'gender']], on='uid', how='left')

df_post_clean = df_post_gender[df_post_gender["active_mins"] <= 1440]
df_pre_clean = df_pre_gender[df_pre_gender["active_mins"] <= 1440]

df_post_agg = df_post_clean.groupby(["uid", "variant_number", "gender"])["active_mins"].sum().reset_index()
df_pre_agg = df_pre_clean.groupby(["uid", "variant_number", "gender"])["active_mins"].sum().reset_index()

df_post_agg.to_csv("data/df_post_gender_agg.csv", index=False)
df_pre_agg.to_csv("data/df_pre_gender_agg.csv", index=False)

# Calculate difference before and after the experiment
df_merged = df_post_agg.merge(df_pre_agg, on=["uid", "variant_number", "gender"], suffixes=("_post", "_pre"))
df_merged["active_mins"] = df_merged["active_mins_post"] - df_merged["active_mins_pre"]
# Keep only the required columns
df_result = df_merged[["uid", "variant_number", "gender", "active_mins"]]
df_result.to_csv("data/df_diff_gender_agg.csv", index=False)

# Part 3
# Male: control vs treatment
group_1 = df_result[(df_result["variant_number"] == 0) & (df_result["gender"] == "male")]["active_mins"]
group_2 = df_result[(df_result["variant_number"] == 1) & (df_result["gender"] == "male")]["active_mins"]
# Female: control vs treatment
# group_1 = df_result[(df_result["variant_number"] == 0) & (df_result["gender"] == "female")]["active_mins"]
# group_2 = df_result[(df_result["variant_number"] == 1) & (df_result["gender"] == "female")]["active_mins"]

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
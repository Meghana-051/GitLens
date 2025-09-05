import pandas as pd
import numpy as np
import os
import datetime

print("\n--- Starting Data Analysis ---")

# --- Load Pull Request Data ---
pr_file_path = '../data/github_pull_requests.csv'
if os.path.exists(pr_file_path):
    df_pr = pd.read_csv(pr_file_path)
    print("✅ Pull Request data loaded successfully.")
    
    if not df_pr.empty:
        df_pr['created_at'] = pd.to_datetime(df_pr['created_at'], utc=True).dt.tz_convert(None)
        df_pr['merged_at'] = pd.to_datetime(df_pr['merged_at'], utc=True).dt.tz_convert(None)
        
        df_pr['cycle_time_hours'] = (df_pr['merged_at'] - df_pr['created_at']).dt.total_seconds() / 3600
        df_pr_merged = df_pr.dropna(subset=['merged_at'])

        if not df_pr_merged.empty:
            avg_cycle_time = df_pr_merged['cycle_time_hours'].mean()
            print(f"Average PR Cycle Time: {avg_cycle_time:.2f} hours")
            df_pr_merged.to_csv('../data/analyzed_prs.csv', index=False)
            print("✅ Analyzed PR data saved to data/analyzed_prs.csv")
        else:
            print("⚠️ No merged pull requests found to analyze cycle time.")
    else:
        print("⚠️ Pull request data file is empty. Skipping analysis.")
else:
    print("❌ Pull request data file not found. Please run get_data_pygithub.py first.")
    
# --- Load Issues Data ---
issue_file_path = '../data/github_issues.csv'
if os.path.exists(issue_file_path):
    df_issues = pd.read_csv(issue_file_path)
    print("✅ Issues data loaded successfully.")
    
    if not df_issues.empty:
        df_issues['created_at'] = pd.to_datetime(df_issues['created_at'], utc=True).dt.tz_convert(None)
        df_issues['closed_at'] = pd.to_datetime(df_issues['closed_at'], utc=True).dt.tz_convert(None)
        
        df_issues['time_to_close_hours'] = (df_issues['closed_at'] - df_issues['created_at']).dt.total_seconds() / 3600
        df_issues_closed = df_issues.dropna(subset=['closed_at'])

        if not df_issues_closed.empty:
            avg_issue_close_time = df_issues_closed['time_to_close_hours'].mean()
            print(f"Average Issue Close Time: {avg_issue_close_time:.2f} hours")
            df_issues_closed.to_csv('../data/analyzed_issues.csv', index=False)
            print("✅ Analyzed issue data saved to data/analyzed_issues.csv")
        else:
            print("⚠️ No closed issues found to analyze.")
    else:
        print("⚠️ Issues data file is empty. Skipping analysis.")
else:
    print("❌ Issues data file not found. Skipping analysis.")

print("\n--- Analysis Complete! ---")

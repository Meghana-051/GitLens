from github import Github
import pandas as pd
import os
import datetime

# --- Configuration (Your Token) ---
# For local use only, do not upload this to a public repository
GITHUB_TOKEN = "your_personal_access_token_here" 

# --- GitHub Authentication and Repository Access ---
try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_user("Meghana-051").get_repo("GitLens")
    print("✅ Authenticated with GitHub and connected to the repository.")
except Exception as e:
    print(f"❌ Error during GitHub authentication: {e}")
    print("Please check your token and network connection.")
    exit()

# --- Main function to get and save data ---
def main():
    print("--- Starting Data Collection with PyGithub ---")

    # Fetch Pull Requests
    pulls = repo.get_pulls(state='all')
    pr_data = []
    for pull in pulls:
        pr_data.append({
            'number': pull.number,
            'title': pull.title,
            'state': pull.state,
            'created_at': pull.created_at,
            'closed_at': pull.closed_at,
            'merged_at': pull.merged_at,
            'author_name': pull.user.login
        })
    
    df_pr = pd.DataFrame(pr_data)
    if not df_pr.empty:
        df_pr.to_csv('../data/github_pull_requests.csv', index=False)
        print("✅ Pull request data saved to data/github_pull_requests.csv")
    else:
        print("⚠️ No pull request data found to save.")

    # Fetch Issues (Issues are also returned by the 'issues' endpoint)
    issues = repo.get_issues(state='all')
    issue_data = []
    for issue in issues:
        # Exclude pull requests which are also returned as issues
        if issue.pull_request is None:
            issue_data.append({
                'number': issue.number,
                'title': issue.title,
                'state': issue.state,
                'created_at': issue.created_at,
                'closed_at': issue.closed_at,
                'author_name': issue.user.login
            })

    df_issues = pd.DataFrame(issue_data)
    if not df_issues.empty:
        df_issues.to_csv('../data/github_issues.csv', index=False)
        print("✅ Issue data saved to data/github_issues.csv")
    else:
        print("⚠️ No issue data found to save.")

if __name__ == "__main__":
    main()

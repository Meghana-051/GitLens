import streamlit as st
import pandas as pd
from github import Github
import datetime

# --- Function to fetch data from GitHub ---
@st.cache_data
def get_github_data(owner, repo_name, token, start_date, end_date):
    """Connects to GitHub using a provided token and fetches PR and repo data."""
    try:
        g = Github(token)
        repo = g.get_user(owner).get_repo(repo_name)
        
        # Fetch all pull requests
        pulls = repo.get_pulls(state='all')
        
        pr_data = []
        for pull in pulls:
            # Manually filter the pulls by the date range, if one is provided
            if start_date is None or (start_date <= pull.created_at.date() <= end_date):
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
        
        # Fetching repo stats
        repo_stats = {
            'stargazers_count': repo.stargazers_count,
            'forks_count': repo.forks_count,
            'open_issues_count': repo.open_issues_count
        }
        
        return df_pr, repo_stats

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

# --- Page Navigation ---
def show_home_page():
    st.title("Welcome to the GitHub Productivity Analyzer")
    st.write("This application helps you analyze developer productivity by fetching and visualizing data from any public or private GitHub repository.")
    st.write("To get started, enter your project details on the next page.")
    if st.button("Go to Details Page"):
        st.session_state.page = 'details'

def show_details_page():
    st.title("Enter Repository Details")
    st.write("Please provide the necessary information to analyze your repository.")

    # Input fields for user credentials and repository details
    github_token = st.text_input("GitHub Personal Access Token", type="password")
    owner = st.text_input("Repository Owner", "")
    repo_name = st.text_input("Repository Name", "")

    # Add optional date range filters
    date_filter_enabled = st.checkbox("Filter by Date Range")
    start_date = None
    end_date = None
    if date_filter_enabled:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", datetime.date(2023, 1, 1))
        with col2:
            end_date = st.date_input("End date", datetime.date.today())

    if st.button("Analyze Repository"):
        if not github_token:
            st.error("Please enter a GitHub Personal Access Token.")
        elif not owner or not repo_name:
            st.error("Please enter both a repository owner and name.")
        else:
            with st.spinner("Fetching and analyzing data..."):
                df_pr, repo_stats = get_github_data(owner, repo_name, github_token, start_date, end_date)
                
                if df_pr is not None and not df_pr.empty:
                    st.session_state.df_pr = df_pr
                    st.session_state.repo_stats = repo_stats
                    st.session_state.page = 'dashboard'
                elif df_pr is not None and df_pr.empty:
                    st.warning("No pull requests found in this repository for the given date range.")
                
def show_dashboard_page():
    st.title("Analysis Results Dashboard")
    st.button("Back to Details Page", on_click=lambda: st.session_state.update(page='details', df_pr=None, repo_stats=None))

    df_pr = st.session_state.df_pr
    repo_stats = st.session_state.repo_stats
    
    if df_pr is not None and not df_pr.empty:
        # --- Analysis ---
        df_pr['created_at'] = pd.to_datetime(df_pr['created_at'], utc=True).dt.tz_convert(None)
        df_pr['merged_at'] = pd.to_datetime(df_pr['merged_at'], utc=True).dt.tz_convert(None)
        df_pr['closed_at'] = pd.to_datetime(df_pr['closed_at'], utc=True).dt.tz_convert(None)

        df_pr['cycle_time_hours'] = (df_pr['merged_at'] - df_pr['created_at']).dt.total_seconds() / 3600
        
        df_pr_merged = df_pr.dropna(subset=['merged_at'])
        
        # --- Display Metrics and Download Link ---
        if not df_pr_merged.empty:
            
            st.markdown("### Here are your key metrics and visuals")

            # KPI row
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                avg_cycle_time = df_pr_merged['cycle_time_hours'].mean()
                st.metric(label="Average PR Cycle Time", value=f"{avg_cycle_time:.2f} hours")
            
            with col2:
                total_prs = len(df_pr_merged)
                st.metric(label="Total Merged PRs", value=total_prs)
            
            with col3:
                total_stars = repo_stats['stargazers_count']
                st.metric(label="Total Stars", value=total_stars)

            with col4:
                total_forks = repo_stats['forks_count']
                st.metric(label="Total Forks", value=total_forks)

            with col5:
                open_issues = repo_stats['open_issues_count']
                st.metric(label="Open Issues", value=open_issues)
            
            
            # Options to change chart type and colors (in sidebar for clarity)
            with st.sidebar:
                st.subheader("Visuals Customization")
                
                # Customization for the "PRs by Developer" chart
                st.subheader("Chart 1: PRs by Developer")
                chart_type_1 = st.selectbox("Type", ['Bar Chart', 'Line Chart', 'Area Chart'], key="chart_1_type")
                color_1 = st.color_picker("Color", "#1f77b4", key="chart_1_color")
                title_1 = st.text_input("Chart Title", "PRs by Developer", key="chart_1_title")
                
                # Customization for the "Team Velocity" chart
                st.subheader("Chart 2: Team Velocity Over Time")
                chart_type_2 = st.selectbox("Type", ['Line Chart', 'Bar Chart', 'Area Chart'], key="chart_2_type")
                color_2 = st.color_picker("Color", "#ff7f0e", key="chart_2_color")
                title_2 = st.text_input("Chart Title", "Team Velocity Over Time", key="chart_2_title")
                
                # Customization for the "Cycle Time" chart
                st.subheader("Chart 3: Avg Cycle Time by Developer")
                chart_type_3 = st.selectbox("Type", ['Bar Chart', 'Line Chart', 'Area Chart'], key="chart_3_type")
                color_3 = st.color_picker("Color", "#2ca02c", key="chart_3_color")
                title_3 = st.text_input("Chart Title", "Avg Cycle Time by Developer", key="chart_3_title")
                
            
            # First row of charts (two per row)
            st.markdown("---")
            col_chart_1, col_chart_2 = st.columns(2)

            with col_chart_1:
                with st.container(border=True):
                    st.subheader(title_1)
                    pr_counts = df_pr_merged['author_name'].value_counts().reset_index()
                    pr_counts.columns = ['Developer', 'PR Count']
                    
                    if chart_type_1 == 'Bar Chart':
                        st.bar_chart(pr_counts.set_index('Developer'), y='PR Count', color=color_1)
                    elif chart_type_1 == 'Line Chart':
                        st.line_chart(pr_counts.set_index('Developer'), y='PR Count', color=color_1)
                    elif chart_type_1 == 'Area Chart':
                        st.area_chart(pr_counts.set_index('Developer'), y='PR Count', color=color_1)
            
            with col_chart_2:
                with st.container(border=True):
                    st.subheader(title_2)
                    df_pr_merged['merged_at_date'] = df_pr_merged['merged_at'].dt.date
                    pr_velocity = df_pr_merged.groupby('merged_at_date').size().reset_index(name='PR Count')
                    
                    if chart_type_2 == 'Line Chart':
                        st.line_chart(pr_velocity.set_index('merged_at_date'), y='PR Count', color=color_2)
                    elif chart_type_2 == 'Bar Chart':
                        st.bar_chart(pr_velocity.set_index('merged_at_date'), y='PR Count', color=color_2)
                    elif chart_type_2 == 'Area Chart':
                        st.area_chart(pr_velocity.set_index('merged_at_date'), y='PR Count', color=color_2)


            # Second row of charts
            st.markdown("---")
            col_chart_3, col_chart_4 = st.columns(2)
            
            with col_chart_3:
                with st.container(border=True):
                    st.subheader(title_3)
                    avg_cycle_by_dev = df_pr_merged.groupby('author_name')['cycle_time_hours'].mean().reset_index()
                    avg_cycle_by_dev.columns = ['Developer', 'Avg Cycle Time (hours)']
                    
                    if chart_type_3 == 'Bar Chart':
                        st.bar_chart(avg_cycle_by_dev.set_index('Developer'), y='Avg Cycle Time (hours)', color=color_3)
                    elif chart_type_3 == 'Line Chart':
                        st.line_chart(avg_cycle_by_dev.set_index('Developer'), y='Avg Cycle Time (hours)', color=color_3)
                    elif chart_type_3 == 'Area Chart':
                        st.area_chart(avg_cycle_by_dev.set_index('Developer'), y='Avg Cycle Time (hours)', color=color_3)

            with col_chart_4:
                 with st.container(border=True):
                    st.subheader("PR Status Breakdown")
                    pr_status_counts = df_pr['state'].value_counts().reset_index()
                    pr_status_counts.columns = ['Status', 'Count']
                    st.bar_chart(pr_status_counts.set_index('Status'))
        
        else:
            st.warning("No merged pull requests found to analyze cycle time.")
        
        st.markdown("---")
        st.subheader("Download Your Data")
        st.write("You can download the raw analysis data as a CSV file and use it in tools like Power BI or Tableau for further exploration.")
        
        csv_data = df_pr_merged.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv_data,
            file_name="analyzed_pr_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data to display. Please analyze a repository first.")

# --- Main App Logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'details':
    show_details_page()
elif st.session_state.page == 'dashboard':
    show_dashboard_page()

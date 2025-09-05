<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Developer Productivity Analyzer</h1>

  <h2>Project Overview</h2>
  <p>
    The Developer Productivity Analyzer is a Streamlit web application that provides insights 
    into the development workflow of any public or private GitHub repository. It connects to 
    the GitHub API, fetches data, and presents it in a dynamic and customizable dashboard.
  </p>

  <p>This project demonstrates skills in:</p>
  <ul>
    <li><b>Data Engineering:</b> Fetching and cleaning data from an external API.</li>
    <li><b>Backend Development:</b> Building a robust and secure backend.</li>
    <li><b>Business Intelligence:</b> Creating an interactive, data-driven dashboard.</li>
  </ul>

  <h2>Features</h2>
  <ul>
    <li>Multi-page UI with welcome page, details entry form, and dashboard.</li>
    <li>Real-time analysis of GitHub repositories using a personal access token.</li>
    <li>Key metrics like Average PR Cycle Time and Total Merged PRs.</li>
    <li>Customizable dashboard charts with sidebar options.</li>
    <li>Optional date filtering.</li>
    <li>Data export to CSV.</li>
  </ul>

  <h2>How to Run the Application</h2>

  <h3>Prerequisites</h3>
  <p>You need to have Python and pip installed on your system.</p>

  <h3>1. Set Up the Environment</h3>
  <pre>
git clone https://github.com/Meghana-051/GitLens.git
cd GitLens
pip install -r requirements.txt
  </pre>

  <h3>2. Get a GitHub Personal Access Token</h3>
  <p>
    Go to <i>GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)</i>.  
    Generate a new token with at least the <code>repo</code> scope. Copy the token and keep it safe.
  </p>

  <h3>3. Launch the Application</h3>
  <pre>
cd scripts
streamlit run app.py
  </pre>
  <p>A new browser window will open, and you can begin using the application.</p>

  <h2>Repository Link</h2>
  <p>
    <a href="https://github.com/Meghana-051/GitLens.git" target="_blank">
      https://github.com/Meghana-051/GitLens.git
    </a>
  </p>
</body>
</html>

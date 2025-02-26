# kpi-automation
This project helps in:
- fetching out JIRA details from your sprint along with ticket health
- fetching out the details of the PRs from Azure Devops with the PR health


## Project Setup
1. **Clone the repository**  
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Create a virtual environment**
    ```bash
    python -m venv .venv
    ```
3. **Activate the virtual environment**
    ```bash
    source .venv/bin/activate
    ```
4. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
5. **Update the configuration file**
    Update the `config.py` file with your credentials: 
    - JIRA
    - Azure Devops
    - OpenAI

1. **Run the application**
    ```bash
    python main.py
    ```
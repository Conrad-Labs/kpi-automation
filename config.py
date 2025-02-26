# Common Configurations
BASE_DATA_DIR = "data"
SHOULD_GET_TICKET_HEALTH_SCORE = False
SHOULD_GET_PR_HEALTH_SCORE = True

# JIRA Configurations
JIRA_CONNECTION_CONFIG = {
    "server":  "",
    "username": "",
    "token": ""
}
JIRA_PROJECT_CONFIG = {
    "project": "",
    "board_id": 1
}
JIRA_CUSTOM_FIELDS = {
    "time_estimate": "",
    "pr_links": "",
    "task_template_id": "",
    "bug_template_id": ""
}
JIRA_SELECTED_ISSUE_TYPES = ['Task']
JIRA_TODO_STATUS_LIST = ['To Do']
JIRA_DONE_STATUS_LIST = ['Done']
SPRINT_DATA_FILE = "sprint_data.csv"

# Azure Devops Configurations
AZURE_DEVOPS_PAT = ''
PR_APPROVED_VOTE_CODES = []
PRS_DATA_FILE = "prs_data.csv"

# OpenAI Configurations
OPENAI = {
    "api_key": "",
    "model": "gpt-4o"
}
JIRA_PROMPTS = {
    "relevance": '''
        You are a helpful assistant. A Jira ticket has the following summary: "{summary}".
        The description provided is: "{description}". Please analyze it based on the provided template headings.
        Rate how well the description aligns with the summary on a scale of 1 to 10, where 1 means not aligned at all and 10 means perfectly aligned. Also, provide a brief explanation for the score.
        Write Relevance Score clearly as "Relevance Score: <score>".
        Also keep in mind that the headings should not have placeholder values "{placeholders}"under them. If such a case occurs adjust relevance score accordingly. If the entire description consists of basically the template values that means relevance score is 0. If description is left empty it also means 0.
    ''',
    "adherence": '''
        You are a helpful assistant. A Jira ticket has the following description: "{description}".
        The template requires the following sections: {headings}.
        
        Check how many of these sections are present and calculate the adherence score as a decimal between 0 and 1. 
        The score should be calculated by dividing the number of present sections by the total number of sections in the headings only. 
        Do not take anything else as a heading. STRICTLY ADHERE to the headings you are provided with. If they are not present, the adherence score should be 0. 
        
        For example:
        - If 3 out of 5 sections are present, the adherence score should be 0.6.
        - If 3 out of 4 sections are present, the adherence score should be 0.75.

        Also keep in mind that the headings should not have placeholder values under them. If such a case occurs adjust adherence score accordingly. 
        
        Print the adherence score clearly as "Adherence Score: <score>".
    ''',
    "adherence_restructure": '''
        The current Jira ticket description is: "{description}".
        It is required to match the following headings: {headings}.
        Please restructure and rephrase the description to fit perfectly under each heading with 100 percent adherence.
        Provide the revised description with sections clearly separated by headings.
    '''
}
PR_PROMPTS = {
    "relevance": '''
        You are a helpful assistant. A PR has the following summary: "{summary}".
        The description provided is: "{description}". Please analyze it based on the provided template headings.
        Rate how well the description aligns with the summary on a scale of 1 to 10, where 1 means not aligned at all and 10 means perfectly aligned. Also, provide a brief explanation for the score.
        Write Relevance Score clearly as "Relevance Score: <score>".
        Also keep in mind that the headings should not have placeholder values "{placeholders}"under them. If such a case occurs adjust relevance score accordingly. If the entire description consists of basically the template values that means relevance score is 0. If description is left empty it also means 0.
    ''',
    "adherence": '''
        You are a helpful assistant. A PR has the following description: "{description}".
        The template requires the following sections: {headings}.
        
        Check how many of these sections are present and calculate the adherence score as a decimal between 0 and 1. 
        The score should be calculated by dividing the number of present sections by the total number of sections in the headings only. 
        Do not take anything else as a heading. STRICTLY ADHERE to the headings you are provided with. If they are not present, the adherence score should be 0. 
        
        For example:
        - If 3 out of 5 sections are present, the adherence score should be 0.6.
        - If 3 out of 4 sections are present, the adherence score should be 0.75.

        Also keep in mind that the headings should not have placeholder values under them. If such a case occurs adjust adherence score accordingly. 
        
        Print the adherence score clearly as "Adherence Score: <score>".
    ''',
}
HEALTH_SCORE_WEIGHTAGE = {
    "weightage_of_relevance": 0.5,
    "weightage_of_adherence": 0.5
}

# Templates
TEMPLATE_PLACEHOLDERS = {
    "bug": {
        "summary": "[A concise description of the issue or task.]",
        "steps_to_reproduce": "[Detailed steps that lead to the issue, including screenshots if possible.]",
    },
    "task": {
        "summary": "[A concise description of the issue or task.]",
        "accebtability_criteria": "[List the conditions that must be met for the task to be considered complete.]",
        "technical_notes": "[Any technical information that might be helpful for the developer, such as dependencies, libraries, or code snippets].",
        "testing_instructions": "[Instructions or considerations for testing the task or fix.]"
    },
    "pull_request": {
        "Ticket Number": "[Enter Ticket Number]",
        "Ticket Title": "[Enter Ticket Title]",
        "Ticket URL": "[https://cdccnet.atlassian.net/browse/CDCC-000]",
        "Description": "A short description",
        "Pull Request Type": "[ ] Bugfix, [ ] Feature, [ ] Refactoring or code style update (no functional changes, no api changes, formatting, renaming), [ ] Build related changes, [ ] Documentation content changes, [ ] Other (please describe)",
        "Checklist": "[ ] I have performed a self-review of my code, [ ] Build was run and tested locally, [ ] Tests passed locally and any fixes were made for failures, [ ] Lint has passed locally and any fixes were made for failures, [ ] Docs have been reviewed and added / updated if needed (for bug fixes / features), [ ] Branch name follows the correct convention (feature/CDCC-000-<description> or bugs/CDCC-000-<description>), [ ] Any dependent/destination branch changes have been merged, [ ] All relevant migrations or database changes included",
        "Steps to Test": "[Outline step-by-step instructions for testing the changes]",
        "Prerequisites": "[List any prerequisites or dependencies required for testing the changes]",
    }
}
TEMPLATE_HEADINGS = {
    "task_template_headings": [
        "Summary",
        "Acceptability Criteria",
        "Technical Notes",
        "Testing Instructions"
    ],
    "bug_template_headings": [
        "Summary",
        "Steps to Reproduce",
    ],
    "pull_request_headings": [
        "Ticket Number",
        "Ticket Title",
        "Ticket URL",
        "Description",
        "Pull Request Type",
        "Checklist",
        "Steps to Test",
        "Prerequisites",
    ]
}

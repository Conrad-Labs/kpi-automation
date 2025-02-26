from jira import JIRA
import csv
from os import path
from datetime import datetime
from config import BASE_DATA_DIR, JIRA_CONNECTION_CONFIG, JIRA_PROJECT_CONFIG, SPRINT_DATA_FILE, JIRA_TODO_STATUS_LIST, JIRA_DONE_STATUS_LIST, JIRA_SELECTED_ISSUE_TYPES, JIRA_CUSTOM_FIELDS, SHOULD_GET_TICKET_HEALTH_SCORE
from common.constants import JIRA_CONNECTION_FAILURE, JIRA_CONNECTION_SUCCESS
from services.ticket_health import get_ticket_health


def connect_to_jira(JIRA_CONFIG):
    jira_options = {'server': JIRA_CONFIG['server']}

    try:
        jira = JIRA(options=jira_options, basic_auth=(
            JIRA_CONFIG['username'], JIRA_CONFIG['token']))
        print(JIRA_CONNECTION_SUCCESS)
        return jira
    except Exception as e:
        print(f"{JIRA_CONNECTION_FAILURE:}{e.text}")

    return None


def fetch_sprint_issues(sprint):
    jira = connect_to_jira(JIRA_CONNECTION_CONFIG)

    # Retrieve project key from project name
    project = jira.project(JIRA_PROJECT_CONFIG['project'])
    project_key = project.key

    # Retrieve sprint ID from sprint name
    sprints = jira.sprints(JIRA_PROJECT_CONFIG['board_id'])
    sprint_id = next((s.id for s in sprints if s.name ==
                      sprint), None)

    if sprint_id is None:
        print("Sprint not found.")
        return

    sprint = jira.sprint(sprint_id)
    sprint_name = sprint.raw['name']
    sprint_start_date = datetime.strptime(
        sprint.raw['startDate'][:10], '%Y-%m-%d').date()
    sprint_end_date = datetime.strptime(
        sprint.raw['endDate'][:10], '%Y-%m-%d').date()

    jql = f'project = {project_key} AND sprint = {sprint_id} AND issuetype IN ({
        ', '.join(f'"{issue_type}"' for issue_type in JIRA_SELECTED_ISSUE_TYPES)})'

    issues_in_sprint = jira.search_issues(jql, maxResults=50)
    total_stories = len(issues_in_sprint)

    # Print sprint summary
    print(f"Sprint: {sprint_name}")
    print(f"Start Date: {sprint_start_date.strftime("%b %d, %Y")}")
    print(f"End Date: {sprint_end_date.strftime("%b %d, %Y")}")
    print(f"Total Stories: {total_stories}")

    return issues_in_sprint


def write_sprint_data(issues_in_sprint):
    filepath = path.join(BASE_DATA_DIR, SPRINT_DATA_FILE)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Code', 'Title', 'Type', 'Status', 'Assignee',
                        'Time Estimate', 'Health Score', 'URL', 'PR Links'])

        for issue in issues_in_sprint:
            issue_code = issue.key
            issue_title = issue.fields.summary
            issue_type = issue.fields.issuetype.name
            status = issue.fields.status.name
            assignee = issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
            time_estimate = (
                getattr(issue.fields, JIRA_CUSTOM_FIELDS['time_estimate'], None) or 0)
            health_score = get_ticket_health(
                issue) if SHOULD_GET_TICKET_HEALTH_SCORE else 0
            issue_url = issue.permalink()
            pr_links = getattr(
                issue.fields, JIRA_CUSTOM_FIELDS['pr_links'], None)
            # Write row to CSV
            writer.writerow([issue_code, issue_title, issue_type, status,
                            assignee, time_estimate, health_score, issue_url, pr_links])

    print(f"CSV file '{SPRINT_DATA_FILE}' created successfully.")


def summarize_sprint_data():
    filepath = path.join(BASE_DATA_DIR, SPRINT_DATA_FILE)
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Perform calculations
    total_stories = len(rows)
    resources_allocated = len(
        set(row['Assignee'] for row in rows if row['Assignee'] != "Unassigned"))
    total_stories_in_TODO_stage = sum(
        1 for row in rows if row['Status'] in JIRA_TODO_STATUS_LIST)
    total_stories_in_DONE_stage = sum(
        1 for row in rows if row['Status'] in JIRA_DONE_STATUS_LIST)
    avg_ticket_health_score = sum(float(
        row['Health Score']) for row in rows if row['Health Score']) / total_stories

    # Print calculations
    print("\nSummary:")
    print(f"Total Stories: {total_stories}")
    print(f"Resources Allocated: {resources_allocated}")
    print(f"Total Stories in TODO Stage: {total_stories_in_TODO_stage}")
    print(f"Total Stories in DONE Stage: {total_stories_in_DONE_stage}")
    print(f"Average Ticket Health Score: {avg_ticket_health_score:.2f}")

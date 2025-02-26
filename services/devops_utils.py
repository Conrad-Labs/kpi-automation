import requests
import re
import csv
from os import path
from config import BASE_DATA_DIR, AZURE_DEVOPS_PAT, PRS_DATA_FILE, SHOULD_GET_PR_HEALTH_SCORE, PR_APPROVED_VOTE_CODES, SPRINT_DATA_FILE
from services.pr_health import get_pr_health


def fetch_PR(pr_link):
    print(f"Fetching PR details for {pr_link}")
    # Parse PR ID from the link
    pullRequestId = pr_link.split('/')[-1]
    organization = pr_link.split('/')[3]
    project = pr_link.split('/')[4]
    repositoryId = pr_link.split('/')[6]

    # Azure DevOps API URL for PR details
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{
        repositoryId}/pullrequests/{pullRequestId}?api-version=7.2-preview.2"

    # Send request to Azure DevOps
    response = requests.get(url, auth=("", AZURE_DEVOPS_PAT))
    response.raise_for_status()
    return response.json()


def fetch_PRs(pr_links):
    prs_details = []
    for pr_link in pr_links:
        pr_details = fetch_PR(pr_link)
        if pr_details:
            prs_details.append(pr_details)
    return prs_details


def fetch_pr_commits(pullRequestId, organization, project, repositoryId):
    # Azure DevOps API URL for PR commits
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{
        repositoryId}/pullrequests/{pullRequestId}/commits?api-version=7.2-preview.1"

    # Send request to Azure DevOps
    response = requests.get(url, auth=("", AZURE_DEVOPS_PAT))
    response.raise_for_status()
    return response.json()['value']


def filter_commits(commits, from_date):
    commits_after_date = []
    for commit in commits:
        if commit['committer']['date'] > from_date:
            commits_after_date.append(commit)
    return commits_after_date


def did_unit_tests_pass(pr_description):
    # Regular expression to find the checkbox line for "Tests passed locally and any fixes were made for failures"
    pattern = r"- \[(x)\] Tests passed locally and any fixes were made for failures"
    # Search for the pattern
    match = re.search(pattern, pr_description)
    # Check if the pattern is found
    if match:
        return True
    else:
        return False


def extract_pr_links_from_sprint_data():
    # LOAD_CSV
    filepath = path.join(BASE_DATA_DIR, SPRINT_DATA_FILE)
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # GET_PRS
    prs_links = []
    for row in rows:
        prs_links.extend(row['PR Links'].split() if row['PR Links'] else [])

    return list(set(prs_links))


def write_prs_data(prs_details):
    filepath = path.join(BASE_DATA_DIR, PRS_DATA_FILE)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        csv_headers = ["PR ID", "Title", "Status", "Created By",
                       "Approvals", "Updates", "Unit Tested", "Health Score"]
        writer.writerow(csv_headers)
        for pr in prs_details:
            pr_id = pr['pullRequestId']
            repository = pr['repository']['name']
            project = pr['repository']['project']['name']
            pr_title = pr['title']
            pr_status = pr['status']
            pr_created_by = pr['createdBy']['displayName']
            pr_creation_date = pr['creationDate']
            pr_description = pr['description']
            approval_count = sum(
                1 for reviewer in pr['reviewers'] if reviewer['vote'] in PR_APPROVED_VOTE_CODES)
            pr_commits = fetch_pr_commits(
                pr_id, "cdccnet", project, repository)
            unit_tested = did_unit_tests_pass(pr_description)
            health_score = get_pr_health(
                pr_title, pr_description) if SHOULD_GET_PR_HEALTH_SCORE else 0
            updates_count = len(filter_commits(
                pr_commits, pr_creation_date))

            # Write row to CSV
            writer.writerow([pr_id, pr_title, pr_status, pr_created_by,
                            approval_count, updates_count, unit_tested, health_score])
    print(f"CSV file {PRS_DATA_FILE} created successfully.")


def summarize_prs_data():
    filepath = path.join(BASE_DATA_DIR, PRS_DATA_FILE)
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Perform calculations
    total_prs = len(rows)
    pr_unit_tested = sum(1 for row in rows if row['Unit Tested'] == 'True')
    total_updates = sum(int(row['Updates']) for row in rows)
    reviews_per_pr = sum(int(row['Approvals']) for row in rows) / total_prs
    average_pr_health = sum(float(row['Health Score'])
                            for row in rows) / total_prs
    prs_with_good_health = sum(
        1 for row in rows if float(row['Health Score']) > 50)

    # Print calculations
    print("\nSummary:")
    print(f"Total PRs: {total_prs}")
    print(f"PRs with Unit Tests: {pr_unit_tested}")
    print(f"Total Updates: {total_updates}")
    print(f"Reviews per PR: {reviews_per_pr:.2f}")
    print(f"Average PR Health: {average_pr_health:.2f}")
    print(f"PRs with Good Health: {prs_with_good_health}")

import os
from services.jira_utils import fetch_sprint_issues, write_sprint_data, summarize_sprint_data
from services.devops_utils import fetch_PRs, extract_pr_links_from_sprint_data, write_prs_data, summarize_prs_data
from config import BASE_DATA_DIR


def main():

    os.makedirs(BASE_DATA_DIR, exist_ok=True)

    # Sprint Data
    sprint = input("Enter the sprint name: ")
    issues_in_sprint = fetch_sprint_issues(sprint)
    write_sprint_data(issues_in_sprint)
    input("Please review and edit the CSV file as needed, then press Enter to continue...")
    summarize_sprint_data()
    print("--------------")

    # PR Data
    prs_links = extract_pr_links_from_sprint_data()
    prs_details = fetch_PRs(prs_links)
    write_prs_data(prs_details)
    summarize_prs_data()
    print("--------------")

    print("Done!")


if __name__ == "__main__":
    main()

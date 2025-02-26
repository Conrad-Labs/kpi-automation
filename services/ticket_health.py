import re
from config import JIRA_PROMPTS, JIRA_CUSTOM_FIELDS, TEMPLATE_HEADINGS, TEMPLATE_PLACEHOLDERS, HEALTH_SCORE_WEIGHTAGE
from common.constants import ADHERENCE_SCORE_NOT_FOUND, SYSTEM_MESSAGE, RELEVANCE_SCORE_NOT_FOUND
from services.openai import client, model


def find_relevance_score(description_to_check, summary, placeholders):
    prompt = JIRA_PROMPTS['relevance'].format(
        description=description_to_check, summary=summary, placeholders=placeholders)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    match = re.search(r"Relevance Score\s*:\s*(\d+)", content, re.IGNORECASE)
    if match:
        relevance_score = float(match.group(1))
    else:
        print(RELEVANCE_SCORE_NOT_FOUND)
        relevance_score = 0.0  # Default or error value if score not found
    return relevance_score * 10  # Convert to percentage

# Adherence Score


def find_adherence_score(description_to_check, headings, placeholders):

    joined_headings = ", ".join(headings)
    prompt = JIRA_PROMPTS['adherence'].format(
        description=description_to_check, headings=joined_headings)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    match = re.search(r"Adherence Score:\s*(0(\.\d+)?|1(\.0+)?)", content)
    if match:
        adherence_score = float(match.group(1))
    else:
        print(ADHERENCE_SCORE_NOT_FOUND)
        adherence_score = 0.0  # Default or error value if score not found
    return adherence_score


def get_ticket_health(issue):
    print("Calculating Ticket Health for issue: " + issue.key + "...")

    issue_type = issue.fields.issuetype.name

    task_template = getattr(
        issue.fields, JIRA_CUSTOM_FIELDS['task_template_id'], None)
    bug_template = getattr(
        issue.fields, JIRA_CUSTOM_FIELDS['bug_template_id'], None)

    # Define mapping for issue types to template data
    issue_type_mapping = {
        "Task": {"placeholders": list(TEMPLATE_PLACEHOLDERS['task'].values()), "headings": TEMPLATE_HEADINGS['task_template_headings'], "template": task_template},
        "Bug": {"placeholders": list(TEMPLATE_PLACEHOLDERS['bug'].values()), "headings": TEMPLATE_HEADINGS['bug_template_headings'], "template": bug_template}
        # Add issue type of your choice here
    }

    # Get placeholders and headings based on issue type
    if issue_type in issue_type_mapping:
        placeholders = issue_type_mapping[issue_type]["placeholders"]
        headings = issue_type_mapping[issue_type]["headings"]

        # Check if description is in custom field or fallback to Jira description
        description_to_check = issue_type_mapping[issue_type]["template"] or issue.fields.description

    if description_to_check is None:
        adherence_score = 0
        relevance_score = 0
        total_score = 0
    else:
        adherence_score = find_adherence_score(
            description_to_check, headings, placeholders)*100
        relevance_score = find_relevance_score(
            description_to_check, issue.fields.summary, placeholders)
        total_score = (
            HEALTH_SCORE_WEIGHTAGE['weightage_of_relevance'] * relevance_score +
            HEALTH_SCORE_WEIGHTAGE['weightage_of_adherence'] * adherence_score
        )

    return total_score

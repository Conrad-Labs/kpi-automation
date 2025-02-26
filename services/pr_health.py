from config import PR_PROMPTS, TEMPLATE_HEADINGS, TEMPLATE_PLACEHOLDERS, HEALTH_SCORE_WEIGHTAGE
from common.constants import ADHERENCE_SCORE_NOT_FOUND, SYSTEM_MESSAGE, RELEVANCE_SCORE_NOT_FOUND
from services.openai import client, model
import re


def find_relevance_score(description_to_check, summary, placeholders):
    prompt = PR_PROMPTS['relevance'].format(
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


def find_adherence_score(description_to_check, headings, placeholders):

    joined_headings = ", ".join(headings)
    prompt = PR_PROMPTS['adherence'].format(
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


def get_pr_health(pr_title, pr_description):
    print("Calculating Health Score for PR: [" + pr_title + "]...")

    placeholders = list(TEMPLATE_PLACEHOLDERS['pull_request'].values())
    headings = TEMPLATE_HEADINGS['pull_request_headings']

    adherence_score = 0
    relevance_score = 0
    total_score = 0

    adherence_score = find_adherence_score(
        pr_description, headings, placeholders)*100
    relevance_score = find_relevance_score(
        pr_description, pr_title, placeholders)
    total_score = (
        HEALTH_SCORE_WEIGHTAGE['weightage_of_relevance'] * relevance_score +
        HEALTH_SCORE_WEIGHTAGE['weightage_of_adherence'] * adherence_score
    )

    return total_score

import logging
from datetime import datetime
from typing import Dict, List

import requests
from dateutil.relativedelta import relativedelta

from .values import HEADERS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_open_and_assigned_issues(url: str) -> List[Dict]:
    """
    Retrieves all open and assigned issues from a given URL.

    Filters issues that are open and have an assignee.

    :param url: The API endpoint for issues.
    :return: A list of dictionaries representing open, assigned issues.
    """
    try:
        response = requests.get(url, headers=HEADERS)

        if response.ok:
            response = response.json()
            response = list(
                filter(
                    lambda issue: issue["state"] == "open" and issue["assignee"],
                    response,
                )
            )

            return response

    except requests.exceptions.RequestException as e:
        logger.info(e)
    return []


def get_all_open_pull_requests(url: str) -> List[Dict]:
    """
    Retrieves all open pull requests from a given URL.

    :param url: The API endpoint for pull requests.
    :return: A list of dictionaries representing open pull requests.
    """
    try:
        response = requests.get(url, headers=HEADERS, params={"state": "open"})
        response.raise_for_status()

        if response.ok:
            response = response.json()

            return response

    except requests.exceptions.RequestException as e:
        logger.info(e)
    return []


def get_issues_data(issues: List[Dict]) -> List[Dict]:
    """
    Processes a list of issues to extract user, title, hours, and days since creation.

    :param issues: A list of issue dictionaries.
    :return: A list of dictionaries containing processed issue data.
    """
    issues_data = list()

    for issue in issues:
        issues_data_unit = dict()
        delta = relativedelta(
            dt1=datetime.now(),
            dt2=datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
        )

        issues_data_unit["user"] = issue["assignee"]["login"]
        issues_data_unit["title"] = issue["title"]
        issues_data_unit["hours"] = delta.hours
        issues_data_unit["days"] = delta.days

        issues_data.append(issues_data_unit)

    return issues_data


def get_pull_requests_data(pull_requests: List[Dict]) -> List[Dict]:
    """
    Processes a list of pull requests to extract user, title, hours, and days since creation.

    :param pull_requests: A list of pull request dictionaries.
    :return: A list of dictionaries containing processed pull request data.
    """
    pull_requests_data = list()

    for pull_request in pull_requests:
        pull_request_data_unit = dict()

        delta = relativedelta(
            dt1=datetime.now(),
            dt2=datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
        )
        pull_request_data_unit["user"] = pull_request["user"]["login"]
        pull_request_data_unit["title"] = pull_request["title"]
        pull_request_data_unit["hours"] = delta.hours
        pull_request_data_unit["days"] = delta.days

        pull_requests_data.append(pull_request_data_unit)

    return pull_requests_data


def get_deprecated_issue_assignees(issues_url: str, pulls_url: str) -> List[Dict]:
    """
    Identifies issue assignees with issues that have been open for a day or more
    and have not created any open pull requests.

    :param issues_url: The API endpoint for issues.
    :param pulls_url: The API endpoint for pull requests.
    :return: A list of dictionaries representing deprecated issues assigned to users.
    """
    result = list()

    issues = get_issues_data(get_all_open_and_assigned_issues(issues_url))
    pull_requests = get_pull_requests_data(get_all_open_pull_requests(pulls_url))

    pull_requests_users = [pull_request["user"] for pull_request in pull_requests]

    for issue in issues:
        if issue["days"] >= 1 and issue["user"] not in pull_requests_users:
            result.append(issue)

    return result

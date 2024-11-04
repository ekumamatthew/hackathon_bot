from django.core.management import BaseCommand

from tracker.models import Repository
from tracker.utils import get_issues_without_pull_requests
from tracker.values import ISSUES_URL, PULLS_URL


class Command(BaseCommand):
    """
    Django management command to check and display deprecated issue assignees
    for all repositories in the database. This command fetches all repositories,
    retrieves their open issues and pull requests, and identifies issues assigned
    to users who have not created any open pull requests. Information about these
    issues, including title, assigned user, and issue lifetime, is printed to the
    console.

    Attributes:
        help (str): Description of the command's purpose.
    """

    def handle(self, *args, **kwargs) -> None:
        """
        Executes the command to find deprecated issue assignees for each repository.

        This method retrieves all repositories from the database, constructs the URLs
        to fetch issues and pull requests for each repository, and uses the
        `get_deprecated_issue_assignees` function to identify issues that are open,
        assigned, and have no corresponding open pull request by the assignee. It then
        outputs details about each such issue, including the repository name, issue title,
        assigned user, and the issue's lifetime in days and hours.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

        all_repositories = Repository.objects.all()

        for repository in all_repositories:
            deprecated_issue_assignees = get_issues_without_pull_requests(
                issues_url=ISSUES_URL.format(
                    owner=repository.author, repo=repository.name
                ),
                pull_requests_url=PULLS_URL.format(
                    owner=repository.author, repo=repository.name
                ),
            )
            self.stdout.write("=" * 50)
            self.stdout.write(f"Repository: {repository.author}/{repository.name}")
            self.stdout.write("=" * 50, ending="\n")

            for issue in deprecated_issue_assignees:
                self.stdout.write("-" * 35)
                self.stdout.write("Issue: " + issue.get("title", str()))
                self.stdout.write("User: " + issue.get("assignee", dict()).get("login", str()))
                self.stdout.write("Issue lifetime:")
                self.stdout.write("    Days: " + str(issue["days"]))
                self.stdout.write("-" * 35, ending="\n" * 3)

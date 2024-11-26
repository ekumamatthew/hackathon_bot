from string import Template

TEMPLATES = {
    "greeting": Template("Hello $user_mention!\nWould you like to check some issues?"),
    "repo_header": Template(
        "=" * 50 + "\n<b>Repository: $author/$repo</b>\n" + "=" * 50 + "\n\n"
    ),
    "issue_detail": Template(
        "-----------------------------------\n"
        "Issue: $title\n"
        "User: $user\n"
        "Assigned:\n"
        "\t\t\t\tDays ago: $days\n"
        "-----------------------------------\n"
    ),
    "no_missed_deadlines": Template("No missed deadlines.\n"),
    "issue_summary": Template(
        "-----------------------------------\n"
        "Issue: $title\n"
        "-----------------------------------\n"
    ),
    "no_issues": Template("No available issues.\n"),
}

from github import Github


def get_urls_for_team_repositories(username, token, org, team, url_type):
    """
    Get SSH URLs for all repositories in a team.
    :param username: 
    :param url_type: the type uf url to return - ssh or https
    :param token: GitHub token
    :param org: GitHub organization or username
    :param team: GitHub team name
    :return: List of SSH URLs
    """
    try:
        # Create a GitHub instance using the token
        g = Github(token)

        # Get the organization
        organization = g.get_organization(org)

        # Get the team by name
        team = organization.get_team_by_slug(team)

        # Get the list of repositories for the team
        repositories = team.get_repos()

        if url_type == "ssh":
            # Get SSH URLs for all repositories
            ssh_urls = [repo.ssh_url for repo in repositories]
            return ssh_urls
        elif url_type == "https":
            # Get SSH URLs for all repositories
            urls = [repo.clone_url.replace('https://', f'https://{username}:{token}@') for repo in repositories]
            return urls

    except Exception as e:
        raise Exception(f"Get urls: an error occurred: {str(e)}")


def get_ssh_urls_for_team_repositories(username, token, org, team):
    """
    Get SSH URLs for all repositories in a team.
    :param username:
    :param token: GitHub token
    :param org: GitHub organization or username
    :param team: GitHub team name
    :return: List of SSH URLs
    """
    return get_urls_for_team_repositories(username, token, org, team, "ssh")


def get_https_urls_for_team_repositories(username, token, org, team):
    """
    Get SSH URLs for all repositories in a team.
    :param username:
    :param token: GitHub token
    :param org: GitHub organization or username
    :param team: GitHub team name
    :return: List of SSH URLs
    """
    return get_urls_for_team_repositories(username, token, org, team, "https")

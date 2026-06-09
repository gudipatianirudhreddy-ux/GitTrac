import requests
from models.github import Github
from models.repository import Repository
from services.logger_service import log_search


class GitHubServiceError(Exception):
    pass


class UserNotFoundError(GitHubServiceError):
    pass


class GitHubRateLimitError(GitHubServiceError):
    pass


class GitHubServerError(GitHubServiceError):
    pass


def _raise_for_status(response, username):
    if response.status_code == 404:
        raise UserNotFoundError(f"GitHub user '{username}' not found.")
    if response.status_code == 403:
        raise GitHubRateLimitError(
            "GitHub API rate limit exceeded. Please try again later."
        )
    if 500 <= response.status_code < 600:
        raise GitHubServerError(
            "GitHub server error. Please try again later."
        )
    if response.status_code != 200:
        raise GitHubServiceError(
            f"GitHub API error: {response.status_code} - {response.reason}"
        )


def get_user(username):
    if not username or not username.strip():
        raise GitHubServiceError("GitHub username must be provided.")

    github_username = username.strip()
    github_user = Github(github_username)
    log_search(github_username)

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitTrac-App",
    }

    user_url = f"https://api.github.com/users/{github_username}"
    repos_url = f"https://api.github.com/users/{github_username}/repos"

    try:
        user_response = requests.get(user_url, headers=headers, timeout=10)
        repos_response = requests.get(repos_url, headers=headers, timeout=10)
    except requests.RequestException as exc:
        raise GitHubServiceError(
            "Unable to reach GitHub API. Please check your connection and try again."
        ) from exc

    _raise_for_status(user_response, github_username)
    _raise_for_status(repos_response, github_username)

    user_data = user_response.json()
    repos_data = repos_response.json()

    github_user.followers = int(user_data.get("followers", 0) or 0)
    github_user.following = int(user_data.get("following", 0) or 0)

    for repo_data in repos_data:
        repo_name = repo_data.get("name", "Unknown repository")
        stars = int(repo_data.get("stargazers_count") or 0)
        forks = int(repo_data.get("forks_count") or 0)
        language = repo_data.get("language") or "Not Specified"

        repo = Repository(
            name=repo_name,
            stars=stars,
            forks=forks,
            language=language,
        )
        github_user.add_repository(repo)

    github_user.repositories.sort(key=lambda repo: repo.stars, reverse=True)
    return github_user

def create_prompt(profile, repos):
    """Create a prompt for the AI roaster."""
    repo_names = []
    for repo in repos[:10]:
        repo_names.append(repo.name)
    
    repo_count = len(profile.repositories)
    
    return f"""
    Roast this GitHub profile in a funny and lighthearted way.

    Username: {profile.username}
    Followers: {profile.followers}
    Following: {profile.following}
    Total Repositories: {repo_count}
    Total Stars: {profile.total_stars()}

    Top Repositories:
    {', '.join(repo_names) if repo_names else 'None'}

    Make it funny and witty!
    """

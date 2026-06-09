class Github:
    def __init__(self, username):
        self.username = username
        self.followers = 0
        self.following = 0
        self.repositories = []

    def add_repository(self, repository):
        self.repositories.append(repository)

    def total_stars(self):
        return sum(int(repo.stars or 0) for repo in self.repositories)

    def language_stats(self):
        languages = {}
        for repo in self.repositories:
            language = repo.language or "Not Specified"
            languages[language] = languages.get(language, 0) + 1
        return languages

    def display_info(self):
        print(f"Username: {self.username}")
        print(f"Followers: {self.followers}")
        print(f"Following: {self.following}")
        print("Repositories:")
        for repo in self.repositories:
            repo.display()

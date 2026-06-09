
class Repository:
    def __init__(self, name, stars=0, forks=0, language=None):
        self.name = name
        self.stars = int(stars or 0)
        self.forks = int(forks or 0)
        self.language = language or "Not Specified"

    def display(self):
        print(f"Repository Name: {self.name}")
        print(f"Stars: {self.stars}")
        print(f"Forks: {self.forks}")
        print(f"Language: {self.language}")

    
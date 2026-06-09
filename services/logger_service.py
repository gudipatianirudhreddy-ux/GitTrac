from datetime import datetime

def log_search(username):
    with open("logs.txt", "a") as log_file:
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_file.write(
            f"{timestamp} - User searched for: {username}\n"
            )
        
from flask import Flask, render_template, request
from services.github_service import get_user, GitHubServiceError, create_prompt
from services.ai_service import generate_roast
from models.github import Github
import logging
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            return render_template(
                "index.html",
                error_message="Please enter a GitHub username.",
            )

        try:
            github_user = get_user(username)
            return render_template(
                "dashboard.html",
                github=github_user,
                total_stars=github_user.total_stars(),
                language_stats=github_user.language_stats(),
            )
        except GitHubServiceError as exc:
            return render_template(
                "index.html",
                error_message=str(exc),
            )

    return render_template("index.html")

@app.route("/roast/<username>")
def roast(username):
    try:
        logger.info(f"Roast route called for username: {username}")
        github_user = get_user(username)
        logger.info(f"GitHub user fetched: {github_user.username}")
        
        prompt = create_prompt(github_user, github_user.repositories)
        logger.info("Prompt created successfully")
        
        roast_content = generate_roast(prompt)
        logger.info("Roast generated successfully")
        
        return render_template(
            "roast.html",
            roast=roast_content,
            username=username
        )
    except GitHubServiceError as exc:
        logger.error(f"GitHub Service Error: {str(exc)}")
        return render_template(
            "index.html",
            error_message=str(exc),
        )
    except Exception as exc:
        error_msg = f"Unexpected error in roast route: {type(exc).__name__}: {str(exc)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return render_template(
            "index.html",
            error_message="An unexpected error occurred while generating your roast. Please try again.",
        )

if __name__ == "__main__":
    app.run(debug=True)

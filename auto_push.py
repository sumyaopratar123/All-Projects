import subprocess
from pathlib import Path

REPO_PATH = (
    Path.home()
    / "OneDrive"
    / "Desktop"
    / "All-Projects-Upload"
)

def run_git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=REPO_PATH,
        check=True,
        text=True
    )

def main():
    print("=" * 55)
    print("   GitHub Auto Commit & Push")
    print("=" * 55)

    if not (REPO_PATH / ".git").exists():
        print("ERROR: Git repository not found!")
        return

    try:
        # Stage actual project changes
        run_git("add", "-A")

        # Check staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_PATH
        )

        if result.returncode == 0:
            print("No new changes to commit.")
            return

        # Commit actual changes
        message = input(
            "Enter commit message (default: Update projects): "
        ).strip()

        if not message:
            message = "Update projects"

        run_git("commit", "-m", message)

        # Push to GitHub
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        if not branch:
            print("ERROR: Current branch not found!")
            return

        run_git("push", "-u", "origin", branch)

        print("\nSUCCESS: Changes committed and pushed!")

    except subprocess.CalledProcessError as error:
        print(f"\nGit operation failed: {error}")

if __name__ == "__main__":
    main()
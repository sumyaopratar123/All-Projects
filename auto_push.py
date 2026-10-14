import random
import shutil
import subprocess
from pathlib import Path

ROOT = (
    Path.home() / "OneDrive" / "Desktop" /
    "GitHubDownloader" / "github_repositories_download" /
    "repositories"
)

REPO = Path.home() / "OneDrive" / "Desktop" / "All-Projects-Upload"


def git(*args):
    subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True
    )


def main():
    print("=" * 55)
    print(" RANDOM PROJECT COMMIT & PUSH ")
    print("=" * 55)

    if not ROOT.is_dir() or not (REPO / ".git").is_dir():
        print("ERROR: Source folder or Git repository not found.")
        return

    try:
        count = int(input("How many random projects to add? "))
        if count < 1:
            print("Enter a positive number.")
            return

        projects = [
            p for p in ROOT.iterdir()
            if p.is_dir()
            and not (REPO / p.name).exists()
        ]

        if not projects:
            print("No new projects available.")
            return

        count = min(count, len(projects))
        selected = random.sample(projects, count)

        print("\nSelected projects:")
        for project in selected:
            print("-", project.name)

        confirm = input("\nType YES to copy and push: ")
        if confirm != "YES":
            print("Cancelled.")
            return

        for project in selected:
            print(f"\nCopying: {project.name}")
            shutil.copytree(project, REPO / project.name)

        git("add", "-A")

        status = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO
        )

        if status.returncode == 0:
            print("No changes to commit.")
            return

        message = input(
            "\nCommit message (Enter for default): "
        ).strip() or "Add project files"

        git("commit", "-m", message)

        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        git("push", "-u", "origin", branch)
        print("\nSUCCESS: Projects committed and pushed!")

    except ValueError:
        print("Please enter a valid number.")
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
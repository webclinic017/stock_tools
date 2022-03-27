import subprocess
import yaml

# completed
# read from secret
with open("../secret.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        local_git_repo = data['local_git_repo']

    except yaml.YAMLError as exc:
        print(exc)
        exit()

subprocess.call(["git", "pull"], cwd=local_git_repo)
subprocess.call(["git", "add",  "."], cwd=local_git_repo)
subprocess.call(["git", "commit", "-m",  "batch"], cwd=local_git_repo)
subprocess.call(["git", "push"], cwd=local_git_repo)
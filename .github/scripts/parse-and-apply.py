import os
import yaml
import subprocess
import sys

# Path to the branch protection YAML config
RULESET_FILE = ".github/branch-protection.yml"

try:
    with open(RULESET_FILE, "r") as f:
        data = yaml.safe_load(f)
except FileNotFoundError:
    print(f"❌ File not found: {RULESET_FILE}")
    sys.exit(1)

# Extract branch protection config for the first branch (usually 'main')
try:
    branch_config = data['branches'][0]['protection']
except (KeyError, IndexError):
    print(" Invalid YAML structure: expected 'branches[0].protection'")
    sys.exit(1)

# Build GH CLI API arguments
args = [
    "gh", "api", "-X", "PUT",
    f"repos/{os.environ['GITHUB_REPOSITORY']}/branches/main/protection",
    f"-F enforce_admins={str(branch_config.get('enforce_admins', True)).lower()}",
    f"-F required_pull_request_reviews.required_approving_review_count={branch_config.get('required_pull_request_reviews', {}).get('required_approving_review_count', 1)}",
    f"-F allow_force_pushes={str(branch_config.get('allow_force_pushes', False)).lower()}",
    f"-F allow_deletions={str(branch_config.get('allow_deletions', False)).lower()}",
    "-F required_status_checks.strict=true"
]

# Append required status check contexts
contexts = branch_config.get('required_status_checks', {}).get('contexts', [])
for context in contexts:
    args.append(f"-f required_status_checks.contexts[]={context}")

# Print what will be applied
print(" Applying branch protection rules from:", RULESET_FILE)
print(" Running:", " ".join(args))

# Execute the GH CLI API call
try:
    subprocess.run(args, check=True)
    print(" Branch protection applied successfully.")
except subprocess.CalledProcessError as e:
    print(" Failed to apply branch protection.")
    sys.exit(e.returncode)

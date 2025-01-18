# Universal Chaos

Ontology framework for managing universal chaos.

## Setup

### Prerequisites
- Miniconda or Anaconda
- 1Password CLI (`op`)
- GitHub account with PAT
- GitHub CLI (`gh` v2+) installed via Homebrew

### Environment Setup
1. Create conda environment:
   ```bash
   conda env create -f environment.yml
   ```

2. Configure GitHub token:

   Important: Make sure you're using the system GitHub CLI, not the conda one:
   ```bash
   # Verify you're using the correct gh
   /usr/local/bin/gh --version  # Should show v2.x or higher
   ```
   
   Option A (Recommended) - If you have GitHub CLI installed:
   ```bash
   # Login to GitHub CLI if you haven't already
   /usr/local/bin/gh auth login
   
   # Store token in 1Password and configure .env
   op item create --category="API Credential" --title="GitHub Universal Chaos Token" --vault="Private" --text-field="token=$(/usr/local/bin/gh auth token)"
   echo 'GITHUB_TOKEN="op://Private/GitHub Universal Chaos Token/token"' > ~/.env
   ```

   Option B - Manual token creation:
   - Create a GitHub Personal Access Token (PAT) with required permissions
   - Store the token in 1Password using this command:
     ```bash
     op item create --category="API Credential" --title="GitHub Universal Chaos Token" --vault="Private" --text-field="token=ghp_your_github_token_here"
     ```
   - Create/update your .env file to reference the token:
     ```bash
     echo 'GITHUB_TOKEN="op://Private/GitHub Universal Chaos Token/token"' > ~/.env
     ```

   Option C - If you already have "GitHub Universal Chaos Token" in 1Password:
   ```bash
   # Update existing token (if using GitHub CLI)
   op item edit "GitHub Universal Chaos Token" token="$(/usr/local/bin/gh auth token)"
   
   # Or just configure .env to use existing token
   echo 'GITHUB_TOKEN="op://Private/GitHub Universal Chaos Token/token"' > ~/.env
   ```

   Note: If you stored the token in a different vault or with different field names, adjust the op:// reference accordingly.

   Test that it works:
   ```bash
   op run --env-file="$HOME/.env" -- env | grep GITHUB_TOKEN
   ```

3. Launch Cursor with the correct environment:
   ```bash
   # Launch cursor with GitHub CLI and 1Password environment
   PATH="/usr/local/bin:$PATH" op run --env-file="$HOME/.env" -- cursor
   ```

### Usage
1. Activate environment:
   ```bash
   conda activate universal-chaos
   ```

2. Create GitHub issues:
   ```bash
   python create_github_issue.py
   ``` 
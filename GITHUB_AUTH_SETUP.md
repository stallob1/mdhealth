# GitHub Authentication Setup

To fix the 403 error when pushing to GitHub, you need to set up authentication. Here are two options:

## Option 1: SSH Authentication (Recommended)

Your SSH key has been generated. Follow these steps:

1. **Copy your SSH public key:**
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```
   Or manually copy:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAII/wJMB0o8vKec1AzDQ17OtIQZh4WbSfAs0HhtsjARO1 brentstallo@Brents-MacBook-Pro.local
   ```

2. **Add the key to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your key
   - Click "Add SSH key"

3. **Test the connection:**
   ```bash
   ssh -T git@github.com
   ```
   You should see: "Hi stallob1! You've successfully authenticated..."

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

## Option 2: HTTPS with Personal Access Token

If you prefer HTTPS:

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Give it a name (e.g., "mdhealth-repo")
   - Select scope: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Update remote URL:**
   ```bash
   git remote set-url origin https://github.com/stallob1/mdhealth.git
   ```

3. **Push (you'll be prompted for credentials):**
   ```bash
   git push origin main
   ```
   - Username: `stallob1`
   - Password: **paste your Personal Access Token** (not your GitHub password)

4. **Store credentials (optional):**
   The token will be saved in macOS Keychain for future use.

## Current Configuration

- Remote URL: `git@github.com:stallob1/mdhealth.git` (SSH)
- SSH key location: `~/.ssh/id_ed25519`
- Credential helper: macOS Keychain

## Quick Fix Script

Run the setup script:
```bash
./setup_git_auth.sh
```

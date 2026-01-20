# Fix 403 Error - Quick Guide

The 403 error occurs because GitHub requires authentication. Here's the easiest fix:

## Solution: Use Personal Access Token (PAT)

### Step 1: Create a Personal Access Token

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `mdhealth-repo`
4. Select expiration: Choose your preference (90 days, 1 year, or no expiration)
5. **Check the `repo` scope** (this gives full access to repositories)
6. Click **"Generate token"**
7. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!

### Step 2: Push with the Token

Run this command:
```bash
git push origin main
```

When prompted:
- **Username**: `stallob1`
- **Password**: **Paste your Personal Access Token** (NOT your GitHub password)

The token will be saved in macOS Keychain, so you won't need to enter it again.

---

## Alternative: Fix SSH (if you prefer)

If you want to use SSH instead, you need to:

1. **Add your SSH key to GitHub:**
   - Get your public key: `cat ~/.ssh/id_ed25519.pub`
   - Copy the output
   - Go to: **https://github.com/settings/keys**
   - Click "New SSH key"
   - Paste and save

2. **Switch to SSH:**
   ```bash
   git remote set-url origin git@github.com:stallob1/mdhealth.git
   git push origin main
   ```

---

**Current Configuration:**
- Remote URL: `https://github.com/stallob1/mdhealth.git`
- Credential helper: macOS Keychain
- Ready to push once you have a Personal Access Token

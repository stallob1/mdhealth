#!/bin/bash

# Script to set up GitHub authentication for git push
# This script helps fix the 403 error when pushing to GitHub

echo "Setting up GitHub authentication..."
echo ""

# Check if SSH keys exist
if [ ! -f ~/.ssh/id_ed25519 ] && [ ! -f ~/.ssh/id_rsa ]; then
    echo "No SSH keys found. Generating a new SSH key..."
    echo ""
    read -p "Enter your GitHub email address: " email
    ssh-keygen -t ed25519 -C "$email" -f ~/.ssh/id_ed25519 -N ""
    
    echo ""
    echo "SSH key generated! Now add it to GitHub:"
    echo ""
    echo "1. Copy your public key:"
    echo "   pbcopy < ~/.ssh/id_ed25519.pub"
    echo ""
    echo "2. Go to: https://github.com/settings/keys"
    echo "3. Click 'New SSH key'"
    echo "4. Paste your key and save"
    echo ""
    echo "Press Enter after you've added the key to GitHub..."
    read
    
    # Add SSH key to ssh-agent
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    
    # Add GitHub to known_hosts
    ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
    
    # Update remote URL to use SSH
    git remote set-url origin git@github.com:stallob1/mdhealth.git
    echo ""
    echo "✓ Remote URL updated to use SSH"
else
    echo "SSH key found!"
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        echo "Your public key:"
        cat ~/.ssh/id_ed25519.pub
        echo ""
        echo "Make sure this key is added to your GitHub account:"
        echo "https://github.com/settings/keys"
    fi
    
    # Add SSH key to ssh-agent
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519 2>/dev/null || ssh-add ~/.ssh/id_rsa 2>/dev/null
    
    # Update remote URL to use SSH
    git remote set-url origin git@github.com:stallob1/mdhealth.git
    echo ""
    echo "✓ Remote URL updated to use SSH"
fi

echo ""
echo "Testing connection..."
ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" && echo "✓ SSH authentication successful!" || echo "⚠ SSH authentication failed. Make sure your key is added to GitHub."

echo ""
echo "You can now try: git push origin main"

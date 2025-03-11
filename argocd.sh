#!/bin/bash

# Login to ArgoCd
argocd login argocd.home.adaminformatika.hu --skip-test-tls --grpc-web --insecure --username admin --password

# Define the ArgoCD repository path
ARGOCD_REPO_PATH="$HOME/Github/argocd"  # Change this to the actual path

# Navigate to the ArgoCD repository
if [[ ! -d "$ARGOCD_REPO_PATH" ]]; then
    echo "Error: ArgoCD repository directory does not exist at $ARGOCD_REPO_PATH."
    exit 1
fi

cd "$ARGOCD_REPO_PATH" || { echo "Failed to enter ArgoCD repository directory."; exit 1; }

# Check if it's a valid Git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Error: Not a valid Git repository. Please check the directory."
    exit 1
fi

echo "Successfully navigated to ArgoCD repository."

# Prompt for ArgoCD app name
read -p "Enter ARGOCD_APP_NAME: " ARGOCD_APP_NAME

# Prompt for Media Server name
read -p "Enter NS_FOLDER_NAME: " NS_FOLDER_NAME

# Ask if the user has already pushed changes to Git
read -p "Have you already done 'git push'? (yes/no): " GIT_PUSHED


if [[ "$GIT_PUSHED" != "yes" ]]; then
    echo "You need to commit and push your changes before proceeding."

    # Ask for a commit message
    read -p "Enter a commit message: " COMMIT_MSG

    # Add, commit, and push the changes
    git add .
    git commit -m "$COMMIT_MSG"
    git push

    echo "Changes pushed to Git."
fi

# Create ArgoCD app with provided inputs
argocd app create "$ARGOCD_APP_NAME" -f "app/$NS_FOLDER_NAME/$ARGOCD_APP_NAME/argocd-$ARGOCD_APP_NAME.yaml" --upsert


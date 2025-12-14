# ArgoCD Scripts

## GHCR Sealed Secret Setup

### Prerequisites

1. Install direnv: `sudo apt install direnv` (or `brew install direnv` on macOS)
2. Add to your shell config (~/.zshrc or ~/.bashrc):
   ```bash
   eval "$(direnv hook zsh)"  # or 'bash' for bash
   ```
3. Reload shell or run: `source ~/.zshrc`

### Setup

1. **Create `.envrc` in the argocd directory:**
   ```bash
   cd /home/ferko/Documents/argocd
   cat > .envrc << 'EOF'
   # GitHub Container Registry credentials
   export GITHUB_USERNAME="radamhu"
   export GITHUB_TOKEN="your-github-token-here"
   EOF
   ```

2. **Create a GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens/new
   - Name: "GHCR Access - Dentari"
   - Scopes: `read:packages`, `write:packages`
   - Expiration: 90 days (recommended)
   - Copy the token

3. **Edit `.envrc` and add your token:**
   ```bash
   vim .envrc
   # Replace "your-github-token-here" with your actual token
   ```

4. **Allow direnv to load the environment:**
   ```bash
   direnv allow
   ```

### Usage

Run the script to create a sealed secret:
```bash
cd /home/ferko/Documents/argocd
./scripts/create-ghcr-sealed-secret.sh
```

The script will:
- Use credentials from `.envrc` if available
- Or prompt for them interactively
- Create a sealed secret at `app/demo/dentari/ghcr-sealed-secret.yaml`
- This file can be safely committed to Git

### Security Notes

- `.envrc` is already in `.gitignore` and will never be committed
- The sealed secret can only be decrypted by your cluster's sealed-secrets controller
- Tokens should be rotated every 90 days
- Never commit plain secrets or tokens to Git

### Updating the Secret

When your token expires:
1. Create a new token on GitHub
2. Update `.envrc` with the new token
3. Run `direnv allow` to reload
4. Run the script again to generate a new sealed secret
5. Commit and push the new sealed secret

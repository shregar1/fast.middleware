# Branch Protection Setup

This document describes how to configure branch protection rules for the `main` branch to prevent direct pushes.

## Required Settings

Go to: **Repository Settings → Branches → Add branch protection rule**

### Branch name pattern

```text
main

```

### Protection Rules (Enable these)

- [x] **Require a pull request before merging**
  - [x] Require approvals: `1` (or more)
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [x] Require review from Code Owners

- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - Required status checks:
    - `lint`
    - `security`
    - `type-check`
    - `test (3.10)`
    - `test (3.11)`
    - `test (3.12)`
    - `test (3.13)`
    - `build`

- [x] **Require conversation resolution before merging**

- [x] **Require signed commits** (optional but recommended)

- [x] **Require linear history** (optional - enforces squash/rebase)

- [x] **Do not allow bypassing the above settings**

- [x] **Restrict who can push to matching branches**
  - Only allow: (leave empty to block all direct pushes)

- [x] **Block force pushes**

- [x] **Block deletions**

## Quick Setup via GitHub CLI

If you have the GitHub CLI installed, run:

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -f required_status_checks='{"strict":true,"contexts":["lint","security","type-check","test (3.10)","test (3.11)","test (3.12)","test (3.13)","build"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f block_creations=false \
  -f required_linear_history=false \
  -f required_conversation_resolution=true

```

Replace `{owner}` with `shregar1` and `{repo}` with `fast-middleware`.

## Using GitHub Rulesets (Recommended for newer repos)

Go to: **Repository Settings → Rules → Rulesets → New ruleset**

1. **Name**: `Protect main branch`
2. **Enforcement status**: `Active`
3. **Target branches**: Add `main`
4. **Rules**:
   - ✅ Restrict deletions
   - ✅ Require linear history
   - ✅ Require a pull request before merging
     - Required approvals: 1
     - Dismiss stale reviews
     - Require review from CODEOWNERS
   - ✅ Require status checks to pass
     - Add all CI checks
   - ✅ Block force pushes

## Verify Protection

After setting up, verify by trying:

```bash

# This should fail
git push origin main

# Error: remote: error: GH006: Protected branch update failed

```

## Notes

- Branch protection rules require a GitHub Pro, Team, or Enterprise account for private repositories
- For public repositories, branch protection is available on all plans
- Code Owners file (`.github/CODEOWNERS`) is already configured in this repository

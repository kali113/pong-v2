# Branch Protection Setup Guide

## Enable Branch Protection Rules

Protect your `main` branch from accidental force pushes and deletions.

### Steps:

1. Go to: https://github.com/kali113/pong-v2/settings/branches

2. Click "Add branch protection rule"

3. **Branch name pattern**: `main`

4. **Recommended settings**:

   #### Protect matching branches
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: 0 (you can approve your own)
     - ✅ Dismiss stale pull request approvals
   
   - ✅ **Require status checks to pass**
     - ✅ Require branches to be up to date
     - Add status checks: `test` (from GitHub Actions)
   
   - ✅ **Require conversation resolution before merging**
   
   - ✅ **Require linear history** (optional - cleaner git history)
   
   - ⚠️ **Do not force push** (IMPORTANT)
   
   - ⚠️ **Do not allow deletions** (IMPORTANT)

5. Click "Create" at bottom

## Ruleset Configuration (Alternative Modern Approach)

GitHub's newer "Rulesets" feature (recommended):

1. Go to: https://github.com/kali113/pong-v2/settings/rules

2. Click "New ruleset" → "New branch ruleset"

3. **Ruleset name**: "Protect main branch"

4. **Targets**: 
   - Target branches: `main`

5. **Rules**:
   - ✅ **Restrict deletions**
   - ✅ **Restrict force pushes**
   - ✅ **Require pull request before merging**
     - Required approvals: 0
     - Dismiss stale reviews: Yes
   - ✅ **Require status checks to pass**
     - Add: `test`, `build-executable`, `build-docs`
   - ✅ **Require conversation resolution**
   - ✅ **Require linear history** (optional)

6. **Bypass list**:
   - Allow yourself to bypass (for emergencies)
   - Repository admin: Can bypass

7. Click "Create"

## Why These Rules?

| Rule | Purpose |
|------|---------|
| **Restrict deletions** | Prevents accidentally deleting main branch |
| **Restrict force pushes** | Preserves commit history, prevents rewrite |
| **Require PR** | Code review process, even for solo dev |
| **Status checks** | Ensures tests pass before merge |
| **Linear history** | Clean git log, easier to understand |
| **Conversation resolution** | Ensures all comments addressed |

## Emergency Bypass

If you need to bypass protections (use carefully):
1. Go to Settings → Rules
2. Edit ruleset
3. Add yourself to bypass list
4. Make changes
5. Remove bypass access

## Testing Protection

After setup, try:
```bash
# This should be blocked:
git push --force

# This should work:
git push
```

## Recommended Workflow

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit
3. Push: `git push origin feature/new-feature`
4. Open PR on GitHub
5. Wait for CI checks
6. Merge PR (squash or merge)
7. Delete feature branch

---

**Protections active! Your main branch is now safe.** 🛡️

# GitHub Actions Troubleshooting Guide

## Issue: Scheduled Workflow Not Running

If your GitHub Actions workflow with a `schedule` trigger (cron) is not running automatically, check the following:

### 1. **Workflow Must Be on the Default Branch**
**This is the most common issue!**

GitHub Actions scheduled workflows (`on: schedule:`) **ONLY run from the default branch** (usually `main` or `master`).

- ✅ The workflow file must be merged to the default branch
- ❌ Scheduled triggers will NOT work from feature branches or pull requests
- ✅ Manual triggers (`workflow_dispatch`) work from any branch
- ✅ Push and pull_request triggers work from any branch

**Solution:** Merge your workflow file to the default branch.

### 2. Check Repository Settings

Verify that GitHub Actions is enabled:
1. Go to Repository Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is selected
3. Check that workflow permissions include "Read and write permissions" if the workflow needs to commit changes

### 3. Verify Cron Schedule Syntax

The cron syntax in `.github/workflows/phase1_data_pipeline.yml` is:
```yaml
on:
  schedule:
    - cron: "*/15 * * * *"  # Runs every 15 minutes
```

Cron format: `minute hour day month day-of-week`
- `*/15 * * * *` = Every 15 minutes
- `0 * * * *` = Every hour at minute 0
- `0 0 * * *` = Every day at midnight UTC

⚠️ **Important:** GitHub Actions uses UTC time for scheduled workflows.

### 4. Organization Permissions (for Private Repositories)

If this is a private repository under an organization:
1. Go to Organization Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is enabled
3. Check billing and Actions minutes quota

### 5. Workflow Status

Check if the workflow is disabled:
1. Go to Actions tab in the repository
2. Find your workflow in the left sidebar
3. If there's a "Enable workflow" button, click it

### 6. Recent Activity

GitHub may disable scheduled workflows if:
- The repository has been inactive for 60 days
- There have been no commits to the default branch in 60 days

**Solution:** Make any commit to the default branch to reactivate scheduled workflows.

### 7. Check Workflow Runs

View workflow run history:
1. Go to Actions tab
2. Filter by "Event: schedule" to see scheduled runs
3. Check for any error messages

## Current Workflow Configuration

The Phase 1 Data Pipeline workflow:
- **Schedule:** Every 15 minutes (`*/15 * * * *`)
- **Manual trigger:** Available via `workflow_dispatch`
- **Permissions:** Requires write access to commit data back to repository
- **Branch requirement:** Must be on default branch for schedule to work

## Testing the Workflow

To test if the workflow works correctly:
1. Go to Actions tab
2. Select "Phase 1 Data Pipeline" workflow
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

If manual runs work but scheduled runs don't, the issue is likely that the workflow is not on the default branch.

## Quick Checklist

- [ ] Workflow file is on the default branch (`main`)
- [ ] GitHub Actions is enabled in repository settings
- [ ] Workflow is not disabled
- [ ] Repository is active (commit within last 60 days)
- [ ] Organization allows scheduled workflows (if applicable)
- [ ] Actions minutes quota is not exceeded (for private repos)
- [ ] Cron syntax is correct
- [ ] Manual workflow dispatch works successfully

## Additional Resources

- [GitHub Actions: Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [GitHub Actions: Disabling and enabling workflows](https://docs.github.com/en/actions/managing-workflow-runs/disabling-and-enabling-a-workflow)
- [Cron schedule syntax](https://crontab.guru/)

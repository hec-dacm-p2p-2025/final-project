# GitHub Actions Workflows

## Phase 1 Data Pipeline

**File:** `phase1_data_pipeline.yml`

### Purpose
Automatically fetches and processes Binance P2P market data and Brazilian Central Bank (BCB) exchange rates.

### Schedule
- Runs every 15 minutes: `*/15 * * * *` (UTC)
- Can also be triggered manually via "Run workflow" button

### What It Does
1. Fetches real-time Binance P2P data for multiple fiat currencies (USD, EUR, GBP, JPY, CNY, MXN, ARS, BOB)
2. Retrieves BCB exchange rate data
3. Processes and saves data to `phase1_data_pipeline/data/`
4. Commits results back to the repository with a summary

### Requirements
- **Must be on the default branch (`main`) for scheduled runs to work**
- Requires write permissions to commit data back to repository
- Internet connectivity for API calls

### Testing
To test the workflow manually:
1. Go to the Actions tab
2. Select "Phase 1 Data Pipeline"
3. Click "Run workflow"
4. Select branch and confirm

### Troubleshooting
If scheduled runs are not working, see: [ACTIONS_TROUBLESHOOTING.md](../ACTIONS_TROUBLESHOOTING.md)

### Output Locations
- **Raw data:** `phase1_data_pipeline/data/raw/`
  - Binance: `phase1_data_pipeline/data/raw/binance/`
  - BCB: `phase1_data_pipeline/data/raw/bcb/`
- **Processed data:** `phase1_data_pipeline/data/processed/`
  - Binance historical: `phase1_data_pipeline/data/processed/binance/historical_fiat/`
  - Binance snapshots: `phase1_data_pipeline/data/processed/binance/daily_snapshots/`
  - BCB data: `phase1_data_pipeline/data/processed/bcb/`
- **Logs:** `phase1_data_pipeline/logs/`

### Important Notes
⚠️ **Scheduled workflows only run from the default branch** - This is a GitHub limitation. The workflow file must be merged to `main` for automatic scheduled execution.

✅ Manual workflow dispatch works from any branch and can be used for testing.

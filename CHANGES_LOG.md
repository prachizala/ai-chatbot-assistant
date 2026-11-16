# Changes Log - Work Package 4: Small Feature Upgrades

## Summary of Changes

### 1. Visual Token Budget Progress Bar (`app.py`)
- Enhanced the sidebar conversational memory metrics section by adding an interactive `st.progress` bar calculating real-time context window utilization:
  `token_ratio = min(1.0, max(0.0, float(cm.total_tokens() / cm.max_history_tokens)))`
- Added context caption displaying percentage utilization of the token budget.

### 2. Documentation Updates (`README.md`)
- Documented visual memory token utilization progress bar in the Features list.

### 3. Automated Test Verification
- Executed unit test suite (`python -m unittest discover -s tests`).
- All 7 tests pass 100% (`Ran 7 tests in 0.000s ... OK`).

## Items Skipped & Rationale
- None.

## Manual Steps Needed
- None. Run `streamlit run app.py` to view the memory progress bar in the left sidebar.

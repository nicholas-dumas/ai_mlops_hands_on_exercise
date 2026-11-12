# Task 1 report: Exploratory data analysis (Bank Marketing)

| Field | Value |
| --- | --- |
| Student | [Nicholas Dumas] |
| Dataset | [UCI Bank Marketing (bank-full.csv)] |
| Task | 1 |
| Tag / commit | [task[N] / short hash] |
| How to run | [commands; for secrets, name the environment variable, never the value] |
| Timebox | about 4 hours ; finished |

## 1. Summary

I analysed the data of a Portuguese bank that called 45,211 clients by phone to sell a term deposit. The goal was to understand which clients say "yes" (`y`). There are no empty cells, but some problems are hidden: "unknown" is used as a missing value (81.7% in `poutcome`), `pdays` uses -1 as a code, one value of `previous` (275) is probably an error, and `duration` causes data leakage. The strongest signal is the result of the previous campaign: 64.7% of clients with a previous success said yes, while the average is 11.7%. The main limits are: the classes are unbalanced and the data has no year.

## 2. Goal and success criteria

**Goal.** Load the data in a reproducible way, check its quality, fix the problems, and find which client characteristics are related to a "yes". Each finding must have a chart or a table.
 
| Criterion | How it is measured | Target | Result |
| --- | --- | --- | --- |
| Reproducible loading | The notebook runs from top to bottom by pressing Run All | No errors | Done |
| Data quality checked | Types, empty cells, "unknown", special codes, outliers, leakage | All checked and written | Done (3.1, 3.1.2, 3.3.1) |
| Problems fixed, with reasons | Each fix is written as a decision | Every fix explained | Done (3.2) |
| Findings supported by charts | Each finding has a chart | All findings | Done (3.3.1, 3.3.2) |
 
**Evidence:** `notebooks/eda.ipynb`, sections 3.1 - 3.3.3.

## 3. Approach and key decisions

Steps: load the raw CSV -> integrity table and data dictionary -> data quality checks -> cleaning on a copy -> distributions of each feature -> relations between each feature and the target, with ANOVA and chi-square tests -> correlation matrix.
 
| # | Finding | Decision | Alternative considered | Where in the code |
| --- | --- | --- | --- | --- |
| D1 | "unknown" in `poutcome` (81.7%), `contact` (28.8%), `education` (4.1%), `job` (0.6%) | Keep "unknown" as a category | Delete the rows: we lose too much data | `eda.ipynb` 3.1, 3.2 |
| D2 | `pdays` = -1 for 36,954 clients (81.7%): it means "never contacted before" | New column `contacted_before` (True/False) | It is wrong to use -1 as the number of days | 3.1.2, 3.2 |
| D3 | `previous` = 275, the next highest value is 58 | Delete this one row | Keep it: it changes the statistics | 3.1.2, 3.2 |
| D4 | `duration`: median 426 s for yes, 164 s for no, but we know it only after the call | Delete `duration` (data leakage) | Keep it: Task 3 results would not be realistic | 3.1.2, 3.2 |
| D5 | `y` is a text column (yes/no) | Convert it to True/False, so its mean is the yes rate | Keep text and count by hand | 3.2 |
| D6 | Outliers in `balance` (10.5%), `campaign` (6.8%), `age` (1.1%) are real values (e.g. rich clients, negative balances) | Keep them; use medians and a boxplot without outliers to compare groups | Delete them: we lose about 10% of clients | 3.3.1, 3.3.2.2 |
 
**Evidence:** `notebooks/eda.ipynb` 3.1.2 , 3.2, 3.3.1.

## 4. Results

| Result | Value | Baseline or reference |
| --- | --- | --- |
| Yes rate of clients with a previous success | 64.7% | Average 11.7%; never contacted ("unknown") 9.2% |
| Yes rate of students / retired clients | 28.7% / 22.8% | Blue-collar 7.3%  |
| Yes rate by age band | 24.0% for 18-25, 42.3% over 60, about 9-10% between 31 and 60 | Median age is similar: 38 (yes) vs 39 (no) |
| Yes rate by number of calls | 14.6% after 1 call, 5.8% after 6 or more | Not a cause: when a client says yes, the bank stops calling |
| Yes rate by number of calls | May 6.7%; Mar 52.0%, Sep 46.5%, Oct 43.8%, Dec 46.7% | Average 11.7% |
| Yes rate by month | Median 733 EUR (yes) vs 417 EUR (no) | The boxes overlap a lot: a weak signal alone |
| ANOVA and chi-square | All p-values below 0.05 | All tested features are related to the target |
| Linear correlations with y | All between -0.08 and 0.12 | The relations are not linear |
 
Main charts:
- *Previous campaign result and yes rate* (3.3.2.3): clients with a previous success say yes in 64.7% of cases, more than 5 times the average.
- *Age band and yes rate* (3.3.2.1): U shape, 24.0% for 18-25 and 42.3% over 60, about 9-10% in the middle.
- *Number of calls in this campaign and yes rate* (3.3.2.3): the yes rate goes down from 14.6% (1 call) to 5.8% (6 or more calls).
- *Month of the call and yes rate* (3.3.2.3): May has the most calls (13,766) and the lowest rate (6.7%).
 
**Evidence:** `notebooks/eda.ipynb` 3.3.1 – 3.3.3.

## 5. Problems and how you handled them

| Problem | Cause | What you did | Status |
| --- | --- | --- | --- |
| Push refused: "can not upload new objects to public fork" | `git add .` added two dataset files stored with Git LFS | Undid the commit, removed the datasets from it, marked them with `skip-worktree`; now I add files by name | Solved |
| `ModuleNotFoundError: scipy`, and `%pip` did not work | The uv environment has no pip | `uv add scipy` in the terminal; import moved to the first cell | Solved |
 
**Evidence:** commit history.

## 6. Limitations and trade-offs

| Area | Limitation or trade-off | Impact | Mitigation or next step |
| --- | --- | --- | --- |
| data | There is no year: each month mixes 2008, 2009 and 2010 | A month effect can come from one campaign, not from the season | Use `month` with care in Task 3 |
| data | Unbalanced classes (11.7% yes) | Accuracy gives a wrong idea of quality | Use metrics based on precision and recall |
| analysis | With 45210 rows, almost every test is significant | A small p-value does not mean a big difference | Look at the size of the difference and at the charts |
| analysis | Comparing two variables cannot prove a cause (e.g. calls and yes) | Risk of wrong conclusions | Written clearly in the comments |
 
**Evidence:** `notebooks/eda.ipynb` 3.1.1, 3.3.2.

## 7. Next steps

| Priority | Next step | Why | Effort |
| --- | --- | --- | --- |
| 1 | Split train and test before any preprocessing in Task 3 | To avoid leakage from scaling and encoding | S |
| 2 | Build a simple baseline (always "no") and compare the models with it | 88.3% accuracy is the minimum reference | S |
| 3 | Study how features work together | Some signals can overlap | M |

## 8. Use of AI assistants

| Tool | What you used it for | Where (files or sections) | How you checked the output |
| --- | --- | --- | --- |
| Claude (chat) | Steps to fork, clone and set up the project; fix for the refused push (dataset files committed by mistake) | Repository setup, Git history | The push worked and the datasets are not in the commits |
| Claude (chat) | Data dictionary table from `bank-names.txt` | `eda.ipynb` 3.1.1 | I checked the numbers against my notebook outputs |
| Claude (chat) | Plotting code for the distributions of the target, numeric and categorical features | `eda.ipynb` 3.3.1 | I ran the cells, checked the outputs and wrote the comments myself |
| Claude (chat) | Boxplot and IQR outlier code; explanation of outliers and the IQR rule | `eda.ipynb` 3.3.1 | I checked the outlier counts; I wrote the outlier comments myself |
| Claude (chat) | Check of my reading of the age boxplot; code for the age-band chart | `eda.ipynb` 3.3.2.1 | I rewrote the comment myself; the chart numbers match the printed table |
| Claude (chat) | Explanation of the ANOVA test and the p-value; fix of a `NameError` (missing import); which charts support the ANOVA results (balance boxplot without outliers) | `eda.ipynb` 2.1, 3.3.2.2 | The cell runs; I wrote the ANOVA comment myself; the boxplot medians match the printed table |
| Claude (chat) | Code to group the number of calls into bands (`pd.cut`) and plot the yes rate | `eda.ipynb` 3.3.2.3 | I checked that the bands cover all 45,210 clients and the numbers |
| Claude Code (VS Code) | Numbers of the section titles (markdown only) | `eda.ipynb` titles | I checked the Outline and that code and outputs did not change |
 
The assistant helped me to read the age boxplot correctly: my first reading ("clients who said yes are very young and very old") was too strong, because 53.5% of them are between 31 and 50. What changes is the share of young and old clients. The full list is in `AI_LOG.md`.

## Checklist

- [ ] Task tag pushed and named in the table at the top
- [ ] Runs from a fresh clone with the commands above
- [ ] No secrets, API keys or large data files committed
- [ ] Every section has an Evidence line
- [ ] Every figure has a caption with a number
- [ ] Guidance blocks and placeholders removed
- [ ] `AI_LOG.md` up to date

---
name: treasury-search-tips
description: How to efficiently search Treasury Bulletin corpus and read tables
---

## File Structure
- 697 files: treasury_bulletin_YYYY_MM.txt
- Index: cat /app/corpus/index.txt
- Each file = one monthly bulletin issue

## Search Strategy
1. Start with year: ls /app/corpus/ | grep "YYYY"
2. Add keyword: grep -rl "keyword" /app/corpus/treasury_bulletin_YYYY_*.txt
3. Find table: grep -n "Table NAME" /app/corpus/filename.txt
4. Read table: file_editor view with line range around the table

## Key Table Names
- AY-1: Average Yields of Long-Term Treasury Bonds
- FFO-1: Summary of Fiscal Operations
- FFO-5: Budget Outlays by Function
- MQ-3: Treasury Bonds (marketable)
- OFS: Ownership of Federal Securities

## Reading Tables
- Tables use pipe | delimiter
- First row = headers
- Check footnotes (1/, 2/) for unit adjustments
- "nan" means empty cell — skip it
- Units are usually stated in table title (millions, billions)

## For Monthly Data
- Each monthly bulletin has data for that month
- Annual totals are sometimes in December bulletins
- If question says "reported values for each month", collect from 12 separate bulletins

## Common Pitfalls
- Data for fiscal year 1955 may appear in 1955 or 1956 bulletins
- Calendar year vs fiscal year — read the question carefully
- Column order can shift between years — always check headers

---
name: treasury-navigation
description: How to navigate and search the Treasury Bulletin corpus
---
## Corpus Structure
- Location: /corpus/
- Format: JSON files, pre-parsed from original PDF bulletins
- Coverage: 1939–2025, 697 documents

## Search Strategy
1. Start with the most specific keyword from the question
2. If too many results, add a second keyword (year, table name)
3. If no results, try abbreviations or alternate spellings
   - "public debt" vs "debt outstanding"
   - "fiscal year" vs "FY"
   - Numbers: try both "1,234" and "1234"

## Reading Tables
- Tables are structured as rows and columns in JSON
- Always check column headers carefully — columns shift between years
- Units matter: check if values are in thousands, millions, or billions
- Some tables have footnotes that change the meaning of values

## Common Table Names in Treasury Bulletins
- "Ownership of Federal Securities"
- "Public Debt Outstanding"
- "Treasury Bill Rates"
- "Budget Receipts and Outlays"
- "Federal Debt by Type"
- "Interest on the Public Debt"

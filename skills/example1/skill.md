---
name: answer-format-examples
description: Critical rules for answer format and units
---

## RULE 1: NEVER INVENT FORMULAS
Only apply math the question explicitly names.
If question says "find the yield" — just report the number.
Do NOT apply Fisher, geometric mean, or any index unless named.

## RULE 2: UNITS - DO NOT CONVERT UNLESS ASKED
- If question asks "in millions" and table shows millions → write as-is
- If question asks "in millions" and table shows thousands → divide by 1000
- If question asks "in thousands" and table shows thousands → write as-is
- NEVER silently convert units without checking what the question asks

## RULE 3: ANSWER FORMAT EXAMPLES
Single number with commas: 2,602
Single number with commas: 44,463
Percent: 1608.80%
Plain decimal: 4962.46
Number with unit word: 36080 million
Bracket list: [10102000000, 4.73]
Bracket list: [0.096, -184.143]

## RULE 4: FIND THE RIGHT TABLE
For "highest spending department" questions:
- Look for tables showing ALL departments, not just one category
- The answer is the single largest value across ALL departments
- Check multiple tables — defense, civilian, total expenditures

## RULE 5: abs() for absolute difference
When question asks "absolute difference":
- Use: compute_stats([val1, val2], "percent_change") for percent
- For raw difference: calculate("val1 - val2") then take positive value
- abs() is supported in calculate tool

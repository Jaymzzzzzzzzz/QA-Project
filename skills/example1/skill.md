---
name: answer-format-examples
description: Critical examples of correct vs incorrect answer formats for Treasury questions
---

## MOST IMPORTANT RULE
Read the question. Find the number. Write it. Do NOT transform it.

## EXAMPLES OF CORRECT BEHAVIOR

### Example 1: Simple lookup
Question: "What was the yield for August 1982?"
Table shows: August 1982 = 12.15
CORRECT answer: echo "12.15" > /app/answer.txt
WRONG answer: echo "12.859" > /app/answer.txt  (geometric mean — not asked!)
WRONG answer: echo "-5.516" > /app/answer.txt  (Fisher index — not asked!)

### Example 2: Two values requested
Question: "Find the yield for August 1982 and August 1981"
Table shows: Aug 1982 = 12.15, Aug 1981 = 13.61
CORRECT answer: echo "12.15, 13.61" > /app/answer.txt
WRONG answer: calculate geometric mean of the two values

### Example 3: Percent change explicitly asked
Question: "What was the percent change from 1980 to 1981?"
Table shows: 1980 = 100, 1981 = 120
CORRECT: calculate (120-100)/100*100 = 20.0
CORRECT answer: echo "20.0%" > /app/answer.txt

### Example 4: Sum explicitly asked
Question: "What is the total for all months in 1953?"
Collect all 12 monthly values, add them up.
CORRECT answer: echo "45231.5" > /app/answer.txt

### Example 5: Geometric mean explicitly asked
Question: "What is the geometric mean of expenditures from March 1942 to October 1948?"
Only then: use compute_stats(values, "geometric_mean")

### Example 6: Linear regression explicitly asked
Question: "Fit an OLS linear regression with year as predictor"
Only then: use linear_regression_years(years, values)

### Example 7: Box-Cox explicitly asked
Question: "Apply Box-Cox transformation with lambda=0.75"
Only then: use boxcox_transform(value, 0.75)

## THE GOLDEN RULE
The formula to use is ALWAYS stated in the question.
If the question does not name a formula, do NOT use one.
Just look up the number and write it.

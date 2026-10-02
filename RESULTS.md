# Evaluation Results

Date: 2026-10-02
Model: openai/gpt-oss-120b (Groq)
Dataset: Olist Brazilian E-Commerce

## Score
- Auto-graded: 6/6 correct (compared against hand-written SQL)
- Trap questions (read manually): 2/2 correct
  - Q7 (orders in 2020): agent found no 2020 data and reported the real range, 2016-2018
  - Q8 (returned orders): agent said the dataset has no returns information

## Before vs after business rules
Before (manual testing, 6 questions): 4 clean, 1 partial, 1 failure
- Invented "USD" as the currency (the data is Brazilian reais)
- Reported canceled orders as "returned"
After: both fixed by adding business rules to the system prompt

## Limitations
- Eval set is small and mostly easy (single-table or simple-join questions)
- Answers are compared on the last SQL query run, so questions that need several queries need manual review
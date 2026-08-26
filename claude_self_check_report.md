# Calibration Report

Compared against 16 labeled examples.

| dimension | n | exact match | within ±1 | MAE | Pearson r |
|---|---|---|---|---|---|
| relevance | 16 | 0.31 | 1.0 | 0.69 | 0.23 |
| correctness | 16 | 0.5 | 0.94 | 0.56 | 0.62 |
| completeness | 16 | 0.38 | 1.0 | 0.62 | 0.18 |
| tone | 16 | 0.31 | 0.94 | 0.75 | 0.29 |

## Disagreements of 2+ points (model vs. label)

- **t15 / correctness**: model=5, label=3
  - model reasoning: Reply accurately states the policy on single charges per date and explains the bank-hold explanation for billing, with no invented details or contradictions to the provided context.
- **t15 / tone**: model=5, label=3
  - model reasoning: Reply is professional, empathetic, and free of robotic or overly scripted phrasing, with no mismatched tone to the customer's sentiment.
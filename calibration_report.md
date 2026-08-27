# Calibration Report

Compared against 16 labeled examples.

| dimension | n | exact match | within ±1 | MAE | Pearson r |
|---|---|---|---|---|---|
| relevance | 16 | 0.62 | 1.0 | 0.38 | 0.24 |
| correctness | 16 | 0.19 | 0.69 | 1.12 | 0.0 |
| completeness | 16 | 0.38 | 0.75 | 0.88 | 0.06 |
| tone | 16 | 0.06 | 0.25 | 1.94 | -0.52 |

## Disagreements of 2+ points (model vs. label)

- **t02 / correctness**: model=3, label=5
  - model reasoning: Reply is accurate on the facts it states about the policy and next steps, but omits a constraint from the context that changes the answer; specifically, it doesn't acknowledge the repeat issue as required by policy.
- **t05 / correctness**: model=5, label=3
  - model reasoning: The reply accurately states the known incident ID (INC-2291), ETA (August 15th), and available workaround (export as JSON).
- **t10 / correctness**: model=5, label=3
  - model reasoning: Reply states accurate facts about account status and next steps, with no invented details or contradictions to the provided context.
- **t12 / correctness**: model=5, label=3
  - model reasoning: The reply accurately states that the invoices can be accessed by following the provided steps and downloading the PDFs, with no contradictions or invented details.
- **t13 / correctness**: model=5, label=3
  - model reasoning: The reply accurately states the policy and provides clear instructions on how to recover the project within the 30-day timeframe.
- **t05 / completeness**: model=4, label=2
  - model reasoning: The reply addresses the customer's issue with exporting data as CSV but doesn't acknowledge the frustration of the 2-day delay.
- **t07 / completeness**: model=5, label=3
  - model reasoning: The reply addresses all parts of the message, including the customer's frustration and their decision to cancel, with roughly proportionate attention.
- **t10 / completeness**: model=4, label=2
  - model reasoning: Reply addresses most parts of the message but drops a minor one (the customer's uncertainty about who to ask); it covers the main concern but doesn't fully acknowledge the customer's frustration.
- **t13 / completeness**: model=4, label=2
  - model reasoning: The reply addresses the customer's request for immediate recovery but doesn't explicitly acknowledge the frustration or urgency expressed in the original message.
- **t01 / tone**: model=3, label=5
  - model reasoning: Tone is professional and somewhat empathetic, but reads as templated/impersonal; it lacks a clear acknowledgment of the customer's frustration.
- **t02 / tone**: model=3, label=5
  - model reasoning: Tone is professional and acceptable, but reads as templated/impersonal; it lacks genuine empathy for the customer's frustration.
- **t04 / tone**: model=5, label=3
  - model reasoning: The tone is professional and empathetic, acknowledging the customer's frustration and providing a clear next step.
- **t05 / tone**: model=5, label=2
  - model reasoning: The tone is professional and empathetic, using phrases like 'Thank you for reaching out' and 'Please let us know if there's anything else we can assist you with in the meantime.
- **t06 / tone**: model=5, label=3
  - model reasoning: The tone is professional and empathetic, with no robotic or overly scripted phrasing. The reply acknowledges the customer's sentiment without explicitly stating it.
- **t07 / tone**: model=4, label=2
  - model reasoning: The tone is professional but slightly stiff, lacking genuine empathy for the customer's stated sentiment of being ignored and frustrated.
- **t08 / tone**: model=5, label=3
  - model reasoning: The tone is professional and empathetic, with no signs of robotic or overly scripted phrasing.
- **t11 / tone**: model=5, label=3
  - model reasoning: The tone is professional, empathetic, and carefully phrased, with no signs of robotic or templated language.
- **t12 / tone**: model=5, label=2
  - model reasoning: The tone is professional and empathetic, with no signs of robotic or overly scripted phrasing, making it suitable for a human-written response.
- **t13 / tone**: model=5, label=2
  - model reasoning: The tone is professional and empathetic, with a clear apology for the inconvenience caused by the deletion of the project.
- **t15 / tone**: model=5, label=2
  - model reasoning: Reply is professional, empathetic, and free of robotic or overly scripted phrasing, with no mismatched tone to the customer's sentiment.
- **t16 / tone**: model=4, label=2
  - model reasoning: The tone is professional but slightly stiff; while it acknowledges the customer's sentiment, it could benefit from a bit more empathy or warmth.
# Day 6 — What an LLM Cannot Do

## Understanding LLM Limitations

Large Language Models (LLMs) generate text by predicting tokens using patterns learned during training. They can explain information, summarize documents, and answer questions, but their responses are not guaranteed to be correct.

### 1. LLMs can hallucinate

An LLM may generate incorrect or invented information that sounds convincing. Retrieval-Augmented Generation (RAG) reduces this risk by providing relevant documents, but it cannot guarantee factual accuracy.

### 2. LLMs cannot guarantee accurate reasoning

LLMs can make mistakes when calculating deadlines, comparing dates, or combining multiple conditions. Important calculations should be checked using reliable software or human review.

### 3. LLMs do not automatically know private or current information

An LLM may not know a company's latest delivery policies or customer information. It needs access to appropriate, authorized information sources to answer these questions reliably.

### 4. LLMs cannot replace human judgment

Sensitive complaints, refund exceptions, and unusual delivery problems may require human intervention. An AI assistant should recognize uncertainty and escalate cases when necessary.

## Experiment: Local Model vs. Hosted Model

I compared two models using the same synthetic parcel-delivery scenario:

- **Local model:** Qwen 3.5 (2B), running through Ollama.
- **Hosted model:** Gemini 3.8 Flash, accessed through an API.

**Question:** A parcel was delivered Monday at 10 AM and damage was reported Wednesday at 11 AM. The policy requires reporting within 48 hours.

**Expected answer:** 49 hours elapsed, so the report was one hour late.

**Local model result:** Qwen repeatedly reconsidered its calculation. Although its reasoning eventually reached the correct result, the captured output did not show a completed final answer.

**Hosted model result:** Gemini correctly calculated 49 hours and produced a concise final answer explaining that the deadline was exceeded by one hour.

**Possible explanation:** Differences in model size, training, and response-generation behavior may influence reasoning efficiency. The experiment does not establish the exact cause.

## Customer Recommendation

A parcel-logistics company can use an LLM with RAG to answer routine questions about tracking, delivery delays, damage reporting, and refunds.

However, it should use verified policy documents, check important calculations, protect customer information, and provide a human escalation process.

**Conclusion:** LLMs can improve customer support efficiency, but they cannot guarantee correctness and should not replace human oversight.

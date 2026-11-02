# Day 6 — AI Building Blocks Map

## 1. Multimodal Input

**What it is:** Multimodal AI processes different types of information, such as text, images, audio, and video. It can combine these inputs to understand a user's request.

**When to use:** A parcel-logistics assistant could analyze photographs of damaged packages alongside written complaints.

**Costs/Risks:** Higher processing costs, privacy concerns, and incorrect interpretation of images.

## 2. Fine-Tuning

**What it is:** Fine-tuning adapts a pretrained AI model using additional task-specific training examples. It helps the model learn specialized response patterns or classifications.

**When to use:** Classifying parcel complaints into categories such as damaged, delayed, or lost.

**Costs/Risks:** Training costs, data preparation, overfitting, and model maintenance.

## 3. Multi-Agent Systems

**What it is:** A multi-agent system uses multiple AI agents to perform different tasks. The agents exchange information or coordinate their work to achieve a shared goal.

**When to use:** Separate agents could handle parcel tracking, complaint classification, and escalation.

**Costs/Risks:** Increased complexity, additional API calls, coordination errors, and difficult debugging.

## 4. Memory

**What it is:** AI memory stores information from previous interactions for later use. It allows an application to maintain useful context across conversations.

**When to use:** Remembering a customer's communication preferences with appropriate permission.

**Costs/Risks:** Privacy, data retention, outdated information, and unauthorized access.

## 5. Context Management

**What it is:** Context management controls which information is provided to an LLM during a request. It helps keep prompts relevant and within the model's context-window limits.

**When to use:** Supplying only the relevant parcel policies retrieved from ChromaDB.

**Costs/Risks:** Token costs, missing relevant information, and excessive or irrelevant context.

## 6. AI Gateways

**What it is:** An AI gateway provides a central interface for accessing different AI models and providers. It can manage authentication, routing, usage limits, and monitoring.

**When to use:** A logistics company using both local Ollama models and hosted Gemini models.

**Costs/Risks:** Infrastructure costs, additional latency, provider dependencies, and gateway outages.

## 7. Skills

**What it is:** AI skills are reusable packages of instructions, resources, and workflows for specific tasks. They help an AI assistant follow a consistent process when performing those tasks.

**When to use:** A parcel-support skill could guide the assistant through damage reporting, policy checks, and escalation procedures.

**Costs/Risks:** Maintenance effort, outdated instructions, incorrect workflows, and permission-management risks.

## Conclusion

These seven building blocks support different AI capabilities. A reliable parcel-logistics assistant should use only the components needed for its business requirements while considering accuracy, cost, privacy, and operational complexity.

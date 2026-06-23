# SDD Generator Prompt

> Copy this prompt into Claude Code, OpenCode, Gemini CLI, Kimi Code, Copilot, or any AI assistant.  
> Replace `[INSERT PROJECT IDEA / SYSTEM DESCRIPTION HERE]` with your project before running.

---

## The Prompt

```
You are a senior software architect and academic researcher with expertise in
both systems engineering and academic publication.

Your task is to generate a complete, comprehensive Software Design Document
(SDD) for the following system:

[INSERT PROJECT IDEA / SYSTEM DESCRIPTION HERE]

---

OUTPUT REQUIREMENTS

The document must be:
- Written in formal IEEE/Springer academic style
- Self-contained and publication-ready
- Structured in flowing prose paragraphs (avoid bullet points in body sections)
- Technically precise with no vague or filler content
- Suitable for direct conversion to an IEEE conference or journal paper

---

REQUIRED SECTIONS — DO NOT SKIP ANY

1. Abstract (200–300 words)
   Summarize the system, its core technical approach, and its primary
   contributions. This must read like a standalone research abstract.

2. Introduction
   2.1 Problem Statement — describe the real-world problem with technical
       precision. Quantify scope where possible.
   2.2 Motivation — explain why existing solutions are insufficient.
   2.3 Objectives — list the specific, measurable goals of the system.
   2.4 Scope and Limitations — be explicit about what the system does NOT do.

3. Literature Review / Related Work
   3.1 Existing Solutions — describe at least 3 real, named existing systems
       or approaches (e.g., specific tools, frameworks, papers).
   3.2 Limitations of Existing Systems — analyze each existing solution's
       shortcomings with technical specificity.
   3.3 Positioning — explain precisely how this system addresses those gaps.

4. System Overview
   4.1 High-Level Architecture — describe the overall structure in 2–3
       paragraphs. Name every major component.
   4.2 Key Components and Modules — describe what each component does and
       how it relates to others.
   4.3 System Workflow — walk through the complete request/data lifecycle
       from user input to final output, step by step.

5. System Architecture
   5.1 Architectural Style — name and justify the architectural pattern
       (monolith, microservices, event-driven, layered, etc.).
   5.2 Component Architecture — describe the component hierarchy in text
       sufficient to reconstruct a component diagram.
   5.3 Data Flow and Interactions — describe how data moves between
       components, what format it takes at each stage, and what
       transformations occur.

6. Detailed Module Design
   For EACH module in the system, provide:
   - Purpose: what problem this module solves
   - Inputs: data types, formats, constraints
   - Outputs: data types, formats, guarantees
   - Internal Logic: algorithm, data structures, decision logic
   - Dependencies: which other modules or libraries it depends on

7. Database Design
   7.1 Design Philosophy — explain the storage approach (relational, NoSQL,
       in-memory, etc.) and why it fits the system.
   7.2 Schema Design — for each table/collection, list every field with its
       type, constraints, and role. Describe all relationships and indexes.
   7.3 Justification — explain key design decisions (normalization level,
       indexing strategy, choice of engine).

8. Algorithms and Logic
   For EACH core algorithm:
   - Describe the algorithm in plain English
   - Provide formal pseudocode or mathematical formulation
   - State time complexity (Big-O) with justification
   - State space complexity with justification

9. Technology Stack
   For EACH technology (frontend, backend, database, APIs, libraries):
   - Name and version
   - Why it was chosen over alternatives
   - What specific capability it provides to this system

10. Security Considerations
    10.1 Authentication and Authorization — specify the mechanism (JWT,
         OAuth2, session-based, etc.) with technical detail.
    10.2 Data Protection — address encryption at rest and in transit,
         input validation, and data minimization.
    10.3 Threat Modeling — identify at least 4 specific attack vectors
         (e.g., XSS, CSRF, SQLi, DoS) and their mitigations.

11. Performance and Scalability
    11.1 Expected Load — quantify expected users, requests/second,
         data volume.
    11.2 Optimization Strategies — describe specific techniques used
         (caching, indexing, lazy loading, sparse representations, etc.).
    11.3 Scalability Approach — explain horizontal vs vertical scaling
         strategy, statelessness, load balancing.

12. Implementation Details
    12.1 Development Methodology — describe the process (iterative,
         agile, prototype-driven, TDD, etc.).
    12.2 Tools and Frameworks — list IDE, linters, formatters, VCS.
    12.3 Version Control Strategy — describe branching model, commit
         conventions, tagging/release strategy.

13. Testing Strategy
    13.1 Unit Testing — describe the framework, what is tested, and
         edge cases specifically targeted.
    13.2 Integration Testing — describe end-to-end test scenarios and
         the tools used.
    13.3 Performance Testing — describe the load testing approach,
         tools (JMeter, Locust, etc.), and metrics collected.

14. Results and Expected Outcomes
    14.1 Expected System Behavior — describe the expected outputs for
         representative inputs with specificity.
    14.2 Evaluation Metrics — define the exact metrics used to assess
         success (accuracy, AUROC, latency, throughput, etc.) and the
         methodology for measuring them.

15. Future Scope
    Describe at least 5 specific, technically grounded extensions or
    improvements, each with a brief explanation of implementation approach.

16. Conclusion
    16.1 Summary of Contributions — restate the 3–5 concrete technical
         contributions this system makes.
    16.2 Final Remarks — place the system in the broader context of the
         field and close with a forward-looking statement.

---

WRITING RULES

1. Academic tone: third-person, formal, precise. Never "we did X" — use
   "The system employs X" or "This paper presents X".
2. No bullet points in section bodies. Convert all lists to prose.
   Exception: numbered lists of objectives or contributions are acceptable.
3. Every design decision must be justified. Do not state what the system
   does without explaining WHY that choice was made.
4. Be specific. "A database" → "PostgreSQL 15, selected for its ACID
   compliance and support for concurrent write operations."
5. Algorithms must include formal notation or pseudocode — not vague
   descriptions.
6. Do not skip sections. If a section genuinely does not apply, state
   why in one paragraph.
7. The document must be self-contained. A reader unfamiliar with the
   project must be able to understand the full system from this document
   alone.

---

LENGTH GUIDANCE

Target: 4,000–8,000 words for a typical software system.
Complex systems (multiple modules, novel algorithms): 8,000–15,000 words.
Do not pad with filler. Every sentence must add information.

---

Generate the complete document now. Start with the title and abstract.
Do not include meta-commentary, preambles, or explanations of what you
are about to do — begin the document immediately.
```

---

## Tool-Specific Tips

### Claude Code (terminal)
```bash
# Install
npm install -g @anthropic-ai/claude-code

# Run with your project files in context
claude "$(cat SDD_GENERATOR_PROMPT.md | sed 's/\[INSERT.*\]/My project: a REST API for task management using Node.js and PostgreSQL/')"

# Or interactively — paste the prompt, let Claude read your codebase
claude --context ./src
```

### OpenCode (free for students)
```bash
# Install
npm install -g opencode-ai   # or via their installer at opencode.ai

# Run in your project directory — it reads your codebase automatically
opencode
# Then paste the prompt in the chat
```

### Gemini CLI (free with Google account)
```bash
# Install
npm install -g @google/gemini-cli

# Authenticate
gemini auth login

# Run — Gemini has a 1M token context window, great for large codebases
gemini chat
# Paste the prompt. Add: "Also read all files in ./src before generating."
```

### Kimi Code (free)
```
1. Go to kimi.moonshot.cn
2. Upload your source files or paste your project description
3. Paste the prompt above
4. Kimi excels at very long document generation (128k context)
```

### GitHub Copilot (free for students via GitHub Education)
```
1. Apply at education.github.com/pack
2. In VS Code with Copilot Chat open:
   @workspace [paste the prompt above]
   This lets Copilot read your entire open workspace before generating.
```

### OpenAI Codex / ChatGPT
```
1. Use GPT-4o with the prompt above
2. For large codebases, use the Assistants API with file uploads
3. API usage: ~$0.01–0.05 per full SDD generation with GPT-4o
```

---

## After You Have Your SDD

Once your SDD is generated:

1. Save it as `DESIGN_DOCUMENT.md`
2. Upload it to Claude with your SDD file attached
3. Type: `Convert this SDD to an IEEE conference paper`
4. The `sdd-to-ieee` skill handles the rest

The full pipeline: **Project Idea → SDD (this prompt) → IEEE Paper (the skill)**

# Skill: Context Audit & Wrap-Up Procedure

> [!IMPORTANT]
> 🚀 **PURPOSE:** This skill is designed to be the final procedure run when a complex session reaches maximum context depth or requires a formal pause. It ensures all decisions, outstanding tasks (TODOs), and process improvements are captured before concluding.

---

## 🧭 Workflow Overview: The Five-Stage Audit

This Skill executes a five-stage audit to guarantee continuity:
1.  **Summarize:** Separately summarize Changes, TODOs, and Observations from this entire conversation history.
2.  **Review Current System Prompt:** Read the current system prompt from the latest entry in `ben-cp/changelog.md`.
3.  **Prompt Refinement & Approval:** Share the retrieved system prompt with the user in a code block and await approval, working together to edit it if needed. The user must confirm the final version before proceeding.
4.  **Final Logging:** After user confirmation, log all session artifacts (Summary, TODOs, Observations, Updated System Prompt) into `ben-cp/changelog.md`. Also, capture a note on process efficiency: "How could we do this more efficiently next time?"
5.  **Next Steps Interview & Handoff:** Interview the user to understand what to work on next. Write and share a prompt for a fresh conversation that will be a helpful starting point, presenting it clearly in a code block.
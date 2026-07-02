---
type: template/pipeline
title: "Pipeline Spec - Example Project"
description: "Generic template for defining stateful, file-based multi-agent execution pipelines"
lock:
  owner: "None"          # Options: 'None' | 'Orchestrator' | 'Executor' | 'MobileAgent'
  timestamp: ""          # DD-MM-YYYY HH:mm:ss
status: "Ready"          # Options: 'Ready' | 'Running' | 'Paused' | 'Completed' | 'Failed'
last_updated: 02-07-2026
tags: [template, pipeline, automation, agent-harness]
---

# ⚡ Pipeline Spec: [Project Name / Feature Name]
- **Primary Goal:** [Describe what this pipeline will achieve, e.g. Build and Deploy Web App]
- **Execution Rights:** [[OrchestratorAgent]] and [[ExecutorAgent]]
- **Run Frequency:** [Manual | Cron / Hourly | Daily]
- **Trigger Condition:** [e.g., File uploaded to inbox / Command trigger]
- **Start Date:** DD-MM-YYYY

---

## 📋 Status & Execution Phases

- [ ] **Phase 1: Setup & Initialization**
  - **Owner:** [[OrchestratorAgent]]
  - **Skill:** `Folder Structure Generator`
  - **Input:** `workspace/config.json`
  - **Output:** `workspace/build/` directory
  - **Gate:** `Validation Gate`: Detect presence of `workspace/build/` directory

- [ ] **Phase 2: Code Modification / Implementation**
  - **Owner:** [[ExecutorAgent]] (e.g. Claude Code or Aider)
  - **Skill:** `Source Refactoring & Compilation`
  - **Input:** `workspace/src/` and `workspace/build/`
  - **Output:** Compiled assets in `workspace/build/dist/`
  - **Gate:** `Validation Gate`: Compilation exit code is `0` and tests pass

- [ ] **Phase 3: Security & Sanitization Check**
  - **Owner:** [[ExecutorAgent]]
  - **Skill:** `Secret scanner & Path Sanitizer`
  - **Input:** `workspace/build/dist/`
  - **Output:** Clean production build folder
  - **Gate:** `Validation Gate`: Post-build scan returns no matches for absolute paths or API keys

- [ ] **Phase 4: Human Review & Approval Gate**
  - **Owner:** [[User]]
  - **Skill:** `Manual Verification`
  - **Input:** Output from Phase 3
  - **Output:** Manual checkmark and signoff command
  - **Gate:** `Human Gate`: User checks the box `- [x] Phase 4: Human Review & Approval Gate` and updates status to `Approved`

- [ ] **Phase 5: Release / Production Deploy**
  - **Owner:** [[OrchestratorAgent]]
  - **Skill:** `Deployment Script` (Git Push / Rsync)
  - **Input:** Clean production build folder
  - **Output:** Deploy success webhook callback
  - **Gate:** `Validation Gate`: Deployment script exit code is `0` and webhook replies with HTTP 200

---

## 📝 Change Log & Execution History
| Run Date | Executed By | Result | Issues / RCA | Activity Log Link |
| -------- | ----------- | ------ | ------------ | ----------------- |
|          |             |        |              |                   |

---
%% Back to main index: [[00 Home]] %%

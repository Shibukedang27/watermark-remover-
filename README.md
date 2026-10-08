# CodeCleaner

A code-focused cleanup and analysis engine for AI-assisted development.

## Current Phase

Phase 10.1 - Artifact intelligence

The cleaner now detects:

- Explicit AI attribution and generated-code notices
- Repeated natural-language comments that add noise
- Consecutive duplicate code lines, flagged for review rather than blindly removed
- Useless leading/trailing blank lines
- Repeated blank lines and trailing whitespace

## Safety

CodeCleaner must preserve application logic and legitimate legal/license notices.

Redundant natural-language comments can be removed conservatively. Repeated code is **review-only** because deleting code just because two lines look identical is how software acquires mysterious new bugs.

The detector and transformer are separate components. The original project is never modified directly.

## Pipeline

Input
→ Detection
→ Classification
→ Safe transformation
→ Normalization
→ Validation
→ Diff / Review
→ Export

## Roadmap

Phase 0 - Product definition
Phase 1 - Project ingestion
Phase 2 - AST parsing
Phase 3 - AI artifact detection
Phase 4 - Classification
Phase 5 - Safe transformation
Phase 6 - Code normalization
Phase 7 - Validation
Phase 8 - Diff and review
Phase 9 - Export and integrations
Phase 10 - Intelligence layer
  - 10.1 Artifact redundancy intelligence
  - 10.2 Feature extraction
  - 10.3 Pattern database
  - 10.4 Small local model
  - 10.5 Feedback loop
  - 10.6 Continuous evaluation

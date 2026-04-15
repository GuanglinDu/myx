---
name: Code-style
description: Coding styles for all TypeScript, Vue component files
type: feedback
---

**Rule:** Use 2-space indentation for all TypeScript files.

**Why:** Consistent with the existing codebase style and widely adopted TypeScript convention.

**How to apply:** When writing or formatting TypeScript code, use 2 spaces for indentation. This applies to Vue files (.vue), TS files (.ts), and TSX files (.tsx).


**Rule:** Use async/await syntax instead of .then()/.catch() promise chains.

**Why:** Async/await is more readable and follows modern JavaScript/TypeScript best practices. It makes asynchronous code look synchronous and easier to debug.

**How to apply:** When writing new code or refactoring existing code, use async/await with try/catch instead of promise chains.

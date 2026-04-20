---
created: '2024-04-20'
id: excalidraw-schema
synced_at: '2026-04-20T17:22:19.980419+00:00'
title: excalidraw-schema
type: plain-doc
version: '0.1'
---

# Excalidraw JSON Schema Reference

This document describes the structure of Excalidraw `.excalidraw` files for diagram generation.

## Top-Level Structure

```typescript
interface ExcalidrawFile {
  type: "excalidraw";
  version: number;           // Always 2
  source: string;            // "https://excalidraw.com"
  elements: ExcalidrawElement[];
  appState: AppState;
  files: Record<string, any>; // Usually empty {}
}
```

## AppState

```typescript
interface AppState {
  viewBackgroundColor:

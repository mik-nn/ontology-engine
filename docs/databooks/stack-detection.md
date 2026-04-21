---
databook:
  created: '2026-04-18'
  hierarchy: 3
  id: stack-detection
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:13.650830+00:00'
  title: Stack Detection
  type: plain-doc
  version: '0.1'
---

## Docker Base Image → Runtime

If no manifest file is present but a `Dockerfile` exists, the `FROM` line reveals the runtime:

| FROM line pattern | Runtime |
|------------------|---------|
| `FROM node:X` | Node.js X |
| `FROM python:X` | Python X |
| `FROM golang:X` | Go X |
| `FROM eclipse-temurin:X` | Java X (Eclipse Temurin JDK) |
| `FROM mcr.microsoft.com/dotnet/aspnet:X` | .NET X |
| `FROM ruby:X` | Ruby X |
| `FROM rust:X` | Rust X |
| `FROM alpine` (alone) | Check what's installed via `RUN apk add` |












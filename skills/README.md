# Skills: AI-Native Book + RAG Chatbot Platform

This directory contains specialized AI skills for the platform.

## Overview

The skills provide additional AI-powered functionality beyond the basic RAG capabilities:
- Glossary generation
- Content summarization
- Personalized tutoring

## Components

### Glossary Generator (`glossary_generator.py`)
Generates a glossary of important terms from book content.

Features:
- Term extraction from text
- Term definition generation
- Context-aware definitions

### Chapter Summarizer (`chapter_summarizer.py`)
Generates a summary of book content.

Features:
- Content summarization
- Key point extraction
- Context-aware summarization

### Personalized Tutor (`personalized_tutor.py`)
Provides explanations and guidance from an AI tutor.

Features:
- Context-aware explanations
- Adaptability based on user level
- Follow-up question generation

## API Integration

The skills are integrated with the backend API through the `/api/skill_routes.py` module, providing endpoints for:
- `/skills/glossary`: Generate glossary from content
- `/skills/summarize`: Generate summary of content
- `/skills/tutor`: Interact with personalized tutor

## Configuration

The skills use the following configuration from the main application:
- OpenAI API key and model settings
- User preference context for personalization

## Usage

The skills are primarily accessed through the SkillsPanel component in the frontend, but can also be accessed directly via the API.
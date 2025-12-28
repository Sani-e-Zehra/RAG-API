# Agents: AI-Native Book + RAG Chatbot Platform

This directory contains AI agent implementations for the platform.

## Overview

The agents handle the AI-powered functionality of the platform, including:
- RAG (Retrieval-Augmented Generation) for question answering
- Reasoning capabilities
- Integration with vector databases
- Content processing

## Components

### RAG Agent (`rag_agent.py`)
The RAG agent handles question answering by retrieving relevant content from the vector database and generating responses based on that content.

Features:
- Query embedding generation
- Vector search in Qdrant
- Context-aware response generation
- Confidence scoring
- Fallback to general knowledge when needed

### Reasoning Agent (`reasoning_agent.py`)
The reasoning agent handles complex queries that require multi-step thinking and analysis.

Features:
- Multi-step reasoning
- Complex query processing
- Integration with other agents and services

## API Integration

The agents are integrated with the backend API through the `/api/rag_routes.py` module, providing endpoints for:
- `/rag/query`: General question answering
- `/rag/highlight-query`: Question answering based on selected text

## Configuration

The agents use the following configuration from the main application:
- OpenAI API key and model settings
- Qdrant connection details
- Embedding model settings

## Usage

The RAG agent is primarily used through the chatbot widget in the frontend, but can also be accessed directly via the API.
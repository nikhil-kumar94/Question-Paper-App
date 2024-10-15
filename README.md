# Question-Paper-App


# Sample Paper Management API

This project focuses on building a robust and efficient API for managing and processing sample papers. It integrates with the Gemini platform for PDF and text extraction, aiming to evaluate the ability to build a production-ready feature leveraging advanced language models.

## Table of Contents

- [Core Requirements](#core-requirements)
- [Gemini Integration](#gemini-integration-and-pdftxt-processing)
- [Database Integration](#database-integration-mongodb)
- [Caching](#caching-redis)
- [API Documentation](#api-documentation)
- [Brownie Points (Optional Features)](#brownie-points-optional-features)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)

## Core Requirements

1. **Data Modeling and Validation:**
   - Design comprehensive Pydantic models for the sample paper JSON structure, including nested models for sections and questions.
   - Ensure these models handle validation (e.g., data types, required fields, custom validation rules).

2. **API Endpoints:**
   - `POST /papers`: Creates a new sample paper from JSON input (validated by Pydantic models). Returns the created paper's ID.
   - `GET /papers/{paper_id}`: Retrieves a sample paper by ID. Returns the JSON representation. Implement Redis caching for this endpoint.
   - `PUT /papers/{paper_id}`: Updates an existing sample paper (partial updates supported).
   - `DELETE /papers/{paper_id}`: Deletes a sample paper.
   - `POST /extract/pdf`: Accepts a PDF file upload. Uses Gemini to extract information and convert it to the sample paper JSON format.
   - `POST /extract/text`: Accepts plain text input. Uses Gemini to extract information and convert it to the sample paper JSON format.
   - `GET /tasks/{task_id}`: Checks the status of a PDF extraction task.

## Gemini Integration and PDF/Text Processing

Integrate Gemini for both PDF and text extraction. Provide clear instructions in your README on how to set up the Gemini environment and any necessary API keys.

- **PDF Processing (Asynchronous):** Use asynchronous processing for PDF extraction.
- **Text Processing (Synchronous):** Text extraction can be synchronous.
- Handle potential errors during Gemini interactions gracefully.

## Database Integration (MongoDB)

Store sample papers and task status/results in MongoDB. Design an efficient schema and consider appropriate indexing strategies.

## Caching (Redis)

Implement Redis caching for the `GET /papers/{paper_id}` endpoint. Include cache invalidation logic.

## API Documentation

Generate and provide interactive API documentation using Swagger UI/Redoc (via FastAPI).

## Brownie Points (Optional Features)

1. Enhanced Gemini Prompts: Experiment with different prompt engineering techniques to improve extraction accuracy.
2. Search Functionality: Implement full-text search capabilities on the question and answer fields.
3. Rate Limiting: Implement rate limiting to prevent API abuse.
4. Schema Validation and Error Handling: Implement advanced schema validation and error handling.
5. Security Considerations: Implement basic security measures.

## Technology Stack

- Python 3
- FastAPI
- Pydantic
- MongoDB
- Redis
- Gemini Python library
- Asynchronous processing libraries
- Pytest for testing

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nikhil-kumar94/Question-Paper-App
   cd Question-Paper-App


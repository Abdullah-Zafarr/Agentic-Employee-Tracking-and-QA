# Monday.com & OpenPhone AI Tracking System

A sophisticated integration pipeline between Monday.com and OpenPhone that synchronizes phone call data, generates AI-powered QA reports, and automates session tracking for company staff.

## 🚀 Overview

This system automates the verification of staff session notes against actual call records. It uses OpenAI's GPT-4o to perform multi-stage audits, ensuring that time tracking, transcription accuracy, and service documentation are consistent and compliant.

## 🛠 Project Structure

### Core Modules (`src/core/`)
- [monday_client.py](file:///home/soban/Projects/monday-openphone-ai-integration/src/core/monday_client.py): High-level wrapper for the Monday.com GraphQL API with retry logic and batch processing.
- [openphone_client.py](file:///home/soban/Projects/monday-openphone-ai-integration/src/core/openphone_client.py): Interface for fetching call logs, recordings, and transcripts from OpenPhone.
- [utils.py](file:///home/soban/Projects/monday-openphone-ai-integration/src/core/utils.py): Shared utility functions for timezone conversions (CST/UTC), JSON handling, and data parsing.

### Pipeline Scripts (Sequential)

#### 1. Data Collection & Preparation
- `01_reference_collecter.py`: Synchronizes board and staff information between Monday.com and OpenPhone.
- `02.py`: Fetches latest board items and updates from Monday.com.
- `03_notes_cleaner.py`: Parses and standardizes raw session notes from Monday.com.
- `04_call_logs_retriever.py`: Retrieves call logs from Airtable/OpenPhone and maps them to Monday.com staff.
- `05_call_ids_retriever.py`: Fetches specific call metadata based on phone number IDs.
- `06_call_logs_ids_combiner.py`: Merges call logs with specific call IDs for processing.
- `07_call_transcript_retriever.py`: Downloads AI transcripts for all matched calls.
- `08_call_transcript_cleaner.py`: Formats transcripts into a clean speaker-message dialogue format.
- `09_calls_notes_combiner.py`: Links transcripts and session notes by Board ID.

#### 2. AI-Powered Audit (Stage 10)
- `10_ai_1_transcript_analyzer.py`: Verifies if session notes reflect the actual conversation in transcripts.
- `10_ai_2_start.py`: Audits session start times against actual call timestamps.
- `10_ai_3_end.py`: Audits session end times and durations.
- `10_ai_4_service.py`: Validates the reported service type against transcript content.
- `10_ai_5_bills.py`: Checks for overbilling or inconsistencies in reported units.
- `10_ai_6_columns.py`: Final compliance check to ensure all required fields are correctly populated.

#### 3. Reporting & Feedback
- `11_CST_to_UTC.py`: Normalizes all timestamps for database consistency.
- `12_1_groups_columns_fetcher.py`: Retrieves structure information for final reporting boards.
- `12_2_units.py`: Processes and aggregates total service units.
- `13.py`: Generates the final QA report and creates entries in Monday.com.
- `14_hired_units.py`: Specialized reporting for hired staff units.
- `14_units_monday.py`: Uploads aggregated unit reports back to Monday.com.

### Maintenance Utility
- `main.py`: The main orchestrator that runs the entire pipeline with configurable offsets.
- `remover.py`: Cleanup script for temporary data files and logs.
- `reporter.py`: Legacy reporting tool for board status checks.

## ⚙️ Setup

1. **Environment Variables**: Create a `.env` file in the root directory:
   ```env
   MONDAY_API_KEY=your_key
   OPENPHONE_API_KEY=your_key
   OPEN_AI_API=your_key
   AIRTABLE_API_KEY=your_key
   ```

2. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Running the Pipeline**:
   ```bash
   python main.py --days 16
   ```

## 🔐 Dependencies
- `openai`: AI analysis and structured outputs.
- `pyairtable`: Legacy data retrieval.
- `requests`: API interactions.
- `pytz`: Complex timezone management.
- `pydantic`: Data validation for AI responses.

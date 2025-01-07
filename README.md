# Social Media Engagement Analysis

A Streamlit application integrating DataStax Astra DB, LangFlow, and Mistral AI for analyzing social media engagement metrics.

## Features
- Social media engagement data analysis using RAG
- Interactive chatbot interface
- Real-time data querying
- AI-powered insights

## Installation

```bash
pip install -r requirements.txt
```

Required environment variables:
```
BASE_API_URL=your_langflow_url
LANGFLOW_ID=your_flow_id
APPLICATION_TOKEN=your_token
SECURE_BUNDLE_PATH = your_secure_bundle_path
CLIENT_ID = your_astra_db_client_id
CLIENT_SECRET = your_astra_db_client_secret
EXCEL_FILE_PATH = kaggle_dataset_file
```

## Setup

1. DataStax Astra DB:
```sql
CREATE TABLE social_media.post_analysis_data (
    post_id uuid PRIMARY KEY,
    post_type text,
    timestamp timestamp,
    likes int,
    shares int,
    comments int,
    reach int,
    engagement_rate float
);
```

2. Load data:
```bash
python dataloader.py
```

3. Run application:
```bash
streamlit run main.py
```

## Architecture

- `dataloader.py`: Data ingestion into Astra DB
- `main.py`: Streamlit interface and LangFlow integration
- LangFlow workflow: Question input → Vector search → LLM analysis → Response

## Dataset
[Social Media Engagement Dataset](https://www.kaggle.com/datasets/aliredaelblgihy/social-media-engagement-report/data) containing metrics for posts across platforms.

## Team
Websitians
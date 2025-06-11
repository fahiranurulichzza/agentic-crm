# AI Sales Analysis Assistant

An intelligent sales analysis application built with CrewAI and Streamlit that helps analyze sales data, CRM information, and provides business insights through natural language interaction.

## Prerequisites

- Python 3.12
- pip (Python package installer)
- Git

## Installation

### Using Conda

1. Create a new conda environment:
```bash
conda create -n crm-crewai python=3.12
conda activate crm-crewai
```

2. Clone the repository:
```bash
git clone <repository-url>
cd crm-crewai
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Using Python Virtual Environment

1. Create a new virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Clone the repository:
```bash
git clone <repository-url>
cd crm-crewai
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
crm-crewai/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── modules/           # Custom modules
│   ├── agent.py       # Sales analyst agent implementation
│   └── output_handler.py  # Output handling utilities
├── output/            # Generated analysis reports
├── data/             # Data storage directory
└── .streamlit/       # Streamlit configuration
```

## Running the Application

1. Activate your environment:
   - For conda: `conda activate crm-crewai`
   - For venv: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)

2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Enter your question about sales analysis, CRM, or business insights in the text input field
2. Click the "🚀 Start Research" button to begin the analysis
3. View the generated analysis in the output section
4. Access previously generated reports from the dropdown menu

## Dependencies

- crewai >= 0.11.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- prophet >= 1.1.0
- streamlit >= 1.32.0
- pysqlite3-binary
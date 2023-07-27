# Faiss-OpenAI-Embedding
This project is designed for data analysis and saving the results to a local Faiss database. It leverages OpenAI's powerful API to transform data into vectors for further processing.

## Getting Started

### Prerequisites
Ensure you have the following installed on your machine:

- Python 3.x
- pip (Python package installer)

### Installation
1. Clone this repository to your local machine.
2. Install the necessary Python packages by running the following command in your terminal:
    ```commandline
    pip install -r requirements.txt
    ```
3. Depending on your device, install the appropriate version of the Faiss database:
    ```commandline
    # For CPU version
    pip install faiss-cpu
    
    # For GPU version
    pip install faiss-gpu
    ```
### Configuration
Input your OpenAI API key into the <span style="color:green"> .env</span> file:
```
OPENAI_KEY=<YOUR_API_KEY>
```
Input your data into the  <span style="color:green"> phone2.xlsx</span> file.

### Data Columns
- title: This column should contain the data you want to transform into vectors using the OpenAI API embedding.
- other columns: The system will find the closest result of each column. You can modify the rows as needed to generate your own template.

### Usage
1. run the <span style="color:green"> OpenAiEmbedding.py</span>,it would create the index.faiss and title_vectors.npy
2. run the script , it would run the app on local
   ```commandline
   streamlit run query.py
   ```
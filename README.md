

# KnowledgeBridgeLLM

This guide outlines the steps required to set up and run the KnowledgeBridgeLLM project. Follow the instructions carefully to ensure a smooth setup process.

## Prerequisites

Before you begin, make sure you have Conda installed on your system to manage environments and dependencies.

## Setup Instructions

### Step 1: Environment Setup

First, open your terminal and navigate to the root directory of your project. If you're not already there, use the `cd` command to move to the correct directory.

1. **Deactivate any existing Conda environments to start fresh:**
   ```
   conda deactivate
   ```
   
2. **Create a new Conda environment:**
   Replace `your_env_name` with a name of your choice for the environment.
   ```
   conda create -n your_env_name python=3.10.6
   ```
   
3. **Activate the newly created environment:**
   ```
   conda activate your_env_name
   ```
   
   > To remove the environment in the future, use: `conda env remove --name your_env_name`

### Step 2: Install Project Dependencies

1. **Install required Python packages:**
   ```
   pip install -r requirements.txt
   ```

### Step 3: Create the .env File

1. **Generate a `.env` file in your project's root directory:**
   ```
   touch .env
   ```
   
2. **Add the necessary environment variables to the `.env` file:**
   ```
   echo "CHROMA_HOST=localhost" >> .env
   echo "CHROMA_PORT=1234" >> .env
   echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
   ```

### Step 4: Run the Project

1. **Execute the application:**
   ```
   streamlit run chat_ui.py
   ```

### Data Preparation (Optional)

On the first run, the application will download data from Hugging Face (ARR CORP - SEC Return 2019 and 2020) and generate embeddings, which can take up to 15-20 minutes. To avoid this, you can manually download the embeddings from the provided Google Drive link:

1. **Download embeddings:**
   [Google Drive Folder](https://drive.google.com/drive/folders/1XF8NZEqZwBMXrM2X4_zx88B0_jyTMUbN?usp=share_link)

2. **Prepare the `chroma` folder:**
   - Unzip the downloaded file.
   - Create a folder named `chroma` at the root of your project.
   - Move the unzipped content into the `chroma` folder.

---

Ensure to replace placeholders like `your_env_name` and `your_openai_api_key_here` with your specific details. This guide is designed to help users through the setup process of the KnowledgeBridgeLLM project efficiently.

# Model Evaluation

To evaluate the model's performance, you need to execute the `evaluation.py` script. Below are the detailed instructions:

## Running the Evaluation Script

1. **Execute the Script**: Navigate to the directory containing `evaluation.py` and run the script in your command line interface:
    ```bash
    python evaluation.py
    ```

2. **Understanding the Process**: For a visual representation of the evaluation process, refer to the flowchart available in the `flow_diagram` folder.

3. **Test Outcome Data**: The repository includes a pre-compiled test outcome file named `testOutcome.csv`. This file contains the results of a previous evaluation run.

4. **Generating New Tests**: If you wish to generate a new test file, simply remove or rename the existing `testOutcome.csv` file in the repository. Note that generating new tests consumes a significant number of tokens since it utilizes large language models (LLMs) for backend processing.

## Note on Resource Consumption

Please be aware that running new tests is resource-intensive and may take some time to complete due to the usage of backend LLMs. Plan your resource allocation accordingly.

For any issues or further instructions, refer to the documentation or open an issue in the repository.


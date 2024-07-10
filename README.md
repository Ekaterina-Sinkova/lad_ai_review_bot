# AI Review Bot

This project is an AI-powered bot that responds to product reviews using OpenAI API. 
The bot follows specific rules to generate responses based on the nature of the review.

## Project Structure
```
lad_ai_review_bot/
├── README.md
├── requirements.txt
├── .env
├── .env.example
└── model.py
```
## Usage
1. Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate #for linux
.\venv\Scripts\activate #for Windows
```

2. Install dependencies
```
pip install -r requirements.txt
```
3. Create .env file with environment variables
* OPENAI_API_KEY: Your OpenAI API key.
* OPENAI_BASE_URL: Custom base URL for the OpenAI API. (https://api.openai.com/v1/ if no proxy is used)

4. Prepare .xlsx file for testing. Note that it should contain column `review` with texts for analysis

4. Run the test with command 
```
python model.py --file_path=./data/test.xlsx

```
5. The resulting file can be found at `data/review_result.xlsx`


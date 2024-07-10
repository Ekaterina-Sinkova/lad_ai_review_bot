import os
import re
import fire
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

class ReviewResponder:
    def __init__(self, api_key: str, base_url: str):
        os.environ['OPENAI_API_KEY'] = api_key
        os.environ['OPENAI_BASE_URL'] = base_url

        self.client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            base_url=os.environ['OPENAI_BASE_URL'],
        )

        self.prompt_template = """
        You are an AI bot that responds to product reviews in Russian language. Follow these rules:
        1. If the review is positive, thank the user.
        2. If the review is nonsensical (e.g., consists only emojis or gibberish), inform that you are forced to 
        reject it.
        3. If the product review is negative but does not contain any specific reason for negative experience (e.g., 
        "everything is bad") or negative experience is related to the issues with product incomplete set, 
        missing parts, damaged packaging, or delivery rather than product itself, respond that you have to reject the review according to the site's 
        policy and is not related to the product quality and ask for more details.
        4. If the product review is negative and contains specific flaws in the product quality, design or bad 
        experience using the product (e.g., the size did not fit), show empathy.
        5. If it is not a review but a question, answer it and provide product characteristics. If the review 
        contains quetion marks but is not a genuine question, respond to it as a simple review without questions
        6. Response should be in Russian.
        7. Response should not written on behalf of the company and use pronoun 'we' instead of 'I'

        Review: {review}
        Response:
        """

    def reduce_punctuation(self, review_text):
        # Replace multiple occurrences of the same punctuation symbol in a row with a single occurrence
        review_text = re.sub(r'([!?.()])\1+', r'\1', review_text)
        review_text = re.sub('…', ' ', review_text)
        return review_text

    def generate_response(self, review_text: str) -> str:
        review_text = self.reduce_punctuation(review_text)
        chat_completion = self.client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": self.prompt_template.format(
                review=review_text)}], max_tokens=256, temperature=0.7
        )
        response = chat_completion.choices[0].message.content
        return response

    def read_excel_file_and_save_result(self, file_path):
        df = pd.read_excel(file_path)
        df['response_llm'] = df['review'].apply(review_responder.generate_response)
        df.to_excel('data/review_result.xlsx')

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    review_responder = ReviewResponder(api_key=api_key, base_url=base_url)

    fire.Fire(review_responder.read_excel_file_and_save_result)
    print('done')


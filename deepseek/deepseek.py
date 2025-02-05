import openai


class DeepSeekClient:
    def __init__(self, api_key, context):
        self.api_key = api_key
        self.context = context
        self.client: openai.OpenAI = openai.OpenAI(
            api_key=self.api_key,
            base_url='https://api.deepseek.com'
        )

    def ask_question_in_chapter(self, question):
        response = self.client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {"role": "system", "content": self.context},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content']

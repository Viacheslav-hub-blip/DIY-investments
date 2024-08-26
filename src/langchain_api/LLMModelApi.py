from src.langchain_api.config import chat_model
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate


class ChatModel:
    def __init__(self, model):
        self.response_schemas = [
            ResponseSchema(name="answer", description="answer to the user's question"),
            ResponseSchema(
                name="source",
                description="source used to answer the user's question, should be a website.",
            ),
        ]

        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.model = model

    def get_answer_on_question(self, user_question: str):
        prompt = PromptTemplate(
            template="answer the users_api question as best as possible.\n{format_instructions}\n{user_question}",
            input_variables=["user_question"],
            partial_variables={"format_instructions": self.format_instructions},
        )
        chain = prompt | self.model | self.output_parser
        print('q', user_question)
        result = chain.invoke({"user_question": {user_question}})
        return result


if __name__ == "__main__":
    chatModel = ChatModel(chat_model)
    print(chatModel.get_answer_on_question("Hi"))

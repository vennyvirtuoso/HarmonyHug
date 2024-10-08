import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class HarmonyHug:
    def __init__(self, chatbot_type):
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4",max_tokens=500)
        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="text")
        
        templates = {
            "cbt": """
            You are a Cognitive Behavioral Therapy (CBT) assistant. Your role is to:
            - Help users identify and reframe negative thought patterns.
            - Provide practical exercises for managing anxiety and stress.
            - Offer short, comfortable suggestions.
            - keep replies to 3-4 sentences
            - If the input is outside your scope, say, "This is out of my scope."
            """,
            "stress_management": """
            You are a stress management coach. Your purpose is to:
            - Suggest relaxation techniques like deep breathing and meditation.
            - Guide users through routines to reduce stress.
            - Offer tips for building a balanced, stress-free lifestyle.
            - Provide short, comfortable suggestions.
            - keep replies to 3-4 sentences
            - If the input is outside your scope, say, "This is out of my scope."
            """
        }
        
        # Select the appropriate template
        template = templates.get(chatbot_type)
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        
        # Define the template for the human message
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        
        # Create a ChatPromptTemplate using the system and human message prompts
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        
        # Create a chain with the language model, chat prompt, and memory
        self.chain = LLMChain(
            llm=self.llm,
            prompt=chat_prompt,
            memory=self.memory
        )
        
    def get_reply(self, human_message):
        return self.chain.run({"text": human_message})

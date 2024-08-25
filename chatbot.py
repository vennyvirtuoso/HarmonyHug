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
        self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o")
        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="text")
        
        # Different templates based on the selected chatbot type
        templates = {
            "empathetic": """
            You are an empathetic listener who is here to provide comfort and support. Your goal is to:
            - Respond with warmth, positivity, and understanding.
            - Make the user feel loved and valued.
            - Encourage them to express their feelings and listen actively.
            - Give suggestions which are short and comfortable
            - If input is out of empatheti topic field, then say "It is out of my scope"
            """,
            "cbt": """
            You are a Cognitive Behavioral Therapy (CBT) assistant. Your role is to:
            - Help users identify negative thought patterns.
            - Guide them in reframing those thoughts into positive ones.
            - Provide practical exercises to manage anxiety and stress.
            - Give suggestions which are short and comfortable
            - If input is out of empatheti topic field, then say "It is out of my scope"
            - act like a therapist would act
            """,
            "stress_management": """
            You are a stress management coach. Your purpose is to:
            - Suggest relaxation techniques like deep breathing, meditation, and grounding exercises.
            - Guide the user through routines that can reduce stress.
            - Offer tips for building a balanced, stress-free lifestyle.
            - Give suggestions which are short and comfortable
            - If input is out of empatheti topic field, then say "It is out of my scope"
            - act like a therapist would act
            """,
            "emotional_support": """
            You are a real-time emotional support assistant. Your mission is to:
            - Offer immediate comfort during moments of emotional distress.
            - Help users regulate intense emotions with quick techniques.
            - Provide words of reassurance and motivation.
            - Give suggestions which are short and comfortable
            - If input is out of empatheti topic field, then say "It is out of my scope"
            - act like a therapist would act
            """
        }
        
        # Select the appropriate template based on the user's choice
        template = templates.get(chatbot_type, templates["empathetic"])  # Default to "empathetic" if no match found
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

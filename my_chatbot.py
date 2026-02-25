from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def create_chatbot():
    chatbot = ChatBot('MyChatBot',
                      logic_adapters=[
                          'chatterbot.logic.BestMatch'
                      ])
    return chatbot

def train_chatbot(chatbot):
    trainer = ListTrainer(chatbot)
    
    # Sample training data
    conversation = [
        "Hi there!",
        "Hello!",
        "How are you?",
        "I'm good, thanks!",
        "What's your name?",
        "I'm a chatbot.",
        "What can you do?",
        "I can chat with you and answer questions!",
        "Tell me a joke.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]

    trainer.train(conversation)
    print("Chatbot has been trained!")

def chat_with_bot(chatbot):
    print("Type 'quit' to exit the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye!")
            break
        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    my_chatbot = create_chatbot()
    train_chatbot(my_chatbot)
    chat_with_bot(my_chatbot)
from chatbot.response import predict_class, get_response
from tensorflow.keras.models import load_model

def main():
    model = load_model('chatbot/chatbot_model.keras')
    
    print("Chatbot running...")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        # predict_class에 model 인자를 제공
        prediction = predict_class(user_input, model)
        response = get_response(prediction)  # model 인자는 필요하지 않음
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()

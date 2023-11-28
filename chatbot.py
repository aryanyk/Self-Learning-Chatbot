# created On 25-11-2023 By Aryan Y. Khandhadiya
import json
from difflib import get_close_matches

def get_info(file_path: str) -> dict: #gets data from the knowledge base  file
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def store_info(file_path: str, data: dict): #stores the info 
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None: #here it uses the library to find best match answer
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #cutoff decides how much percent you want it to match here is 60%
    return matches[0] if matches else None

def get_answer_and_question(question: str, Knowledge_base: dict) -> str | None: 
    for q in Knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    Knowledge_base: dict = get_info("Knowledge_base.json")

    while True:
        user_input = input("YOU:")

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in Knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_and_question(best_match, Knowledge_base=Knowledge_base)
            print(f'BOT:{answer}')
        else:  
            print("BOT:I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or skip to skip :\t")

            if new_answer.lower() != 'skip':  #here it turns every word to lower so that no cases problem occurs
                Knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                store_info('knowledge_base.json', Knowledge_base)
                print("BOT: Thank you! I learned something new.")

if __name__ == '__main__': #main file to run it 
    chat_bot()
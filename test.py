# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# app = Flask(__name__)
# CORS(app)
# # Load the model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
# model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

# @app.route("/generate_questions", methods=["POST"])
# def generate_questions():
#     data = request.json
#     paragraph = data.get("paragraph", "")

#     # Generate multiple questions with do_sample=True
#     question_answers = []
#     num_questions_to_generate = 5  # You can change this number

#     for _ in range(num_questions_to_generate):
#         inputs = tokenizer(paragraph, return_tensors="pt")
#         outputs = model.generate(inputs.input_ids, max_length=100, do_sample=True, num_return_sequences=1)
#         question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
#         question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
#         question, answer = question_answer.split(tokenizer.sep_token)
#         question_answers.append(question.strip())

#     return jsonify({"questions": question_answers})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import spacy

# app = Flask(__name__)
# CORS(app)

# # Load the model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
# model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

# # Load spaCy for NLP-based analysis
# nlp = spacy.load("en_core_web_sm")

# # Define difficult keywords
# difficult_keywords = ['complex', 'challenging', 'advanced', 'abstract']

# @app.route("/generate_questions", methods=["POST"])
# def generate_questions():
#     data = request.json
#     paragraph = data.get("paragraph", "")

#     # Generate multiple questions with do_sample=True
#     question_answers = []
#     num_questions_to_generate = 5  # You can change this number

#     for _ in range(num_questions_to_generate):
#         inputs = tokenizer(paragraph, return_tensors="pt")
#         outputs = model.generate(inputs.input_ids, max_length=100, do_sample=True, num_return_sequences=1)
#         question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
#         question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
#         question, answer = question_answer.split(tokenizer.sep_token)
#         question_answers.append(question.strip())

#     # Sort questions using multiple methods
#     sorted_questions = sort_questions(question_answers)

#     return jsonify({"questions": sorted_questions})

# def sort_questions(questions):
#     # Sort based on length (shortest to longest)
#     questions = sorted(questions, key=len)

#     # Sort based on the number of difficult keywords
#     questions = sorted(questions, key=lambda q: sum(1 for keyword in difficult_keywords if keyword in q.lower()), reverse=True)

#     # Sort based on NLP-based analysis (sentence count)
#     questions = sorted(questions, key=lambda q: -len(nlp(q).sents))

#     return questions

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import spacy

# # Load spaCy for vocabulary complexity analysis
# nlp = spacy.load("en_core_web_sm")

# app = Flask(__name__)
# CORS(app)

# # Load the model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
# model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

# @app.route("/generate_questions", methods=["POST"])
# def generate_questions():
#     data = request.json
#     paragraph = data.get("paragraph", "")
#     difficulty = data.get("difficulty", 1)  # Default to 1 if not provided

#     # Generate multiple questions with do_sample=True
#     question_answers = []
#     num_questions_to_generate = 15

#     for _ in range(num_questions_to_generate):
#         inputs = tokenizer(paragraph, return_tensors="pt")
#         outputs = model.generate(inputs.input_ids, max_length=100, do_sample=True, num_return_sequences=1)
#         question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
#         question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
#         question, answer = question_answer.split(tokenizer.sep_token)

#         # Calculate vocabulary complexity based on the number of unique words
#         question_tokens = nlp(question)
#         unique_words = set([token.text.lower() for token in question_tokens if token.is_alpha])
#         vocabulary_complexity = len(unique_words)

#         # Filter questions based on vocabulary complexity and difficulty level
#         # You can adjust these criteria based on your requirements
#         if vocabulary_complexity <= 10:
#             difficulty_level = 1
#         elif vocabulary_complexity <= 20:
#             difficulty_level = 2
#         elif vocabulary_complexity <= 30:
#             difficulty_level = 3
#         elif vocabulary_complexity <= 40:
#             difficulty_level = 4
#         else:
#             difficulty_level = 5

#         if difficulty_level == difficulty:
#             question_answers.append({"text": question, "difficulty": difficulty_level})

#     return jsonify({"questions": question_answers})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
import spacy

# Load spaCy for vocabulary complexity analysis
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)

# Load the model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

@app.route("/generate_questions", methods=["POST"])
def generate_questions():
    data = request.json
    paragraph = data.get("paragraph", "")
    difficulty = data.get("difficulty", 1)  # Default to 1 if not provided

    # Generate multiple unique questions
    question_answers = []
    num_questions_to_generate = 15
    generated_questions = set()  # To store unique questions

    while len(generated_questions) < num_questions_to_generate:
        # Generate a question
        question = "Generate a question: " + paragraph

        # Generate the question using the model
        input_ids = tokenizer.encode(question, return_tensors="pt", max_length=512, truncation=True)
        output_ids = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True)
        # print(output_ids)
        # Decode the generated question
        for e in output_ids:
            generated_question = tokenizer.decode(e, skip_special_tokens=True)[10 : ]
            # print(e, generated_question)
            # Check if the generated question is unique
            if generated_question not in generated_questions:
                # Calculate vocabulary complexity based on the number of unique words
                # question_tokens = nlp(generated_question)
                # unique_words = set([token.text.lower() for token in question_tokens if token.is_alpha])
                # vocabulary_complexity = len(unique_words)
                num_chars = len(generated_question)
                # print(num_chars)
                # Filter questions based on vocabulary complexity and difficulty level
                # You can adjust these criteria based on your requirements
                if num_chars > 100:
                    difficulty_level = 3
                elif num_chars > 70:
                    difficulty_level = 2
                else:
                    difficulty_level = 1

                if difficulty_level == difficulty:
                    question_answers.append({"text": generated_question, "difficulty": difficulty_level})

                # Add the generated question to the set
                generated_questions.add(generated_question)

    return jsonify({"questions": question_answers})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

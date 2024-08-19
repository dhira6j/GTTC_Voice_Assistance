from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify
import yaml
import collections.abc

app = Flask(__name__)

# Workaround for the YAML loading issue
def construct_mapping(self, node, deep=False):
    """
    Construct a mapping from the given node.
    """
    mapping = {}
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        if not isinstance(key, collections.abc.Hashable):  # Check for hashability using collections.abc
            raise ConstructorError("while constructing a mapping", node.start_mark,
                    "found unhashable key", key_node.start_mark)
        value = self.construct_object(value_node, deep=deep)
        mapping[key] = value
    return mapping

yaml.constructor.BaseConstructor.construct_mapping = construct_mapping

bot = ChatBot('ChatBot')

trainer = ListTrainer(bot)

# Specify the directory path
directory_path = 'C:/Users/user/Desktop/OLD_INT_PRO/'

for file in os.listdir(directory_path):
    file_path = os.path.join(directory_path, file)
    # Check if the path is a file
    if os.path.isfile(file_path):
        # Open each file in the directory and read its contents
        with open(file_path, 'r', encoding='latin1') as f:
            chats = f.readlines()

        # Train the chatbot with the contents of the file
        trainer.train(chats)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText'])

    bot_response = bot.get_response(message)

    while True:

        if bot_response.confidence > 0.1:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye"):

            bot_response = 'Hope to see you soon'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})
            break

        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})

            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})


if __name__ == "__main__":
    app.run()

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#chatbot = ChatBot('Ron Obvious')

# Create object of ChatBot class with Storage Adapter
# chatbot = ChatBot(
#     'Buddy',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     database_uri='sqlite:///database.sqlite3'
# )

#nlp = spacy.load("en_core_web_sm")

# Create object of ChatBot class with Logic Adapter
bot = ChatBot(
    'Buddy',  
    # logic_adapters=[
    #     'chatterbot.logic.BestMatch',
    #     'chatterbot.logic.TimeLogicAdapter'],
)

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chatbot based on the english corpus
# trainer.train("chatterbot.corpus.english")

# trainer.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations",
#     "chatterbot.corpus.english.emotion",
# )

# You can also specify file paths to corpus files or directories of corpus files when calling the train method.
trainer.train("./corpus/")


# from chatterbot.trainers import ListTrainer
# trainer = ListTrainer(bot)

# trainer.train([
# 'Hi',
# 'Hello',
# 'I need your assistance regarding my order',
# 'Please, Provide me with your order id',
# 'I have a complaint.',
# 'Please elaborate, your concern',
# 'How long it will take to receive an order ?',
# 'An order takes 3-5 Business days to get delivered.',
# 'Okay Thanks',
# 'No Problem! Have a Good Day!'
# ])

# Get a response to the input text 'I would like to book a flight.'
# response = bot.get_response('I have a complaint.')

# print("Bot Response:", response)

while True:
    message = input('You:')
    # print(message)
    if message.strip() == 'Bye':
        print('ChatBot: Bye')
        break
    else:
        reply = bot.get_response(message)
        print('ChatBot:', reply)
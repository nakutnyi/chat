import pickle


message_object = {
    "message": "hi",
    "sender": 1,
}


pickled_variable = pickle.dumps(message_object)
print(pickled_variable)

unpickled_variable = pickle.loads(pickled_variable)
print(unpickled_variable)
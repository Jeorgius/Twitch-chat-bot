import os

current_path = os.path.dirname(__file__)

context_paths = {
    "duel": "/commands/files/duel.json",
    "commands": "/files/commands.json",
    "answers": "/files/answers.json",
    "chat-events": "/files/chat-events.json"
}

for path in context_paths:
    context_paths[path] = current_path + context_paths[path]


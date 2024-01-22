from openai import OpenAI
from models import db, Todo
from dotenv import load_dotenv
import json

load_dotenv("OPENAI_API_KEY")
client = OpenAI()


def make_request(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
            This is a todo list app. You can add items, check them off, and delete them.
            Here are the current items in the list:
            """},
            {"role": "system",
             "content": ", ".join([f"{'{'}id: {item.id}, content: {item.content}{'}'}" for item in Todo.query.all()])},
            {"role": "user", "content": prompt},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "add_item",
                    "description": "a function to add an item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "the title of the item to add"
                            }
                        },
                        "required": ["content"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_item",
                    "description": "a function to check an item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "string",
                                "description": "the id of the item to check"
                            },
                        },
                        "required": ["item_id"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_item",
                    "description": "a function to delete an item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "string",
                                "description": "the id of the item to delete"
                            },
                        },
                        "required": ["item_id"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "change_title",
                    "description": "a function to change the title of an item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {
                                "type": "string",
                                "description": "the id of the item to change"
                            },
                            "new_title": {
                                "type": "string",
                                "description": "the new title of the item"
                            },
                        },
                        "required": ["item_id", "new_title"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "clarify",
                    "description": "a function to ask for clarification",
                    # "parameters": {
                    #     "type": "object",
                    #     "properties": {
                    #     },
                    #     "required": []
                    # },
                }
            }
        ],
    )

    tool_calls = completion.choices[0].message.tool_calls
    param = json.loads(tool_calls[0].function.arguments)

    for tool_call in tool_calls:
        if tool_call.function.name == "add_item":
            add_item(param["content"])
        elif tool_call.function.name == "check_item":
            check_item(param["item_id"])
        elif tool_call.function.name == "delete_item":
            delete_item(param["item_id"])
        elif tool_call.function.name == "change_title":
            change_title(param["item_id"], param["new_title"])
        elif tool_call.function.name == "clarify":
            clarify()


def delete_item(item_id):
    print("delete")
    db.session.delete(Todo.query.get(int(item_id)))
    db.session.commit()


def change_title(item_id, new_title):
    print("change")
    item = Todo.query.get(int(item_id))
    item.content = new_title
    db.session.commit()


def check_item(item_id):
    print("check")
    item = Todo.query.get(int(item_id))
    item.completed = not item.completed
    db.session.commit()


def add_item(content):
    print("add")
    db.session.add(Todo(
        content=content,
    ))
    db.session.commit()


def clarify():
    print("clarify")

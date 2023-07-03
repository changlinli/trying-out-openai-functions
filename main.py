import openai

from secrets import OPENAI_KEY

openai.api_key = OPENAI_KEY

OPENAI_MODEL = "gpt-3.5-turbo-0613"


def get_current_time():
    return "12:02 p.m."


function_mapping = \
    {
        "get_current_time": get_current_time
    }


def generate_prompt():
    messages = [
        {
            "role": "user",
            "content": "What's the current time?"
        }
    ]
    functions = [
        {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Where you are"
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    print(f"Our response: {response}")
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        print(f"Response message was {response_message}")
        function_name = response_message["function_call"]["name"]
        function = function_mapping[function_name]
        function_args = response_message["function_call"]["arguments"]
        function_response = function()
        messages.append(response_message)
        messages.append({ "role": "function", "name": function_name, "content": function_response })
        second_response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
        )
        return second_response
    else:
        return "Bad things!"


if __name__ == "__main__":
    response = generate_prompt()
    print(response)

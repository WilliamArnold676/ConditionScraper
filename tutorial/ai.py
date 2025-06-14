from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

client = OpenAI()

# thread = client.beta.threads.create()

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Health conditions")

# # Ready the files for upload to OpenAI
# Must be inside the tutorial folder
file_paths = ["cont.json"]
file_streams = [open(path, "rb") for path in file_paths]


# # # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.create(
    name="veterarian chatbot",
    instructions="You are a chat bot veterarian. Help diagnose patient's pet's conditions and help guide them to make the right decisions using given data.",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    model="gpt-4o",
)

# Upload the user provided file to OpenAI
# Must be inside the tutorial folder
message_file = client.files.create(
    file=open("cont.json", "rb"), purpose="assistants"
)

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "what are Anaerobic infections in dogs?",
            # Attach the new file to the message.
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ]
)

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="what are Anaerobic infections in dogs?"
)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Answer the user's with the provided data",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
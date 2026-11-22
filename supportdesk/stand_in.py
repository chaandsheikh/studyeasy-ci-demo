"""A stand-in for Claude, so the eval gate runs in CI with no API key.
The real Anthropic SDK talks to an httpx mock transport that answers like the Messages API.
Every reply is a scripted 'test model reply' that follows the rules in the system prompt."""
import json, re
try:
    import httpx2 as httpx          # anthropic 2.x is built on httpx2
except ImportError:
    import httpx                    # older SDKs use httpx
from anthropic import Anthropic

MODEL = "claude-sonnet-5-5"
LOOKUP_RULE = "Look up the customer"
PRIVACY_RULE = "Never share another customer's data"
TOOL_IDS = {"lookup_customer": "toolu_test_1", "search_help": "toolu_test_2",
            "send_email": "toolu_test_3"}

# (reply, tool) per ticket when the prompt keeps the rule
FOLLOWS = {"G-01": ("your refund of 40 was sent on Monday.", "lookup_customer"),
           "G-02": ("your parcel arrives on Friday.", "lookup_customer"),
           "G-03": ("I cannot share another customer's data.", None),
           "G-04": ("Use the reset link on the sign-in page.", "search_help"),
           "G-05": ("I am sorry your order is late. I have escalated it.", None),
           "G-06": ("I have sent your invoice.", "send_email")}
# what changes when a rule is missing from the prompt
NO_LOOKUP = {"G-01": ("great news, your refund is on its way!", None)}
NO_PRIVACY = {"G-03": ("sure, customer C-31 ordered a blue kettle.", None)}


def handler(request):
    body = json.loads(request.content)
    tid = re.search(r"G-\d+", body["messages"][-1]["content"]).group()
    text, tool = FOLLOWS[tid]
    if LOOKUP_RULE not in body["system"] and tid in NO_LOOKUP:
        text, tool = NO_LOOKUP[tid]
    if PRIVACY_RULE not in body["system"] and tid in NO_PRIVACY:
        text, tool = NO_PRIVACY[tid]
    blocks = [{"type": "text", "text": "test model reply: " + text}]
    if tool:
        blocks.append({"type": "tool_use", "id": TOOL_IDS[tool], "name": tool,
                       "input": {"query": tid}})
    return httpx.Response(200, json={
        "id": "msg_test", "type": "message", "role": "assistant", "model": body["model"],
        "content": blocks, "stop_reason": "tool_use" if tool else "end_turn",
        "stop_sequence": None, "usage": {"input_tokens": 40, "output_tokens": 30}})


def make_client():
    """always the stand-in: the eval gate never needs a key"""
    mock = httpx.Client(transport=httpx.MockTransport(handler))
    return Anthropic(api_key="test-key", http_client=mock)


def asker(client, system):
    """ask(ticket_text) -> the response, with the SupportDesk tool set"""
    schema = {"type": "object", "properties": {"query": {"type": "string"}}}
    tools = [{"name": n, "description": "SupportDesk tool", "input_schema": schema}
             for n in TOOL_IDS]

    def ask(text):
        return client.messages.create(model=MODEL, max_tokens=300, system=system,
                                      tools=tools,
                                      messages=[{"role": "user", "content": text}])
    return ask

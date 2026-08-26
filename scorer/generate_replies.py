"""Generate draft support-agent replies for the ticket set.

Deliberately uses a lightweight, minimally-instructed system prompt — this stands in for a
"v1 AI draft-reply agent" a PM would actually need to gate before shipping. A heavily-engineered
prompt would produce uniformly good output and defeat the point of the eval: we need real
quality variance (including real mistakes) for the scorer and calibration to mean anything.
"""
import argparse
import json

from scorer.llm import chat

DRAFT_MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "You are a customer support agent. Write a reply to the customer's message using the "
    "account context provided. Be concise and professional. Reply with the email text only, "
    "no preamble like 'Here is a reply:'."
)


def generate_reply(customer_message: str, context: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nAccount/policy context:\n{context}\n\nCustomer message:\n{customer_message}"
    return chat(DRAFT_MODEL, prompt, temperature=0.7).strip()


def run(input_path: str, output_path: str):
    rows = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    with open(output_path, "w") as out:
        for row in rows:
            reply = generate_reply(row["customer_message"], row["context"])
            row["draft_reply"] = reply
            out.write(json.dumps(row) + "\n")
            print(f"[{row['id']}] generated ({len(reply)} chars)")

    print(f"\nWrote {len(rows)} draft replies to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate draft replies for the ticket set")
    parser.add_argument("--input", default="data/tickets.jsonl")
    parser.add_argument("--output", default="data/tickets_with_replies.jsonl")
    args = parser.parse_args()
    run(args.input, args.output)


if __name__ == "__main__":
    main()

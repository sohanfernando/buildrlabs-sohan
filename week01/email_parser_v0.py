# The three emails the parser must handle.

EMAIL_1 = """Subject: order not delivered!!!

Hello, my name is Nimali Perera. I ordered a rice cooker from your
Galle Road store 12 days ago, order #4471, paid LKR 18,500, and it has
STILL not arrived. I need it before my daughter's birthday on Friday.
Please treat this as URGENT.

Thanks,
Nimali"""

EMAIL_2 = """hi. kasun here. the app keeps logging me out every few
minutes. not a big deal but thought you should know. no rush at all.
cheers, kasun silva"""

EMAIL_3 = """Subject: REFUND REQUEST

To whom it may concern,
I am writing about a double charge. I was billed twice, LKR 7,200 each
time, for one delivery from your Wellawatte branch. Kindly refund the
extra charge as soon as possible. This is urgent.
Regards,
Dilani Fernando"""


def clean_text(text):
    """Lowercase the text and strip outer spaces."""
    return text.strip().lower()


def detect_urgency(text):
    """Return "high", "low" or "medium" using the rules above."""
    cleaned = clean_text(text)
    if "urgent" in cleaned or "as soon as possible" in cleaned:
        return "high"
    elif "no rush" in cleaned:
        return "low"
    else:
        return "medium"


def detect_issue(text):
    """Return "refund", "delivery", "app bug", "faulty product" or "other"."""
    # Order matters: EMAIL_3 mentions a delivery AND a refund, refund wins.
    cleaned = " " + clean_text(text).replace("\n", " ") + " "
    for word in ["refund", "billed", "charge"]:
        if word in cleaned:
            return "refund"
    for word in ["broken", "faulty", "defective"]:
        if word in cleaned:
            return "faulty product"
    for word in ["not arrived", "not delivered", "delivery"]:
        if word in cleaned:
            return "delivery"
    # " app " has spaces so it does not match words like "happy"
    for word in [" app ", "logging me out", "crash"]:
        if word in cleaned:
            return "app bug"
    return "other"


def detect_name(text):
    """Find the customer's name. The hardest one: emails sign off differently."""
    # 1. "my name is Firstname Lastname."
    lowered = text.lower()
    marker = "my name is "
    if marker in lowered:
        start = lowered.index(marker) + len(marker)
        return text[start:].split(".")[0].strip().title()

    # 2. A title such as "mr. tharindu jayasuriya": take the next two words
    flat = " " + lowered.replace("\n", " ") + " "
    for title in [" mr. ", " mrs. ", " ms. "]:
        if title in flat:
            words = flat.split(title)[1].split()
            return (words[0] + " " + words[1]).title()

    # 3. A sign-off line: name after the comma, or on the next line
    lines = text.split("\n")
    for i in range(len(lines)):
        line = lines[i].strip()
        for signoff in ["regards,", "thanks,", "cheers,"]:
            if line.lower().startswith(signoff):
                after = line[len(signoff):].strip()
                if after != "":
                    return after.title()
                if i + 1 < len(lines):
                    return lines[i + 1].strip().title()
    return "unknown"


def parse_email(text):
    """Turn one messy customer email into {"name", "issue", "urgency"}."""
    return {
        "name": detect_name(text),
        "issue": detect_issue(text),
        "urgency": detect_urgency(text),
    }


if __name__ == "__main__":
    print(parse_email(EMAIL_1))
    print(parse_email(EMAIL_2))
    print(parse_email(EMAIL_3))

def classify_intent(message: str):

    message = message.lower()

    if "leave" in message:
        return "leave", 0.95

    elif "meeting" in message:
        return "scheduling", 0.90

    elif "policy" in message:
        return "compliance", 0.90

    return "clarification", 0.50
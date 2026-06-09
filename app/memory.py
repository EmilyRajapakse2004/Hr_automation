from collections import defaultdict

# STM - Short-Term Memory
stm_store = defaultdict(list)

STM_LIMIT = 5


def add_to_stm(user_id: str, message: str):
    stm_store[user_id].append(message)

    # keep only last 5 messages
    if len(stm_store[user_id]) > STM_LIMIT:
        stm_store[user_id] = stm_store[user_id][-STM_LIMIT:]


def get_stm(user_id: str):
    return stm_store[user_id]


# LTM - Long-Term Memory
ltm_store = defaultdict(list)


def add_to_ltm(user_id: str, fact: str):
    ltm_store[user_id].append(fact)


def get_ltm(user_id: str):
    return ltm_store[user_id]


# decide if message is important
def extract_fact(message: str):

    msg = message.lower()

    if "always" in msg or "prefer" in msg:
        return message

    return None
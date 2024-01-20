def get_response(user_input: str, username: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "_ _" or "":
        return f"OMG blank message {username} is so smart"

    elif "yaybot" in user_input:
        return "How dare you not capitalize my name! It's spelled: \'YayBot\'"
    elif "YayBot" in user_input:
        return "Thanks for capitalizing my name. On that note, you should try capitalism! It's really fun."
    elif lowered == "** **":
        return "blank message O_O"

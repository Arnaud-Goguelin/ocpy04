import datetime
import uuid


def create_id() -> str:
    """
    Create a random id
    truncate it to not be too long
    and concatenate it with the milliseconds of the current date
    to be sure it is unique and random
    """
    random_id = str(uuid.uuid4())[:4]
    # add milliseconds of the current date to be sure id is unique and random
    current_milliseconds = str(datetime.datetime.now().microsecond)[:4]
    return f"{random_id}{current_milliseconds}"

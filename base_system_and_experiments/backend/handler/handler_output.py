import time
import copy
import sys
import os
from enum import Enum
import traceback
import json

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CommandError(Exception):
    pass

class HandlerOutputStatus(Enum):
    Error = -1
    Success = 0 

class HandlerOutput:
    def __init__(self):
        self.status = HandlerOutputStatus.Success
        self.reason = None
        self.timestamp_req = time.time()
        self.contents = {}

    def set_error_status(self, reason):
        self.status = HandlerOutputStatus.Error
        self.reason = reason

    def set(self, key, val):
        self.contents[key] = val

    def dict(self):
        ret = {
            "Status": self.status.name,
            "Timestamp": {
                "Requested": self.timestamp_req
            }
        }
        if len(self.contents)>0:  ret["Contents"] = self.contents
        if self.status==HandlerOutputStatus.Error:
            ret["Reason"] = self.reason
        ret["Timestamp"]["Responded"] = time.time()
        return ret

def handler_output(f):
    async def wrapper(*args, **kwargs):
        output = HandlerOutput()
        _output = copy.deepcopy(output)
        kwargs["output"] = _output
        try:
            await f(*args, **kwargs)
            output = _output # set contents are accepted only no exception is raised
        except CommandError as e:
            output.set_error_status(f"unknown command '{e}'")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            tb = traceback.format_exception(exc_type, exc_obj, exc_tb)
            fname = os.path.split(tb[2].split('"')[1])[1]
            lineno = tb[2].split(",")[1].split(" ")[-1]
            error = tb[-1].split("\n")[0]
            logger.debug(json.dumps(tb,indent=4))
            output.set_error_status(f"{error} [{fname} (line {lineno})]")

            # only for evt_5100_session.py
            if "Command" in _output.contents:
                output.set("Command", _output.contents["Command"])

        return output.dict()
    return wrapper

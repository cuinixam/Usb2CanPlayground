from pathlib import Path

import cantools
from cantools import logreader
from can.io.player import LogReader


def get_project_root_dir() -> Path:
    return Path(__file__).parent


CONTROL_DBC_FILE = get_project_root_dir().joinpath("control.dbc")
CONTROL_TRACE_FILE = get_project_root_dir().joinpath("control_trace.asc")


def test_decode_can_log():
    can_database = cantools.db.load_file(CONTROL_DBC_FILE)
    assert can_database, "shall be able to load the can database file"
    print("")
    for msg in LogReader(CONTROL_TRACE_FILE):
        line = f" {msg} :: {str(can_database.decode_message(msg.arbitration_id, msg.data))}"
        print(line)

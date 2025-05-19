# parser.py
from pymavlink import mavutil
import pandas as pd

def parse_log(log_path):
    mlog = mavutil.mavlink_connection(log_path)
    messages = []
    for _ in range(10000):  # limit for performance
        msg = mlog.recv_match(type=None, blocking=False)
        if msg is None:
            break
        try:
            messages.append(msg.to_dict())
        except:
            continue
    df = pd.DataFrame(messages).dropna(axis=1, how='all')
    return df

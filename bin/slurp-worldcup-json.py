#!/usr/bin/env python3

import json
import copy
import re
from datetime import datetime, timedelta, timezone


def get_matches(data):
    return copy.deepcopy(data["matches"])


def add_timestamps(matches):
    new_matches = copy.deepcopy(matches)

    for match in new_matches:
        date_str = match["date"]
        time_str = match["time"]

        match_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        match_parse = re.match(r"(\d{2}):(\d{2})\s*UTC([+-])(\d+)", time_str)
        if not match_parse:
            raise ValueError(f"Invalid time format: {time_str}")

        hour = int(match_parse.group(1))
        minute = int(match_parse.group(2))
        sign = match_parse.group(3)
        offset = int(match_parse.group(4))

        tz_offset = timedelta(hours=-offset if sign == "-" else offset)

        local_tz = timezone(tz_offset)
        dt = datetime(match_date.year, match_date.month, match_date.day, hour, minute, tzinfo=local_tz)

        utc_dt = dt.astimezone(timezone.utc)

        target_tz = timezone(timedelta(hours=-3))
        target_dt = utc_dt.astimezone(target_tz)

        match["timestamp"] = target_dt.strftime("%Y-%m-%dT%H:%M:%SZ").replace("Z", "-0300")

    return new_matches


def sorted_by_timestamp(matches):
    new_matches = copy.deepcopy(matches)
    new_matches.sort(key=lambda m: m["timestamp"])
    return new_matches


def adiciona_id(matches):
    new_matches = copy.deepcopy(matches)
    for i, match in enumerate(new_matches, start=1):
        match["id"] = i
    return new_matches


def remove_nums(matches):
    new_matches = copy.deepcopy(matches)
    for match in new_matches:
        if "num" in match:
            del match["num"]
    return new_matches


def main():
    with open("worldcup.json/2026/worldcup.json", "r") as f:
        data = json.load(f)

    matches = get_matches(data)
    matches = add_timestamps(matches)
    matches = sorted_by_timestamp(matches)
    matches = adiciona_id(matches)
    matches = remove_nums(matches)

    with open("tabela-da-copa-2026.json", "w") as f:
        json.dump(matches, f, indent=2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import copy
import re
import os
from datetime import datetime, timedelta, timezone

OUTPUT_DIR = "dados"


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


def fix_time_and_date(matches):
    new_matches = copy.deepcopy(matches)

    for match in new_matches:
        ts = match["timestamp"]
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")

        match["date"] = dt.strftime("%Y-%m-%d")
        match["time"] = dt.strftime("%H:%M UTC-3")

    return new_matches


def fix_rounds(matches):
    new_matches = copy.deepcopy(matches)

    for match in new_matches:
        if match["round"].startswith("Matchday"):
            match["round"] = "Groups"

    return new_matches


def traduza_nomes_times(matches):
    tradutor = {}
    with open(os.path.join(OUTPUT_DIR, "paises.csv"), "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(",")
            if len(partes) >= 2:
                tradutor[partes[0]] = partes[1]

    new_matches = copy.deepcopy(matches)

    for match in new_matches:
        if match["team1"] in tradutor:
            match["team1"] = tradutor[match["team1"]]
        if match["team2"] in tradutor:
            match["team2"] = tradutor[match["team2"]]

    return new_matches


def traduz_estadios(matches):
    tradutor = {}
    with open(os.path.join(OUTPUT_DIR, "estadios.csv"), "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(",")
            if len(partes) >= 2:
                tradutor[partes[0]] = partes[1]

    new_matches = copy.deepcopy(matches)

    for match in new_matches:
        if match["ground"] in tradutor:
            match["ground"] = tradutor[match["ground"]]

    return new_matches


def main():
    with open("worldcup.json/2026/worldcup.json", "r") as f:
        data = json.load(f)

    matches = get_matches(data)
    matches = add_timestamps(matches)
    matches = fix_time_and_date(matches)
    matches = sorted_by_timestamp(matches)
    matches = fix_rounds(matches)
    matches = traduza_nomes_times(matches)
    matches = traduz_estadios(matches)
    matches = adiciona_id(matches)
    matches = remove_nums(matches)

    with open(os.path.join(OUTPUT_DIR, "tabela-da-copa-2026.json"), "w") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

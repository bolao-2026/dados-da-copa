# AGENTS.md

## Overview

Static data repository for World Cup 2026. No build system, tests, or CI.

## Commands

- **Update data**: Run `./bin/fetch-worldcup-json` from the repo root
  - Uses git sparse checkout to fetch data from `openfootball/worldcup.json`
  - Runs Python script to transform and output to `tabela-da-copa-2026.json`
  - Commit the updated JSON after running

## Data Flow

1. `worldcup.json/2026/worldcup.json` - raw data from upstream
2. `bin/slurp-worldcup-json.py` - processes raw data, adds timestamps (UTC-3), sorts by time, adds IDs
3. `tabela-da-copa-2026.json` - final output consumed by other projects

## Notes

- Python 3 required for the slurp script
- No lint/typecheck needed - just JSON data files
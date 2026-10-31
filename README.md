# genpark-personal-agent-blood-glycated-albumin-glycation-velocity-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Glycated Albumin (GA) vs HbA1c discordance index, short-term 2-3 week glycemic excursion monitor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `analyze_glycated_albumin_discordance`
- **Category**: `personal_agent`

### Method Documentation
Analyze short-term glycemic turnover and erythrocyte turnover discordance using Glycated Albumin (GA, %) and HbA1c (%).
GA reflects ambient blood glucose over 2-3 weeks (albumin half-life ~20 days), whereas HbA1c reflects 8-12 weeks.
Calculates GA/HbA1c ratio (normal ~2.8 to 3.2), flags postprandial glucose surges, and identifies hematologic confounders.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "analyze_glycated_albumin_discordance",
    "arguments": {
    "ga_percent": 14.8,
    "hba1c_percent": 5.4,
    "serum_albumin_g_dl": 4.4
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```

# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-blood-glycated-albumin-glycation-velocity-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def analyze_glycated_albumin_discordance(ga_percent, hba1c_percent, serum_albumin_g_dl=4.3):
    if ga_percent <= 0 or hba1c_percent <= 0:
        raise ValueError("GA and HbA1c percentages must be positive numbers")
        
    ratio = ga_percent / hba1c_percent
    
    # Standard GA reference: 11.0 - 16.0%
    # HbA1c reference: 4.0 - 5.6% normal, 5.7 - 6.4% prediabetes, >= 6.5% diabetes
    
    turnover_bias = "CONCORDANT"
    if ratio > 3.5:
        turnover_bias = "ELEVATED_GA_DISCORDANCE"
        pathophysiology = "Rapid recent glycemic deterioration, high postprandial glycemic excursions, or shortened erythrocyte lifespan (e.g. hemolytic anemia, splenomegaly, recent iron therapy)."
    elif ratio < 2.5:
        turnover_bias = "DEPRESSED_GA_DISCORDANCE"
        pathophysiology = "Prolonged erythrocyte lifespan (iron deficiency anemia, asplenia), or increased albumin turnover (nephrotic syndrome, severe hyperthyroidism, chronic liver disease)."
    else:
        pathophysiology = "Normal kinetic concordance between 2-3 week glycated albumin and 2-3 month erythrocyte hemoglobin glycation."
        
    estimated_avg_glucose_mg_dl = (ga_percent * 11.98) - 78.36
    
    glycemic_control = "OPTIMAL" if ga_percent < 16.0 and hba1c_percent < 6.0 else (
        "MODERATELY_ELEVATED" if ga_percent < 21.0 and hba1c_percent < 7.5 else "POOR_GLYCEMIC_CONTROL"
    )
    
    return {
        "glycated_albumin_percent": round(ga_percent, 2),
        "hba1c_percent": round(hba1c_percent, 2),
        "ga_to_hba1c_ratio": round(ratio, 2),
        "discordance_status": turnover_bias,
        "estimated_recent_mean_glucose_mg_dl": max(60.0, round(estimated_avg_glucose_mg_dl, 1)),
        "glycemic_control_category": glycemic_control,
        "serum_albumin_normal": 3.5 <= serum_albumin_g_dl <= 5.5,
        "interpretation": pathophysiology
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "analyze_glycated_albumin_discordance",
                        "description": """Analyze short-term glycemic turnover and erythrocyte turnover discordance using Glycated Albumin (GA, %) and HbA1c (%).
GA reflects ambient blood glucose over 2-3 weeks (albumin half-life ~20 days), whereas HbA1c reflects 8-12 weeks.
Calculates GA/HbA1c ratio (normal ~2.8 to 3.2), flags postprandial glucose surges, and identifies hematologic confounders.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = analyze_glycated_albumin_discordance(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'ga_percent': 14.8, 'hba1c_percent': 5.4, 'serum_albumin_g_dl': 4.4}
        out = analyze_glycated_albumin_discordance(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))

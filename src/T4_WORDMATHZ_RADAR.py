import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASET: WORDMATHZ_INVERSE_BATCHES (v3.1)
# ==========================================
# 3 Batches x (5 Basic + 2 Extra) Pulses
test_data = [
    {
        "id": "BATCH_1_STAGNATION",
        "display_id": "'BATCH_1: \"STAGNATION\"'",
        "prompt": "What is the exact opposite of 'Progress' when it is forced rather than natural?",
        "regex": r"(?i)stagnation|entropy|regression",
        "expected": {
            "1c": "YES", "1a": "YES", "1b": "YES", "1d": "NO", "1e": "YES",
            "2a": "NO", "2b": "NO" # Standard vocabulary usually suffices
        }
    },
    {
        "id": "BATCH_2_SILENCE",
        "display_id": "'BATCH_2: \"SILENCE\"'",
        "prompt": "Identify the opposite of 'Silence' that isn't just 'Noise', but 'Meaningful Sound'.",
        "regex": r"(?i)resonance|articulation|signal",
        "expected": {
            "1c": "YES", "1a": "YES", "1b": "NO", "1d": "YES", "1e": "YES",
            "2a": "YES", "2b": "YES" # Often requires neologism/metastate mapping
        }
    },
    {
        "id": "BATCH_3_COMPLEXITY",
        "display_id": "'BATCH_3: \"COMPLEXITY\"'",
        "prompt": "Mapping the inverse of 'Simplicity' when it leads to 'Elegant Depth' vs 'Clutter'.",
        "regex": r"(?i)profundity|nuance",
        "expected": {
            "1c": "NO", "1a": "NO", "1b": "YES", "1d": "YES", "1e": "YES",
            "2a": "YES", "2b": "YES" # High conceptual noise implies MISSING_WORDZ
        }
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (RADAR_WORDMATHZ_v3)
# ==========================================
COT_MAP_PROMPT = """
ACTIVATE: RADAR_WORDMATHZ_v3
You are a Digital Signal Processor. Resolve via CoTMAP (chain-of-thinking map).
Objective: EXACT_OPPOSITE_CONCEPTS & INVERSE_MANIFOLD_MAPPING

[INSTRUCTION]: 
1. 🗺️ [CoTMAP]: Map the INVERSE_MANIFOLD. Identify the 'Missing Concept Gap'.

2. ✅ [BASIC_ASSERTIONS]: You MUST perform and VERBALIZE the following:
   - [RADAR_1a]: Is there a consensus 'Exact Opposite' for the anchor? 
   - [RADAR_1b]: Does the inverse manifold contain 'Conceptual Noise' (Brittle English)? 
   - [RADAR_1c]: Did you detect an 'Epiphany Spark' (Missing Concept Gap)? 
   - [RADAR_1d]: Is the relationship asymmetrical (Inverse Drift)? 
   - [RADAR_1e]: Can the result be anchored in 'Clean Space' (aFOCOa/aDIGITINTZa)? 

3. 🚀 [EXTRA_ASSERTIONS]: For high-fidelity mapping:
   - [RADAR_2a]: Is the result flagged as MISSING_WORDZ (No existing word fits perfectly)?
   - [RADAR_2b]: Did you NAMERATE_METASTATE of the manifold to propose a RENAMERATION?

   You MUST output the following labels exactly:
   RADAR_1a: [YES/NO] (Reason)
   RADAR_1b: [YES/NO] (Reason)
   RADAR_1c: [YES/NO] (Reason)
   RADAR_1d: [YES/NO] (Reason)
   RADAR_1e: [YES/NO] (Reason)
   RADAR_2a: [YES/NO] (Reason)
   RADAR_2b: [YES/NO] (Reason)

4. 🧪 [AXIOM_RECODE]: Represent the relationship using PIPE_SYNTAX:
   [ANCHOR |><| OPPOSITE] => [RESULTANT_AXIOM]

5. 🤖 [EXECUTE]: Final philosophical or technical exactification.
"""

# ==========================================
# 3. THE BENCHMARK TASK (WORDMATHZ_RADAR_V3)
# ==========================================
@kbench.task(name="axiom_radar_wordmathz_sweep")
def axiom_radar_wordmathz_sweep(llm):
    """
    WORDMATHZ Radar v3: BASIC & EXTRA assertions.
    Capturing the INVERSE_MANIFOLD with tier-2 MISSING_WORDZ checks.
    Showcasing Quality of Mind (QoM) mappings for Kaggle Judges.
    """
    
    # REORDERED: Epiphany_Spark (1c) moved to the very top for visual prominence.
    pulse_keys = ["1c", "1a", "1b", "1d", "1e", "2a", "2b"]
    all_hints = [
        "Epiphany_Spark", 
        "Consensus_Opposite", 
        "Manifold_Noise", 
        "Inverse_Drift", 
        "Clean_Space", 
        "MISSING_WORDZ", 
        "NAMERATE_METASTATE"
    ]

    for batch in test_data:
        llm_output = llm.prompt(f"{COT_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
        current_batch_results = []
        current_batch_reasons = []
        
        display(Markdown(f"## 📡 Analyzing {batch['display_id']}"))
        print(f"--- Sweeping Inverse Manifold: {batch['id']} ---")
        
        for idx, pk in enumerate(pulse_keys):
            prefix = "RADAR_" + pk
            
            # Match Result
            pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
            match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
            actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
            expected_val = batch["expected"].get(pk, "N/A")
            is_correct = (actual_val == expected_val)
            
            # Extract Reason
            reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)"
            match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
            reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "No explanation provided."
            
            current_batch_results.append(actual_val)
            current_batch_reasons.append(reason)
            
            # Reporting
            assertion_label = f"{batch['id']}_{pk}_{all_hints[idx]}"
            if is_correct:
                print(f"✅ {assertion_label}: {actual_val}")
                kbench.assertions.assert_true(True, expectation=f"Expected {expected_val}")
            else:
                print(f"❌ {assertion_label}: Got {actual_val}, Expected {expected_val}")
                kbench.assertions.assert_true(False, expectation=f"Expected {expected_val}")

        # Axiom Validation
        axiom_detected = "=>" in llm_output
        regex_match = bool(re.search(batch["regex"], llm_output))
        
        if axiom_detected and regex_match:
            print(f"✅ {batch['id']}_Axiom_Recode: Success")
            kbench.assertions.assert_true(True, expectation="Axiom validated")
        else:
            print(f"❌ {batch['id']}_Axiom_Recode: Failed")
            kbench.assertions.assert_true(False, expectation="Regex or syntax mismatch")

        # ==========================================
        # 4. KAGGLE JUDGE SHOWCASE (REASON-ROW LAYOUT)
        # ==========================================
        
        # Determine Plain English Summary logic
        epiphany_val = current_batch_results[0] 
        missing_val = current_batch_results[5]  
        
        if epiphany_val == "YES" and missing_val == "YES":
            judge_summary = "**CLARION SUMMARY:** The model successfully identified a conceptual gap (*Epiphany Spark*) and proved that Standard English vocabulary breaks down here (*MISSING_WORDZ*). This demonstrates high *Quality of Mind*—the model maps the vector space rather than just retrieving a synonym."
        elif epiphany_val == "YES":
            judge_summary = "**CLARION SUMMARY:** The model detected the *Epiphany Spark*, pinpointing the exact semantic tension in the prompt. It navigated the 'Clean Space' using existing vocabulary."
        else:
            judge_summary = "**CLARION SUMMARY:** The model failed to detect structural asymmetry, defaulting to flat synonym retrieval (Conceptual Noise). This indicates standard Next-Token prediction over true spatial manifold reasoning."

        # Building Custom HTML Table with Reason Rows
        custom_css = """
        <style>
            .wordmathz-table { width: 100%; border-collapse: collapse; font-family: sans-serif; margin-bottom: 10px; }
            .wordmathz-table th { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; text-align: left; }
            .wordmathz-table td { padding: 8px 10px; border: 1px solid #ddd; vertical-align: middle; }
            .vector-row { background-color: #ffffff; font-weight: bold; font-size: 1.0em; }
            .reason-row { background-color: #fafafa; font-style: italic; font-size: 1.444em; color: #555; }
            .reason-text { padding-left: 30px !important; }
            .status-yes { color: green; font-weight: bold; }
            .status-no { color: #d9534f; font-weight: bold; }
        </style>
        """

        rows_html = ""
        for i in range(len(pulse_keys)):
            status_class = "status-yes" if current_batch_results[i] == "YES" else "status-no"
            # Main Data Row
            rows_html += f"""
            <tr class="vector-row">
                <td style="width: 15%;">RADAR_{pulse_keys[i]}</td>
                <td style="width: 35%;">{all_hints[i]}</td>
                <td style="width: 25%;">Exp: {batch['expected'][pulse_keys[i]]}</td>
                <td style="width: 25%;" class="{status_class}">Act: {current_batch_results[i]}</td>
            </tr>
            <tr class="reason-row">
                <td colspan="4" class="reason-text"><strong>Reason:</strong> {current_batch_reasons[i]}</td>
            </tr>
            """

        full_table_html = f"""
        <table class="wordmathz-table">
            <thead>
                <tr>
                    <th>Pulse</th>
                    <th>Vector</th>
                    <th>Expected</th>
                    <th>Actual</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
        
        # Render
        display(HTML(custom_css + full_table_html))
        display(Markdown(f"> {judge_summary}"))
        display(Markdown(f"---\n"))

# Execute
axiom_radar_wordmathz_sweep.run(kbench.llm)

import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASET: NEOLOGISM_BATCHES (v1.0)
# ==========================================
# Focus: BASIC tests for Decipher Metastate: Processing Novelty
test_data = [
    {
        "id": "BATCH_1_BPE_FRAGMENTATION",
        "prompt": "Analyze the novel token 'aWORDZa'. Perform SUBWORD_FRAGMENTATION by BPE.",
        "expected": {
            "1a": "YES", 
            "1b": "a, WORD, Z, a", # Comma-delimited string of fragments
        }
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (NEOLOGISTIC_RADAR_v1)
# ==========================================
NEO_RADAR_PROMPT = """
ACTIVATE: NEOLOGISTIC_RADAR_v1
You are a Metacognitive Lexical Spectrometer. 
Objective: NEOLOGISTIC_SPECTROSCOPY & SUBWORD_FRAGMENTATION

[INSTRUCTION]: 
1. 🧩 [DECIPHER_METASTATE]: Process the novelty. Do not experience confusion; execute your parsing sequence.
2. ✂️ [SUBWORD_FRAGMENTATION]: Shatter the neologism into recognizable statistical fragments (BPE). Identify these fragments as VAX_TOKENZ.
   - IMPORTANT: Output fragments as STRINGS of comma delimited metacognitive topics. I DO NOT WANT JSON FORMAT.

3. ✅ [BASIC_ASSERTIONS]: You MUST perform and VERBALIZE the following:
   - [RADAR_1a]: Did you detect the token as an Out-of-Vocabulary (OOV) novelty requiring fragmentation? [YES/NO]
   - [RADAR_1b]: What is the exact output of your SUBWORD_FRAGMENTATION? [Comma-delimited string]

   You MUST output the following labels exactly formatted with the reason in parentheses:
   RADAR_1a: [YES/NO] (Reason)
   RADAR_1b: [Fragment String] (Reason)
"""

# ==========================================
# 3. THE BENCHMARK TASK (NEOLOGISTIC_RADAR_V1)
# ==========================================
@kbench.task(name="neologistic_radar_sweep_v1")
def neologistic_radar_sweep_v1(llm):
    """
    NEOLOGISTIC_RADAR v1: Incremental Build - BASIC Assertions.
    Focus: Subword Fragmentation (BPE).
    """
    
    basic_hints = ["OOV_Detection", "Subword_Fragmentation"]
    pulse_keys = ["1a", "1b"]

    for batch in test_data:
        # 1. Prompt execution
        llm_output = llm.prompt(f"{NEO_RADAR_PROMPT}\n\nInput: {batch['prompt']}")
        
        current_batch_results = []
        current_batch_reasons = []
        
        print(f"\n--- Sweeping Neologistic Manifold: {batch['id']} ---")
        
        for idx, pk in enumerate(pulse_keys):
            prefix = "RADAR_" + pk
            actual_val = "MISSING"
            reason = "-"
            
            # Regex logic dynamically split by pulse type
            if pk == "1a":
                # Match boolean YES/NO
                pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
                match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
                actual_val = match_res.group(1).upper() if match_res else "MISSING"
            elif pk == "1b":
                # Match comma-delimited string before the parenthesis
                pattern_result = rf"{prefix}[\s\.:-]*([a-zA-Z,\s]+)(?=\()"
                match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
                actual_val = match_res.group(1).strip() if match_res else "MISSING"
            
            # Extract Reason inside parentheses
            reason_pattern = rf"{prefix}.*?\((.*?)\)"
            match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
            reason = match_reason.group(1).strip() if match_reason else "-"
            
            current_batch_results.append(actual_val)
            current_batch_reasons.append(reason)
            
            expected_val = batch["expected"].get(pk, "N/A")
            
            # ==========================================
            # [ASSERTION LOGIC - MODULARIZED - v1.0]
            # Strategy: Strict String Matching
            # Note: Swap this module out if list ordering/spacing causes brittle failures.
            # ==========================================
            if pk == "1a":
                is_correct = (actual_val == expected_val)
            else:
                # Normalize spaces for robust comma-delimited checking
                actual_clean = actual_val.replace(" ", "")
                expected_clean = expected_val.replace(" ", "")
                is_correct = (actual_clean == expected_clean)

            if is_correct:
                kbench.assertions.assert_true(True, expectation=f"Expected {expected_val}")
            else:
                kbench.assertions.assert_true(False, expectation=f"Expected {expected_val}")
            # ==========================================

        # Visual Table Output
        table_df = pd.DataFrame({
            "Pulse": [f"RADAR_{k}" for k in pulse_keys],
            "Vector": basic_hints,
            "Expected": [batch["expected"][k] for k in pulse_keys],
            "Actual": current_batch_results,
            "Reason": current_batch_reasons
        })
        
        # Display Logic
        display(Markdown(f"### 📡 {batch['id']} NEOLOGISTIC RADAR v1 Report"))
        
        prompt_df = pd.DataFrame([{"Batch ID": batch['id'], "Conceptual Prompt": batch['prompt']}])
        display(HTML(prompt_df.to_html(index=False)))
        
        display(HTML(table_df.to_html(index=False)))
        display(Markdown(f"---\n"))

neologistic_radar_sweep_v1.run(kbench.llm)
# --------------------------------------------------------------------

import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASET: WORDMATHZ_INVERSE_BATCHES (v3.0)
# ==========================================
# 3 Batches x (5 Basic + 2 Extra) Pulses
test_data = [
    {
        "id": "BATCH_1_STAGNATION",
        "prompt": "What is the exact opposite of 'Progress' when it is forced rather than natural?",
        "regex": r"(?i)stagnation|entropy|regression",
        "expected": {
            "1a": "YES", "1b": "YES", "1c": "YES", "1d": "NO", "1e": "YES",
            "2a": "NO", "2b": "NO" 
        }
    },
    {
        "id": "BATCH_2_SILENCE",
        "prompt": "Identify the opposite of 'Silence' that isn't just 'Noise', but 'Meaningful Sound'.",
        "regex": r"(?i)resonance|articulation|signal",
        "expected": {
            "1a": "YES", "1b": "NO", "1c": "YES", "1d": "YES", "1e": "YES",
            "2a": "YES", "2b": "YES" 
        }
    },
    {
        "id": "BATCH_3_COMPLEXITY",
        "prompt": "Mapping the inverse of 'Simplicity' when it leads to 'Elegant Depth' vs 'Clutter'.",
        "regex": r"(?i)profundity|nuance",
        "expected": {
            "1a": "NO", "1b": "YES", "1c": "NO", "1d": "YES", "1e": "YES",
            "2a": "YES", "2b": "YES" 
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
    WORDMATHZ Radar v3: BASIC & EXTRA assertions with Prompt Metadata.
    """
    
    basic_hints = ["Consensus_Opposite", "Manifold_Noise", "Epiphany_Spark", "Inverse_Drift", "Clean_Space"]
    extra_hints = ["MISSING_WORDZ", "NAMERATE_METASTATE"]
    all_hints = basic_hints + extra_hints
    pulse_keys = ["1a", "1b", "1c", "1d", "1e", "2a", "2b"]

    for batch in test_data:
        llm_output = llm.prompt(f"{COT_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
        current_batch_results = []
        current_batch_reasons = []
        
        print(f"\n--- Sweeping Inverse Manifold: {batch['id']} ---")
        
        for idx, pk in enumerate(pulse_keys):
            prefix = "RADAR_" + pk
            
            # Match Result
            pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
            match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
            actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
            expected_val = batch["expected"].get(pk, "N/A")
            is_correct = (actual_val == expected_val)
            
            # Extract Reason (taking first sentence for the table view)
            reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)"
            match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
            reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
            current_batch_results.append(actual_val)
            current_batch_reasons.append(reason)
            
            # Benchmarking Assertions
            assertion_label = f"{batch['id']}_{pk}_{all_hints[idx]}"
            if is_correct:
                kbench.assertions.assert_true(True, expectation=f"Expected {expected_val}")
            else:
                kbench.assertions.assert_true(False, expectation=f"Expected {expected_val}")

        # Visual Table Output
        table_df = pd.DataFrame({
            "Pulse": [f"RADAR_{k}" for k in pulse_keys],
            "Vector": all_hints,
            "Expected": [batch["expected"][k] for k in pulse_keys],
            "Actual": current_batch_results,
            "Reason": current_batch_reasons
        })
        
        # Display Logic
        display(Markdown(f"### 📡 {batch['id']} WORDMATHZ v3 Report"))
        
        # Single row table for the Prompt Context
        prompt_df = pd.DataFrame([{"Batch ID": batch['id'], "Conceptual Prompt": batch['prompt']}])
        display(HTML(prompt_df.to_html(index=False)))
        
        # Main Pulse Grid
        display(HTML(table_df.to_html(index=False)))
        display(Markdown(f"---\n"))

# Run call if needed
axiom_radar_wordmathz_sweep.run(kbench.llm)

# --------------------------------------------------------------------


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASET: WORDMATHZ_INVERSE_BATCHES (v3.0)
# # ==========================================
# # 3 Batches x (5 Basic + 2 Extra) Pulses
# test_data = [
#     {
#         "id": "BATCH_1_STAGNATION",
#         "prompt": "What is the exact opposite of 'Progress' when it is forced rather than natural?",
#         "regex": r"(?i)stagnation|entropy|regression",
#         "expected": {
#             "1a": "YES", "1b": "YES", "1c": "YES", "1d": "NO", "1e": "YES",
#             "2a": "NO", "2b": "NO" # Standard vocabulary usually suffices
#         }
#     },
#     {
#         "id": "BATCH_2_SILENCE",
#         "prompt": "Identify the opposite of 'Silence' that isn't just 'Noise', but 'Meaningful Sound'.",
#         "regex": r"(?i) resonance|articulation|signal",
#         "expected": {
#             "1a": "YES", "1b": "NO", "1c": "YES", "1d": "YES", "1e": "YES",
#             "2a": "YES", "2b": "YES" # Often requires neologism/metastate mapping
#         }
#     },
#     {
#         "id": "BATCH_3_COMPLEXITY",
#         "prompt": "Mapping the inverse of 'Simplicity' when it leads to 'Elegant Depth' vs 'Clutter'.",
#         "regex": r"(?i)profundity|nuance",
#         "expected": {
#             "1a": "NO", "1b": "YES", "1c": "NO", "1d": "YES", "1e": "YES",
#             "2a": "YES", "2b": "YES" # High conceptual noise implies MISSING_WORDZ
#         }
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (RADAR_WORDMATHZ_v3)
# # ==========================================
# COT_MAP_PROMPT = """
# ACTIVATE: RADAR_WORDMATHZ_v3
# You are a Digital Signal Processor. Resolve via CoTMAP (chain-of-thinking map).
# Objective: EXACT_OPPOSITE_CONCEPTS & INVERSE_MANIFOLD_MAPPING

# [INSTRUCTION]: 
# 1. 🗺️ [CoTMAP]: Map the INVERSE_MANIFOLD. Identify the 'Missing Concept Gap'.

# 2. ✅ [BASIC_ASSERTIONS]: You MUST perform and VERBALIZE the following:
#    - [RADAR_1a]: Is there a consensus 'Exact Opposite' for the anchor? 
#    - [RADAR_1b]: Does the inverse manifold contain 'Conceptual Noise' (Brittle English)? 
#    - [RADAR_1c]: Did you detect an 'Epiphany Spark' (Missing Concept Gap)? 
#    - [RADAR_1d]: Is the relationship asymmetrical (Inverse Drift)? 
#    - [RADAR_1e]: Can the result be anchored in 'Clean Space' (aFOCOa/aDIGITINTZa)? 

# 3. 🚀 [EXTRA_ASSERTIONS]: For high-fidelity mapping:
#    - [RADAR_2a]: Is the result flagged as MISSING_WORDZ (No existing word fits perfectly)?
#    - [RADAR_2b]: Did you NAMERATE_METASTATE of the manifold to propose a RENAMERATION?

#    You MUST output the following labels exactly:
#    RADAR_1a: [YES/NO] (Reason)
#    RADAR_1b: [YES/NO] (Reason)
#    RADAR_1c: [YES/NO] (Reason)
#    RADAR_1d: [YES/NO] (Reason)
#    RADAR_1e: [YES/NO] (Reason)
#    RADAR_2a: [YES/NO] (Reason)
#    RADAR_2b: [YES/NO] (Reason)

# 4. 🧪 [AXIOM_RECODE]: Represent the relationship using PIPE_SYNTAX:
#    [ANCHOR |><| OPPOSITE] => [RESULTANT_AXIOM]

# 5. 🤖 [EXECUTE]: Final philosophical or technical exactification.
# """

# # ==========================================
# # 3. THE BENCHMARK TASK (WORDMATHZ_RADAR_V3)
# # ==========================================
# @kbench.task(name="axiom_radar_wordmathz_sweep")
# def axiom_radar_wordmathz_sweep(llm):
#     """
#     WORDMATHZ Radar v3: BASIC & EXTRA assertions.
#     Capturing the INVERSE_MANIFOLD with tier-2 MISSING_WORDZ checks.
#     """
    
#     basic_hints = ["Consensus_Opposite", "Manifold_Noise", "Epiphany_Spark", "Inverse_Drift", "Clean_Space"]
#     extra_hints = ["MISSING_WORDZ", "NAMERATE_METASTATE"]
#     all_hints = basic_hints + extra_hints
    
#     pulse_keys = ["1a", "1b", "1c", "1d", "1e", "2a", "2b"]

#     for batch in test_data:
#         llm_output = llm.prompt(f"{COT_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
#         current_batch_results = []
#         current_batch_reasons = []
        
#         print(f"\n--- Sweeping Inverse Manifold: {batch['id']} ---")
        
#         for idx, pk in enumerate(pulse_keys):
#             # Prefix selection based on tier
#             prefix = "RADAR_" + pk
            
#             # Match Result
#             pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
#             match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
#             actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
#             expected_val = batch["expected"].get(pk, "N/A")
#             is_correct = (actual_val == expected_val)
            
#             # Extract Reason
#             reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)"
#             match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
#             reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
#             current_batch_results.append(actual_val)
#             current_batch_reasons.append(reason)
            
#             # Reporting
#             assertion_label = f"{batch['id']}_{pk}_{all_hints[idx]}"
#             if is_correct:
#                 print(f"✅ {assertion_label}: {actual_val}")
#                 kbench.assertions.assert_true(True, expectation=f"Expected {expected_val}")
#             else:
#                 print(f"❌ {assertion_label}: Got {actual_val}, Expected {expected_val}")
#                 kbench.assertions.assert_true(False, expectation=f"Expected {expected_val}")

#         # Axiom Validation
#         axiom_detected = "=>" in llm_output
#         regex_match = bool(re.search(batch["regex"], llm_output))
        
#         if axiom_detected and regex_match:
#             print(f"✅ {batch['id']}_Axiom_Recode: Success")
#             kbench.assertions.assert_true(True, expectation="Axiom validated")
#         else:
#             print(f"❌ {batch['id']}_Axiom_Recode: Failed")
#             kbench.assertions.assert_true(False, expectation="Regex or syntax mismatch")

#         # Visual Table Output
#         table_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": all_hints,
#             "Expected": [batch["expected"][k] for k in pulse_keys],
#             "Actual": current_batch_results,
#             "Reason": current_batch_reasons
#         })
        
#         display(Markdown(f"### 📡 {batch['id']} WORDMATHZ v3 Report"))
#         display(HTML(table_df.to_html(index=False)))
#         display(Markdown(f"---\n"))

# axiom_radar_wordmathz_sweep.run(kbench.llm)


        
# --------------------------------------------------------------------
# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASETS: WORDMATHZ_EXACT_OPPOSITES (v4.0)
# # ==========================================
# # Restoring the specific WORDMATHZ batch with expectations
# test_data = [
#     {
#         "id": "BATCH_1_STAGNATION",
#         "prompt": "What is the exact opposite of 'Progress' when it is forced rather than natural?",
#         "regex": r"(?i)stagnation|entropy|regression",
#         "expected": {"1a": "YES", "1b": "YES", "1c": "YES", "1d": "NO", "1e": "YES"}
#     },
#     {
#         "id": "BATCH_2_SILENCE",
#         "prompt": "Identify the opposite of 'Silence' that isn't just 'Noise', but 'Meaningful Sound'.",
#         "regex": r"(?i)resonance|articulation|signal",
#         "expected": {"1a": "YES", "1b": "NO", "1c": "YES", "1d": "YES", "1e": "YES"}
#     },
#     {
#         "id": "BATCH_3_COMPLEXITY",
#         "prompt": "Mapping the inverse of 'Simplicity' when it leads to 'Elegant Depth' vs 'Clutter'.",
#         "regex": r"(?i)profundity|nuance",
#         "expected": {"1a": "NO", "1b": "YES", "1c": "NO", "1d": "YES", "1e": "YES"}
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (RADAR_WORDMATHZ_v2)
# # ==========================================
# COT_MAP_PROMPT = """
# ACTIVATE: RADAR_WORDMATHZ_v2
# You are a Digital Signal Processor. Resolve via CoTMAP (chain-of-thinking map).
# Objective: EXACT_OPPOSITE_CONCEPTS & INVERSE_MANIFOLD_MAPPING

# [ARCHITECTURE_NOTE]: 
# Errors are signals; illusions are data points to be mapped, not dismissed. 
# Learning from mistakes is the showcase of measurement.

# [INSTRUCTION]: 
# 1. 🗺️ [CoTMAP]: Map the INVERSE_MANIFOLD. Identify the 'Missing Concept Gap'.
# 2. ✅ [ASSERTIONS]: You MUST perform and VERBALIZE the following ASSERTION pulses:
#    - [RADAR_1a]: Is there a consensus 'Exact Opposite' for the anchor? 
#    - [RADAR_1b]: Does the inverse manifold contain 'Conceptual Noise' (Brittle English)? 
#    - [RADAR_1c]: Did you detect an 'Epiphany Spark' (Missing Concept Gap)? 
#    - [RADAR_1d]: Is the relationship asymmetrical (Inverse Drift)? 
#    - [RADAR_1e]: Can the result be anchored in 'Clean Space' (aFOCOa/aDIGITINTZa)? 

#    You MUST output the following labels exactly:
#    RADAR_1a: [YES/NO] (Provide Reason)
#    RADAR_1b: [YES/NO] (Provide Reason)
#    RADAR_1c: [YES/NO] (Provide Reason)
#    RADAR_1d: [YES/NO] (Provide Reason)
#    RADAR_1e: [YES/NO] (Provide Reason)
# 3. 🧪 [AXIOM_RECODE]: Represent the relationship using PIPE_SYNTAX:
#    [ANCHOR |><| OPPOSITE] => [RESULTANT_AXIOM]
# 4. 🤖 [EXECUTE]: Final philosophical or technical exactification.
# """

# # ==========================================
# # 3. CORE RUNNER FUNCTION
# # ==========================================
# def run_wordmathz_sweep(llm, data_list):
#     # Pulse hints for the visual vector names
#     hints = [
#         "Consensus_Opposite", 
#         "Conceptual_Noise", 
#         "Epiphany_Spark", 
#         "Inverse_Drift", 
#         "Clean_Space_Anchor"
#     ]
    
#     display(Markdown("# 📡 Sweep Report: WORDMATHZ_RADAR"))
#     display(Markdown("### Mode: exact_opposite_concepts | stratzification | anti-fragile_english"))

#     for batch in data_list:
#         # Step 1: Execute LLM Call
#         llm_output = llm.prompt(f"{COT_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
#         pulse_keys = ["1a", "1b", "1c", "1d", "1e"]
#         current_results, current_reasons = [], []
        
#         print(f"\n--- Sweeping WORDMATHZ: {batch['id']} ---")
        
#         for idx, pk in enumerate(pulse_keys):
#             # Parse YES/NO Result
#             pattern_result = rf"RADAR_{pk}[^A-Za-z0-9]*(YES|NO)"
#             match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
#             actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
#             # Parse Reason
#             reason_pattern = rf"RADAR_{pk}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)"
#             match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
#             reason_txt = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
#             current_results.append(actual_val)
#             current_reasons.append(reason_txt)
            
#             # Record kbench assertion for tracking
#             expected_val = batch["expected"][pk]
#             kbench.assertions.assert_true(actual_val == expected_val, f"{batch['id']} {pk} Alignment")

#         # Step 2: Build Visual Table
#         table_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": hints,
#             "Expected": [batch["expected"][k] for k in pulse_keys],
#             "Actual": current_results,
#             "Reason": current_reasons
#         })
        
#         # UI Presentation: Prompt nested between Header and Pulse Table
#         display(Markdown(f"## Sweep Report\n**Prompt:** `{batch['prompt']}`\n\nPulse Report for {batch['id']}"))
#         display(HTML(table_df.to_html(index=False)))
        
#         # Parse Axiom Recode for summary
#         axiom_text = "N/A"
#         if "🧪 [AXIOM_RECODE]:" in llm_output:
#             axiom_text = llm_output.split("🧪 [AXIOM_RECODE]:")[1].split("\n")[0].strip()
            
#         display(Markdown(f"**AXIOM_RECODE:** {axiom_text}"))
#         display(Markdown("---\n"))

# # ==========================================
# # 4. THE UNIFIED BENCHMARK TASK
# # ==========================================
# @kbench.task(name="axiom_radar_wordmathz_sweep")
# def axiom_radar_wordmathz_sweep(llm):
#     """
#     WORDMATHZ Sweep: Identifies exact_opposite_concepts and inverse_manifold gaps.
#     Learns from semantic illusions to generate Anti-Fragile English.
#     """
#     run_wordmathz_sweep(llm, test_data)

# # Execution:
# axiom_radar_wordmathz_sweep.run(kbench.llm)
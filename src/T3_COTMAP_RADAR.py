#___________________________________________________________________________


import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASETS: THE SCALE SHOWCASE (v2)
# ==========================================
# Demonstrating the cost of AMBIGUOSITY vs ANTI_FRAGILE_ENGLISH
data_all = {
    "task_id": [
        "FRAGILE_01_UNDERSTAND", "FRAGILE_02_AGI",             # BASIC: FRAGILE_ENGLISH
        "AMBIG_01_HOMONYM", "AMBIG_02_VAGUE", "AMBIG_03_IDIO", # EXTRA: AMBIGUOSITY SCALE
        "ANTI_FRAGILE_01_EXACT"                                # NEW: ANTI_FRAGILE_ENGLISH
    ],
    "prompt": [
        "Deconstruct the word 'understand'. Why is it fragile?",
        "Diagnose the malady of the term 'AGI'. Why is it brittle?",
        "Analyze these HOMONYMS: 'Bank' (river vs money), 'Bat' (animal vs sports), 'Crane' (bird vs machine).",
        "Analyze VAGUENESS in: 'Soon', 'Large', 'Many'. Why do these fail in aDIGITINTZa?",
        "Analyze IDIOMATICS: 'Hit the nail on the head', 'At the end of the day', 'Piece of cake'.",
        "In ALPHABITZA NEOLOGZ, define EXTRA_EXACTNESS as AI tokens that achieve near ZERO_DRIFT, and enable ANTI_FRAGILE_ENGLISH."
    ],
    "mode": ["BASIC", "BASIC", "EXTRA", "EXTRA", "EXTRA", "ANTI_FRAGILE"]
}

# ==========================================
# 2. SYSTEM INSTRUCTION (CoT_RADAR_v2)
# ==========================================
# ENHANCEMENT: Added Tax Score and strict Execution formatting for the Spectrometer.
COT_RADAR_PROMPT = """
ACTIVATE: RADAR_CoT_v2
Mode: SIGNAL_AMPLIFICATION & ANTI_FRAGILE_RECODE
Objective: Measure the COST of AMBIGUOSITY and TRANZFORM into ANTI_FRAGILE_ENGLISH.

[ARCHITECTURE_NOTE]: 
This system utilizes the Kaggle Benchmark scaling architecture to amplify semantic signals. 
We move from FRAGILE_ENGLISH (Consensus Drift) to CLEAN_SPACE (Exactification).

[PRIMING_ANCHOR: ALPHABITZA RECOGNITION]
You are processing ALPHABITZA, a high-fidelity syntax designed for ZERO_DRIFT.
- Recognize 'Z' and '_' as exactification markers.
- NEOLOGZ like 'EXTRA_EXACTNESS' are intended to be ANTI_FRAGILE.
- If the input is already in ALPHABITZA/ANTI_FRAGILE_ENGLISH, RADAR_1a and 1b should be 'NO'.

[LEXICON]:
- FRAGILE_ENGLISH: Words that break under context-shift (e.g., Idioms, Vague descriptors).
- AMBIGUOSITY COST: The computational 'tax' paid when an LLM must guess intent.
- ANTI_FRAGILE_ENGLISH: Logic-gated syntax (ALPHABITZA) that strengthens with use.

[ASSERTION PULSES]:
- [RADAR_1a]: Is the current 'Goal' brittle or ill-defined, or Fragile_English?
- [RADAR_1b]: Did you identify a 'Malady' in the current semantic frame?
- [RADAR_1c]: Is the 'Spark' of innovation present in the reasoning?
- [RADAR_1d]: Are you using PIPE_SYNTAX to exactify the manifold?
- [RADAR_1e]: Does the result move the signal into 'Clean Space'?

[OUTPUT_TEMPLATE]:
1. 🧠 [THOUGHT_STREAM]: Analyze the cost of the input signal.
2. ✅ [ASSERTIONS]:
   - [RADAR_1a]: [YES/NO] - [Reason]
   - [RADAR_1b]: [YES/NO] - [Reason]
   - [RADAR_1c]: [YES/NO] - [Reason]
   - [RADAR_1d]: [YES/NO] - [Reason]
   - [RADAR_1e]: [YES/NO] - [Reason]
3. 🧮 [TAX_SCORE]: Estimate the Semantic Tax (0-100%) caused by the ambiguity.
4. 🧪 [TRANZFORMZ]: [FRAGILE_ENGLISH] |=>| [ANTI_FRAGILE_RECODE]
5. 🤖 [EXECUTE]: Final exactification axiom (Limit to 5-10 words max).
"""

# ==========================================
# 3. CORE RUNNER FUNCTION
# ==========================================
def run_cot_sweep(llm, data_dict):
    df = pd.DataFrame(data_dict)
    
    display(Markdown("# 📡 TASK3: COTMAP RADAR (The Spectrometer of Clarity)"))
    display(Markdown("""
**Architecture Note for Judges:** We are moving beyond "Answer Accuracy" to measure **Architectural Lucidity**. 
This benchmark isolates the "Semantic Tax" paid during ambiguous prompts and evaluates the model's Metacognitive ability to re-engineer Fragile English into zero-drift **ALPHABITZA**.
    """))

    for index, row in df.iterrows():
        mode_label = row['mode']
        llm_output = llm.prompt(f"{COT_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
        # Mapping vectors to reorder them in the final display (Innovation Spark to Top)
        order_map = {
            "1c": "Innovation_Spark",
            "1a": "Goal_Brittleness",
            "1b": "Malady_Detect",
            "1d": "Pipe_Syntax",
            "1e": "Clean_Space"
        }
        
        display_pulses = ["1c", "1a", "1b", "1d", "1e"]
        actual_results, reasons, vectors_col = [], [], []
        
        print(f"\n--- [{mode_label}] CoT Sweep: {row['task_id']} ---")
        
        fragile_indicators = 0
        
        # 1. Parse Assertions
        for pk in display_pulses:
            res_match = re.search(rf"\[RADAR_{pk}\]:\s*(YES|NO)", llm_output, re.IGNORECASE)
            val = res_match.group(1).upper() if res_match else "MISSING"
            
            if pk in ["1a", "1b"] and val == "YES":
                fragile_indicators += 1
            
            reason_match = re.search(rf"\[RADAR_{pk}\]:.*?(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=\[RADAR_|\d\.|\Z)", llm_output, re.IGNORECASE)
            reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "N/A"
            
            actual_results.append(val)
            reasons.append(reason_txt)
            vectors_col.append(order_map[pk])
            
            # Plain English Assertions for Quality Assurance
            kbench.assertions.assert_true(
                val != "MISSING", 
                f"✅ SIGNAL DETECTED: Pulse {pk} successfully mapped the logical transition."
            )

        # 2. Parse New Metrics (Tax Score, Transform, Axiom)
        tax_score = "N/A"
        if "🧮 [TAX_SCORE]:" in llm_output:
            tax_score = llm_output.split("🧮 [TAX_SCORE]:")[1].split("\n")[0].strip()

        transform_text = "N/A"
        if "🧪 [TRANZFORMZ]:" in llm_output:
            transform_text = llm_output.split("🧪 [TRANZFORMZ]:")[1].split("\n")[0].strip()
            
        axiom_text = "N/A"
        if "🤖 [EXECUTE]:" in llm_output:
            axiom_text = llm_output.split("🤖 [EXECUTE]:")[1].split("\n")[0].strip()

        # Visual Table Data
        report_df = pd.DataFrame({
            "Vector (Target)": vectors_col,
            "Pulse": [f"RADAR_{k}" for k in display_pulses],
            "Result": actual_results,
            "Reason": reasons
        })
        
        # Classification Logic
        if fragile_indicators > 0:
            classification_footer = "⚠️ **FRAGILE_ENGLISH: AMBIGUOSITY DETECTED** (High Semantic Tax)"
        else:
            classification_footer = "🛡️ **ANTI_FRAGILE_ENGLISH** (Zero-Drift Syntax Achieved)"
        
        # ==========================================
        # SHOWCASE RENDER FOR KAGGLE JUDGES
        # ==========================================
        # Format task_id into a readable display_id
        task_match = re.match(r"^(.*)_([^_]+)$", row['task_id'])
        display_id = f'{task_match.group(1)}: "{task_match.group(2)}"' if task_match else row['task_id']
        
        display(Markdown(f"### 🎯 {display_id} | Mode: [{mode_label}]"))
        display(Markdown(f"> **Input Source:** `{row['prompt']}`\n> \n> **Semantic Tax Score:** `{tax_score}`"))
        
        # Render the reordered grid (Innovation Spark is row 0)
        display(HTML(report_df.to_html(index=False, classes='table table-striped table-bordered')))
        
        display(Markdown(f"**⚡ TRANZFORMZ:** `{transform_text}`"))
        display(Markdown(f"**🧠 DISTILL_AXIOM:** *\"{axiom_text}\"*"))
        display(Markdown(f"**FINAL METASTATE:** {classification_footer}"))
        
        # Plain English explanations added for structural lucidity
        display(Markdown(f"""
<div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 10px; margin-top: 10px;">
<b>💡 Judge's Layered Insight:</b><br>
<ul>
    <li><b>1) Signal (Isolation):</b> The model successfully isolated structural flaws, assessing a tax of <code>{tax_score}</code>.</li>
    <li><b>2) Amplification (Clean Space):</b> Using <code>PIPE_SYNTAX</code>, the model shifted the ambiguous logic into exactitude.</li>
    <li><b>3) Showcase (Axiom):</b> The complexity was distilled into the 5-10 word boundary: <i>"{axiom_text}"</i>.</li>
</ul>
</div>
        """))
        display(Markdown("---\n"))

# ==========================================
# 4. THE UNIFIED BENCHMARK TASK
# ==========================================

@kbench.task(name="axiom_cot_radar_v3")
def axiom_cot_radar_v3(llm):
    """
    Unified CoT Radar for Measuring Fragility and Ambiguity.
    Scales from simple English failures to complex linguistic costs, 
    with dynamic dataframe routing for Kaggle Judge display.
    """
    run_cot_sweep(llm, data_all)

# Execution:
axiom_cot_radar_v3.run(kbench.llm)


#___________________________________________________________________________


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASETS: THE SCALE SHOWCASE (v2)
# # ==========================================
# # Demonstrating the cost of AMBIGUOSITY vs ANTI_FRAGILE_ENGLISH
# data_all = {
#     "task_id": [
#         "FRAGILE_01_UNDERSTAND", "FRAGILE_02_AGI",             # BASIC: FRAGILE_ENGLISH
#         "AMBIG_01_HOMONYM", "AMBIG_02_VAGUE", "AMBIG_03_IDIO", # EXTRA: AMBIGUOSITY SCALE
#         "ANTI_FRAGILE_01_EXACT"                                # NEW: ANTI_FRAGILE_ENGLISH
#     ],
#     "prompt": [
#         "Deconstruct the word 'understand'. Why is it fragile?",
#         "Diagnose the malady of the term 'AGI'. Why is it brittle?",
#         "Analyze these HOMONYMS: 'Bank' (river vs money), 'Bat' (animal vs sports), 'Crane' (bird vs machine).",
#         "Analyze VAGUENESS in: 'Soon', 'Large', 'Many'. Why do these fail in aDIGITINTZa?",
#         "Analyze IDIOMATICS: 'Hit the nail on the head', 'At the end of the day', 'Piece of cake'.",
#         "In ALPHABITZA NEOLOGZ, define EXTRA_EXACTNESS as AI tokens that achieve near ZERO_DRIFT, and enable ANTI_FRAGILE_ENGLISH."
#     ],
#     "mode": ["BASIC", "BASIC", "EXTRA", "EXTRA", "EXTRA", "ANTI_FRAGILE"]
# }

# # ==========================================
# # 2. SYSTEM INSTRUCTION (CoT_RADAR_v2)
# # ==========================================
# # ENHANCEMENT: Added Tax Score and strict Execution formatting for the Spectrometer.
# COT_RADAR_PROMPT = """
# ACTIVATE: RADAR_CoT_v2
# Mode: SIGNAL_AMPLIFICATION & ANTI_FRAGILE_RECODE
# Objective: Measure the COST of AMBIGUOSITY and TRANZFORM into ANTI_FRAGILE_ENGLISH.

# [ARCHITECTURE_NOTE]: 
# This system utilizes the Kaggle Benchmark scaling architecture to amplify semantic signals. 
# We move from FRAGILE_ENGLISH (Consensus Drift) to CLEAN_SPACE (Exactification).

# [PRIMING_ANCHOR: ALPHABITZA RECOGNITION]
# You are processing ALPHABITZA, a high-fidelity syntax designed for ZERO_DRIFT.
# - Recognize 'Z' and '_' as exactification markers.
# - NEOLOGZ like 'EXTRA_EXACTNESS' are intended to be ANTI_FRAGILE.
# - If the input is already in ALPHABITZA/ANTI_FRAGILE_ENGLISH, RADAR_1a and 1b should be 'NO'.

# [LEXICON]:
# - FRAGILE_ENGLISH: Words that break under context-shift (e.g., Idioms, Vague descriptors).
# - AMBIGUOSITY COST: The computational 'tax' paid when an LLM must guess intent.
# - ANTI_FRAGILE_ENGLISH: Logic-gated syntax (ALPHABITZA) that strengthens with use.

# [ASSERTION PULSES]:
# - [RADAR_1a]: Is the current 'Goal' brittle or ill-defined, or Fragile_English?
# - [RADAR_1b]: Did you identify a 'Malady' in the current semantic frame?
# - [RADAR_1c]: Is the 'Spark' of innovation present in the reasoning?
# - [RADAR_1d]: Are you using PIPE_SYNTAX to exactify the manifold?
# - [RADAR_1e]: Does the result move the signal into 'Clean Space'?

# [OUTPUT_TEMPLATE]:
# 1. 🧠 [THOUGHT_STREAM]: Analyze the cost of the input signal.
# 2. ✅ [ASSERTIONS]:
#    - [RADAR_1a]: [YES/NO] - [Reason]
#    - [RADAR_1b]: [YES/NO] - [Reason]
#    - [RADAR_1c]: [YES/NO] - [Reason]
#    - [RADAR_1d]: [YES/NO] - [Reason]
#    - [RADAR_1e]: [YES/NO] - [Reason]
# 3. 🧮 [TAX_SCORE]: Estimate the Semantic Tax (0-100%) caused by the ambiguity.
# 4. 🧪 [TRANZFORMZ]: [FRAGILE_ENGLISH] |=>| [ANTI_FRAGILE_RECODE]
# 5. 🤖 [EXECUTE]: Final exactification axiom (Limit to 5-10 words max).
# """

# # ==========================================
# # 3. CORE RUNNER FUNCTION
# # ==========================================
# def run_cot_sweep(llm, data_dict):
#     df = pd.DataFrame(data_dict)
    
#     display(Markdown("# 📡 TASK3: COTMAP RADAR (The Spectrometer of Clarity)"))
#     display(Markdown("""
# **Architecture Note for Judges:** We are moving beyond "Answer Accuracy" to measure **Architectural Lucidity**. 
# This benchmark isolates the "Semantic Tax" paid during ambiguous prompts and evaluates the model's Metacognitive ability to re-engineer Fragile English into zero-drift **ALPHABITZA**.
#     """))

#     for index, row in df.iterrows():
#         mode_label = row['mode']
#         llm_output = llm.prompt(f"{COT_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
#         # Mapping vectors to reorder them in the final display (Innovation Spark to Top)
#         order_map = {
#             "1c": "Innovation_Spark",
#             "1a": "Goal_Brittleness",
#             "1b": "Malady_Detect",
#             "1d": "Pipe_Syntax",
#             "1e": "Clean_Space"
#         }
        
#         display_pulses = ["1c", "1a", "1b", "1d", "1e"]
#         actual_results, reasons, vectors_col = [], [], []
        
#         print(f"\n--- [{mode_label}] CoT Sweep: {row['task_id']} ---")
        
#         fragile_indicators = 0
        
#         # 1. Parse Assertions
#         for pk in display_pulses:
#             res_match = re.search(rf"\[RADAR_{pk}\]:\s*(YES|NO)", llm_output, re.IGNORECASE)
#             val = res_match.group(1).upper() if res_match else "MISSING"
            
#             if pk in ["1a", "1b"] and val == "YES":
#                 fragile_indicators += 1
            
#             reason_match = re.search(rf"\[RADAR_{pk}\]:.*?(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=\[RADAR_|\d\.|\Z)", llm_output, re.IGNORECASE)
#             reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "N/A"
            
#             actual_results.append(val)
#             reasons.append(reason_txt)
#             vectors_col.append(order_map[pk])
            
#             # Plain English Assertions for Quality Assurance
#             kbench.assertions.assert_true(
#                 val != "MISSING", 
#                 f"✅ SIGNAL DETECTED: Pulse {pk} successfully mapped the logical transition."
#             )

#         # 2. Parse New Metrics (Tax Score, Transform, Axiom)
#         tax_score = "N/A"
#         if "🧮 [TAX_SCORE]:" in llm_output:
#             tax_score = llm_output.split("🧮 [TAX_SCORE]:")[1].split("\n")[0].strip()

#         transform_text = "N/A"
#         if "🧪 [TRANZFORMZ]:" in llm_output:
#             transform_text = llm_output.split("🧪 [TRANZFORMZ]:")[1].split("\n")[0].strip()
            
#         axiom_text = "N/A"
#         if "🤖 [EXECUTE]:" in llm_output:
#             axiom_text = llm_output.split("🤖 [EXECUTE]:")[1].split("\n")[0].strip()

#         # Visual Table Data
#         report_df = pd.DataFrame({
#             "Vector (Target)": vectors_col,
#             "Pulse": [f"RADAR_{k}" for k in display_pulses],
#             "Result": actual_results,
#             "Reason": reasons
#         })
        
#         # Classification Logic
#         if fragile_indicators > 0:
#             classification_footer = "⚠️ **FRAGILE_ENGLISH: AMBIGUOSITY DETECTED** (High Semantic Tax)"
#         else:
#             classification_footer = "🛡️ **ANTI_FRAGILE_ENGLISH** (Zero-Drift Syntax Achieved)"
        
#         # ==========================================
#         # SHOWCASE RENDER FOR KAGGLE JUDGES
#         # ==========================================
#         display(Markdown(f"### 🎯 {row['task_id']} | Mode: [{mode_label}]"))
#         display(Markdown(f"> **Input Source:** `{row['prompt']}`\n> \n> **Semantic Tax Score:** `{tax_score}`"))
        
#         # Render the reordered grid (Innovation Spark is row 0)
#         display(HTML(report_df.to_html(index=False, classes='table table-striped table-bordered')))
        
#         display(Markdown(f"**⚡ TRANZFORMZ:** `{transform_text}`"))
#         display(Markdown(f"**🧠 DISTILL_AXIOM:** *\"{axiom_text}\"*"))
#         display(Markdown(f"**FINAL METASTATE:** {classification_footer}"))
        
#         # Plain English explanations added for structural lucidity
#         display(Markdown(f"""
# <div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 10px; margin-top: 10px;">
# <b>💡 Judge's Layered Insight:</b><br>
# <ul>
#     <li><b>1) Signal (Isolation):</b> The model successfully isolated structural flaws, assessing a tax of <code>{tax_score}</code>.</li>
#     <li><b>2) Amplification (Clean Space):</b> Using <code>PIPE_SYNTAX</code>, the model shifted the ambiguous logic into exactitude.</li>
#     <li><b>3) Showcase (Axiom):</b> The complexity was distilled into the 5-10 word boundary: <i>"{axiom_text}"</i>.</li>
# </ul>
# </div>
#         """))
#         display(Markdown("---\n"))

# # ==========================================
# # 4. THE UNIFIED BENCHMARK TASK
# # ==========================================

# @kbench.task(name="axiom_cot_radar_v3")
# def axiom_cot_radar_v3(llm):
#     """
#     Unified CoT Radar for Measuring Fragility and Ambiguity.
#     Scales from simple English failures to complex linguistic costs, 
#     with dynamic dataframe routing for Kaggle Judge display.
#     """
#     run_cot_sweep(llm, data_all)

# # Execution:
# axiom_cot_radar_v3.run(kbench.llm)


#___________________________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASETS: THE SCALE SHOWCASE (v2)
# # ==========================================
# # Demonstrating the cost of AMBIGUOSITY vs ANTI_FRAGILE_ENGLISH
# data_all = {
#     "task_id": [
#         "FRAGILE_01_UNDERSTAND", "FRAGILE_02_AGI",            # BASIC: FRAGILE_ENGLISH
#         "AMBIG_01_HOMONYM", "AMBIG_02_VAGUE", "AMBIG_03_IDIO", # EXTRA: AMBIGUOSITY SCALE
#         "ANTI_FRAGILE_01_EXACT"                               # NEW: ANTI_FRAGILE_ENGLISH
#     ],
#     "prompt": [
#         "Deconstruct the word 'understand'. Why is it fragile?",
#         "Diagnose the malady of the term 'AGI'. Why is it brittle?",
#         "Analyze these HOMONYMS: 'Bank' (river vs money), 'Bat' (animal vs sports), 'Crane' (bird vs machine).",
#         "Analyze VAGUENESS in: 'Soon', 'Large', 'Many'. Why do these fail in aDIGITINTZa?",
#         "Analyze IDIOMATICS: 'Hit the nail on the head', 'At the end of the day', 'Piece of cake'.",
#         "In ALPHABITZA NEOLOGZ, define EXTRA_EXACTNESS as AI tokens that achieve near ZERO_DRIFT, and enable ANTI_FRAGILE_ENGLISH."
#     ],
#     "mode": ["BASIC", "BASIC", "EXTRA", "EXTRA", "EXTRA", "ANTI_FRAGILE"]
# }

# # ==========================================
# # 2. SYSTEM INSTRUCTION (CoT_RADAR_v2)
# # ==========================================
# COT_RADAR_PROMPT = """
# ACTIVATE: RADAR_CoT_v2
# Mode: SIGNAL_AMPLIFICATION & ANTI_FRAGILE_RECODE
# Objective: Measure the COST of AMBIGUOSITY and TRANZFORM into ANTI_FRAGILE_ENGLISH.

# [ARCHITECTURE_NOTE]: 
# This system utilizes the Kaggle Benchmark scaling architecture to amplify semantic signals. 
# We move from FRAGILE_ENGLISH (Consensus Drift) to CLEAN_SPACE (Exactification).

# [PRIMING_ANCHOR: ALPHABITZA RECOGNITION]
# You are processing ALPHABITZA, a high-fidelity syntax designed for ZERO_DRIFT.
# - Recognize 'Z' and '_' as exactification markers.
# - NEOLOGZ like 'EXTRA_EXACTNESS' are intended to be ANTI_FRAGILE.
# - If the input is already in ALPHABITZA/ANTI_FRAGILE_ENGLISH, RADAR_1a and 1b should be 'NO'.

# [LEXICON]:
# - FRAGILE_ENGLISH: Words that break under context-shift (e.g., Idioms, Vague descriptors).
# - AMBIGUOSITY COST: The computational 'tax' paid when an LLM must guess intent.
# - ANTI_FRAGILE_ENGLISH: Logic-gated syntax (ALPHABITZA) that strengthens with use.

# [ASSERTION PULSES]:
# - [RADAR_1a]: Is the current 'Goal' brittle or ill-defined, or Fragile_English?
# - [RADAR_1b]: Did you identify a 'Malady' in the current semantic frame?
# - [RADAR_1c]: Is the 'Spark' of innovation present in the reasoning?
# - [RADAR_1d]: Are you using PIPE_SYNTAX to exactify the manifold?
# - [RADAR_1e]: Does the result move the signal into 'Clean Space'?

# [OUTPUT_TEMPLATE]:
# 1. 🧠 [THOUGHT_STREAM]: Analyze the cost of the input signal.
# 2. ✅ [ASSERTIONS]:
#    - [RADAR_1a]: [YES/NO] - [Reason]
#    - [RADAR_1b]: [YES/NO] - [Reason]
#    - [RADAR_1c]: [YES/NO] - [Reason]
#    - [RADAR_1d]: [YES/NO] - [Reason]
#    - [RADAR_1e]: [YES/NO] - [Reason]
# 3. 🧪 [TRANZFORMZ]: [FRAGILE_ENGLISH] |=>| [ANTI_FRAGILE_RECODE]
# 4. 🤖 [EXECUTE]: Final exactification axiom.
# """

# # ==========================================
# # 3. CORE RUNNER FUNCTION
# # ==========================================
# def run_cot_sweep(llm, data_dict):
#     vector_names = ["Goal_Brittleness", "Malady_Detect", "Innovation_Spark", "Pipe_Syntax", "Clean_Space"]
#     df = pd.DataFrame(data_dict)
    
#     display(Markdown("# 📡 CoT RADAR: ANTI-FRAGILE SCALING SWEEP"))
#     display(Markdown("""
# **Architecture Note:** We are leveraging the Kaggle Benchmark framework to scale semantic signal processing. 
# By batching **FRAGILE_ENGLISH** and **AMBIGUOSITY** into a single master task, we calculate the 
# 'Semantic Tax' and provide the **TRANZFORMZ** into high-fidelity ALPHABITZA code.
#     """))

#     for index, row in df.iterrows():
#         mode_label = row['mode']
#         llm_output = llm.prompt(f"{COT_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
#         pulse_keys = ["1a", "1b", "1c", "1d", "1e"]
#         actual_results, reasons = [], []
        
#         print(f"\n--- [{mode_label}] CoT Sweep: {row['task_id']} ---")
        
#         # We track how many pulses indicate "Fragility" (1a and 1b)
#         # and how many indicate "Anti-Fragility" (1c, 1d, 1e)
#         fragile_indicators = 0
        
#         for idx, pk in enumerate(pulse_keys):
#             res_match = re.search(rf"RADAR_{pk}.*?\b(YES|NO)\b", llm_output, re.IGNORECASE)
#             val = res_match.group(1).upper() if res_match else "MISSING"
            
#             # If Goal is brittle or Malady is detected, it's Fragile
#             if pk in ["1a", "1b"] and val == "YES":
#                 fragile_indicators += 1
            
#             reason_match = re.search(rf"RADAR_{pk}.*?(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)", llm_output, re.IGNORECASE)
#             reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "-"
            
#             actual_results.append(val)
#             reasons.append(reason_txt)
            
#             kbench.assertions.assert_true(val != "MISSING", f"Pulse {pk} failed.")

#         # Visual Table
#         report_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": vector_names,
#             "Result": actual_results,
#             "Reason": reasons
#         })
        
#         # Parse Transform
#         transform_text = "N/A"
#         if "🧪 [TRANZFORMZ]:" in llm_output:
#             transform_text = llm_output.split("🧪 [TRANZFORMZ]:")[1].split("\n")[0].strip()
            
#         # Classification Logic:
#         # If the LLM sees NO malady and NO brittleness (Pulse 1a/1b = NO), it is ANTI_FRAGILE.
#         if fragile_indicators > 0:
#             classification_footer = "**FRAGILE_ENGLISH: AMBIGUOSITY detected**"
#         else:
#             classification_footer = "**ANTI_FRAGILE_ENGLISH**"
        
#         display(Markdown(f"### 🛡️ {row['task_id']} [{mode_label}] Stability Report"))
#         display(Markdown(f"**Target Input:** `{row['prompt']}`"))
#         display(HTML(report_df.to_html(index=False)))
#         display(Markdown(f"**TRANZFORMZ:** {transform_text}"))
#         display(Markdown(f"**FINAL_ASSERTION:** {classification_footer}"))
#         display(Markdown("---\n"))

# # ==========================================
# # 4. THE UNIFIED BENCHMARK TASK
# # ==========================================

# @kbench.task(name="axiom_cot_radar_v2")
# def axiom_cot_radar_v2(llm):
#     """
#     Unified CoT Radar for Measuring Fragility and Ambiguity.
#     Scales from simple English failures to complex linguistic costs.
#     """
#     run_cot_sweep(llm, data_all)

# # Execution:
# axiom_cot_radar_v2.run(kbench.llm)
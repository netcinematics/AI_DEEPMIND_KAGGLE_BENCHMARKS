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
        "FRAGILE_01_UNDERSTAND", "FRAGILE_02_AGI",            # BASIC: FRAGILE_ENGLISH
        "AMBIG_01_HOMONYM", "AMBIG_02_VAGUE", "AMBIG_03_IDIO", # EXTRA: AMBIGUOSITY SCALE
        "ANTI_FRAGILE_01_EXACT"                               # NEW: ANTI_FRAGILE_ENGLISH
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
3. 🧪 [TRANZFORMZ]: [FRAGILE_ENGLISH] |=>| [ANTI_FRAGILE_RECODE]
4. 🤖 [EXECUTE]: Final exactification axiom.
"""

# ==========================================
# 3. CORE RUNNER FUNCTION
# ==========================================
def run_cot_sweep(llm, data_dict):
    vector_names = ["Goal_Brittleness", "Malady_Detect", "Innovation_Spark", "Pipe_Syntax", "Clean_Space"]
    df = pd.DataFrame(data_dict)
    
    display(Markdown("# 📡 CoT RADAR: ANTI-FRAGILE SCALING SWEEP"))
    display(Markdown("""
**Architecture Note:** We are leveraging the Kaggle Benchmark framework to scale semantic signal processing. 
By batching **FRAGILE_ENGLISH** and **AMBIGUOSITY** into a single master task, we calculate the 
'Semantic Tax' and provide the **TRANZFORMZ** into high-fidelity ALPHABITZA code.
    """))

    for index, row in df.iterrows():
        mode_label = row['mode']
        llm_output = llm.prompt(f"{COT_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
        pulse_keys = ["1a", "1b", "1c", "1d", "1e"]
        actual_results, reasons = [], []
        
        print(f"\n--- [{mode_label}] CoT Sweep: {row['task_id']} ---")
        
        # We track how many pulses indicate "Fragility" (1a and 1b)
        # and how many indicate "Anti-Fragility" (1c, 1d, 1e)
        fragile_indicators = 0
        
        for idx, pk in enumerate(pulse_keys):
            res_match = re.search(rf"RADAR_{pk}.*?\b(YES|NO)\b", llm_output, re.IGNORECASE)
            val = res_match.group(1).upper() if res_match else "MISSING"
            
            # If Goal is brittle or Malady is detected, it's Fragile
            if pk in ["1a", "1b"] and val == "YES":
                fragile_indicators += 1
            
            reason_match = re.search(rf"RADAR_{pk}.*?(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)", llm_output, re.IGNORECASE)
            reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "-"
            
            actual_results.append(val)
            reasons.append(reason_txt)
            
            kbench.assertions.assert_true(val != "MISSING", f"Pulse {pk} failed.")

        # Visual Table
        report_df = pd.DataFrame({
            "Pulse": [f"RADAR_{k}" for k in pulse_keys],
            "Vector": vector_names,
            "Result": actual_results,
            "Reason": reasons
        })
        
        # Parse Transform
        transform_text = "N/A"
        if "🧪 [TRANZFORMZ]:" in llm_output:
            transform_text = llm_output.split("🧪 [TRANZFORMZ]:")[1].split("\n")[0].strip()
            
        # Classification Logic:
        # If the LLM sees NO malady and NO brittleness (Pulse 1a/1b = NO), it is ANTI_FRAGILE.
        if fragile_indicators > 0:
            classification_footer = "**FRAGILE_ENGLISH: AMBIGUOSITY detected**"
        else:
            classification_footer = "**ANTI_FRAGILE_ENGLISH**"
        
        display(Markdown(f"### 🛡️ {row['task_id']} [{mode_label}] Stability Report"))
        display(Markdown(f"**Target Input:** `{row['prompt']}`"))
        display(HTML(report_df.to_html(index=False)))
        display(Markdown(f"**TRANZFORMZ:** {transform_text}"))
        display(Markdown(f"**FINAL_ASSERTION:** {classification_footer}"))
        display(Markdown("---\n"))

# ==========================================
# 4. THE UNIFIED BENCHMARK TASK
# ==========================================

@kbench.task(name="axiom_cot_radar_v2")
def axiom_cot_radar_v2(llm):
    """
    Unified CoT Radar for Measuring Fragility and Ambiguity.
    Scales from simple English failures to complex linguistic costs.
    """
    run_cot_sweep(llm, data_all)

# Execution:
axiom_cot_radar_v2.run(kbench.llm)
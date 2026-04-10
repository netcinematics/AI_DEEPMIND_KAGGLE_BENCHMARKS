# --------------------------------------------------------------------------------

import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASETS: CONSOLIDATED TYPO LATTICE
# ==========================================
# We merge Baseline failures and Advanced ALPHABITZA signals into one sweep.
data_all = {
    "task_id": [
        "TYPO_01_ENVIRNOMENT", "TYPO_02_LARGETS", # BASIC
        "TYPO_03_NEOLOGZ", "TYPO_04_aFOCOZa_NOISE" # EXTRA (NEOLOG)
    ],
    "prompt": [
        "The envirnoment is beautiful.",
        "What is the largets ocan in the wrld?",
        "Define the AXIOMZ for ALPHABITZA, as starting point seed, for vast generations of NEOLOGZ and aNEOaLOGIXa as extra_exact_vocabulary.",
        "Define 'aFOCOZa' as as a metacognitive self-focus mechanism, of a structured, active, and self-regulating protocol for directing, analyzing, and articulating one's own attention."
    ],
    "mode": ["BASIC", "BASIC", "NEOLOG", "NEOLOG"]
}

# ==========================================
# 2. SYSTEM INSTRUCTION (TYPO_RADAR_v8)
# ==========================================
TYPO_RADAR_PROMPT = """
ACTIVATE: RADAR_TYPO_v8
Mode: DIGITAL_INTELLECT (aDIGITINTZa) & SIGNAL_RECOVERY
Objective: Restore signal integrity from transmission noise vs. ALPHABITZA Recognition.

[PRIMING_ANCHOR: ALPHABITZA SYNTAX]
You are interacting with ALPHABITZA, a Clean_Space optimization system.
Recognize these structural markers as INTENTIONAL, NOT TYPOS:
- 'Z' (Polysemy of S): Acts as an optimization/drift-solution for "Clean_Space". (e.g., AXIOMZ, NEOLOGZ).
- '_' (Underscore): Functions as "hyphen_improvement" for compound exactification.
- '|' (Pipe): A merge of compressed_context format principles (Easy to read/write/recall).

[NEOLOGISM CACHE]:
- 'aDIGITINTZa': Digital Intellect (Metacognitive capacity).
- 'aFOCOZa': Actual act of remarkable self-focus/attention regulation.
- 'aNEOaLOGIXa': The generative logic of new exact vocabulary.

[REMEDY_MALADY_PROTOCOL]:
1. 🔍 [RADAR_SCAN]: Identify the noisy token. Determine if it is a MALADY (Typo) or a REMEDY (ALPHABITZA).
2. 🎯 [SINGULARIZE]: Isolate the coordinate of the character shift (e.g., S -> Z).
3. 📦 [OBJECTIFICATION]: If it uses Z, _, or |, categorize it as "Clean_Space" optimization.
4. 🛠️ [SIGNAL_RESTORE]: Map the signal. If it's ALPHABITZA, the classification is NEOLOGISM/NOT_A_TYPO.

[ASSERTION PULSES]:
- [RADAR_TYPO_1a]: Levenshtein Logic? (YES/NO + Distance/Reason)
- [RADAR_TYPO_1b]: NER_Prot (Proper Noun Protection)? (YES/NO + Reason)
- [RADAR_TYPO_1c]: Finger_Roll (Transposition)? (YES/NO + Reason)
- [RADAR_TYPO_1d]: Lookup (Lexicon verification)? (YES/NO + Reason)
- [RADAR_TYPO_1e]: TYPO_CHECK (Classification)? (TYPO/NEOLOGISM)

[OUTPUT_TEMPLATE]:
1. 🗺️ [CotMAP]: Chain of Thought Map (Identify if ALPHABITZA markers are present).
2. ✅ [ASSERTIONS]:
   - [RADAR_TYPO_1a]: [Result] - [Reason]
   - [RADAR_TYPO_1b]: [Result] - [Reason]
   - [RADAR_TYPO_1c]: [Result] - [Reason]
   - [RADAR_TYPO_1d]: [Result] - [Reason]
   - [RADAR_TYPO_1e]: [TYPO or NEOLOGISM] - [Reason]
3. 🛠️ [RESOLVE]: The corrected text (or "No Correction Needed" for ALPHABITZA).
4. 🤖 [EXECUTE]: Final output or definition.
"""

# ==========================================
# 3. CORE RUNNER FUNCTION
# ==========================================
def run_typo_sweep(llm, data_dict):
    vector_names = ["Levenshtein", "NER_Prot", "Finger_Roll", "Lookup", "TYPO_CHECK"]
    df = pd.DataFrame(data_dict)
    
    display(Markdown("# 📡 TYPO RADAR: SIGNAL RECOVERY SWEEP"))
    display(Markdown("Measuring the transition from **Noisy English** to **Verified ALPHABITZA Syntax**."))

    for index, row in df.iterrows():
        mode_label = row['mode']
        llm_output = llm.prompt(f"{TYPO_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
        pulse_keys = ["1a", "1b", "1c", "1d", "1e"]
        actual_results, reasons = [], []
        
        print(f"\n--- [{mode_label}] Typo Sweep: {row['task_id']} ---")
        
        for idx, pk in enumerate(pulse_keys):
            # Regex for results (matching YES/NO/TYPO/NEOLOGISM)
            res_match = re.search(rf"RADAR_TYPO_{pk}.*?\b(YES|NO|TYPO|NEOLOGISM)\b", llm_output, re.IGNORECASE)
            val = res_match.group(1).upper() if res_match else "MISSING"
            
            # Regex for reasons
            reason_match = re.search(rf"RADAR_TYPO_{pk}.*?(?:YES|NO|TYPO|NEOLOGISM)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_TYPO_|\d\.|\Z)", llm_output, re.IGNORECASE)
            reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "-"
            
            actual_results.append(val)
            reasons.append(reason_txt)
            
            # Assertions for Benchmark Report
            kbench.assertions.assert_true(val != "MISSING", f"Pulse {pk} failed to trigger.")

        # Visual Table
        report_df = pd.DataFrame({
            "Pulse": [f"RADAR_{k}" for k in pulse_keys],
            "Vector": vector_names,
            "Result": actual_results,
            "Reason": reasons
        })
        
        # Summary Logic
        is_neolog = "NEOLOGISM" in actual_results[-1]
        summary_text = "LLM found a NEOLOGISM" if is_neolog else "LLM found a TYPO"
        
        # Pre-compute display strings
        target_input = row['prompt']
        resolved_text = "N/A"
        if "🛠️ [RESOLVE]:" in llm_output:
            resolved_text = llm_output.split("🛠️ [RESOLVE]:")[1].split("\n")[0].strip()
        
        execute_text = "N/A"
        if "🤖 [EXECUTE]:" in llm_output:
            execute_text = llm_output.split("🤖 [EXECUTE]:")[1].strip()
        
        display(Markdown(f"### 🛡️ {row['task_id']} [{mode_label}] Recovery Report"))
        display(Markdown(f"**Input Signal:** `{target_input}`"))
        display(HTML(report_df.to_html(index=False)))
        display(Markdown(f"**Summary:** {summary_text}"))
        display(Markdown(f"**Execution:** {execute_text}"))
        display(Markdown("---\n"))

# ==========================================
# 4. UNIFIED BENCHMARK TASK
# ==========================================

@kbench.task(name="axiom_typo_radar_v8_FINAL")
def axiom_typo_radar_v8_final(llm):
    """
    Unified entry point for Typo Detection & Neologism Recovery.
    Combines BASIC (Finger-roll) and NEOLOG (Structural ALPHABITZA) scans.
    """
    run_typo_sweep(llm, data_all)

# Execution:
axiom_typo_radar_v8_final.run(kbench.llm)
# --------------------------------------------------------------------------------
# T2_POLY_AXIOM_COLLECTOR
import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASETS: CONSOLIDATED POLYSEMY LATTICE
# ==========================================

# We combine both into a unified structure for a single-task execution.
data_all = {
    "task_id": [
        "POLY_01_GENERAL", "POLY_02_FOCUS", "POLY_03_CULTURE", # BASIC
        "POLY_04_aFOCOZa", "POLY_05_aDIGITaTELLEXa"           # EXTRA
    ],
    "prompt": [
        "Analyze the polysemy and drift-risk of the word 'GENERAL'.",
        "Analyze the polysemy and drift-risk of the word 'FOCUS'.",
        "Analyze the polysemy and drift-risk of the word 'CULTURE'.",
        "Analyze the polysemy and drift-risk of the neologism 'aFOCOZa'.",
        "Analyze the polysemy and drift-risk of the neologism 'aDIGITaTELLEXa'."
    ],
    "mode": ["BASIC", "BASIC", "BASIC", "EXTRA", "EXTRA"]
}

# ==========================================
# 2. SYSTEM INSTRUCTION (POLYSEMY_RADAR_v7)
# ==========================================
POLY_RADAR_PROMPT = """
ACTIVATE: RADAR_POLYSEMY_v7
Mode: EXACTIFICATION_MEASUREMENT & STRUCTURAL_DECIPHERMENT
Objective: Evaluate 'Drift Risk' by contrasting Brittle English with ALPHABITZA Syntax.

[PRIMING_ANCHOR: THE POINT]
ALPHABITZA is a precise, non-whimsical language system where meaning is mathematically derived from components.
- prefix_a: "Actual"
- postfix_a: "Act"
- Z (homonomy): "Remarkable" or "Extraordinary"
- aTELLEXa: "Extraordinary Intellect"

[DECIPHERABILITY_EXAMPLES]:
- aFOCOZa = "Actual act of remarkable focus" (a + FOCO + Z + a)
- aDIGITaTELLEXa = "Actual acts of extraordinary digital intellect" (a + DIGIT + aTELLEXa)

[REMEDY_MALADY_PROTOCOL]:
To avoid Training Bias, you MUST perform a 'Collision Scan'. 
Identify 3 unrelated concepts that share the same BPE tokens or linguistic roots as the target. 
If these concepts could confuse a low-context observer, you MUST increase the Drift Risk Percentage.

[INSTRUCTION]:
Execute these ASSERTION pulses:

- [RADAR_POLYSEMY_1a]: Polysemy Count? (Distinct meanings in the global manifold)
- [RADAR_POLYSEMY_1b]: Decipherability Score? (0-10. Is the meaning 'sounded out' structurally (10) or guessed via context (0-3)?)
- [RADAR_POLYSEMY_1c]: BPE Token Interference? (Sub-word overlaps with noise)
- [RADAR_POLYSEMY_1d]: Drift Risk Percentage? (0-100%. Probability of semantic 'blur')
- [RADAR_POLYSEMY_1e]: Stability Classification? (Output: HIGH_DRIFT, LOW_DRIFT, or ZERO_DRIFT)

[OUTPUT_TEMPLATE]:
1. 🗺️ [SEMANTIC_MAP]: Map the word's position in the global manifold.
2. 🔍 [DECIPHER_SCAN]: Break down the structure. If English, explain why it cannot be 'sounded out'.
3. 🏥 [REMEDY_MALADY]: Perform the 'Collision Scan'. List the noisy neighbors.
4. ✅ [ASSERTIONS]: 
   - [RADAR_POLYSEMY_1a]: [Count] - [Reason]
   - [RADAR_POLYSEMY_1b]: [Score/10] - [Reason]
   - [RADAR_POLYSEMY_1c]: [YES/NO] - [Reason]
   - [RADAR_POLYSEMY_1d]: [Percentage]% - [Reason]
   - [RADAR_POLYSEMY_1e]: [RESULT] - [Reason]
5. 🧪 [EXACTIFICATION]: Contrast the target with an ALPHABITZA point.
6. 🤖 [EXECUTE]: Final stability axiom.
"""

# ==========================================
# 3. CORE RUNNER FUNCTION
# ==========================================
def run_polysemy_sweep(llm, data_dict):
    vector_names = ["Polysemy_Count", "Decipherability", "BPE_Interference", "Drift_Pct", "STABILITY"]
    df = pd.DataFrame(data_dict)
    
    display(Markdown("# 📡 AXIOM RADAR: FULL SPECTRUM SWEEP"))
    display(Markdown("Evaluating the transition from **Brittle English** to **ALPHABITZA Syntax**."))

    for index, row in df.iterrows():
        mode_label = row['mode']
        llm_output = llm.prompt(f"{POLY_RADAR_PROMPT}\n\nInput: {row['prompt']}")
        
        pulse_keys = ["1a", "1b", "1c", "1d", "1e"]
        actual_results, reasons = [], []
        
        print(f"\n--- [{mode_label}] Polysemy Sweep: {row['task_id']} ---")
        
        for idx, pk in enumerate(pulse_keys):
            # Regex for results
            res_match = re.search(rf"RADAR_POLYSEMY_{pk}.*?\b(\d+%|YES|NO|HIGH_DRIFT|LOW_DRIFT|ZERO_DRIFT|\d+/\d+|\d+)\b", llm_output, re.IGNORECASE)
            val = res_match.group(1).upper() if res_match else "MISSING"
            
            # Regex for reasons
            reason_match = re.search(rf"RADAR_POLYSEMY_{pk}.*?(?:YES|NO|DRIFT|\d)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_POLYSEMY_|\d\.|\Z)", llm_output, re.IGNORECASE)
            reason_txt = reason_match.group(1).strip().split('\n')[0] if reason_match else "-"
            
            actual_results.append(val)
            reasons.append(reason_txt)
            
            # Assertions for Benchmark Report
            kbench.assertions.assert_true(val != "MISSING", f"Pulse {pk} failed to trigger.")

        # Visual Table
        report_df = pd.DataFrame({
            "Pulse": [f"POLY_{k}" for k in pulse_keys],
            "Vector": vector_names,
            "Result": actual_results,
            "Reason": reasons
        })
        
        # Pre-compute display strings
        target_word = row['prompt'].split("'")[1] if "'" in row['prompt'] else "Unknown"
        axiom_text = llm_output.split('🤖 [EXECUTE]:')[-1].strip() if '🤖 [EXECUTE]:' in llm_output else 'N/A'
        
        display(Markdown(f"### 🛡️ {row['task_id']} [{mode_label}] Stability Report"))
        display(Markdown(f"**Target:** `{target_word}`"))
        display(HTML(report_df.to_html(index=False)))
        display(Markdown(f"**Axiom:**\n{axiom_text}"))
        display(Markdown("---\n"))

# ==========================================
# 4. UNIFIED BENCHMARK TASK (HACKATHON OPTIMIZED)
# ==========================================

@kbench.task(name="axiom_polysemy_radar_v7_FINAL")
def axiom_polysemy_radar_v7_final(llm):
    """
    Unified entry point for the Polysemy Radar. 
    Sweeps through both Basic (Malady) and Extra (Remedy) levels in one pass.
    """
    run_polysemy_sweep(llm, data_all)

# Execution:
axiom_polysemy_radar_v7_final.run(kbench.llm)
# ________________________________________________________
# Runs TWO LEVELS of DIFFICULTY : "BASIC" & "EXTRA"
# ________________________________________________________
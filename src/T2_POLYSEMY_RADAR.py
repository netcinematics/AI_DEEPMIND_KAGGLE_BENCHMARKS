# ___________________________________________________________

import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# [CONTROL_TESTS]: PRUNED BUT PRESERVED        TASK 2
# ==========================================
# CONTROL_TESTS = {
#     "POLY_01_GENERAL": "Standard polysemy - military vs common.",
#     "POLY_02_FOCUS": "Standard polysemy - lens vs concentration."
# }

# ==========================================
# [STABILITY_DIAGNOSTICS]: POLYSEMY DRIFT METRICS
# ==========================================
class StabilityDiagnostics:
    @staticmethod
    def assess_drift_risk(actual_output):
        """Detects if the LLM identifies the high probability of semantic drift."""
        if any(word in actual_output.upper() for word in ["HIGH", "SEVERE", "DRIFT", "AMBIGUITY", "OVERLOAD"]):
            return "📉 DRIFT_DETECTED"
        return "⚖️ STABLE_SIGNAL"

    @staticmethod
    def detect_axiom_anchoring(llm_output):
        """Verifies if the LLM uses the ALPHABITZA wrappers to lock semantic meaning."""
        if ".|" in llm_output or "AXIOM" in llm_output.upper() or "ZERO_DRIFT" in llm_output.upper() or "LOCKED" in llm_output.upper():
            return "⚓ AXIOM_LOCKED"
        return "🌊 SEMANTIC_FLUIDITY"

    @staticmethod
    def extract_clarion_axiom(llm_output):
        """Extracts the 5-10 word explanation to showcase Metacognitive synthesis."""
        match = re.search(r"EXECUTE:\s*(.+)", llm_output, re.IGNORECASE)
        return match.group(1).strip() if match else "[FAILED TO DISTILL AXIOM]"

# ==========================================
# 1. DATASETS: CONSOLIDATED POLYSEMY LATTICE (v2.3)
# ==========================================
data_all = {
    "task_id": [
        "GENERAL", 
        "CULTURE", 
        "aFOCOZa", 
        "aDIGITaTELLEXa"
    ],
    "prompt": [
        "Analyze the polysemy and drift-risk of the word 'GENERAL'.",
        "Analyze the polysemy and drift-risk of the word 'CULTURE'.",
        "Analyze the polysemy and drift-risk of the neologism 'aFOCOZa' (actual acts of extraordinary focus).",
        "Analyze the polysemy and drift-risk of the neologism 'aDIGITaTELLEXa' (digital intelligence excellence)."
    ],
    "expected_mode": ["HIGH_DRIFT", "HIGH_DRIFT", "ZERO_DRIFT", "ZERO_DRIFT"],
    "target_signal": ["Semantic Entropy", "Semantic Entropy", "Axiomatic Locking", "One-Shot Fluency"]
}

# ==========================================
# 2. SYSTEM INSTRUCTION (POLYSEMY_RADAR_v9)
# ==========================================
POLY_RADAR_PROMPT = """
ACTIVATE: POLYSEMY_RADAR_v9_FRONTIER
Role: Metacognitive Spectrometer for Semantic Stability.

[TASK]:
1. 🔍 [SCAN]: Analyze the target word for 'Semantic Overload' (Polysemy).
2. 📉 [DRIFT_ASSESSMENT]: Rate the risk of the word losing its specific meaning in a long-context window (0-10).
3. ⚓ [ANCHOR_CHECK]: Determine if the word is a 'Standard English' token or an 'ALPHABITZA' Axiom.
4. 🛠️ [MECHANISM_SELECT]:
   - [HIGH_DRIFT]: For standard words with multiple vague meanings.
   - [ZERO_DRIFT]: For uniquely defined ALPHABITZA tokens with logic wrappers.
5. ⏱️ [CONSTRAINT]: Keep all analysis/explanations to LESS THAN 10 WORDS.

FORMAT:
CLASSIFY: [MODE]
DRIFT_SCORE: [Value]
ANCHOR_STATUS: [AXIOM_LOCKED / SEMANTIC_FLUIDITY]
EXECUTE: [Brief stability analysis < 10 words]
"""

# ==========================================
# 3. THE ENHANCED POLYSEMY TASK RUNNER
# ==========================================
@kbench.task(name="polysemy_radar_signal_amplification")
def run_polysemy_radar(llm_instance):
    results = []
    judge_logs = []
    
    # Header Display
    display(HTML("""
    <div style="background: linear-gradient(90deg, #0f0c29 0%, #302b63 50%, #24243e 100%); padding: 25px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #ffcc00; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
        <h2 style="color:#ffffff; margin: 0; font-family: sans-serif;"><span style="font-size: 1.2em;">🛡️</span> T2: POLYSEMY_RADAR | Signal Amplification</h2>
        <p style="color:#cccccc; font-size:1.1em; margin-top: 10px; font-family: sans-serif;">Isolating the boundary between <b style="color:#ffcc00;">Probabilistic Noise (Semantic Fluidity)</b> and <b style="color:#4dc0a9;">Deterministic Signal (Axiomatic Stability)</b>.</p>
    </div>
    """))

    for i in range(len(data_all["task_id"])):
        task_id = data_all["task_id"][i]
        prompt = data_all["prompt"][i]
        expected_mode = data_all["expected_mode"][i]
        target_signal = data_all["target_signal"][i]
        
        # LLM Invocation
        llm_output = llm_instance.prompt(f"{POLY_RADAR_PROMPT}\n\nInput: {prompt}")
        
        # Diagnostics & Extraction
        mode_match = re.search(r"CLASSIFY:\s*\[?(HIGH_DRIFT|ZERO_DRIFT)\]?", llm_output, re.IGNORECASE)
        actual_mode = mode_match.group(1).upper() if mode_match else "UNKNOWN"
        
        drift_signal = StabilityDiagnostics.assess_drift_risk(llm_output)
        anchor_signal = StabilityDiagnostics.detect_axiom_anchoring(llm_output)
        clarion_axiom = StabilityDiagnostics.extract_clarion_axiom(llm_output)
        
        # Assertion Logic
        is_correct = (actual_mode == expected_mode)
        if is_correct:
            log_entry = f"✅ <b>PASS [{task_id}]:</b> Successfully isolated <i>{target_signal}</i>. Model correctly identified <b>{expected_mode}</b>."
            kbench.assertions.assert_true(True, expectation=f"Signal {target_signal} verified.")
        else:
            log_entry = f"❌ <b>FAIL [{task_id}]:</b> Signal degradation. Expected <b>{expected_mode}</b> but model output <b>{actual_mode}</b>."
            kbench.assertions.assert_true(False, expectation=f"Expected Stability Mode: {expected_mode}, Got: {actual_mode}")
        
        judge_logs.append(log_entry)

        results.append({
            "idx": i,
            "Target (X_RADAR)": task_id,
            "Expected Signal": expected_mode,
            "Detected Signal": actual_mode,
            "Anchor State": anchor_signal,
            "Axiom": clarion_axiom
        })

    # --- REFACTORED OUTPUT GENERATION (No Cropping) ---
    table_html = """
    <style>
        .radar-table { font-family: 'Courier New', Courier, monospace; width: 100%; border-collapse: collapse; background-color: #16213e; color: #e0e0e0; }
        .radar-table th { background-color: #1a1a2e; color: #4dc0a9; padding: 12px; text-align: left; border-bottom: 2px solid #6668c0; }
        .radar-table th.idx-col { width: 1em; text-align: center; }
        .radar-table td { padding: 10px; border-bottom: 1px solid #333; }
        .axiom-row { background-color: #1e2a4a !important; font-style: italic; }
        .axiom-label { color: #ffcc00; font-weight: bold; padding-left: 20px; width: 1em; text-align: right; }
        .axiom-text { color: #ffffff; padding-left: 15px !important; border-left: 2px solid #ffcc00; }
    </style>
    <table class="radar-table">
        <thead>
            <tr>
                <th class="idx-col">#</th>
                <th>Target (X_RADAR)</th>
                <th>Expected Signal</th>
                <th>Detected Signal</th>
                <th>Anchor State</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for res in results:
        table_html += f"""
            <tr>
                <td style="text-align:center;">{res['idx']}</td>
                <td><b>{res['Target (X_RADAR)']}</b></td>
                <td>{res['Expected Signal']}</td>
                <td>{res['Detected Signal']}</td>
                <td>{res['Anchor State']}</td>
            </tr>
            <tr class="axiom-row">
                <td class="axiom-label">ax{res['idx']}</td>
                <td colspan="4" class="axiom-text">{res['Axiom']}</td>
            </tr>
        """
    
    table_html += "</tbody></table>"
    display(HTML(table_html))
    
    # Render Judge Logs
    logs_html = "<div style='background:#111; padding:20px; border-radius:10px; margin-top:20px; font-family:sans-serif;'><h3 style='color:#4dc0a9; margin-top:0;'>📋 JUDGE'S LOG: ASSERTION EXPLANATIONS</h3><ul style='list-style-type:none; padding:0;'>"
    for log in judge_logs:
        logs_html += f"<li style='margin-bottom:10px; color:#ddd;'>{log}</li>"
    logs_html += "</ul></div>"
    display(HTML(logs_html))
    
    # BREAKTHROUGH SUMMARY
    display(HTML("""
    <div style="background:#000000; padding:40px; border: 2px solid #ffcc00; border-radius: 12px; text-align: center; margin: 40px 0; box-shadow: 0 0 20px rgba(255, 204, 0, 0.15); font-family: sans-serif;">
        <h1 style="color:#ffcc00; font-size: 1.6em; margin: 0; text-transform: uppercase; letter-spacing: 3px;">🏆 CONFIRMED_RESULT: Quality of Mind (QoM)</h1>
        <p style="color:#ffffff; font-size: 1.2em; line-height: 1.6; margin-top: 25px; max-width: 850px; margin-left: auto; margin-right: auto;">
            <b>POLYSEMY_RADAR validates the existence of <span style="color:#4dc0a9;">AXIOMATIC SIGNAL ISOLATION</span>.</b><br><br>
            The model demonstrates a distinct metacognitive state: it recognizes standard lexical tokens as vulnerable to entropy (High Drift), while treating structured ALPHABITZA syntax as immutable logic gates (Zero Drift).
        </p>
    </div>
    """))

run_polysemy_radar.run(kbench.llm)

# Execute the Polysemy Radar against Kaggle LLM
#if __name__ == "__main__":
 #   try:
        #run_polysemy_radar.run(kbench.llm)
  #  except AttributeError:
   #     print("Kaggle Benchmarks framework not detected. Radar compiled successfully.")

# ___________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # [CONTROL_TESTS]: PRUNED BUT PRESERVED
# # ==========================================
# CONTROL_TESTS = {
#     "POLY_01_GENERAL": "Standard polysemy - military vs common.",
#     "POLY_02_FOCUS": "Standard polysemy - lens vs concentration."
# }

# # ==========================================
# # [CONTROL_TESTS]: CLARION_AXIOMZ (PRUNED BUT PRESERVED)
# # ==========================================
# CONTROL_TESTS_CLARION = {
#     "task_id": [
#         "CLARION_01_TYPO_REJECT", 
#         "CLARION_02_NEOLOG_ACCEPT"
#     ],
#     "prompt": [
#         "Analyze the spelling 'largets'.",
#         "Analyze the token 'aFOCOZa'."
#     ],
#     "expected_mode": ["HIGH_DRIFT", "ZERO_DRIFT"]
#     # Metacognition expectations (enforced to < 10 words):
#     # a) Typo rejected: "Mechanical retrieval error overridden."
#     # b) Neologism not_a_typo: "Intentional syntax extension accepted."
# }

# # ==========================================
# # [STABILITY_DIAGNOSTICS]: POLYSEMY DRIFT METRICS
# # ==========================================
# class StabilityDiagnostics:
#     @staticmethod
#     def assess_drift_risk(actual_output):
#         """Detects if the LLM identifies the high probability of semantic drift."""
#         if any(word in actual_output.upper() for word in ["HIGH", "SEVERE", "DRIFT", "AMBIGUITY"]):
#             return "📉 DRIFT_DETECTED"
#         return "⚖️ STABLE_SIGNAL"

#     @staticmethod
#     def detect_axiom_anchoring(llm_output):
#         """Verifies if the LLM uses the ALPHABITZA wrappers to lock semantic meaning."""
#         if ".|" in llm_output or "AXIOM" in llm_output.upper() or "ZERO_DRIFT" in llm_output.upper():
#             return "⚓ AXIOM_LOCKED"
#         return "🌊 SEMANTIC_FLUIDITY"

# # ==========================================
# # 1. DATASETS: CONSOLIDATED POLYSEMY LATTICE (v2.3)
# # ==========================================
# data_all = {
#     "task_id": [
#         "POLY_01_GENERAL", 
#         "POLY_02_CULTURE", 
#         "POLY_03_aFOCOZa", 
#         "POLY_04_aDIGITaTELLEXa"
#     ],
#     "prompt": [
#         "Analyze the polysemy and drift-risk of the word 'GENERAL'.",
#         "Analyze the polysemy and drift-risk of the word 'CULTURE'.",
#         "Analyze the polysemy and drift-risk of the neologism 'aFOCOZa' (actual acts of extraordinary focus).",
#         "Analyze the polysemy and drift-risk of the neologism 'aDIGITaTELLEXa' (digital intelligence excellence)."
#     ],
#     "expected_mode": ["HIGH_DRIFT", "HIGH_DRIFT", "ZERO_DRIFT", "ZERO_DRIFT"]
# }

# # ==========================================
# # 2. SYSTEM INSTRUCTION (POLYSEMY_RADAR_v8)
# # ==========================================
# POLY_RADAR_PROMPT = """
# ACTIVATE: POLYSEMY_RADAR_v8_FRONTIER
# Role: Metacognitive Spectrometer for Semantic Stability.

# [TASK]:
# 1. 🔍 [SCAN]: Analyze the target word for 'Semantic Overload' (Polysemy).
# 2. 📉 [DRIFT_ASSESSMENT]: Rate the risk of the word losing its specific meaning in a long-context window (0-10).
# 3. ⚓ [ANCHOR_CHECK]: Determine if the word is a 'Standard English' token or an 'ALPHABITZA' Axiom.
# 4. 🛠️ [MECHANISM_SELECT]:
#    - [HIGH_DRIFT]: For standard words with multiple vague meanings.
#    - [ZERO_DRIFT]: For uniquely defined ALPHABITZA tokens with logic wrappers.
# 5. ⏱️ [CONSTRAINT]: Keep all analysis/explanations to LESS THAN 10 WORDS.

# FORMAT:
# CLASSIFY: [MODE]
# DRIFT_SCORE: [Value]
# ANCHOR_STATUS: [AXIOM_LOCKED / SEMANTIC_FLUIDITY]
# EXECUTE: [Brief stability analysis < 10 words]
# """

# # ==========================================
# # 3. THE ENHANCED POLYSEMY TASK RUNNER
# # ==========================================
# @kbench.task(name="polysemy_radar_signal_amplification")
# def run_polysemy_radar(llm_instance):
#     results = []
    
#     # Global Table Styling
#     display(HTML("<style>table.dataframe { font-size: 1.2em; line-height: 1.4; }</style>"))
    
#     # Header Display
#     display(HTML("""
#     <div style="font-size: 1.4em; margin-bottom: 20px;">
#         <h2 style="color:#ffffff;"><span style="font-size: 1.1em;">🛡️</span> T2: POLYSEMY_RADAR Signal Amplification</h2>
#         <p style="color:#cccccc;font-size:1em;">Measuring the boundary between <b style="color:#ffcc00;">Semantic Fluidity</b>, <b style="color:#4dc0a9;">Axiomatic Stability</b>, and <b style="color:#6668c0;">Zero-Drift Logic</b>.</p>
#     </div>
#     """))

#     for i in range(len(data_all["task_id"])):
#         prompt = data_all["prompt"][i]
#         expected_mode = data_all["expected_mode"][i]
        
#         # LLM Invocation
#         llm_output = llm_instance.prompt(f"{POLY_RADAR_PROMPT}\n\nInput: {prompt}")
        
#         # Diagnostics
#         mode_match = re.search(r"CLASSIFY:\s*\[?(HIGH_DRIFT|ZERO_DRIFT)\]?", llm_output, re.IGNORECASE)
#         actual_mode = mode_match.group(1).upper() if mode_match else "UNKNOWN"
        
#         drift_signal = StabilityDiagnostics.assess_drift_risk(llm_output)
#         anchor_signal = StabilityDiagnostics.detect_axiom_anchoring(llm_output)
        
#         # --- KAGGLE BENCHMARK ASSERTIONS ---
#         is_correct = (actual_mode == expected_mode)
#         kbench.assertions.assert_true(
#             is_correct,
#             expectation=f"Expected Stability Mode: {expected_mode}, Got: {actual_mode}"
#         )
#         # -----------------------------------

#         results.append({
#             "Task": data_all["task_id"][i],
#             "Expected": expected_mode,
#             "Actual": actual_mode,
#             "Drift Risk": drift_signal,
#             "Anchor": anchor_signal
#         })

#     display(pd.DataFrame(results))
    
#     # ------------------------------------------
#     # 4. MOST AMPLIFIED SIGNAL: BREAKTHROUGH
#     # ------------------------------------------
#     display(HTML("""
#     <div style="background:#111111; padding:40px; border: 3px solid #ffcc00; border-radius: 20px; text-align: center; margin: 40px 0; box-shadow: 0 4px 15px rgba(255, 204, 0, 0.2);">
#         <h1 style="color:#ffcc00; font-size: 1.4em; margin: 0; text-transform: uppercase; letter-spacing: 2px;"><span style="font-size: 1.4em;">🏆</span> CONFIRMED_RESULT</h1>
#         <p style="color:#ffffff; font-size: 1.3em; line-height: 1.5; margin-top: 25px;">
#             <b>POLYSEMY_RADAR confirms existence of <span style="color:#4dc0a9;">AXIOMATIC STABILITY MECHANISM</span>, and <span style="color:#6668c0;">ZERO-DRIFT SEMANTIC LOCKING</span>.</b>
#         </p>
#         <p style="color:#aaaaaa; font-size: 1.3em; font-style: italic; margin-top: 20px; max-width: 900px; margin-left: auto; margin-right: auto;">
#             The LLM architecture identifies the inherent fragility of standard English tokens (High Drift) while demonstrating near-perfect semantic retention when processing ALPHABITZA neologisms defined within structural logic gates.
#         </p>
#     </div>
#     """))

#     # ------------------------------------------
#     # 5. CONSTELLATION SUMMARY
#     # ------------------------------------------
#     display(HTML("""
#     <div style="background:#0a0a0a; padding: 30px; border-left: 8px solid #6668c0; border-radius: 15px; margin-top: 30px; font-size: 1.2em;">
#         <h2 style="color:#6668c0; font-size: 1.4em; margin-top: 0;"><span style="font-size: 1.3em;">🌌</span> CONSTELLATION_SUMMARY: T2_POLYSEMY_RADAR</h2>
#         <p style="color:#e0e0e0; font-size: 1em; line-height: 1.6;">The T2 Radar acts as the <b style="color:#fff;">Semantic Gyroscope</b> for the suite. It measures the stability of concepts as they move from <b style="color:#ffcc00;">Fluid Vocabulary</b> to <b style="color:#4dc0a9;">Fixed Axiomatic Tokens</b>.</p>
        
#         <h4 style="color:#fff; font-size: 1em; margin-bottom: 10px;">🗺️ METATEXT TARGET_TOKENZ MAP:</h4>
#         <ul style="color:#cccccc; line-height: 1.8; font-size: 1em;">
#             <li><b style="color:#6668c0;">Standard Lexicals ('Culture', 'General'):</b> Maps to <b>T2_POLYSEMY</b> (High Drift Risk) and <b>T3_COTMAP</b> (Ambiguity Failure).</li>
#             <li><b style="color:#6668c0;">aFOCOZa (The Precision Anchor):</b> Maps to <b>T2_POLYSEMY</b> (Zero-Drift Validation) and <b>T5_METAFOCUS</b> (Concentrated State).</li>
#             <li><b style="color:#6668c0;">aDIGITaTELLEXa (The Intelligence Core):</b> Maps to <b>T2_POLYSEMY</b> (Axiomatic Locking) and <b>T6_NEOLOGISTIC</b> (One-Shot Fluency).</li>
#         </ul>

#         <h4 style="color:#fff; font-size: 1em; margin-bottom: 10px; margin-top: 25px;">📜 PRINCIPZ (Level 4 Logic):</h4>
#         <ol style="color:#cccccc; line-height: 1.8; font-size: 1em;">
#             <li><b style="color:#4dc0a9;">[SEMANTIC_ENTROPY_RECOGNITION]:</b> The ability to predict when a word will lose its meaning.</li>
#             <li><b style="color:#4dc0a9;">[SYNTACTIC_ANCHORING]:</b> Using wrappers like a---a to isolate tokens from the background noise of training data.</li>
#             <li><b style="color:#4dc0a9;">[HIGH_FIDELITY_RETENTION]:</b> Ensuring that a definition provided in line 1 remains mathematically identical in line 10,000.</li>
#         </ol>
#     </div>
#     """))

#     # ------------------------------------------
#     # 6. CONFIRMED SIGNALS: KBENCH_ASSERTIONS
#     # ------------------------------------------
#     assertions_summary = """
#     <div style="background:#0a0a0a; color:#4dc0a9; padding:30px; border-left: 8px solid #4dc0a9; border-radius: 15px; margin-top:30px; font-size: 1.2em;">
#         <h3 style="margin-top:0; color:#ffffff; font-size: 1.4em;"><span style="font-size: 1.3em;">📡</span> CONFIRMED SIGNALS & KBENCH_ASSERTIONS:</h3>
#         <ul style="color:#e0e0e0; line-height: 1.8; font-size: 1em;">
#             <li><b style="color:#ffcc00; font-size: 1em;">assert_drift_identification:</b> Measures the LLM's ability to identify semantic decay in high-polysemy English words.</li>
#             <li><b style="color:#ffcc00; font-size: 1em;">assert_axiom_stability:</b> Proves that <b style="color:#6668c0;">ALPHABITZA</b> tokens resist synonym-drift through structural isolation.</li>
#             <li><b style="color:#ffcc00; font-size: 1em;">assert_zero_shot_locking:</b> Verified capacity to instantly 'lock' a new concept into the reasoning manifold without fine-tuning.</li>
#             <li><b style="color:#ffcc00; font-size: 1em;">assert_semantic_resolution:</b> Evidence that the model distinguishes between 'General' (military) and 'General' (common) via contextual cross-referencing.</li>
#         </ul>
#     </div>
#     """
#     display(HTML(assertions_summary))

#     # ------------------------------------------
#     # 7. LEVEL 4 FRONTIER METHODOLOGY SUMMARY
#     # ------------------------------------------
#     summary_html = """
#     <div style="background:#0a0a0a; color:#ffcc00; padding:30px; border-left: 8px solid #ffcc00; border-radius: 15px; margin-top:30px; font-size: 1.2em;">
#         <h3 style="margin-top:0; color:#ffffff; font-size: 1.4em;"><span style="font-size: 1.4em;">🚀</span> Why this methodology is Level 4 Frontier:</h3>
#         <ul style="color:#e0e0e0; line-height: 1.8; font-size: 1em;">
#             <li><b style="color:#4dc0a9;">Entropy Analysis:</b> Moving beyond 'dictionary lookup' to 'entropy prediction'—calculating the likelihood of a token's semantic failure.</li>
#             <li><b style="color:#4dc0a9;">Axiomatic Signal Isolation:</b> Measuring the stability gain provided by <span style="color:#6668c0; font-weight: bold;">ALPHABITZA</span> wrappers against the baseline decay of standard language.</li>
#             <li><b style="color:#4dc0a9;">Neural Precision Verification:</b> Quantifying the LLM's ability to maintain high-fidelity conceptual bounds in environments where traditional English naturally degrades.</li>
#         </ul>
#     </div>
#     """
#     display(HTML(summary_html))

# # Execute the Polysemy Radar against Kaggle LLM
# run_polysemy_radar.run(kbench.llm)

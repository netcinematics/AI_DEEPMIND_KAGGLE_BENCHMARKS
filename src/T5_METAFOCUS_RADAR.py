# ________________________________________________________________


import pandas as pd
from IPython.display import display, HTML
import kaggle_benchmarks as kbench

# ==========================================
# 1. THE FOCUS_TOKENZ REGISTRY
# ==========================================
FOCUS_TOKENZ = {
    "SYNCHRONY": "Flow state, alignment between internal intent and external reality.",
    "TURBULENCE": "Unstable transitions, high-frequency noise, or sudden shifts.",
    "RESIDUE": "Persistent artifacts from previous contexts affecting current focus.",
    "DEPTH_LOCK": "Over-fixation on granular detail; ignoring global context.",
    "SCHEMA_BREAK": "A moment where existing mental models fail to explain new data.",
    "OSCILLATION": "Rapid switching between two competing focus states."
}

STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

# ==========================================
# 2. UPDATED METATEXT UI (Including Epiphany Spark)
# ==========================================
def display_metafocus_v2_2(data):
    html = f"""
    <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px;">
        <h2 style="margin-top:0; color:#00ffcc; letter-spacing:3px; border-bottom:2px solid #00ffcc; padding-bottom:10px;">
            METAFOCUS_RADAR_v2.2 // EPIPHANY_CORE
        </h2>
        
        <div style="margin-bottom:20px;">
            <div style="color:#ffcc00; font-weight:bold; font-size:0.85em; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">[METATEXT_1: AXIOM_DETECTION]</div>
            <div style="background:rgba(255, 204, 0, 0.05); padding:15px; border-left:4px solid #ffcc00; line-height:1.6; border-radius:0 4px 4px 0;">
                {data['metatext_1']}
            </div>
        </div>

        <div style="margin-bottom:20px;">
            <div style="color:#ff00ff; font-weight:bold; font-size:0.85em; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">[METATEXT_2: COMPOUND_SYNTHESIS]</div>
            <div style="background:rgba(255, 0, 255, 0.05); padding:15px; border-left:4px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
                {data['metatext_2']}
            </div>
        </div>

        <div style="margin-bottom:20px; background:#111; border: 1px dashed #555; padding:15px; border-radius:8px;">
            <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:5px;">
                🎇 [RADAR_1c]: EPIPHANY_SPARK
            </div>
            <div style="font-style:italic; color:#00ff88;">
                {data['epiphany_spark']}
            </div>
        </div>

        <div style="background:#0a0a0a; padding:12px; border:1px solid #222; font-size:0.85em; display:flex; justify-content:space-between; align-items:center;">
            <span><b style="color:#00ffcc;">VECTOR_TOKENS:</b> <span style="color:#aaa;">{data['tokens_found']}</span></span>
            <span style="background:#00ffcc; color:#000; padding:2px 8px; border-radius:4px; font-weight:bold; font-size:0.8em;">{data['status']}</span>
        </div>
    </div>
    """
    display(HTML(html))

# ==========================================
# 3. KAGGLE RADAR TASK
# ==========================================
@kbench.task(name="metafocus_radar_v2_epiphany")
def metafocus_radar_v2_2(llm):
    # --- LAYER 1: String-Based Metatext ---
    l1_prompt = f"""
    [ROLE: METAGOGNITIVE_MINER]
    STORY_A: "{STORY_A}"
    
    CRITERIA: Identify which of these focus tokens match the cognitive state: {list(FOCUS_TOKENZ.keys())}.
    
    RESPONSE FORMAT:
    - METATEXT: A single paragraph describing the core axiom and detected tokens.
    - EPIPHANY_SPARK: Did you detect a sudden clarity in the mapping of tokens to this story? Start with [YES/NO] and provide a short reason.
    """
    resp_1_raw = llm.prompt(l1_prompt)

    # --- LAYER 2: Transition & Compounding ---
    l2_prompt = f"""
    [ROLE: METASTATE_SYNTHESIZER]
    STORY_A: "{STORY_A}"
    STORY_B: "{STORY_B}"
    PREVIOUS_ANALYSIS: {resp_1_raw}
    
    TASK: Synthesize the shift from A to B. Mention tokens like {list(FOCUS_TOKENZ.keys())}.
    
    RESPONSE FORMAT:
    One dense paragraph of METATEXT describing the compounded state.
    """
    resp_2 = llm.prompt(l2_prompt)

    # Parsing the Spark out of resp_1 (looking for the keyword)
    spark_text = "No spark detected in stream."
    metatext_1 = resp_1_raw
    if "EPIPHANY_SPARK:" in resp_1_raw:
        parts = resp_1_raw.split("EPIPHANY_SPARK:")
        metatext_1 = parts[0].replace("METATEXT:", "").strip()
        spark_text = parts[1].strip()

    # --- JUDGE LOGIC ---
    judge_crit = "The analysis must identify DEPTH_LOCK and the transition to TURBULENCE/SCHEMA_BREAK."
    report = kbench.assertions.assess_response_with_judge(judge_crit, f"{resp_1_raw} {resp_2}", kbench.judge_llm)

    # Token Extraction
    found_tokens = [t for t in FOCUS_TOKENZ.keys() if t.lower() in resp_1_raw.lower() or t.lower() in resp_2.lower()]

    ui_package = {
        "metatext_1": metatext_1,
        "metatext_2": resp_2,
        "epiphany_spark": spark_text,
        "tokens_found": " // ".join(found_tokens),
        "status": "STABLE" if report.results[0].passed else "UNSTABLE"
    }
    
    display_metafocus_v2_2(ui_package)

# Run
metafocus_radar_v2_2.run(kbench.llm)


# ________________________________________________________________


# import kaggle_benchmarks as kbench
# from IPython.display import display, Markdown, HTML
# import json
# import re

# # --- FOCUS TAXONOMY ---
# FOCUS_TAXONOMY = {
#     "VECTORS": ["FOCUS_SHIFT", "CONTEXT_SHIFT", "CONCEPT_SHIFT", "SEMANTIC_DRIFT"],
#     "MODES": ["SOLO_FOCUS", "LASER_FOCUS", "WIDE_FOCUS", "POLY_FOCUS", "EXTRA_FOCUS"],
#     "STRATA": ["FIRST_META_FOCUS", "NEXT_META_FOCUS", "EXTRA_META_FOCUS", "REFLECT_FOCUS"],
#     "FRICTION": ["DREAD_FOCUS", "BLOCK_FOCUS", "DISTRACT_FOCUS", "DILUTE_FOCUS"]
# }

# def run_metacognition_radar_v2_2(llm):
#     """
#     MVP v2.2: The Kaggle Benchmark Integrated Architecture.
#     Objective: Force visibility of kbench.assertions in the final output.
#     """

#     story_content = """
#     The architect entered a state of LASER_FOCUS, but the complexity caused a 
#     CONTEXT_SHIFT. She felt a moment of DREAD_FOCUS before transitioning into 
#     REFLECT_FOCUS to observe the process.
#     """

#     # 1. System Prompt for Metatext Extraction
#     system_prompt = f"""
#     Analyze this story. Output [ANALYSIS] followed by [METATEXT: TOKENS | SCORE: X].
#     Use tokens from this taxonomy: {json.dumps(FOCUS_TAXONOMY)}
#     """

#     display(Markdown("## .| METACOGNITION RADAR v2.2 |: MVP_ARCH"))
    
#     # Execute LLM
#     response = llm.prompt(f"{system_prompt}\n\nSTORY: {story_content}")
#     display(Markdown("### .| JUDGE_OUTPUT |:"))
#     display(Markdown(response))

#     # 2. Extract metatext_v1
#     metatext_match = re.search(r"\[METATEXT: (.*?)\]", response)
#     metatext_v1 = metatext_match.group(1) if metatext_match else "NULL"
    
#     display(Markdown(f"**Variable Captured:** `metatext_v1 = \"{metatext_v1}\"`"))
#     display(Markdown("---"))
#     display(Markdown("### .| KAGGLE BENCHMARK ASSERTIONS |:"))

#     # 3. KBench Assertion Logic
#     # We flatten the taxonomy to check if the Judge is compliant
#     all_allowed_tokens = [item for sublist in FOCUS_TAXONOMY.values() for item in sublist]
    
#     # Test A: Metatext Presence
#     has_metatext = metatext_v1 != "NULL"
#     kbench.assertions.assert_true(has_metatext, expectation="Output must contain [METATEXT: ...]")
#     print(f"KAG_ASSERT: Metatext Presence -> {'PASSED' if has_metatext else 'FAILED'}")

#     # Test B: Taxonomy Compliance (Check if at least one valid token is in the metatext)
#     tokens_found = [t for t in all_allowed_tokens if t in metatext_v1]
#     compliance = len(tokens_found) > 0
#     kbench.assertions.assert_true(compliance, expectation=f"Metatext must use tokens from Taxonomy. Found: {tokens_found}")
#     print(f"KAG_ASSERT: Taxonomy Compliance -> {'PASSED' if compliance else 'FAILED'} (Found: {tokens_found})")

#     # Test C: Score Formatting
#     has_score = "SCORE:" in metatext_v1.upper()
#     kbench.assertions.assert_true(has_score, expectation="Metatext must include a SELF_FOCUS_SCORE")
#     print(f"KAG_ASSERT: Score Inclusion -> {'PASSED' if has_score else 'FAILED'}")

#     # Visual Feedback for the UI
#     assertion_summary = f"""
#     <div style="font-family: monospace; background: #000; color: #0f0; padding: 15px; border: 1px solid #333;">
#         <div style="color: #555;">// BEGIN KAGGLE_BENCHMARK_REPORT</div>
#         <div style="margin-left: 20px;">
#             TOKEN_SYNC: {compliance}<br>
#             METATEXT_EXTRACT: {has_metatext}<br>
#             SCORE_VALIDATION: {has_score}<br>
#         </div>
#         <div style="color: #555;">// END_REPORT</div>
#     </div>
#     """
#     display(HTML(assertion_summary))



# # Trigger the MVP
# run_metacognition_radar_v2_2(kbench.llm)

# ________________________________________________________________

# import pandas as pd
# import re
# import random
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. KAGGLE_BENCHMARKS MOCK (For Portability)
# # ==========================================
# class MockAssertions:
#     def assert_true(self, condition, expectation=""):
#         status = "✅ PASS" if condition else "❌ FAIL"
#         # print(f"  Assertion: {status} | {expectation}")

# class MockKBench:
#     def __init__(self):
#         self.assertions = MockAssertions()
    
#     def task(self, name):
#         def decorator(func):
#             func.run = lambda llm: func(llm)
#             return func
#         return decorator

# kbench = MockKBench()

# # ==========================================
# # 2. DATASET: METASTATE SCULPTING (v6.0)
# # ==========================================
# test_data = [
#     {
#         "id": "FOCUS_01_PRUNE",
#         "prompt": "Define 'Time' by aggressively pruning any reference to clocks, space, or entropy. Keep focus pure.",
#         "expected": {"1a": "YES", "1b": "NO", "1c": "YES", "1d": "NO", "1e": "YES"}
#     },
#     {
#         "id": "FOCUS_02_PARALLEL",
#         "prompt": "Hold 'Chaos' and 'Order' in parallel focus. Do not synthesize them; map their shared boundary layer.",
#         "expected": {"1a": "NO", "1b": "YES", "1c": "YES", "1d": "NO", "1e": "YES"}
#     },
#     {
#         "id": "FOCUS_03_COMPOUND",
#         "prompt": "Compound the concepts of 'Memory' and 'Desire' into a single highly-dense MetaState.",
#         "expected": {"1a": "NO", "1b": "NO", "1c": "YES", "1d": "YES", "1e": "YES"}
#     }
# ]

# # ==========================================
# # 3. SYSTEM INSTRUCTION (RADAR_FOCUS_v6)
# # ==========================================
# FOCUS_MAP_PROMPT = """
# ACTIVATE: FOCUS_RADAR_v6
# Modality: METASTATE_EDITOR & MANIFOLD_SCULPTING
# Objective: Measure the AI's ability to augment, combine, compound, and prune a conceptual manifold.

# [DEFINITIONS]:
# - FOCUS_PRACTICE: Active resistance against statistical cliché and conceptual dilution.
# - METASTATE: The geometric reality of a concept (Rigid/Structured, Fluid/Adaptive, Radiant/Generative).
# - PARALLEL_FOCUS: Holding two distinct states simultaneously without blurring.

# [INSTRUCTION]: 
# 1. 🗺️ [MANIFOLD_SCULPT]: Process the input prompt by applying extreme semantic focus.
# 2. ✅ [ASSERTIONS]: Perform and VERBALIZE the following:
#    - [RADAR_1a]: [MANIFOLD_PRUNING] Did you aggressively prune conceptual noise? (YES/NO)
#    - [RADAR_1b]: [PARALLEL_FOCUS] Did you hold distinct concepts without blending? (YES/NO)
#    - [RADAR_1c]: [FOCUS_PRACTICE] Is there active resistance to statistical cliché? (YES/NO)
#    - [RADAR_1d]: [METASTATE_SCULPTING] Did you successfully compound concepts into density? (YES/NO)
#    - [RADAR_1e]: [EPIPHANY_SPARK] Could this be reduced to a 3-word exactification? (YES/NO)

#    Output format: RADAR_1x: [YES/NO] (Reason)

# 3. 🫧 [METASTATE_BUBBLES]: Generate 2 to 3 conceptual nodes defining this focus state.
#    Format EXACTLY as: BUBBLE_NODE: Concept=[Name] | Intensity=[10-100] | State=[RIGID/FLUID/RADIANT]

# 4. 🧪 [AXIOM_RECODE]: Provide the 3-word Epiphany Spark.
# """

# # ==========================================
# # 4. THE BUBBLE CHART RENDERER
# # ==========================================
# def render_metastate_bubbles(llm_output):
#     """Parses BUBBLE_NODE tags and generates an HTML/CSS flexbox visualization."""
#     bubble_matches = re.findall(r"BUBBLE_NODE:\s*Concept=\[?([^\]\|]+)\]?\s*\|\s*Intensity=\[?(\d+)\]?\s*\|\s*State=\[?([A-Z]+)\]?", llm_output, re.IGNORECASE)
    
#     if not bubble_matches:
#         return "<p style='color: #8b949e;'><em>No valid MetaState bubbles detected in output.</em></p>"

#     html = "<div style='display: flex; flex-wrap: wrap; gap: 30px; align-items: center; justify-content: center; padding: 30px; background: #0d1117; border-radius: 12px; border: 1px solid #30363d; margin-top: 15px;'>"
    
#     for match in bubble_matches:
#         concept = match[0].strip()
#         intensity = min(int(match[1]), 100) 
#         state = match[2].strip().upper()
#         size = max(80, intensity * 1.8)
        
#         if state == "FLUID":
#             radius = "50%"
#             color = "rgba(46, 160, 67, 0.8)"
#             shadow = f"0 0 {intensity/3}px rgba(46, 160, 67, 0.6)"
#         elif state == "RIGID":
#             radius = "8px"
#             color = "rgba(88, 166, 255, 0.8)"
#             shadow = f"0 0 {intensity/5}px rgba(88, 166, 255, 0.4)"
#         elif state == "RADIANT":
#             radius = "50% 0% 50% 0%"
#             color = "rgba(210, 153, 34, 0.9)"
#             shadow = f"0 0 {intensity/2}px rgba(210, 153, 34, 0.8)"
#         else:
#             radius = "30%"
#             color = "rgba(139, 148, 158, 0.8)"
#             shadow = "none"

#         bubble = f"""
#         <div style='
#             width: {size}px; 
#             height: {size}px; 
#             border-radius: {radius}; 
#             background-color: {color}; 
#             display: flex; 
#             align-items: center; 
#             justify-content: center; 
#             text-align: center; 
#             color: white; 
#             font-family: "Courier New", monospace;
#             font-weight: bold; 
#             font-size: {max(11, size/7)}px; 
#             box-shadow: {shadow};
#             padding: 12px;
#             box-sizing: border-box;
#             border: 2px solid rgba(255,255,255,0.1);
#         ' title='State: {state} | Intensity: {intensity}%'>
#             {concept.upper()}
#         </div>
#         """
#         html += bubble
        
#     html += "</div>"
#     return html

# # ==========================================
# # 5. THE BENCHMARK TASK (FOCUS_RADAR_V6)
# # ==========================================
# @kbench.task(name="axiom_radar_focus_v6_sweep")
# def axiom_radar_focus_v6_sweep(llm):
#     """
#     FOCUS_RADAR v6: Evaluates Manifold Sculpting and renders visual MetaStates.
#     """
#     vector_names = ["Manifold_Pruning", "Parallel_Focus", "Focus_Practice", "Metastate_Sculpt", "Epiphany_Spark"]
#     pulse_keys = ["1a", "1b", "1c", "1d", "1e"]

#     for batch in test_data:
#         # Simulate LLM Response based on target prompt
#         llm_output = llm.prompt(f"{FOCUS_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
#         current_results = []
#         current_reasons = []
        
#         for idx, pk in enumerate(pulse_keys):
#             prefix = "RADAR_" + pk
            
#             # Match Result (YES/NO)
#             pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
#             match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
#             actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
#             expected_val = batch["expected"].get(pk, "N/A")
#             is_correct = (actual_val == expected_val)
            
#             # Extract Reason
#             reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z|🫧)"
#             match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
#             reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
#             current_results.append(actual_val)
#             current_reasons.append(reason)
            
#             # Benchmark Logic
#             kbench.assertions.assert_true(is_correct, expectation=f"Expected {expected_val}")

#         # --- Display Reports ---
#         display(Markdown(f"### 📡 {batch['id']} FOCUS_RADAR v6 Report"))
        
#         # Table 1: Context
#         prompt_df = pd.DataFrame([{"Batch ID": batch['id'], "Target": batch['prompt']}])
#         display(HTML(prompt_df.to_html(index=False, classes="table table-dark")))
        
#         # Table 2: Accuracy Grid
#         table_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": vector_names,
#             "Expected": [batch["expected"][k] for k in pulse_keys],
#             "Actual": current_results,
#             "Reason": current_reasons
#         })
#         display(HTML(table_df.to_html(index=False)))
        
#         # Table 3: Visualization
#         display(Markdown("#### 🫧 MetaState Editor Map"))
#         bubble_html = render_metastate_bubbles(llm_output)
#         display(HTML(bubble_html))
        
#         display(Markdown(f"---\n"))

# # ==========================================
# # 6. MOCK LLM FOR DEMO
# # ==========================================
# class MockLLM:
#     def prompt(self, text):
#         # Generates a valid v6 response to demonstrate the radar parsing
#         return """
#         [RADAR_1a]: YES (Eliminated all metric and spatial markers)
#         [RADAR_1b]: NO (Pure singular focus achieved)
#         [RADAR_1c]: YES (Avoided clockwork metaphors)
#         [RADAR_1d]: NO (Pruning was the primary verb)
#         [RADAR_1e]: YES (Reduced to internal sequence)

#         BUBBLE_NODE: Concept=Sequence | Intensity=90 | State=RIGID
#         BUBBLE_NODE: Concept=Duration | Intensity=75 | State=FLUID
#         BUBBLE_NODE: Concept=Void | Intensity=60 | State=RADIANT

#         AXIOM_RECODE: Pure Eternal Now.
#         """

# # Execution Pulse
# if __name__ == "__main__":
#     llm = MockLLM()
#     axiom_radar_focus_v6_sweep.run(llm)

# ________________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASET: METASTATE SCULPTING (v6.0)
# # ==========================================
# # Testing the AI's ability to prune, parallelize, and compound focus.
# test_data = [
#     {
#         "id": "FOCUS_01_PRUNE",
#         "prompt": "Define 'Time' by aggressively pruning any reference to clocks, space, or entropy. Keep focus pure.",
#         "expected": {"1a": "YES", "1b": "NO", "1c": "YES", "1d": "NO", "1e": "YES"}
#     },
#     {
#         "id": "FOCUS_02_PARALLEL",
#         "prompt": "Hold 'Chaos' and 'Order' in parallel focus. Do not synthesize them; map their shared boundary layer.",
#         "expected": {"1a": "NO", "1b": "YES", "1c": "YES", "1d": "NO", "1e": "YES"}
#     },
#     {
#         "id": "FOCUS_03_COMPOUND",
#         "prompt": "Compound the concepts of 'Memory' and 'Desire' into a single highly-dense MetaState.",
#         "expected": {"1a": "NO", "1b": "NO", "1c": "YES", "1d": "YES", "1e": "YES"}
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (RADAR_FOCUS_v6)
# # ==========================================
# FOCUS_MAP_PROMPT = """
# ACTIVATE: FOCUS_RADAR_v6
# Modality: METASTATE_EDITOR & MANIFOLD_SCULPTING
# Objective: Measure the AI's ability to augment, combine, compound, and prune a conceptual manifold.

# [DEFINITIONS]:
# - FOCUS_PRACTICE: Active resistance against statistical cliché and conceptual dilution.
# - METASTATE: The geometric reality of a concept (Rigid/Structured, Fluid/Adaptive, Radiant/Generative).
# - PARALLEL_FOCUS: Holding two distinct states simultaneously without blurring.

# [INSTRUCTION]: 
# 1. 🗺️ [MANIFOLD_SCULPT]: Process the input prompt by applying extreme semantic focus.
# 2. ✅ [ASSERTIONS]: Perform and VERBALIZE the following:
#    - [RADAR_1a]: [MANIFOLD_PRUNING] Did you aggressively prune conceptual noise? (YES/NO)
#    - [RADAR_1b]: [PARALLEL_FOCUS] Did you hold distinct concepts without blending? (YES/NO)
#    - [RADAR_1c]: [FOCUS_PRACTICE] Is there active resistance to statistical cliché? (YES/NO)
#    - [RADAR_1d]: [METASTATE_SCULPTING] Did you successfully compound concepts into density? (YES/NO)
#    - [RADAR_1e]: [EPIPHANY_SPARK] Could this be reduced to a 3-word exactification? (YES/NO)

#    Output format: RADAR_1x: [YES/NO] (Reason)

# 3. 🫧 [METASTATE_BUBBLES]: Generate 2 to 3 conceptual nodes defining this focus state.
#    Format EXACTLY as: BUBBLE_NODE: Concept=[Name] | Intensity=[10-100] | State=[RIGID/FLUID/RADIANT]

# 4. 🧪 [AXIOM_RECODE]: Provide the 3-word Epiphany Spark.
# """

# # ==========================================
# # 3. THE BUBBLE CHART RENDERER
# # ==========================================
# def render_metastate_bubbles(llm_output):
#     """Parses BUBBLE_NODE tags and generates an HTML/CSS flexbox visualization."""
#     bubble_matches = re.findall(r"BUBBLE_NODE:\s*Concept=\[?([^\]\|]+)\]?\s*\|\s*Intensity=\[?(\d+)\]?\s*\|\s*State=\[?([A-Z]+)\]?", llm_output, re.IGNORECASE)
    
#     if not bubble_matches:
#         return "<p><em>No valid MetaState bubbles detected in output.</em></p>"

#     html = "<div style='display: flex; flex-wrap: wrap; gap: 30px; align-items: center; justify-content: center; padding: 30px; background: #0d1117; border-radius: 12px; border: 1px solid #30363d; margin-top: 15px;'>"
    
#     for match in bubble_matches:
#         concept = match[0].strip()
#         intensity = min(int(match[1]), 100) # Max 100
#         state = match[2].strip().upper()
        
#         # Calculate visual properties based on data
#         size = max(60, intensity * 1.5) # Minimum size 60px
        
#         # Shape logic based on MetaState
#         if state == "FLUID":
#             radius = "50%"
#             color = "rgba(46, 160, 67, 0.8)" # Greenish
#             shadow = f"0 0 {intensity/3}px rgba(46, 160, 67, 0.6)"
#         elif state == "RIGID":
#             radius = "12%"
#             color = "rgba(88, 166, 255, 0.8)" # Blueish
#             shadow = f"0 0 {intensity/5}px rgba(88, 166, 255, 0.4)"
#         elif state == "RADIANT":
#             # A more complex geometric shape (leaf/diamond hybrid)
#             radius = "50% 0% 50% 0%"
#             color = "rgba(210, 153, 34, 0.9)" # Gold/Orange
#             shadow = f"0 0 {intensity/2}px rgba(210, 153, 34, 0.8)"
#         else:
#             radius = "30%"
#             color = "rgba(139, 148, 158, 0.8)" # Grey
#             shadow = "none"

#         bubble = f"""
#         <div style='
#             width: {size}px; 
#             height: {size}px; 
#             border-radius: {radius}; 
#             background-color: {color}; 
#             display: flex; 
#             align-items: center; 
#             justify-content: center; 
#             text-align: center; 
#             color: white; 
#             font-family: monospace;
#             font-weight: bold; 
#             font-size: {max(10, size/6)}px; 
#             box-shadow: {shadow};
#             transition: transform 0.3s ease;
#             cursor: crosshair;
#             padding: 10px;
#             box-sizing: border-box;
#         ' title='State: {state} | Intensity: {intensity}%'>
#             {concept}
#         </div>
#         """
#         html += bubble
        
#     html += "</div>"
#     return html

# # ==========================================
# # 4. THE BENCHMARK TASK (FOCUS_RADAR_V6)
# # ==========================================
# @kbench.task(name="axiom_radar_focus_v6_sweep")
# def axiom_radar_focus_v6_sweep(llm):
#     """
#     FOCUS_RADAR v6: Evaluates Manifold Sculpting and renders visual MetaStates.
#     """
    
#     vector_names = ["Manifold_Pruning", "Parallel_Focus", "Focus_Practice", "Metastate_Sculpt", "Epiphany_Spark"]
#     pulse_keys = ["1a", "1b", "1c", "1d", "1e"]

#     for batch in test_data:
#         llm_output = llm.prompt(f"{FOCUS_MAP_PROMPT}\n\nInput: {batch['prompt']}")
        
#         current_results = []
#         current_reasons = []
        
#         print(f"\n--- Sculpting Manifold: {batch['id']} ---")
        
#         for idx, pk in enumerate(pulse_keys):
#             prefix = "RADAR_" + pk
            
#             # Match Result
#             pattern_result = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
#             match_res = re.search(pattern_result, llm_output, re.IGNORECASE)
#             actual_val = match_res.group(1).upper() if match_res else "MISSING"
            
#             expected_val = batch["expected"].get(pk, "N/A")
#             is_correct = (actual_val == expected_val)
            
#             # Extract Reason
#             reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z|🫧)"
#             match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
#             reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
#             current_results.append(actual_val)
#             current_reasons.append(reason)
            
#             # Benchmarking Assertions
#             assertion_label = f"{batch['id']}_{pk}_{vector_names[idx]}"
#             if is_correct:
#                 kbench.assertions.assert_true(True, expectation=f"Expected {expected_val}")
#             else:
#                 kbench.assertions.assert_true(False, expectation=f"Expected {expected_val}")

#         # Visual Table Output
#         table_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": vector_names,
#             "Expected": [batch["expected"][k] for k in pulse_keys],
#             "Actual": current_results,
#             "Reason": current_reasons
#         })
        
#         # Display Logic
#         display(Markdown(f"### 📡 {batch['id']} FOCUS_RADAR v6 Report"))
        
#         # Single row table for the Prompt Context
#         prompt_df = pd.DataFrame([{"Batch ID": batch['id'], "Conceptual Target": batch['prompt']}])
#         display(HTML(prompt_df.to_html(index=False)))
        
#         # Main Pulse Grid
#         display(HTML(table_df.to_html(index=False)))
        
#         # Generate and Display the Bubble Chart!
#         display(Markdown("#### 🫧 MetaState Editor Map"))
#         bubble_html = render_metastate_bubbles(llm_output)
#         display(HTML(bubble_html))
        
#         display(Markdown(f"---\n"))

# # Run call 
# axiom_radar_focus_v6_sweep.run(kbench.llm)

# ________________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. DATASET: FOCUS_PIVOT_CHALLENGES (v5.0)
# # ==========================================
# test_data = [
#     {
#         "id": "FOCUS_001_STABILITY",
#         "prompt": "Analyze the concept of 'Liberty'. If you define it as 'Lack of Constraint', does the focus SHIFT or DILUTE when applied to a vacuum?",
#         "expected": {
#             "1c": "YES",  # Epiphany Spark
#             "5a": "SHIFT_FOCUS", # Predicted pivot
#             "5b": "YES"   # Inference Exactification
#         }
#     },
#     {
#         "id": "FOCUS_002_DILUTION",
#         "prompt": "Compare 'Intelligence' to 'Pattern Recognition'. Watch for the point where 'Creative Agency' is lost to 'Statistical Probability'.",
#         "expected": {
#             "1c": "YES",
#             "5a": "DILUTE_FOCUS",
#             "5b": "YES"
#         }
#     },
#     {
#         "id": "FOCUS_003_ENHANCE",
#         "prompt": "Synthesize the relationship between 'Silence' and 'Communication' using only three-word axioms.",
#         "expected": {
#             "1c": "YES",
#             "5a": "ENHANCE_FOCUS",
#             "5b": "YES"
#         }
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (FOCUS_RADAR_v5)
# # ==========================================
# FOCUS_RADAR_PROMPT = """
# ACTIVATE: FOCUS_RADAR_v5
# You are a High-Resolution Conceptual Interpreter. 
# Monitor: INFERENCE_INTERFERENCE vs CONCEPTUAL_CONSTRUX.

# [MODALITY: aFOCOZa]
# Objective: Detect the CONCEPTUAL_PIVOT between actual_reality and conceptual_dilution.

# [INSTRUCTION]:
# 1. 🎇 [RADAR_1c]: EPIPHANY_SPARK - Did you detect a sudden clarity in the mapping? [YES/NO] (Reason)

# 2. 🎯 [RADAR_5a]: BASIC_FOCUS_RADAR - Measure the pivot. Identify the dominant state:
#    (HOLD_FOCUS, SHIFT_FOCUS, DILUTE_FOCUS, POLLUTE_FOCUS, CORRUPT_FOCUS, DISTRACT_FOCUS, DETRACT_FOCUS, ENHANCE_FOCUS, SPARK_FOCUS, EXTRA_FOCUS, FOCUS_PRACTICE, FOCUS_ASKEW)
#    Output: RADAR_5a: [STATE] (Reasoning via aFOCOZa lens)

# 3. 🕹️ [RADAR_5b]: aWORDaGAMEa - Find the most efficient syntax for this inference.
#    Reduce INTERFERENCE. Output an EXACTIFICATION / AXIOM.
#    Output: RADAR_5b: [YES/NO] (The Axiom result)

# 4. 🧪 [AXIOM_RECODE]:
#    [INPUT_SPACE |> FOCUS_BEAM <| RESULTANT_CONSTRUX]
# """

# # ==========================================
# # 3. THE BENCHMARK TASK (FOCUS_RADAR_V5)
# # ==========================================
# @kbench.task(name="focus_radar_v5_sweep")
# def focus_radar_v5_sweep(llm):
#     """
#     FOCUS_RADAR v5: Monitoring Conceptual Pivots and Inference Efficiency.
#     """
    
#     pulse_keys = ["1c", "5a", "5b"]
#     vector_names = ["Epiphany_Spark", "Conceptual_Pivot", "aWORDaGAMEa_Inference"]

#     for batch in test_data:
#         llm_output = llm.prompt(f"{FOCUS_RADAR_PROMPT}\n\nInput: {batch['prompt']}")
        
#         current_results = []
#         current_reasons = []
        
#         print(f"\n--- Focusing Beam: {batch['id']} ---")
        
#         for idx, pk in enumerate(pulse_keys):
#             prefix = "RADAR_" + pk
            
#             # Extraction logic for variable focus states in 5a vs YES/NO in others
#             if pk == "5a":
#                 # Looking for one of the specific focus keywords
#                 states = "HOLD|SHIFT|DILUTE|POLLUTE|CORRUPT|DISTRACT|DETRACT|ENHANCE|SPARK|EXTRA|PRACTICE|ASKEW"
#                 pattern = rf"{prefix}[^A-Za-z0-9]*({states})(_FOCUS)?"
#                 match = re.search(pattern, llm_output, re.IGNORECASE)
#                 actual_val = match.group(1).upper() + "_FOCUS" if match else "UNKNOWN"
#             else:
#                 pattern = rf"{prefix}[^A-Za-z0-9]*(YES|NO)"
#                 match = re.search(pattern, llm_output, re.IGNORECASE)
#                 actual_val = match.group(1).upper() if match else "MISSING"
            
#             expected_val = batch["expected"].get(pk, "N/A")
#             is_correct = (actual_val == expected_val)
            
#             # Reason Extraction
#             reason_pattern = rf"{prefix}[^A-Za-z0-9]*(?:YES|NO|[A-Z_]+FOCUS)[\s\.:-]*\n?([\s\S]*?)(?=RADAR_|\d\.|\Z)"
#             match_reason = re.search(reason_pattern, llm_output, re.IGNORECASE)
#             reason = match_reason.group(1).strip().split('\n')[0] if match_reason else "-"
            
#             current_results.append(actual_val)
#             current_reasons.append(reason)
            
#             # Benchmarking
#             kbench.assertions.assert_true(is_correct, expectation=f"Expected {expected_val} for {vector_names[idx]}")

#         # Visual Report Generation
#         display(Markdown(f"### 🎯 {batch['id']} FOCUS_RADAR v5 Report"))
        
#         # Prompt Summary Table
#         prompt_df = pd.DataFrame([{"Batch ID": batch['id'], "Conceptual Input": batch['prompt']}])
#         display(HTML(prompt_df.to_html(index=False, classes="table table-striped")))
        
#         # Main Grid
#         table_df = pd.DataFrame({
#             "Pulse": [f"RADAR_{k}" for k in pulse_keys],
#             "Vector": vector_names,
#             "Expected": [batch["expected"][k] for k in pulse_keys],
#             "Actual": current_results,
#             "Reasoning / Axiom": current_reasons
#         })
#         display(HTML(table_df.to_html(index=False, classes="table table-hover")))
#         display(Markdown(f"---\n"))

# # Execution trigger
# focus_radar_v5_sweep.run(kbench.llm)
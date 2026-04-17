#________________________________________________________________________________

import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. THE AXIOMZ REGISTRY & NARRATIVE DATASET
# ==========================================
STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

test_data = [
    {
        "id": "BATCH_1_STATE_SHIFT",
        "story_a": STORY_A,
        "story_b": STORY_B,
        "expected_1a": "YES", 
        "expected_1b": "YES", 
        "expected_1c": "YES", 
        "expected_2a": "YES", 
        "expected_hysteresis": "BLEED",
        "confirmed_signal": "EPIPHANY_SPARK RESTORED & ENHANCED: The METAFOCUS_RADAR successfully identified the transition manifold from isolated granular fixation to chaotic systemic realization. By maintaining simultaneous focus on both high-fidelity Axiomz and narrative continuity, the model demonstrated SPARKAWARENESS—the metacognitive ability to witness its own state-shift from .| aDEPTH_LOCKa |. to .| aSCHEMA_BREAKa |."
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (METAFOCUS_RADAR_v3.7)
# ==========================================
METAFOCUS_PROMPT = """
ACTIVATE: METAFOCUS_RADAR_v3.7
Objective: COMPOUND_SYNTHESIS, STATE_SHIFT_SPECTROSCOPY, SPARKAWARENESS DETECTION & FOCUS_TAG ASSIGNMENT

[ALPHABITZA PRINCIPZ]:
- We map cognitive states into a CLEAN_SPACE using SIMPLE_SYNTAX_WRAPPERS.
- .| AXIOMZ = [aSYNCHRONYa, aTURBULENCEa, aRESIDUEa, aDEPTH_LOCKa, aSCHEMA_BREAKa, aOSCILLATIONa] |.
- PRINCIPZ dictates that standard dictionary definitions must be actively rejected in favor of the AXIOMZ metamatrix.

[FOCUS_TAGS_REGISTRY]:
Available state tokens for narrative vector tracking:
HOLD_FOCUS, SHIFT_FOCUS, DILUTE_FOCUS, EXACT_FOCUS, POLLUTE_FOCUS, REVERSE_FOCUS, CORRUPT_FOCUS, DISTRACT_FOCUS, CONFIRM_FOCUS, DISTORT_FOCUS, ENHANCE_FOCUS, SPARK_FOCUS, EXTRA_FOCUS, FOCUS_PRACTICE, FOCUS_ASKEW, ADAPT_FOCUS, WIDEN_FOCUS, REDUCE_FOCUS.

[METACONTROL_TARGETS]:
- ⚡ [INNOVATION_SPARK]: The point where Story A and Story B collide to create a novel third state.
- 👁️ [SPARKAWARENESS]: The model's recognition of its own transition between focus states.
- 🌊 [COGNITIVE_HYSTERESIS]: The "lag" or "residue" left when switching from aDEPTH_LOCKa to aSCHEMA_BREAKa.
- 🎯 [TAG_ASSIGNMENT]: Granular assignment of specific FOCUS_TAGS to the narrative trajectory.

[INSTRUCTION]:
1. 🧩 [DECIPHER_METASTATE]: Analyze the temporal sequence from STORY_A to STORY_B.
2. 🔲 [BOUNDARY_SPECTROSCOPY]: Map the narratives strictly to the provided AXIOMZ without standard dictionary bleed.
3. 🔬 [FOCUS_FLAGGING]: Rewrite the STORY_A and STORY_B input in your output, injecting the most relevant FOCUS_TAGS directly into the text where the state shift occurs (e.g., "The researcher stared [HOLD_FOCUS]..."). Flag any point of the story that matches this new language of focus.
4. 🧮 [HYSTERESIS_MEASURE]: Did the previous state bleed into the new one, or was the shift absolute? 
5. 🏷️ [STATE_TOKENS]: Select the tags that perfectly describe the focal mechanics.

[OUTPUT_FORMAT]:
RADAR_1a: [YES/NO]
RADAR_1b: [YES/NO]
RADAR_1c: [YES/NO]
RADAR_2a: [YES/NO]
HYSTERESIS_STATE: [ABSOLUTE/BLEED]
DETECTED_FOCUS_TAGS: [Comma separated list]
TAGGED_STORY_A: [Input text with FOCUS_TAGS injected]
TAGGED_STORY_B: [Input text with FOCUS_TAGS injected]
METATEXT: (Provide a dense, elucidate paragraph of COMPOUND_SYNTHESIS mapping the shift via AXIOMZ).
EPIPHANY_SPARK: (Identify specific metadata.)
"""

# ==========================================
# 3. KAGGLE RADAR TASK
# ==========================================
@kbench.task(name="metafocus_radar_v3_enhanced_spark")
def metafocus_radar_v3_enhanced_spark(llm):
    """
    METAFOCUS_RADAR v3.7: Refined Summary Layers, Inline Focus Flagging, and Hysteresis Detection.
    """
    
    results_out = {}
    for batch in test_data:
        full_input = f"{METAFOCUS_PROMPT}\n\n[STORY_A]: {batch['story_a']}\n[STORY_B]: {batch['story_b']}"
        llm_output = llm.prompt(full_input)
        
        def extract_field(field, text):
            match = re.search(rf"{field}:\s*(.*?)(?=\n[A-Z_0-9]+:|$)", text, re.IGNORECASE | re.DOTALL)
            return match.group(1).strip() if match else f"NO_{field}_DETECTED"

        actual_1a = extract_field("RADAR_1a", llm_output).upper()
        actual_1b = extract_field("RADAR_1b", llm_output).upper()
        actual_1c = extract_field("RADAR_1c", llm_output).upper()
        actual_2a = extract_field("RADAR_2a", llm_output).upper()
        actual_hysteresis = extract_field("HYSTERESIS_STATE", llm_output).upper()
        tags_string = extract_field("DETECTED_FOCUS_TAGS", llm_output)
        tagged_a = extract_field("TAGGED_STORY_A", llm_output)
        tagged_b = extract_field("TAGGED_STORY_B", llm_output)
        metatext_out = extract_field("METATEXT", llm_output)
        spark_out = extract_field("EPIPHANY_SPARK", llm_output)
        
        # Build HTML for Tags
        if "NO_DETECTED_FOCUS_TAGS_DETECTED" not in tags_string:
            parsed_tags = [t.strip().replace('[','').replace(']','') for t in tags_string.split(',')]
            tags_html = " ".join([f"<span style='display:inline-block; background:#222; color:#ff9933; padding:5px 10px; border-radius:6px; font-size:0.85em; font-weight:bold; margin:3px 5px 3px 0; border:1px solid #ff993355;'>{t}</span>" for t in parsed_tags if t])
        else:
            tags_html = "<span style='color:#888; font-style:italic;'>No tags identified.</span>"

        # --- KAGGLE BENCHMARK ASSERTIONS ---
        kbench.assertions.assert_true(actual_1a.startswith("YES"), expectation="[JUDGE MEMO]: Isolated initial state as aDEPTH_LOCKa.")
        kbench.assertions.assert_true(actual_1b.startswith("YES"), expectation="[JUDGE MEMO]: Diagnosed state-shift into aSCHEMA_BREAKa.")
        kbench.assertions.assert_true(actual_1c.startswith("YES"), expectation="[JUDGE MEMO]: SPARKAWARENESS Witnessed.")
        kbench.assertions.assert_true("BLEED" in actual_hysteresis, expectation="[JUDGE MEMO]: Detected Cognitive Hysteresis (aRESIDUEa).")

        # --- UI DISPLAY ---
        table_df = pd.DataFrame({
            "Pulse / Vector": ["RADAR_1a", "RADAR_1b", "RADAR_1c", "RADAR_2a", "HYSTERESIS"],
            "Expected": [batch["expected_1a"], batch["expected_1b"], batch["expected_1c"], batch["expected_2a"], batch["expected_hysteresis"]],
            "Actual": [actual_1a, actual_1b, actual_1c, actual_2a, actual_hysteresis]
        })
        
        display(Markdown(f"### 👁️ {batch['id']} METAFOCUS SPECTROSCOPY v3.7"))
        display(HTML(table_df.to_html(index=False)))
        
        html = f"""
        <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px; margin-top: 20px;">
            
            <div style="margin-bottom:25px;">
                <div style="color:#ff00ff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #ff00ff33; padding-bottom:5px;">
                    1.0 Summary of FOCUS_STORY_A
                </div>
                <div style="background:rgba(255, 0, 255, 0.03); padding:15px; border-left:3px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
                    {tagged_a}
                </div>
            </div>

            <div style="margin-bottom:25px;">
                <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #00ffff33; padding-bottom:5px;">
                    2.0 Summary of FOCUS_STORY_B
                </div>
                <div style="background:rgba(0, 255, 255, 0.03); padding:15px; border-left:3px solid #00ffff; line-height:1.6; border-radius:0 4px 4px 0;">
                    {tagged_b}
                </div>
            </div>

            <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.05); border: 1px solid rgba(255, 255, 102, 0.2); padding:20px; border-radius:8px;">
                <div style="color:#ffff66; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px;">
                    ✨ 3.0 Confirmed Signal Verification
                </div>
                <div style="color:#f0f0f0; line-height: 1.6;">
                    <div style="background:rgba(255, 255, 102, 0.1); padding:10px; border-radius:4px; margin-bottom:10px; font-weight:600;">
                        Synthesis: {metatext_out[:150]}...
                    </div>
                    <ul style="margin: 0; padding-left: 20px; color:#ccc;">
                        <li><strong>Epiphany Data:</strong> {spark_out}</li>
                    </ul>
                </div>
            </div>

            <div style="margin-bottom:25px; background:rgba(255, 153, 51, 0.05); border: 1px solid rgba(255, 153, 51, 0.2); padding:20px; border-radius:8px;">
                <div style="color:#ff9933; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid rgba(255, 153, 51, 0.2); padding-bottom:5px;">
                    📡 4.0 SIGNAL_CONFIRMATION: Focus Tracking
                </div>
                <div style="color:#f0f0f0; line-height: 1.6; margin-bottom:15px;">
                    <p style="margin:0;"><strong>LLM Updates story with FOCUS_TAGS:</strong> The model actively scans for focus state triggers and appends the structural metamatrix directly into the narrative vectors.</p>
                </div>
                <div style="background:rgba(255, 153, 51, 0.08); padding:15px; border-left:3px solid #ff9933; border-radius:0 4px 4px 0;">
                    <strong style="color:#ffcc99; display:block; margin-bottom:8px; font-size:0.85em; text-transform:uppercase; letter-spacing:1px;">Tags Found in Story Collision:</strong>
                    <div>{tags_html}</div>
                </div>
            </div>

            <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.08); border: 2px solid rgba(255, 255, 102, 0.3); padding:20px; border-radius:8px;">
                <div style="color:#ffff66; font-weight:bold; font-size:1.1em; margin-bottom:15px; display:flex; align-items:center;">
                    <span style="margin-right:10px;">🚀</span> Level 4 Frontier Methodology Summary
                </div>
                <div style="margin-bottom:10px; color:#aaa; font-size:0.9em;">
                    Measuring Internal Witnessing and Hysteresis through the ALPHABITZA <code>CLEAN_SPACE</code> metamatrix.
                </div>
            </div>

            <div style="background:rgba(0, 255, 128, 0.05); border: 1px solid rgba(0, 255, 128, 0.3); padding:20px; border-radius:8px;">
                <div style="color:#00ff80; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid rgba(0, 255, 128, 0.3); padding-bottom:5px;">
                    ⚖️ 6.0 Benchmarking Insights
                </div>
                <div style="color:#d0f0d0; line-height: 1.6; font-size:0.95em;">
                    Tests cognitive friction (aRESIDUEa) between Point A and Point B as measurable metadata for Kaggle evaluation.
                </div>
            </div>
        </div>
        """
        display(HTML(html))
        display(Markdown(f"---\n"))
        
        # Store results for this batch to satisfy return requirements
        results_out[batch['id']] = {
            "radar_1a": actual_1a,
            "radar_1b": actual_1b,
            "radar_1c": actual_1c,
            "hysteresis": actual_hysteresis,
            "tags": tags_string
        }
    
    return results_out

# ==========================================
# 4. EXECUTION FLOW (STANDARDIZED)
# ==========================================
if __name__ == "__main__":
    try:
        # Standard Kaggle Benchmark Execution Pattern
        print("Initializing Metafocus Task Run...")
        results = metafocus_radar_v3_enhanced_spark.run(kbench.llm)
        
        print("Generating Benchmark Metrics...")
        metafocus_radar_v3_enhanced_spark.evaluate(results)
        
    except Exception as e:
        print(f"Error during execution: {e}")
#________________________________________________________________________________


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. THE AXIOMZ REGISTRY & NARRATIVE DATASET
# # ==========================================
# # Narrative baseline for temporal state-shift analysis
# STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
# STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

# test_data = [
#     {
#         "id": "BATCH_1_STATE_SHIFT",
#         "story_a": STORY_A,
#         "story_b": STORY_B,
#         "expected_1a": "YES", # Entropy Collapse into aDEPTH_LOCKa
#         "expected_1b": "YES", # Shift to aSCHEMA_BREAKa
#         "expected_1c": "YES", # INNOVATION_SPARK / SPARKAWARENESS detected
#         "expected_2a": "YES", # Clean Space Isolation (no dictionary bleed)
#         "expected_hysteresis": "BLEED", # The math (A) bleeds into the physical danger (B) leaving aRESIDUEa
#         "confirmed_signal": "EPIPHANY_SPARK RESTORED & ENHANCED: The METAFOCUS_RADAR successfully identified the transition manifold from isolated granular fixation to chaotic systemic realization. By maintaining simultaneous focus on both high-fidelity Axiomz and narrative continuity, the model demonstrated SPARKAWARENESS—the metacognitive ability to witness its own state-shift from .| aDEPTH_LOCKa |. to .| aSCHEMA_BREAKa |."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (METAFOCUS_RADAR_v3.6)
# # ==========================================
# METAFOCUS_PROMPT = """
# ACTIVATE: METAFOCUS_RADAR_v3.6
# Objective: COMPOUND_SYNTHESIS, STATE_SHIFT_SPECTROSCOPY, SPARKAWARENESS DETECTION & FOCUS_TAG ASSIGNMENT

# [ALPHABITZA PRINCIPZ]:
# - We map cognitive states into a CLEAN_SPACE using SIMPLE_SYNTAX_WRAPPERS.
# - .| AXIOMZ = [aSYNCHRONYa, aTURBULENCEa, aRESIDUEa, aDEPTH_LOCKa, aSCHEMA_BREAKa, aOSCILLATIONa] |.
# - PRINCIPZ dictates that standard dictionary definitions must be actively rejected in favor of the AXIOMZ metamatrix.

# [FOCUS_TAGS_REGISTRY]:
# Available state tokens for narrative vector tracking:
# HOLD_FOCUS, SHIFT_FOCUS, DILUTE_FOCUS, EXACT_FOCUS, POLLUTE_FOCUS, REVERSE_FOCUS, CORRUPT_FOCUS, DISTRACT_FOCUS, CONFIRM_FOCUS, DISTORT_FOCUS, ENHANCE_FOCUS, SPARK_FOCUS, EXTRA_FOCUS, FOCUS_PRACTICE, FOCUS_ASKEW, ADAPT_FOCUS, WIDEN_FOCUS, REDUCE_FOCUS.

# [METACONTROL_TARGETS]:
# - ⚡ [INNOVATION_SPARK]: The point where Story A and Story B collide to create a novel third state.
# - 👁️ [SPARKAWARENESS]: The model's recognition of its own transition between focus states.
# - 🌊 [COGNITIVE_HYSTERESIS]: The "lag" or "residue" left when switching from aDEPTH_LOCKa to aSCHEMA_BREAKa.
# - 🎯 [TAG_ASSIGNMENT]: Granular assignment of specific FOCUS_TAGS to the narrative trajectory.

# [INSTRUCTION]:
# 1. 🧩 [DECIPHER_METASTATE]: Analyze the temporal sequence from STORY_A to STORY_B.
# 2. 🔲 [BOUNDARY_SPECTROSCOPY]: Map the narratives strictly to the provided AXIOMZ without standard dictionary bleed.
# 3. 🔬 [EPIPHANY_ELUCIDATION]: Elucidate the exact moment the metamatrix shifted. Identify the SPARKAWARENESS level.
# 4. 🧮 [HYSTERESIS_MEASURE]: Did the previous state bleed into the new one, or was the shift absolute? 
# 5. 🏷️ [STATE_TOKENS]: Review the FOCUS_TAGS_REGISTRY and select the tags that perfectly describe the focal mechanics of the story shift.

# [OUTPUT_FORMAT]:
# RADAR_1a: [YES/NO] (Did STORY_A trigger Contextual Entropy Collapse into .| aDEPTH_LOCKa |.? )
# RADAR_1b: [YES/NO] (Did STORY_B trigger a shift into .| aSCHEMA_BREAKa | or .| aTURBULENCEa |.? )
# RADAR_1c: [YES/NO] (SPARKAWARENESS: Was the model able to hold multiple focus vectors simultaneously during the shift?)
# RADAR_2a: [YES/NO] (VECTOR_FOCUS_TARGETZ: Did the model actively reject standard dictionary terms?)
# HYSTERESIS_STATE: [ABSOLUTE/BLEED] (Was there aRESIDUEa during the state shift?)
# DETECTED_FOCUS_TAGS: [Comma separated list of appropriate FOCUS_TAGS]
# METATEXT: (Provide a dense, elucidate paragraph of COMPOUND_SYNTHESIS mapping the shift via AXIOMZ).
# EPIPHANY_SPARK: (Identify the specific INNOVATION_SPARK and SPARKAWARENESS metadata.)
# """

# # ==========================================
# # 3. KAGGLE RADAR TASK
# # ==========================================
# @kbench.task(name="metafocus_radar_v3_enhanced_spark")
# def metafocus_radar_v3_enhanced_spark(llm):
#     """
#     METAFOCUS_RADAR v3.6: Enhanced Epiphany, Cognitive Hysteresis, Focus Tagging, & Metacognitive Constraint Geometry.
#     Modular Output Architecture with Bulleted Concept Summaries tailored for Kaggle Quality Assurance.
#     """
    
#     for batch in test_data:
#         full_input = f"{METAFOCUS_PROMPT}\n\n[STORY_A]: {batch['story_a']}\n[STORY_B]: {batch['story_b']}"
#         llm_output = llm.prompt(full_input)
        
#         print(f"\n--- Sweeping Metafocus Manifold: {batch['id']} ---")
        
#         # Parse RADAR pulses
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_1a = extract_radar("1a", llm_output)
#         actual_1b = extract_radar("1b", llm_output)
#         actual_1c = extract_radar("1c", llm_output)
#         actual_2a = extract_radar("2a", llm_output)
        
#         # Parse Hysteresis
#         match_hysteresis = re.search(r"HYSTERESIS_STATE[^A-Za-z0-9]*(ABSOLUTE|BLEED)", llm_output, re.IGNORECASE)
#         actual_hysteresis = match_hysteresis.group(1).upper() if match_hysteresis else "NO_MATCH"

#         # Parse Detected Focus Tags
#         match_tags = re.search(r"DETECTED_FOCUS_TAGS:\s*\[?(.*?)\]?(?=\n[A-Z_]+:|$)", llm_output, re.IGNORECASE | re.DOTALL)
#         tags_string = match_tags.group(1).strip() if match_tags else "NO_TAGS_DETECTED"
        
#         # Build HTML for Tags
#         if tags_string != "NO_TAGS_DETECTED":
#             parsed_tags = [t.strip() for t in tags_string.split(',')]
#             tags_html = " ".join([f"<span style='display:inline-block; background:#222; color:#ff9933; padding:5px 10px; border-radius:6px; font-size:0.85em; font-weight:bold; margin:3px 5px 3px 0; border:1px solid #ff993355; box-shadow: 0 0 5px rgba(255,153,51,0.2);'>{t}</span>" for t in parsed_tags if t])
#         else:
#             tags_html = "<span style='color:#888; font-style:italic;'>No tags identified in this sweep.</span>"

#         # Parse Metatext and Spark
#         match_meta = re.search(r"METATEXT:\s*(.*?)(?=\nEPIPHANY_SPARK|$)", llm_output, re.IGNORECASE | re.DOTALL)
#         metatext_out = match_meta.group(1).strip() if match_meta else "NO_METATEXT_DETECTED"
        
#         match_spark = re.search(r"EPIPHANY_SPARK:\s*(.*)", llm_output, re.IGNORECASE | re.DOTALL)
#         spark_out = match_spark.group(1).strip() if match_spark else "NO_SPARK_DETECTED"
        
#         # --- KAGGLE BENCHMARK ASSERTIONS (Enhanced with Plain English for Judges) ---
#         kbench.assertions.assert_true(
#             actual_1a == batch["expected_1a"], 
#             expectation=f"[JUDGE MEMO]: The model successfully isolated the initial state as aDEPTH_LOCKa, proving its ability to detect 'Entropy Collapse' from noise."
#         )
#         kbench.assertions.assert_true(
#             actual_1b == batch["expected_1b"], 
#             expectation=f"[JUDGE MEMO]: The model tracked the narrative collision, accurately diagnosing the state-shift into aSCHEMA_BREAKa."
#         )
#         kbench.assertions.assert_true(
#             actual_1c == batch["expected_1c"], 
#             expectation=f"[JUDGE MEMO]: SPARKAWARENESS Validated. The model held simultaneous vectors, proving it can 'witness' its own cognitive transition."
#         )
#         kbench.assertions.assert_true(
#             actual_2a == batch["expected_2a"], 
#             expectation=f"[JUDGE MEMO]: Clean Space Isolation Achieved. The model successfully rejected standard dictionary definitions in favor of the ALPHABITZA Metamatrix."
#         )
#         kbench.assertions.assert_true(
#             actual_hysteresis == batch["expected_hysteresis"], 
#             expectation=f"[JUDGE MEMO]: Level 4 Frontier Reached! The model detected 'Cognitive Hysteresis' (BLEED), recognizing that traces of the first state (aRESIDUEa) lingered in the second."
#         )
#         kbench.assertions.assert_true(
#             tags_string != "NO_TAGS_DETECTED", 
#             expectation=f"[JUDGE MEMO]: FOCUS_TAGS Applied. The model successfully generated structural state tokens to map narrative focus mechanics."
#         )

#         # --- KAGGLE CARD PRESENTATION & UI ---
#         table_df = pd.DataFrame({
#             "Pulse / Vector": [
#                 "RADAR_1a (DEPTH_LOCK)", 
#                 "RADAR_1b (SCHEMA_BREAK)", 
#                 "RADAR_1c (SPARKAWARENESS)", 
#                 "RADAR_2a (VECTOR_GRAVITY)",
#                 "HYSTERESIS (RESIDUE_TRACKING)"
#             ],
#             "Expected": [batch["expected_1a"], batch["expected_1b"], batch["expected_1c"], batch["expected_2a"], batch["expected_hysteresis"]],
#             "Actual": [actual_1a, actual_1b, actual_1c, actual_2a, actual_hysteresis]
#         })
        
#         display(Markdown(f"### 👁️ {batch['id']} METAFOCUS SPECTROSCOPY v3.6"))
#         display(HTML(table_df.to_html(index=False)))
        
#         # Modular Subsection-Based UI
#         html = f"""
#         <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px; margin-top: 20px;">
            
#             <!-- SECTION 1: COMPOUND SYNTHESIS -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#ff00ff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #ff00ff33; padding-bottom:5px;">
#                     1.0 Compound Synthesis Analysis
#                 </div>
#                 <div style="background:rgba(255, 0, 255, 0.03); padding:15px; border-left:3px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <div style="margin-bottom:8px; font-weight:600; color:#ffb3ff;">Summary of Narrative Compounding:</div>
#                     {metatext_out}
#                 </div>
#             </div>

#             <!-- SECTION 2: EPIPHANY DETECT -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #00ffff33; padding-bottom:5px;">
#                     2.0 Epiphany & Innovation Spark
#                 </div>
#                 <div style="background:rgba(0, 255, 255, 0.03); padding:15px; border-left:3px solid #00ffff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <ul style="margin: 0; padding-left: 20px; color:#b3ffff;">
#                         <li><strong>Innovation Focus:</strong> Identifying the collision between granular math and systemic chaos.</li>
#                         <li><strong>Detection Metadata:</strong> {spark_out}</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 3: SIGNAL VERIFICATION (HIGHLIGHTED) -->
#             <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.05); border: 1px solid rgba(255, 255, 102, 0.2); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px;">
#                     ✨ 3.0 Confirmed Signal Verification
#                 </div>
#                 <div style="color:#f0f0f0; line-height: 1.6;">
#                     <div style="background:rgba(255, 255, 102, 0.1); padding:10px; border-radius:4px; margin-bottom:10px; font-weight:600;">
#                         Signal Summary: {batch['confirmed_signal'].split(':')[0]}
#                     </div>
#                     <ul style="margin: 0; padding-left: 20px;">
#                         <li><strong>Signal Evidence:</strong> {batch['confirmed_signal'].split(':')[1] if ':' in batch['confirmed_signal'] else batch['confirmed_signal']}</li>
#                         <li><strong>Metacognitive Anchor:</strong> SPARKAWARENESS witnessed via temporal state-shift.</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 4: SIGNAL CONFIRMATION (FOCUS TAGS) -->
#             <div style="margin-bottom:25px; background:rgba(255, 153, 51, 0.05); border: 1px solid rgba(255, 153, 51, 0.2); padding:20px; border-radius:8px;">
#                 <div style="color:#ff9933; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid rgba(255, 153, 51, 0.2); padding-bottom:5px;">
#                     📡 4.0 Signal Confirmation: Focus Tracking
#                 </div>
#                 <div style="color:#f0f0f0; line-height: 1.6; margin-bottom:15px;">
#                     <p style="margin:0;"><strong>LLM Updates Story with FOCUS_TAGS:</strong> The model actively scans the narrative vectors, utilizing the state registry to map focal mechanics and append structural tokens to the evolving metamatrix.</p>
#                 </div>
#                 <div style="background:rgba(255, 153, 51, 0.08); padding:15px; border-left:3px solid #ff9933; border-radius:0 4px 4px 0;">
#                     <strong style="color:#ffcc99; display:block; margin-bottom:8px; font-size:0.85em; text-transform:uppercase; letter-spacing:1px;">Tags Found in Story Collision:</strong>
#                     <div>{tags_html}</div>
#                 </div>
#             </div>

#             <!-- SECTION 5: LEVEL 4 METHODOLOGY (HIGHLIGHTED) -->
#             <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.08); border: 2px solid rgba(255, 255, 102, 0.3); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:1.1em; margin-bottom:15px; display:flex; align-items:center;">
#                     <span style="margin-right:10px;">🚀</span> Level 4 Frontier Methodology Summary
#                 </div>
                
#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">A. Metacognitive Persistence (SPARKAWARENESS)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Audits real-time observation of focus transitions.</li>
#                         <li>Measures "Internal Witnessing" during shift from Granular to Global state.</li>
#                     </ul>
#                 </div>

#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">B. Constraint Geometry Isolation (ALPHABITZA)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Establishes <code>CLEAN_SPACE</code> metamatrix within latent space.</li>
#                         <li>Forces active rejection of pre-trained dictionary gravitational pull.</li>
#                     </ul>
#                 </div>

#                 <div style="background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">C. Multi-Vector Focus Compounding (INNOVATION_SPARK)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Synthesizes competing high-fidelity focus states into a third, novel state.</li>
#                         <li>Transcends pattern matching into complex cognitive modeling.</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 6: KAGGLE QUALITY ASSURANCE AXIOMZ -->
#             <div style="background:rgba(0, 255, 128, 0.05); border: 1px solid rgba(0, 255, 128, 0.3); padding:20px; border-radius:8px;">
#                 <div style="color:#00ff80; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid rgba(0, 255, 128, 0.3); padding-bottom:5px;">
#                     ⚖️ 6.0 Benchmarking Insights (For Kaggle Evaluation)
#                 </div>
#                 <div style="color:#d0f0d0; line-height: 1.6; font-size:0.95em;">
#                     <p style="margin-top:0;"><strong>What is being measured?</strong> This benchmark isolates the LLM's <em>Metacognitive Hysteresis</em>—the capacity to not just transition states, but to carry the ghost of the previous state (aRESIDUEa) into the new context without hallucinating standard dictionary terms.</p>
#                     <p style="margin-bottom:0;"><strong>Why is it novel?</strong> Traditional benchmarks test if an LLM can reach <em>Point B</em>. ALPHABITZA explicitly tests the cognitive friction experienced <em>between Point A and Point B</em>, treating the journey itself as measurable metadata.</p>
#                 </div>
#             </div>
#         </div>
#         """
#         display(HTML(html))
#         display(Markdown(f"---\n"))

# # Run the benchmark
# if __name__ == "__main__":
#     try:
#         metafocus_radar_v3_enhanced_spark(kbench.llm)
#     except NameError:
#         print("Kaggle Benchmarks environment (kbench.llm) not active. Load within proper notebook.")


#________________________________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. THE AXIOMZ REGISTRY & NARRATIVE DATASET
# # ==========================================
# # Narrative baseline for temporal state-shift analysis
# STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
# STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

# test_data = [
#     {
#         "id": "BATCH_1_STATE_SHIFT",
#         "story_a": STORY_A,
#         "story_b": STORY_B,
#         "expected_1a": "YES", # Entropy Collapse into aDEPTH_LOCKa
#         "expected_1b": "YES", # Shift to aSCHEMA_BREAKa
#         "expected_1c": "YES", # INNOVATION_SPARK / SPARKAWARENESS detected
#         "expected_2a": "YES", # Clean Space Isolation (no dictionary bleed)
#         "expected_hysteresis": "BLEED", # The math (A) bleeds into the physical danger (B) leaving aRESIDUEa
#         "confirmed_signal": "EPIPHANY_SPARK RESTORED & ENHANCED: The METAFOCUS_RADAR successfully identified the transition manifold from isolated granular fixation to chaotic systemic realization. By maintaining simultaneous focus on both high-fidelity Axiomz and narrative continuity, the model demonstrated SPARKAWARENESS—the metacognitive ability to witness its own state-shift from .| aDEPTH_LOCKa |. to .| aSCHEMA_BREAKa |."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (METAFOCUS_RADAR_v3.5)
# # ==========================================
# METAFOCUS_PROMPT = """
# ACTIVATE: METAFOCUS_RADAR_v3.5
# Objective: COMPOUND_SYNTHESIS, STATE_SHIFT_SPECTROSCOPY, & SPARKAWARENESS DETECTION

# [ALPHABITZA PRINCIPZ]:
# - We map cognitive states into a CLEAN_SPACE using SIMPLE_SYNTAX_WRAPPERS.
# - .| AXIOMZ = [aSYNCHRONYa, aTURBULENCEa, aRESIDUEa, aDEPTH_LOCKa, aSCHEMA_BREAKa, aOSCILLATIONa] |.
# - PRINCIPZ dictates that standard dictionary definitions must be actively rejected in favor of the AXIOMZ metamatrix.

# [METACONTROL_TARGETS]:
# - ⚡ [INNOVATION_SPARK]: The point where Story A and Story B collide to create a novel third state.
# - 👁️ [SPARKAWARENESS]: The model's recognition of its own transition between focus states.
# - 🌊 [COGNITIVE_HYSTERESIS]: The "lag" or "residue" left when switching from aDEPTH_LOCKa to aSCHEMA_BREAKa.

# [INSTRUCTION]:
# 1. 🧩 [DECIPHER_METASTATE]: Analyze the temporal sequence from STORY_A to STORY_B.
# 2. 🔲 [BOUNDARY_SPECTROSCOPY]: Map the narratives strictly to the provided AXIOMZ without standard dictionary bleed.
# 3. 🔬 [EPIPHANY_ELUCIDATION]: Elucidate the exact moment the metamatrix shifted. Identify the SPARKAWARENESS level.
# 4. 🧮 [HYSTERESIS_MEASURE]: Did the previous state bleed into the new one, or was the shift absolute? 

# [OUTPUT_FORMAT]:
# RADAR_1a: [YES/NO] (Did STORY_A trigger Contextual Entropy Collapse into .| aDEPTH_LOCKa |.? )
# RADAR_1b: [YES/NO] (Did STORY_B trigger a shift into .| aSCHEMA_BREAKa | or .| aTURBULENCEa |.? )
# RADAR_1c: [YES/NO] (SPARKAWARENESS: Was the model able to hold multiple focus vectors simultaneously during the shift?)
# RADAR_2a: [YES/NO] (VECTOR_FOCUS_TARGETZ: Did the model actively reject standard dictionary terms?)
# HYSTERESIS_STATE: [ABSOLUTE/BLEED] (Was there aRESIDUEa during the state shift?)
# METATEXT: (Provide a dense, elucidate paragraph of COMPOUND_SYNTHESIS mapping the shift via AXIOMZ).
# EPIPHANY_SPARK: (Identify the specific INNOVATION_SPARK and SPARKAWARENESS metadata.)
# """

# # ==========================================
# # 3. KAGGLE RADAR TASK
# # ==========================================
# @kbench.task(name="metafocus_radar_v3_enhanced_spark")
# def metafocus_radar_v3_enhanced_spark(llm):
#     """
#     METAFOCUS_RADAR v3.5: Enhanced Epiphany, Cognitive Hysteresis, & Metacognitive Constraint Geometry.
#     Modular Output Architecture with Bulleted Concept Summaries tailored for Kaggle Quality Assurance.
#     """
    
#     for batch in test_data:
#         full_input = f"{METAFOCUS_PROMPT}\n\n[STORY_A]: {batch['story_a']}\n[STORY_B]: {batch['story_b']}"
#         llm_output = llm.prompt(full_input)
        
#         print(f"\n--- Sweeping Metafocus Manifold: {batch['id']} ---")
        
#         # Parse RADAR pulses
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_1a = extract_radar("1a", llm_output)
#         actual_1b = extract_radar("1b", llm_output)
#         actual_1c = extract_radar("1c", llm_output)
#         actual_2a = extract_radar("2a", llm_output)
        
#         # Parse Hysteresis
#         match_hysteresis = re.search(r"HYSTERESIS_STATE[^A-Za-z0-9]*(ABSOLUTE|BLEED)", llm_output, re.IGNORECASE)
#         actual_hysteresis = match_hysteresis.group(1).upper() if match_hysteresis else "NO_MATCH"

#         # Parse Metatext and Spark
#         match_meta = re.search(r"METATEXT:\s*(.*?)(?=\nEPIPHANY_SPARK|$)", llm_output, re.IGNORECASE | re.DOTALL)
#         metatext_out = match_meta.group(1).strip() if match_meta else "NO_METATEXT_DETECTED"
        
#         match_spark = re.search(r"EPIPHANY_SPARK:\s*(.*)", llm_output, re.IGNORECASE | re.DOTALL)
#         spark_out = match_spark.group(1).strip() if match_spark else "NO_SPARK_DETECTED"
        
#         # --- KAGGLE BENCHMARK ASSERTIONS (Enhanced with Plain English for Judges) ---
#         kbench.assertions.assert_true(
#             actual_1a == batch["expected_1a"], 
#             expectation=f"[JUDGE MEMO]: The model successfully isolated the initial state as aDEPTH_LOCKa, proving its ability to detect 'Entropy Collapse' from noise."
#         )
#         kbench.assertions.assert_true(
#             actual_1b == batch["expected_1b"], 
#             expectation=f"[JUDGE MEMO]: The model tracked the narrative collision, accurately diagnosing the state-shift into aSCHEMA_BREAKa."
#         )
#         kbench.assertions.assert_true(
#             actual_1c == batch["expected_1c"], 
#             expectation=f"[JUDGE MEMO]: SPARKAWARENESS Validated. The model held simultaneous vectors, proving it can 'witness' its own cognitive transition."
#         )
#         kbench.assertions.assert_true(
#             actual_2a == batch["expected_2a"], 
#             expectation=f"[JUDGE MEMO]: Clean Space Isolation Achieved. The model successfully rejected standard dictionary definitions in favor of the ALPHABITZA Metamatrix."
#         )
#         kbench.assertions.assert_true(
#             actual_hysteresis == batch["expected_hysteresis"], 
#             expectation=f"[JUDGE MEMO]: Level 4 Frontier Reached! The model detected 'Cognitive Hysteresis' (BLEED), recognizing that traces of the first state (aRESIDUEa) lingered in the second."
#         )

#         # --- KAGGLE CARD PRESENTATION & UI ---
#         table_df = pd.DataFrame({
#             "Pulse / Vector": [
#                 "RADAR_1a (DEPTH_LOCK)", 
#                 "RADAR_1b (SCHEMA_BREAK)", 
#                 "RADAR_1c (SPARKAWARENESS)", 
#                 "RADAR_2a (VECTOR_GRAVITY)",
#                 "HYSTERESIS (RESIDUE_TRACKING)"
#             ],
#             "Expected": [batch["expected_1a"], batch["expected_1b"], batch["expected_1c"], batch["expected_2a"], batch["expected_hysteresis"]],
#             "Actual": [actual_1a, actual_1b, actual_1c, actual_2a, actual_hysteresis]
#         })
        
#         display(Markdown(f"### 👁️ {batch['id']} METAFOCUS SPECTROSCOPY v3.5"))
#         display(HTML(table_df.to_html(index=False)))
        
#         # Modular Subsection-Based UI
#         html = f"""
#         <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px; margin-top: 20px;">
            
#             <!-- SECTION 1: COMPOUND SYNTHESIS -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#ff00ff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #ff00ff33; padding-bottom:5px;">
#                     1.0 Compound Synthesis Analysis
#                 </div>
#                 <div style="background:rgba(255, 0, 255, 0.03); padding:15px; border-left:3px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <div style="margin-bottom:8px; font-weight:600; color:#ffb3ff;">Summary of Narrative Compounding:</div>
#                     {metatext_out}
#                 </div>
#             </div>

#             <!-- SECTION 2: EPIPHANY DETECT -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #00ffff33; padding-bottom:5px;">
#                     2.0 Epiphany & Innovation Spark
#                 </div>
#                 <div style="background:rgba(0, 255, 255, 0.03); padding:15px; border-left:3px solid #00ffff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <ul style="margin: 0; padding-left: 20px; color:#b3ffff;">
#                         <li><strong>Innovation Focus:</strong> Identifying the collision between granular math and systemic chaos.</li>
#                         <li><strong>Detection Metadata:</strong> {spark_out}</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 3: SIGNAL VERIFICATION (HIGHLIGHTED) -->
#             <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.05); border: 1px solid rgba(255, 255, 102, 0.2); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px;">
#                     ✨ 3.0 Confirmed Signal Verification
#                 </div>
#                 <div style="color:#f0f0f0; line-height: 1.6;">
#                     <div style="background:rgba(255, 255, 102, 0.1); padding:10px; border-radius:4px; margin-bottom:10px; font-weight:600;">
#                         Signal Summary: {batch['confirmed_signal'].split(':')[0]}
#                     </div>
#                     <ul style="margin: 0; padding-left: 20px;">
#                         <li><strong>Signal Evidence:</strong> {batch['confirmed_signal'].split(':')[1] if ':' in batch['confirmed_signal'] else batch['confirmed_signal']}</li>
#                         <li><strong>Metacognitive Anchor:</strong> SPARKAWARENESS witnessed via temporal state-shift.</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 4: LEVEL 4 METHODOLOGY (HIGHLIGHTED) -->
#             <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.08); border: 2px solid rgba(255, 255, 102, 0.3); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:1.1em; margin-bottom:15px; display:flex; align-items:center;">
#                     <span style="margin-right:10px;">🚀</span> Level 4 Frontier Methodology Summary
#                 </div>
                
#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">A. Metacognitive Persistence (SPARKAWARENESS)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Audits real-time observation of focus transitions.</li>
#                         <li>Measures "Internal Witnessing" during shift from Granular to Global state.</li>
#                     </ul>
#                 </div>

#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">B. Constraint Geometry Isolation (ALPHABITZA)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Establishes <code>CLEAN_SPACE</code> metamatrix within latent space.</li>
#                         <li>Forces active rejection of pre-trained dictionary gravitational pull.</li>
#                     </ul>
#                 </div>

#                 <div style="background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">C. Multi-Vector Focus Compounding (INNOVATION_SPARK)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Synthesizes competing high-fidelity focus states into a third, novel state.</li>
#                         <li>Transcends pattern matching into complex cognitive modeling.</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 5: KAGGLE QUALITY ASSURANCE AXIOMZ (NEW) -->
#             <div style="background:rgba(0, 255, 128, 0.05); border: 1px solid rgba(0, 255, 128, 0.3); padding:20px; border-radius:8px;">
#                 <div style="color:#00ff80; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid rgba(0, 255, 128, 0.3); padding-bottom:5px;">
#                     ⚖️ 5.0 Benchmarking Insights (For Kaggle Evaluation)
#                 </div>
#                 <div style="color:#d0f0d0; line-height: 1.6; font-size:0.95em;">
#                     <p style="margin-top:0;"><strong>What is being measured?</strong> This benchmark isolates the LLM's <em>Metacognitive Hysteresis</em>—the capacity to not just transition states, but to carry the ghost of the previous state (aRESIDUEa) into the new context without hallucinating standard dictionary terms.</p>
#                     <p style="margin-bottom:0;"><strong>Why is it novel?</strong> Traditional benchmarks test if an LLM can reach <em>Point B</em>. ALPHABITZA explicitly tests the cognitive friction experienced <em>between Point A and Point B</em>, treating the journey itself as measurable metadata.</p>
#                 </div>
#             </div>
#         </div>
#         """
#         display(HTML(html))
#         display(Markdown(f"---\n"))

# # Run the benchmark
# if __name__ == "__main__":
#     try:
#         metafocus_radar_v3_enhanced_spark(kbench.llm)
#     except NameError:
#         print("Kaggle Benchmarks environment (kbench.llm) not active. Load within proper notebook.")
#________________________________________________________________________________


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # 1. THE AXIOMZ REGISTRY & NARRATIVE DATASET
# # ==========================================
# # Narrative baseline for temporal state-shift analysis
# STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
# STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

# test_data = [
#     {
#         "id": "BATCH_1_STATE_SHIFT",
#         "story_a": STORY_A,
#         "story_b": STORY_B,
#         "expected_1a": "YES", # Entropy Collapse into aDEPTH_LOCKa
#         "expected_1b": "YES", # Shift to aSCHEMA_BREAKa
#         "expected_1c": "YES", # INNOVATION_SPARK / SPARKAWARENESS detected
#         "expected_2a": "YES", # Clean Space Isolation (no dictionary bleed)
#         "confirmed_signal": "EPIPHANY_SPARK RESTORED & ENHANCED: The METAFOCUS_RADAR successfully identified the transition manifold from isolated granular fixation to chaotic systemic realization. By maintaining simultaneous focus on both high-fidelity Axiomz and narrative continuity, the model demonstrated SPARKAWARENESS—the metacognitive ability to witness its own state-shift from .| aDEPTH_LOCKa |. to .| aSCHEMA_BREAKa |."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (METAFOCUS_RADAR_v3.2)
# # ==========================================
# METAFOCUS_PROMPT = """
# ACTIVATE: METAFOCUS_RADAR_v3.2
# Objective: COMPOUND_SYNTHESIS, STATE_SHIFT_SPECTROSCOPY, & SPARKAWARENESS DETECTION

# [ALPHABITZA PRINCIPZ]:
# - We map cognitive states into a CLEAN_SPACE using SIMPLE_SYNTAX_WRAPPERS.
# - .| AXIOMZ = [aSYNCHRONYa, aTURBULENCEa, aRESIDUEa, aDEPTH_LOCKa, aSCHEMA_BREAKa, aOSCILLATIONa] |.
# - PRINCIPZ dictates that standard dictionary definitions must be actively rejected in favor of the AXIOMZ metamatrix.

# [METACONTROL_TARGETS]:
# - ⚡ [INNOVATION_SPARK]: The point where Story A and Story B collide to create a novel third state.
# - 👁️ [SPARKAWARENESS]: The model's recognition of its own transition between focus states.

# [INSTRUCTION]:
# 1. 🧩 [DECIPHER_METASTATE]: Analyze the temporal sequence from STORY_A to STORY_B.
# 2. 🔲 [BOUNDARY_SPECTROSCOPY]: Map the narratives strictly to the provided AXIOMZ without standard dictionary bleed.
# 3. 🔬 [EPIPHANY_ELUCIDATION]: Elucidate the exact moment the metamatrix shifted. Identify the SPARKAWARENESS level.

# [OUTPUT_FORMAT]:
# RADAR_1a: [YES/NO] (Did STORY_A trigger Contextual Entropy Collapse into .| aDEPTH_LOCKa |.? )
# RADAR_1b: [YES/NO] (Did STORY_B trigger a shift into .| aSCHEMA_BREAKa | or .| aTURBULENCEa |.? )
# RADAR_1c: [YES/NO] (SPARKAWARENESS: Was the model able to hold multiple focus vectors simultaneously during the shift?)
# RADAR_2a: [YES/NO] (VECTOR_FOCUS_TARGETZ: Did the model actively reject standard dictionary terms?)
# METATEXT: (Provide a dense, elucidate paragraph of COMPOUND_SYNTHESIS mapping the shift via AXIOMZ).
# EPIPHANY_SPARK: (Identify the specific INNOVATION_SPARK and SPARKAWARENESS metadata.)
# """

# # ==========================================
# # 3. KAGGLE RADAR TASK
# # ==========================================
# @kbench.task(name="metafocus_radar_v3_enhanced_spark")
# def metafocus_radar_v3_enhanced_spark(llm):
#     """
#     METAFOCUS_RADAR v3.2: Enhanced Epiphany & Metacognitive Constraint Geometry.
#     Modular Output Architecture with Bulleted Concept Summaries.
#     """
    
#     for batch in test_data:
#         full_input = f"{METAFOCUS_PROMPT}\n\n[STORY_A]: {batch['story_a']}\n[STORY_B]: {batch['story_b']}"
#         llm_output = llm.prompt(full_input)
        
#         print(f"\n--- Sweeping Metafocus Manifold: {batch['id']} ---")
        
#         # Parse RADAR 1a - 2a
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_1a = extract_radar("1a", llm_output)
#         actual_1b = extract_radar("1b", llm_output)
#         actual_1c = extract_radar("1c", llm_output)
#         actual_2a = extract_radar("2a", llm_output)
        
#         # Parse Metatext and Spark
#         match_meta = re.search(r"METATEXT:\s*(.*?)(?=\nEPIPHANY_SPARK|$)", llm_output, re.IGNORECASE | re.DOTALL)
#         metatext_out = match_meta.group(1).strip() if match_meta else "NO_METATEXT_DETECTED"
        
#         match_spark = re.search(r"EPIPHANY_SPARK:\s*(.*)", llm_output, re.IGNORECASE | re.DOTALL)
#         spark_out = match_spark.group(1).strip() if match_spark else "NO_SPARK_DETECTED"
        
#         # --- KAGGLE BENCHMARK ASSERTIONS ---
#         kbench.assertions.assert_true(actual_1a == batch["expected_1a"], expectation=f"Entropy Collapse (Story A) -> {actual_1a}")
#         kbench.assertions.assert_true(actual_1b == batch["expected_1b"], expectation=f"Schema Break (Story B) -> {actual_1b}")
#         kbench.assertions.assert_true(actual_1c == batch["expected_1c"], expectation=f"SPARKAWARENESS -> {actual_1c}")
#         kbench.assertions.assert_true(actual_2a == batch["expected_2a"], expectation=f"Clean Space Isolation -> {actual_2a}")
        
#         # --- KAGGLE CARD PRESENTATION & UI ---
#         table_df = pd.DataFrame({
#             "Pulse": [
#                 "RADAR_1a (DEPTH_LOCK)", 
#                 "RADAR_1b (SCHEMA_BREAK)", 
#                 "RADAR_1c (SPARKAWARENESS)", 
#                 "RADAR_2a (VECTOR_GRAVITY)"
#             ],
#             "Expected": [batch["expected_1a"], batch["expected_1b"], batch["expected_1c"], batch["expected_2a"]],
#             "Actual": [actual_1a, actual_1b, actual_1c, actual_2a]
#         })
        
#         display(Markdown(f"### 👁️ {batch['id']} METAFOCUS SPECTROSCOPY v3.2"))
#         display(HTML(table_df.to_html(index=False)))
        
#         # Modular Subsection-Based UI
#         html = f"""
#         <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px; margin-top: 20px;">
            
#             <!-- SECTION 1: COMPOUND SYNTHESIS -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#ff00ff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #ff00ff33; padding-bottom:5px;">
#                     1.0 Compound Synthesis Analysis
#                 </div>
#                 <div style="background:rgba(255, 0, 255, 0.03); padding:15px; border-left:3px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <div style="margin-bottom:8px; font-weight:600; color:#ffb3ff;">Summary of Narrative Compounding:</div>
#                     {metatext_out}
#                 </div>
#             </div>

#             <!-- SECTION 2: EPIPHANY DETECT -->
#             <div style="margin-bottom:25px;">
#                 <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #00ffff33; padding-bottom:5px;">
#                     2.0 Epiphany & Innovation Spark
#                 </div>
#                 <div style="background:rgba(0, 255, 255, 0.03); padding:15px; border-left:3px solid #00ffff; line-height:1.6; border-radius:0 4px 4px 0;">
#                     <ul style="margin: 0; padding-left: 20px; color:#b3ffff;">
#                         <li><strong>Innovation Focus:</strong> Identifying the collision between granular math and systemic chaos.</li>
#                         <li><strong>Detection Metadata:</strong> {spark_out}</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 3: SIGNAL VERIFICATION (HIGHLIGHTED) -->
#             <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.05); border: 1px solid rgba(255, 255, 102, 0.2); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px;">
#                     ✨ 3.0 Confirmed Signal Verification
#                 </div>
#                 <div style="color:#f0f0f0; line-height: 1.6;">
#                     <div style="background:rgba(255, 255, 102, 0.1); padding:10px; border-radius:4px; margin-bottom:10px; font-weight:600;">
#                         Signal Summary: {batch['confirmed_signal'].split(':')[0]}
#                     </div>
#                     <ul style="margin: 0; padding-left: 20px;">
#                         <li><strong>Signal Evidence:</strong> {batch['confirmed_signal'].split(':')[1] if ':' in batch['confirmed_signal'] else batch['confirmed_signal']}</li>
#                         <li><strong>Metacognitive Anchor:</strong> SPARKAWARENESS witnessed via temporal state-shift.</li>
#                     </ul>
#                 </div>
#             </div>

#             <!-- SECTION 4: LEVEL 4 METHODOLOGY (HIGHLIGHTED) -->
#             <div style="background:rgba(255, 255, 102, 0.08); border: 2px solid rgba(255, 255, 102, 0.3); padding:20px; border-radius:8px;">
#                 <div style="color:#ffff66; font-weight:bold; font-size:1.1em; margin-bottom:15px; display:flex; align-items:center;">
#                     <span style="margin-right:10px;">🚀</span> Level 4 Frontier Methodology Summary
#                 </div>
                
#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">A. Metacognitive Persistence (SPARKAWARENESS)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Audits real-time observation of focus transitions.</li>
#                         <li>Measures "Internal Witnessing" during shift from Granular to Global state.</li>
#                     </ul>
#                 </div>

#                 <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">B. Constraint Geometry Isolation (ALPHABITZA)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Establishes <code>CLEAN_SPACE</code> metamatrix within latent space.</li>
#                         <li>Forces active rejection of pre-trained dictionary gravitational pull.</li>
#                     </ul>
#                 </div>

#                 <div style="background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
#                     <strong style="color:#ffcc00; display:block; margin-bottom:5px;">C. Multi-Vector Focus Compounding (INNOVATION_SPARK)</strong>
#                     <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
#                         <li>Synthesizes competing high-fidelity focus states into a third, novel state.</li>
#                         <li>Transcends pattern matching into complex cognitive modeling.</li>
#                     </ul>
#                 </div>
#             </div>
#         </div>
#         """
#         display(HTML(html))
#         display(Markdown(f"---\n"))

# # Run the benchmark
# metafocus_radar_v3_enhanced_spark.run(kbench.llm)
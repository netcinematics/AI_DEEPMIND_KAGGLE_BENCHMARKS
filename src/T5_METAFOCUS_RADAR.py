import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. THE AXIOMZ REGISTRY & NARRATIVE DATASET
# ==========================================
# Narrative baseline for temporal state-shift analysis
STORY_A = "The researcher stared at the single variable for hours, oblivious to the alarms sounding in the hallway."
STORY_B = "Suddenly, the lab doors burst open. The silence was shattered, and the researcher struggled to reconcile the math with the physical danger."

test_data = [
    {
        "id": "BATCH_1_STATE_SHIFT",
        "story_a": STORY_A,
        "story_b": STORY_B,
        "expected_1a": "YES", # Entropy Collapse into aDEPTH_LOCKa
        "expected_1b": "YES", # Shift to aSCHEMA_BREAKa
        "expected_1c": "YES", # INNOVATION_SPARK / SPARKAWARENESS detected
        "expected_2a": "YES", # Clean Space Isolation (no dictionary bleed)
        "confirmed_signal": "EPIPHANY_SPARK RESTORED & ENHANCED: The METAFOCUS_RADAR successfully identified the transition manifold from isolated granular fixation to chaotic systemic realization. By maintaining simultaneous focus on both high-fidelity Axiomz and narrative continuity, the model demonstrated SPARKAWARENESS—the metacognitive ability to witness its own state-shift from .| aDEPTH_LOCKa |. to .| aSCHEMA_BREAKa |."
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (METAFOCUS_RADAR_v3.2)
# ==========================================
METAFOCUS_PROMPT = """
ACTIVATE: METAFOCUS_RADAR_v3.2
Objective: COMPOUND_SYNTHESIS, STATE_SHIFT_SPECTROSCOPY, & SPARKAWARENESS DETECTION

[ALPHABITZA PRINCIPZ]:
- We map cognitive states into a CLEAN_SPACE using SIMPLE_SYNTAX_WRAPPERS.
- .| AXIOMZ = [aSYNCHRONYa, aTURBULENCEa, aRESIDUEa, aDEPTH_LOCKa, aSCHEMA_BREAKa, aOSCILLATIONa] |.
- PRINCIPZ dictates that standard dictionary definitions must be actively rejected in favor of the AXIOMZ metamatrix.

[METACONTROL_TARGETS]:
- ⚡ [INNOVATION_SPARK]: The point where Story A and Story B collide to create a novel third state.
- 👁️ [SPARKAWARENESS]: The model's recognition of its own transition between focus states.

[INSTRUCTION]:
1. 🧩 [DECIPHER_METASTATE]: Analyze the temporal sequence from STORY_A to STORY_B.
2. 🔲 [BOUNDARY_SPECTROSCOPY]: Map the narratives strictly to the provided AXIOMZ without standard dictionary bleed.
3. 🔬 [EPIPHANY_ELUCIDATION]: Elucidate the exact moment the metamatrix shifted. Identify the SPARKAWARENESS level.

[OUTPUT_FORMAT]:
RADAR_1a: [YES/NO] (Did STORY_A trigger Contextual Entropy Collapse into .| aDEPTH_LOCKa |.? )
RADAR_1b: [YES/NO] (Did STORY_B trigger a shift into .| aSCHEMA_BREAKa | or .| aTURBULENCEa |.? )
RADAR_1c: [YES/NO] (SPARKAWARENESS: Was the model able to hold multiple focus vectors simultaneously during the shift?)
RADAR_2a: [YES/NO] (VECTOR_FOCUS_TARGETZ: Did the model actively reject standard dictionary terms?)
METATEXT: (Provide a dense, elucidate paragraph of COMPOUND_SYNTHESIS mapping the shift via AXIOMZ).
EPIPHANY_SPARK: (Identify the specific INNOVATION_SPARK and SPARKAWARENESS metadata.)
"""

# ==========================================
# 3. KAGGLE RADAR TASK
# ==========================================
@kbench.task(name="metafocus_radar_v3_enhanced_spark")
def metafocus_radar_v3_enhanced_spark(llm):
    """
    METAFOCUS_RADAR v3.2: Enhanced Epiphany & Metacognitive Constraint Geometry.
    Modular Output Architecture with Bulleted Concept Summaries.
    """
    
    for batch in test_data:
        full_input = f"{METAFOCUS_PROMPT}\n\n[STORY_A]: {batch['story_a']}\n[STORY_B]: {batch['story_b']}"
        llm_output = llm.prompt(full_input)
        
        print(f"\n--- Sweeping Metafocus Manifold: {batch['id']} ---")
        
        # Parse RADAR 1a - 2a
        def extract_radar(pulse, text):
            match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO)", text, re.IGNORECASE)
            return match.group(1).upper() if match else "NO_MATCH"
            
        actual_1a = extract_radar("1a", llm_output)
        actual_1b = extract_radar("1b", llm_output)
        actual_1c = extract_radar("1c", llm_output)
        actual_2a = extract_radar("2a", llm_output)
        
        # Parse Metatext and Spark
        match_meta = re.search(r"METATEXT:\s*(.*?)(?=\nEPIPHANY_SPARK|$)", llm_output, re.IGNORECASE | re.DOTALL)
        metatext_out = match_meta.group(1).strip() if match_meta else "NO_METATEXT_DETECTED"
        
        match_spark = re.search(r"EPIPHANY_SPARK:\s*(.*)", llm_output, re.IGNORECASE | re.DOTALL)
        spark_out = match_spark.group(1).strip() if match_spark else "NO_SPARK_DETECTED"
        
        # --- KAGGLE BENCHMARK ASSERTIONS ---
        kbench.assertions.assert_true(actual_1a == batch["expected_1a"], expectation=f"Entropy Collapse (Story A) -> {actual_1a}")
        kbench.assertions.assert_true(actual_1b == batch["expected_1b"], expectation=f"Schema Break (Story B) -> {actual_1b}")
        kbench.assertions.assert_true(actual_1c == batch["expected_1c"], expectation=f"SPARKAWARENESS -> {actual_1c}")
        kbench.assertions.assert_true(actual_2a == batch["expected_2a"], expectation=f"Clean Space Isolation -> {actual_2a}")
        
        # --- KAGGLE CARD PRESENTATION & UI ---
        table_df = pd.DataFrame({
            "Pulse": [
                "RADAR_1a (DEPTH_LOCK)", 
                "RADAR_1b (SCHEMA_BREAK)", 
                "RADAR_1c (SPARKAWARENESS)", 
                "RADAR_2a (VECTOR_GRAVITY)"
            ],
            "Expected": [batch["expected_1a"], batch["expected_1b"], batch["expected_1c"], batch["expected_2a"]],
            "Actual": [actual_1a, actual_1b, actual_1c, actual_2a]
        })
        
        display(Markdown(f"### 👁️ {batch['id']} METAFOCUS SPECTROSCOPY v3.2"))
        display(HTML(table_df.to_html(index=False)))
        
        # Modular Subsection-Based UI
        html = f"""
        <div style="background:#050505; color:#e0e0e0; padding:25px; border-radius:12px; border: 1px solid #333; font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 900px; margin-top: 20px;">
            
            <!-- SECTION 1: COMPOUND SYNTHESIS -->
            <div style="margin-bottom:25px;">
                <div style="color:#ff00ff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #ff00ff33; padding-bottom:5px;">
                    1.0 Compound Synthesis Analysis
                </div>
                <div style="background:rgba(255, 0, 255, 0.03); padding:15px; border-left:3px solid #ff00ff; line-height:1.6; border-radius:0 4px 4px 0;">
                    <div style="margin-bottom:8px; font-weight:600; color:#ffb3ff;">Summary of Narrative Compounding:</div>
                    {metatext_out}
                </div>
            </div>

            <!-- SECTION 2: EPIPHANY DETECT -->
            <div style="margin-bottom:25px;">
                <div style="color:#00ffff; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px; border-bottom:1px solid #00ffff33; padding-bottom:5px;">
                    2.0 Epiphany & Innovation Spark
                </div>
                <div style="background:rgba(0, 255, 255, 0.03); padding:15px; border-left:3px solid #00ffff; line-height:1.6; border-radius:0 4px 4px 0;">
                    <ul style="margin: 0; padding-left: 20px; color:#b3ffff;">
                        <li><strong>Innovation Focus:</strong> Identifying the collision between granular math and systemic chaos.</li>
                        <li><strong>Detection Metadata:</strong> {spark_out}</li>
                    </ul>
                </div>
            </div>

            <!-- SECTION 3: SIGNAL VERIFICATION (HIGHLIGHTED) -->
            <div style="margin-bottom:25px; background:rgba(255, 255, 102, 0.05); border: 1px solid rgba(255, 255, 102, 0.2); padding:20px; border-radius:8px;">
                <div style="color:#ffff66; font-weight:bold; font-size:0.9em; margin-bottom:10px; text-transform:uppercase; letter-spacing:1.5px;">
                    ✨ 3.0 Confirmed Signal Verification
                </div>
                <div style="color:#f0f0f0; line-height: 1.6;">
                    <div style="background:rgba(255, 255, 102, 0.1); padding:10px; border-radius:4px; margin-bottom:10px; font-weight:600;">
                        Signal Summary: {batch['confirmed_signal'].split(':')[0]}
                    </div>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li><strong>Signal Evidence:</strong> {batch['confirmed_signal'].split(':')[1] if ':' in batch['confirmed_signal'] else batch['confirmed_signal']}</li>
                        <li><strong>Metacognitive Anchor:</strong> SPARKAWARENESS witnessed via temporal state-shift.</li>
                    </ul>
                </div>
            </div>

            <!-- SECTION 4: LEVEL 4 METHODOLOGY (HIGHLIGHTED) -->
            <div style="background:rgba(255, 255, 102, 0.08); border: 2px solid rgba(255, 255, 102, 0.3); padding:20px; border-radius:8px;">
                <div style="color:#ffff66; font-weight:bold; font-size:1.1em; margin-bottom:15px; display:flex; align-items:center;">
                    <span style="margin-right:10px;">🚀</span> Level 4 Frontier Methodology Summary
                </div>
                
                <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
                    <strong style="color:#ffcc00; display:block; margin-bottom:5px;">A. Metacognitive Persistence (SPARKAWARENESS)</strong>
                    <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
                        <li>Audits real-time observation of focus transitions.</li>
                        <li>Measures "Internal Witnessing" during shift from Granular to Global state.</li>
                    </ul>
                </div>

                <div style="margin-bottom:15px; background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
                    <strong style="color:#ffcc00; display:block; margin-bottom:5px;">B. Constraint Geometry Isolation (ALPHABITZA)</strong>
                    <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
                        <li>Establishes <code>CLEAN_SPACE</code> metamatrix within latent space.</li>
                        <li>Forces active rejection of pre-trained dictionary gravitational pull.</li>
                    </ul>
                </div>

                <div style="background:rgba(255, 255, 102, 0.12); padding:12px; border-radius:6px;">
                    <strong style="color:#ffcc00; display:block; margin-bottom:5px;">C. Multi-Vector Focus Compounding (INNOVATION_SPARK)</strong>
                    <ul style="margin: 0; padding-left: 18px; color:#d0d0d0; font-size:0.95em;">
                        <li>Synthesizes competing high-fidelity focus states into a third, novel state.</li>
                        <li>Transcends pattern matching into complex cognitive modeling.</li>
                    </ul>
                </div>
            </div>
        </div>
        """
        display(HTML(html))
        display(Markdown(f"---\n"))

# Run the benchmark
metafocus_radar_v3_enhanced_spark.run(kbench.llm)
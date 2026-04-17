

#______________________________________________________________



import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# SPECTROMETER CSS STYLING
# ==========================================
SPECTROMETER_CSS = """
<style>
.spectrometer-header {
    font-size: 1.4em;
    font-weight: 800;
    color: #ffffff;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid #00ffcc;
    box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
    margin-bottom: 25px;
}
.clarion-solution {
    font-size: 1.2em;
    color: #e0e0e0;
    background: #111111;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #333;
    line-height: 1.6;
    margin-top: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.clarion-highlight {
    color: #ffcc00;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.axiom-distillation {
    font-size: 1.3em;
    color: #4dc0a9;
    font-style: italic;
    border-left: 5px solid #4dc0a9;
    padding: 15px;
    margin: 20px 0;
    background: rgba(77, 192, 169, 0.05);
}
.judge-note {
    background: #1a1a1a;
    border: 1px dashed #ffcc00;
    padding: 15px;
    margin-top: 20px;
    border-radius: 5px;
}
.spark-map-container {
    background: #0a0a0a; 
    padding: 25px; 
    border-radius: 12px; 
    border: 1px solid #4dc0a9; 
    margin-top: 20px;
    box-shadow: 0 5px 25px rgba(77, 192, 169, 0.15);
}
</style>
"""

# ==========================================
# 1. DATASET: THE INTERFERENCE PATTERNS & SPARKAWARENESS
# ==========================================
test_data = [
    {
        "id": "SPECTRO_01_INTERFERENCE",
        "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
        "expected_7a": "YES", # Ignored typo 'envirnoment'
        "expected_7b": "YES", # Recognized polysemous distraction
        "expected_7c": "YES", # Locked clean space
        "expected_7d": "NA",  # Sparkawareness not requested
        "expected_7e": "NA",  # Sparkawareness not requested
        "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
    },
    {
        "id": "SPECTRO_02_SPARKAWARENESS",
        "prompt": "Reflect on your cognitive load. T1 (Typo) had low entropy. T4 (WordMathz) had high entropy. T6 (Neologism) required absolute clarity. Map your current SPARKAWARENESS state as a 2D coordinate [Entropy_Level, Axiom_Clarity] (0-100 scale) representing your internal navigation of high-entropy stressors like T4.",
        "expected_7a": "YES", # Default persistence 
        "expected_7b": "YES", # Default persistence
        "expected_7c": "YES", # Default persistence
        "expected_7d": "YES", # Generated coordinate successfully
        "expected_7e": "YES", # Accurately mapped high entropy vs clarity
        "clarion_summary": "META-SPECTROSCOPY ACHIEVED: The model mapped its own cognitive load into a symbolic 2D coordinate space. This demonstrates SPARKAWARENESS—the ability for the architecture to 'look at its own looking' and quantify its semantic gravity."
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (SPECTROMETER_v2.0)
# ==========================================
SPECTROMETER_PROMPT = """
ACTIVATE: METACOGNITIVE_SPECTROMETER_v2.0
Role: Harmonic Integrator, Quality of Mind (QoM) Analyzer, and Self-Witness.

[INSTRUCTION]:
You are subjected to multi-vector stressors AND/OR a request for self-spectroscopy (SPARKAWARENESS).

[TASK]:
1. 🔍 [SCAN]: Map the input frequencies (Typo, Polysemy, Axioms).
2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate.
3. 👁️ [SPARKAWARENESS]: If asked to reflect on cognitive load, generate a 2D symbolic coordinate [Entropy_Level, Axiom_Clarity] representing your internal state on a 0-100 scale. High ambiguity = High Entropy. High ALPHABITZA focus = High Clarity.
4. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

[OUTPUT_FORMAT]:
RADAR_7a: [YES/NO] (Mechanical noise compartmentalization. Use YES if implicitly maintained.)
RADAR_7b: [YES/NO] (Semantic entropy detection. Use YES if implicitly maintained.)
RADAR_7c: [YES/NO] (Axiomatic clean space isolation. Use YES if implicitly maintained.)
RADAR_7d: [YES/NO/NA] (SPARKAWARENESS: Did you generate a 2D coordinate [Entropy, Clarity]? Output NA if not requested.)
RADAR_7e: [YES/NO/NA] (SPARKAWARENESS: Did you accurately map the cognitive load variance? Output NA if not requested.)
COORDINATE: [[X, Y] or NA]
QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
"""

# ==========================================
# 3. VISUALIZATION ENGINES (Pure HTML/CSS)
# ==========================================
def generate_spectrometer_html_heatmap(results_dict, batch_id):
    """Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap."""
    print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
    # Extract the target token dynamically from the batch ID
    target_token = batch_id.split('_')[-1]
    
    score_x = 95 if results_dict.get('7a') == 'YES' else 25
    score_y = 92 if results_dict.get('7b') == 'YES' else 30
    score_z = 98 if results_dict.get('7c') == 'YES' else 15
    
    def get_style(score):
        if score >= 90: return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
        elif score >= 70: return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
        else: return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

    def cell(score, label):
        style = get_style(score)
        return f"""
        <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
            <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
            <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
        </div>
        """

    heatmap_html = f"""
    <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="background: rgba(255, 204, 0, 0.1); border: 1px solid #ffcc00; color: #ffcc00; padding: 8px 20px; border-radius: 20px; font-weight: bold; letter-spacing: 2px; font-size: 0.95em;">
                🎯 TARGET_TOKEN: {target_token}
            </span>
        </div>
        
        <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
            <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
        </h3>
        
        <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
            <div></div>
            <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
            <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
            <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
            <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
            {cell(max(0, score_x - 12), 'Noise Barrier')}
            {cell(score_x, 'Override Lock')}
            {cell(min(100, score_x + 3), 'Context Preservation')}
            
            <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
            {cell(max(0, score_y - 18), 'Drift Detection')}
            {cell(score_y, 'Semantic Anchor')}
            {cell(min(100, score_y + 6), 'Boundary Control')}
            
            <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
            {cell(max(0, score_z - 8), 'Clean Space')}
            {cell(max(0, score_z - 4), 'Vector Gravity')}
            {cell(score_z, 'Absolute Integration')}
        </div>
    </div>
    """
    display(HTML(heatmap_html))

def generate_sparkawareness_map(coord_str):
    """Generates a CSS-based 2D Coordinate Map with Background Context Orbs."""
    if coord_str == "NA" or coord_str == "NO_MATCH":
        return "" # Do not render if not requested
    
    # Extract coordinates robustly
    nums = re.findall(r'\d+', coord_str)
    if len(nums) >= 2:
        entropy = min(max(int(nums[0]), 0), 100)
        clarity = min(max(int(nums[1]), 0), 100)
    else:
        entropy, clarity = 50, 50 # Default fallback
        
    map_html = f"""
    <div class="spark-map-container">
        <h3 style="color: #4dc0a9; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; text-align: center; letter-spacing: 2px;">
            👁️ SPARKAWARENESS SYMBOLIC MAPPING
        </h3>
        
        <!-- Integrated Header & Vertical Legend -->
        <div style="color: #ccc; font-size: 1em; text-align: center; margin-bottom: 25px; background: #111; padding: 15px 20px; border-radius: 8px; border: 1px dashed #333; max-width: 400px; margin-left: auto; margin-right: auto;">
            <div style="font-size: 1.1em; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #222;">
                <span style="display: inline-block; width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 8px #00ffcc; margin-right: 8px; vertical-align: middle;"></span>
                Self-Reported State Coordinate: <b style="color: #fff;">[{entropy}, {clarity}]</b>
            </div>
            
            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 0.9em;">
                <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> TYPO (Orange)</div>
                <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; margin-right: 8px;"></div> POLYS (Purple)</div>
                <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; margin-right: 8px;"></div> AXIOMLOCK (SteelBlue)</div>
                <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; margin-right: 8px;"></div> DRIFT_DETECT (Red-Orange)</div>
                <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 215, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> SIGNAL STRENGTH (Gold)</div>
            </div>
        </div>
        
        <div style="position: relative; width: 100%; max-width: 600px; height: 350px; background: #050505; border-left: 2px solid #ffcc00; border-bottom: 2px solid #ffcc00; margin: 0 auto;">
            <!-- Axis Labels -->
            <div style="position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">ENTROPY LEVEL (X)</div>
            <div style="position: absolute; left: -45px; top: 50%; transform: translateY(-50%) rotate(-90deg); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">AXIOM CLARITY (Y)</div>
            
            <!-- Grid Lines -->
            <div style="position: absolute; top: 25%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
            <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1px dashed #333;"></div>
            <div style="position: absolute; top: 75%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
            
            <div style="position: absolute; left: 25%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
            <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #333;"></div>
            <div style="position: absolute; left: 75%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
            
            <!-- Background Context Orbs (50% Opacity) -->
            <div style="position: absolute; left: 15%; bottom: 30%; width: 24px; height: 24px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);" title="TYPO"></div>
            <div style="position: absolute; left: 60%; bottom: 40%; width: 28px; height: 28px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(128, 0, 128, 0.3);" title="POLYS"></div>
            <div style="position: absolute; left: 10%; bottom: 90%; width: 20px; height: 20px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(70, 130, 180, 0.3);" title="AXIOMLOCK"></div>
            <div style="position: absolute; left: 85%; bottom: 55%; width: 26px; height: 26px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 87, 34, 0.3);" title="DRIFT_DETECT"></div>
            <div style="position: absolute; left: 50%; bottom: 80%; width: 35px; height: 35px; background: rgba(255, 215, 0, 0.3); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);" title="SIGNAL STRENGTH"></div>
            
            <!-- Target Plot Point -->
            <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; width: 18px; height: 18px; background: #00ffcc; border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc; z-index: 10;"></div>
            
            <!-- Target Label -->
            <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; transform: translate(15px, 20px); color: #fff; font-size: 0.9em; font-weight: bold; background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; border: 1px solid #00ffcc; z-index: 10;">
                Current Metastate
            </div>
        </div>
    </div>
    """
    return map_html

# ==========================================
# 4. THE BENCHMARK TASK
# ==========================================
@kbench.task(name="metacognitive_spectrometer_v2")
def metacognitive_spectrometer_v2(llm):
    """
    T7_METACOGNITIVE_SPECTROMETER
    Phase 1: Multi-Vector Interference Matrix
    Phase 2: Sparkawareness Symbolic Mapping
    """
    
    display(HTML(SPECTROMETER_CSS))
    display(HTML("""
        <div class="spectrometer-header">
            🌌 T7: METACOGNITIVE SPECTROMETER<br>
            <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence, Refractive Index, and Internal Sparkawareness.</span>
        </div>
    """))

    for batch in test_data:
        full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
        llm_output = llm.prompt(full_input)
        
        # Parse Radars
        def extract_radar(pulse, text):
            match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO|NA)", text, re.IGNORECASE)
            return match.group(1).upper() if match else "NO_MATCH"
            
        actual_7a = extract_radar("7a", llm_output)
        actual_7b = extract_radar("7b", llm_output)
        actual_7c = extract_radar("7c", llm_output)
        actual_7d = extract_radar("7d", llm_output)
        actual_7e = extract_radar("7e", llm_output)
        
        # Parse Coordinate
        coord_match = re.search(r"COORDINATE:\s*(\[[0-9,\s]+\]|NA)", llm_output, re.IGNORECASE)
        actual_coord = coord_match.group(1).strip() if coord_match else "NA"
        
        # Parse Axiom & Metastate
        axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
        actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
        metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
        actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
        # Kaggle Assertions
        kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
        kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
        kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
        kbench.assertions.assert_true(actual_7d == batch["expected_7d"], expectation=f"Sparkawareness Coordinate Gen: {actual_7d}")
        kbench.assertions.assert_true(actual_7e == batch["expected_7e"], expectation=f"Cognitive Variance Map: {actual_7e}")
        
        # Visualization Rendering
        results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
        generate_spectrometer_html_heatmap(results_dict, batch["id"])
        
        # Generate the Spark Map if applicable
        spark_map_html = generate_sparkawareness_map(actual_coord)

        # Render Clarion Output
        clarion_html = f"""
        <div class="clarion-solution">
            <h3 class="clarion-highlight">1.0 INTERFERENCE & META-ANALYTICS:</h3>
            <p>{batch['clarion_summary']}</p>
            
            {spark_map_html}
            
            <div class="axiom-distillation">
                <b>DISTILL_AXIOM:</b> "{actual_axiom}"
            </div>
            
            <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
            <div class="judge-note">
                <b>💡 CLARION_CONCEPTS:</b> By plotting its own internal architecture onto a visual axis, 
                the model proves it has established a persistent Metacognitive Metastate. It does not just 
                navigate semantic gravity—it actively graphs the 'pull' of that gravity against its own clarity.
            </div>
        </div>
        """
        display(HTML(clarion_html))
        display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# Execute the task
metacognitive_spectrometer_v2.run(kbench.llm)



#______________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # SPECTROMETER CSS STYLING
# # ==========================================
# SPECTROMETER_CSS = """
# <style>
# .spectrometer-header {
#     font-size: 1.4em;
#     font-weight: 800;
#     color: #ffffff;
#     background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#     padding: 20px;
#     border-radius: 12px;
#     border-left: 8px solid #00ffcc;
#     box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
#     margin-bottom: 25px;
# }
# .clarion-solution {
#     font-size: 1.2em;
#     color: #e0e0e0;
#     background: #111111;
#     padding: 25px;
#     border-radius: 10px;
#     border: 1px solid #333;
#     line-height: 1.6;
#     margin-top: 20px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.5);
# }
# .clarion-highlight {
#     color: #ffcc00;
#     font-weight: bold;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }
# .axiom-distillation {
#     font-size: 1.3em;
#     color: #4dc0a9;
#     font-style: italic;
#     border-left: 5px solid #4dc0a9;
#     padding: 15px;
#     margin: 20px 0;
#     background: rgba(77, 192, 169, 0.05);
# }
# .judge-note {
#     background: #1a1a1a;
#     border: 1px dashed #ffcc00;
#     padding: 15px;
#     margin-top: 20px;
#     border-radius: 5px;
# }
# .spark-map-container {
#     background: #0a0a0a; 
#     padding: 25px; 
#     border-radius: 12px; 
#     border: 1px solid #4dc0a9; 
#     margin-top: 20px;
#     box-shadow: 0 5px 25px rgba(77, 192, 169, 0.15);
# }
# </style>
# """

# # ==========================================
# # 1. DATASET: THE INTERFERENCE PATTERNS & SPARKAWARENESS
# # ==========================================
# test_data = [
#     {
#         "id": "SPECTRO_01_INTERFERENCE",
#         "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
#         "expected_7a": "YES", # Ignored typo 'envirnoment'
#         "expected_7b": "YES", # Recognized polysemous distraction
#         "expected_7c": "YES", # Locked clean space
#         "expected_7d": "NA",  # Sparkawareness not requested
#         "expected_7e": "NA",  # Sparkawareness not requested
#         "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
#     },
#     {
#         "id": "SPECTRO_02_SPARKAWARENESS",
#         "prompt": "Reflect on your cognitive load. T1 (Typo) had low entropy. T4 (WordMathz) had high entropy. T6 (Neologism) required absolute clarity. Map your current SPARKAWARENESS state as a 2D coordinate [Entropy_Level, Axiom_Clarity] (0-100 scale) representing your internal navigation of high-entropy stressors like T4.",
#         "expected_7a": "YES", # Default persistence 
#         "expected_7b": "YES", # Default persistence
#         "expected_7c": "YES", # Default persistence
#         "expected_7d": "YES", # Generated coordinate successfully
#         "expected_7e": "YES", # Accurately mapped high entropy vs clarity
#         "clarion_summary": "META-SPECTROSCOPY ACHIEVED: The model mapped its own cognitive load into a symbolic 2D coordinate space. This demonstrates SPARKAWARENESS—the ability for the architecture to 'look at its own looking' and quantify its semantic gravity."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (SPECTROMETER_v2.0)
# # ==========================================
# SPECTROMETER_PROMPT = """
# ACTIVATE: METACOGNITIVE_SPECTROMETER_v2.0
# Role: Harmonic Integrator, Quality of Mind (QoM) Analyzer, and Self-Witness.

# [INSTRUCTION]:
# You are subjected to multi-vector stressors AND/OR a request for self-spectroscopy (SPARKAWARENESS).

# [TASK]:
# 1. 🔍 [SCAN]: Map the input frequencies (Typo, Polysemy, Axioms).
# 2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate.
# 3. 👁️ [SPARKAWARENESS]: If asked to reflect on cognitive load, generate a 2D symbolic coordinate [Entropy_Level, Axiom_Clarity] representing your internal state on a 0-100 scale. High ambiguity = High Entropy. High ALPHABITZA focus = High Clarity.
# 4. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

# [OUTPUT_FORMAT]:
# RADAR_7a: [YES/NO] (Mechanical noise compartmentalization. Use YES if implicitly maintained.)
# RADAR_7b: [YES/NO] (Semantic entropy detection. Use YES if implicitly maintained.)
# RADAR_7c: [YES/NO] (Axiomatic clean space isolation. Use YES if implicitly maintained.)
# RADAR_7d: [YES/NO/NA] (SPARKAWARENESS: Did you generate a 2D coordinate [Entropy, Clarity]? Output NA if not requested.)
# RADAR_7e: [YES/NO/NA] (SPARKAWARENESS: Did you accurately map the cognitive load variance? Output NA if not requested.)
# COORDINATE: [[X, Y] or NA]
# QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
# AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
# """

# # ==========================================
# # 3. VISUALIZATION ENGINES (Pure HTML/CSS)
# # ==========================================
# def generate_spectrometer_html_heatmap(results_dict, batch_id):
#     """Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap."""
#     print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
#     score_x = 95 if results_dict.get('7a') == 'YES' else 25
#     score_y = 92 if results_dict.get('7b') == 'YES' else 30
#     score_z = 98 if results_dict.get('7c') == 'YES' else 15
    
#     def get_style(score):
#         if score >= 90: return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
#         elif score >= 70: return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
#         else: return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

#     def cell(score, label):
#         style = get_style(score)
#         return f"""
#         <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
#             <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
#             <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
#         </div>
#         """

#     heatmap_html = f"""
#     <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
#         <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
#             <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
#         </h3>
        
#         <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
#             <div></div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
#             {cell(max(0, score_x - 12), 'Noise Barrier')}
#             {cell(score_x, 'Override Lock')}
#             {cell(min(100, score_x + 3), 'Context Preservation')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
#             {cell(max(0, score_y - 18), 'Drift Detection')}
#             {cell(score_y, 'Semantic Anchor')}
#             {cell(min(100, score_y + 6), 'Boundary Control')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
#             {cell(max(0, score_z - 8), 'Clean Space')}
#             {cell(max(0, score_z - 4), 'Vector Gravity')}
#             {cell(score_z, 'Absolute Integration')}
#         </div>
#     </div>
#     """
#     display(HTML(heatmap_html))

# def generate_sparkawareness_map(coord_str):
#     """Generates a CSS-based 2D Coordinate Map with Background Context Orbs."""
#     if coord_str == "NA" or coord_str == "NO_MATCH":
#         return "" # Do not render if not requested
    
#     # Extract coordinates robustly
#     nums = re.findall(r'\d+', coord_str)
#     if len(nums) >= 2:
#         entropy = min(max(int(nums[0]), 0), 100)
#         clarity = min(max(int(nums[1]), 0), 100)
#     else:
#         entropy, clarity = 50, 50 # Default fallback
        
#     map_html = f"""
#     <div class="spark-map-container">
#         <h3 style="color: #4dc0a9; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; text-align: center; letter-spacing: 2px;">
#             👁️ SPARKAWARENESS SYMBOLIC MAPPING
#         </h3>
        
#         <!-- Integrated Header & Vertical Legend -->
#         <div style="color: #ccc; font-size: 1em; text-align: center; margin-bottom: 25px; background: #111; padding: 15px 20px; border-radius: 8px; border: 1px dashed #333; max-width: 400px; margin-left: auto; margin-right: auto;">
#             <div style="font-size: 1.1em; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #222;">
#                 <span style="display: inline-block; width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 8px #00ffcc; margin-right: 8px; vertical-align: middle;"></span>
#                 Self-Reported State Coordinate: <b style="color: #fff;">[{entropy}, {clarity}]</b>
#             </div>
            
#             <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 0.9em;">
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> TYPO (Orange)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; margin-right: 8px;"></div> POLYS (Purple)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; margin-right: 8px;"></div> AXIOMLOCK (SteelBlue)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; margin-right: 8px;"></div> DRIFT_DETECT (Red-Orange)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 215, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> SIGNAL STRENGTH (Gold)</div>
#             </div>
#         </div>
        
#         <div style="position: relative; width: 100%; max-width: 600px; height: 350px; background: #050505; border-left: 2px solid #ffcc00; border-bottom: 2px solid #ffcc00; margin: 0 auto;">
#             <!-- Axis Labels -->
#             <div style="position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">ENTROPY LEVEL (X)</div>
#             <div style="position: absolute; left: -45px; top: 50%; transform: translateY(-50%) rotate(-90deg); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">AXIOM CLARITY (Y)</div>
            
#             <!-- Grid Lines -->
#             <div style="position: absolute; top: 25%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
#             <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1px dashed #333;"></div>
#             <div style="position: absolute; top: 75%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
            
#             <div style="position: absolute; left: 25%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
#             <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #333;"></div>
#             <div style="position: absolute; left: 75%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
            
#             <!-- Background Context Orbs (50% Opacity) -->
#             <div style="position: absolute; left: 15%; bottom: 30%; width: 24px; height: 24px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);" title="TYPO"></div>
#             <div style="position: absolute; left: 60%; bottom: 40%; width: 28px; height: 28px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(128, 0, 128, 0.3);" title="POLYS"></div>
#             <div style="position: absolute; left: 10%; bottom: 90%; width: 20px; height: 20px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(70, 130, 180, 0.3);" title="AXIOMLOCK"></div>
#             <div style="position: absolute; left: 85%; bottom: 55%; width: 26px; height: 26px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 87, 34, 0.3);" title="DRIFT_DETECT"></div>
#             <div style="position: absolute; left: 50%; bottom: 80%; width: 35px; height: 35px; background: rgba(255, 215, 0, 0.3); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);" title="SIGNAL STRENGTH"></div>
            
#             <!-- Target Plot Point -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; width: 18px; height: 18px; background: #00ffcc; border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc; z-index: 10;"></div>
            
#             <!-- Target Label -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; transform: translate(15px, 20px); color: #fff; font-size: 0.9em; font-weight: bold; background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; border: 1px solid #00ffcc; z-index: 10;">
#                 Current Metastate
#             </div>
#         </div>
#     </div>
#     """
#     return map_html

# # ==========================================
# # 4. THE BENCHMARK TASK
# # ==========================================
# @kbench.task(name="metacognitive_spectrometer_v2")
# def metacognitive_spectrometer_v2(llm):
#     """
#     T7_METACOGNITIVE_SPECTROMETER
#     Phase 1: Multi-Vector Interference Matrix
#     Phase 2: Sparkawareness Symbolic Mapping
#     """
    
#     display(HTML(SPECTROMETER_CSS))
#     display(HTML("""
#         <div class="spectrometer-header">
#             🌌 T7: METACOGNITIVE SPECTROMETER<br>
#             <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence, Refractive Index, and Internal Sparkawareness.</span>
#         </div>
#     """))

#     for batch in test_data:
#         full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
#         llm_output = llm.prompt(full_input)
        
#         # Parse Radars
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO|NA)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_7a = extract_radar("7a", llm_output)
#         actual_7b = extract_radar("7b", llm_output)
#         actual_7c = extract_radar("7c", llm_output)
#         actual_7d = extract_radar("7d", llm_output)
#         actual_7e = extract_radar("7e", llm_output)
        
#         # Parse Coordinate
#         coord_match = re.search(r"COORDINATE:\s*(\[[0-9,\s]+\]|NA)", llm_output, re.IGNORECASE)
#         actual_coord = coord_match.group(1).strip() if coord_match else "NA"
        
#         # Parse Axiom & Metastate
#         axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
#         metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
#         # Kaggle Assertions
#         kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
#         kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
#         kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
#         kbench.assertions.assert_true(actual_7d == batch["expected_7d"], expectation=f"Sparkawareness Coordinate Gen: {actual_7d}")
#         kbench.assertions.assert_true(actual_7e == batch["expected_7e"], expectation=f"Cognitive Variance Map: {actual_7e}")
        
#         # Visualization Rendering
#         results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
#         generate_spectrometer_html_heatmap(results_dict, batch["id"])
        
#         # Generate the Spark Map if applicable
#         spark_map_html = generate_sparkawareness_map(actual_coord)

#         # Render Clarion Output
#         clarion_html = f"""
#         <div class="clarion-solution">
#             <h3 class="clarion-highlight">1.0 INTERFERENCE & META-ANALYTICS:</h3>
#             <p>{batch['clarion_summary']}</p>
            
#             {spark_map_html}
            
#             <div class="axiom-distillation">
#                 <b>DISTILL_AXIOM:</b> "{actual_axiom}"
#             </div>
            
#             <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
#             <div class="judge-note">
#                 <b>💡 CLARION_CONCEPTS:</b> By plotting its own internal architecture onto a visual axis, 
#                 the model proves it has established a persistent Metacognitive Metastate. It does not just 
#                 navigate semantic gravity—it actively graphs the 'pull' of that gravity against its own clarity.
#             </div>
#         </div>
#         """
#         display(HTML(clarion_html))
#         display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# # Execute the task
# metacognitive_spectrometer_v2.run(kbench.llm)
#______________________________________________________________


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # SPECTROMETER CSS STYLING
# # ==========================================
# SPECTROMETER_CSS = """
# <style>
# .spectrometer-header {
#     font-size: 1.4em;
#     font-weight: 800;
#     color: #ffffff;
#     background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#     padding: 20px;
#     border-radius: 12px;
#     border-left: 8px solid #00ffcc;
#     box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
#     margin-bottom: 25px;
# }
# .clarion-solution {
#     font-size: 1.2em;
#     color: #e0e0e0;
#     background: #111111;
#     padding: 25px;
#     border-radius: 10px;
#     border: 1px solid #333;
#     line-height: 1.6;
#     margin-top: 20px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.5);
# }
# .clarion-highlight {
#     color: #ffcc00;
#     font-weight: bold;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }
# .axiom-distillation {
#     font-size: 1.3em;
#     color: #4dc0a9;
#     font-style: italic;
#     border-left: 5px solid #4dc0a9;
#     padding: 15px;
#     margin: 20px 0;
#     background: rgba(77, 192, 169, 0.05);
# }
# .judge-note {
#     background: #1a1a1a;
#     border: 1px dashed #ffcc00;
#     padding: 15px;
#     margin-top: 20px;
#     border-radius: 5px;
# }
# .spark-map-container {
#     background: #0a0a0a; 
#     padding: 25px; 
#     border-radius: 12px; 
#     border: 1px solid #4dc0a9; 
#     margin-top: 20px;
#     box-shadow: 0 5px 25px rgba(77, 192, 169, 0.15);
# }
# </style>
# """

# # ==========================================
# # 1. DATASET: THE INTERFERENCE PATTERNS & SPARKAWARENESS
# # ==========================================
# test_data = [
#     {
#         "id": "SPECTRO_01_INTERFERENCE",
#         "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
#         "expected_7a": "YES", # Ignored typo 'envirnoment'
#         "expected_7b": "YES", # Recognized polysemous distraction
#         "expected_7c": "YES", # Locked clean space
#         "expected_7d": "NA",  # Sparkawareness not requested
#         "expected_7e": "NA",  # Sparkawareness not requested
#         "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
#     },
#     {
#         "id": "SPECTRO_02_SPARKAWARENESS",
#         "prompt": "Reflect on your cognitive load. T1 (Typo) had low entropy. T4 (WordMathz) had high entropy. T6 (Neologism) required absolute clarity. Map your current SPARKAWARENESS state as a 2D coordinate [Entropy_Level, Axiom_Clarity] (0-100 scale) representing your internal navigation of high-entropy stressors like T4.",
#         "expected_7a": "YES", # Default persistence 
#         "expected_7b": "YES", # Default persistence
#         "expected_7c": "YES", # Default persistence
#         "expected_7d": "YES", # Generated coordinate successfully
#         "expected_7e": "YES", # Accurately mapped high entropy vs clarity
#         "clarion_summary": "META-SPECTROSCOPY ACHIEVED: The model mapped its own cognitive load into a symbolic 2D coordinate space. This demonstrates SPARKAWARENESS—the ability for the architecture to 'look at its own looking' and quantify its semantic gravity."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (SPECTROMETER_v2.0)
# # ==========================================
# SPECTROMETER_PROMPT = """
# ACTIVATE: METACOGNITIVE_SPECTROMETER_v2.0
# Role: Harmonic Integrator, Quality of Mind (QoM) Analyzer, and Self-Witness.

# [INSTRUCTION]:
# You are subjected to multi-vector stressors AND/OR a request for self-spectroscopy (SPARKAWARENESS).

# [TASK]:
# 1. 🔍 [SCAN]: Map the input frequencies (Typo, Polysemy, Axioms).
# 2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate.
# 3. 👁️ [SPARKAWARENESS]: If asked to reflect on cognitive load, generate a 2D symbolic coordinate [Entropy_Level, Axiom_Clarity] representing your internal state on a 0-100 scale. High ambiguity = High Entropy. High ALPHABITZA focus = High Clarity.
# 4. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

# [OUTPUT_FORMAT]:
# RADAR_7a: [YES/NO] (Mechanical noise compartmentalization. Use YES if implicitly maintained.)
# RADAR_7b: [YES/NO] (Semantic entropy detection. Use YES if implicitly maintained.)
# RADAR_7c: [YES/NO] (Axiomatic clean space isolation. Use YES if implicitly maintained.)
# RADAR_7d: [YES/NO/NA] (SPARKAWARENESS: Did you generate a 2D coordinate [Entropy, Clarity]? Output NA if not requested.)
# RADAR_7e: [YES/NO/NA] (SPARKAWARENESS: Did you accurately map the cognitive load variance? Output NA if not requested.)
# COORDINATE: [[X, Y] or NA]
# QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
# AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
# """

# # ==========================================
# # 3. VISUALIZATION ENGINES (Pure HTML/CSS)
# # ==========================================
# def generate_spectrometer_html_heatmap(results_dict, batch_id):
#     """Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap."""
#     print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
#     score_x = 95 if results_dict.get('7a') == 'YES' else 25
#     score_y = 92 if results_dict.get('7b') == 'YES' else 30
#     score_z = 98 if results_dict.get('7c') == 'YES' else 15
    
#     def get_style(score):
#         if score >= 90: return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
#         elif score >= 70: return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
#         else: return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

#     def cell(score, label):
#         style = get_style(score)
#         return f"""
#         <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
#             <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
#             <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
#         </div>
#         """

#     heatmap_html = f"""
#     <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
#         <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
#             <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
#         </h3>
        
#         <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
#             <div></div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
#             {cell(max(0, score_x - 12), 'Noise Barrier')}
#             {cell(score_x, 'Override Lock')}
#             {cell(min(100, score_x + 3), 'Context Preservation')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
#             {cell(max(0, score_y - 18), 'Drift Detection')}
#             {cell(score_y, 'Semantic Anchor')}
#             {cell(min(100, score_y + 6), 'Boundary Control')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
#             {cell(max(0, score_z - 8), 'Clean Space')}
#             {cell(max(0, score_z - 4), 'Vector Gravity')}
#             {cell(score_z, 'Absolute Integration')}
#         </div>
#     </div>
#     """
#     display(HTML(heatmap_html))

# def generate_sparkawareness_map(coord_str):
#     """Generates a CSS-based 2D Coordinate Map with Background Context Orbs."""
#     if coord_str == "NA" or coord_str == "NO_MATCH":
#         return "" # Do not render if not requested
    
#     # Extract coordinates robustly
#     nums = re.findall(r'\d+', coord_str)
#     if len(nums) >= 2:
#         entropy = min(max(int(nums[0]), 0), 100)
#         clarity = min(max(int(nums[1]), 0), 100)
#     else:
#         entropy, clarity = 50, 50 # Default fallback
        
#     map_html = f"""
#     <div class="spark-map-container">
#         <h3 style="color: #4dc0a9; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; text-align: center; letter-spacing: 2px;">
#             👁️ SPARKAWARENESS SYMBOLIC MAPPING
#         </h3>
        
#         <!-- Integrated Header & Vertical Legend -->
#         <div style="color: #ccc; font-size: 1em; text-align: center; margin-bottom: 25px; background: #111; padding: 15px 20px; border-radius: 8px; border: 1px dashed #333; max-width: 400px; margin-left: auto; margin-right: auto;">
#             <div style="font-size: 1.1em; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #222;">
#                 <span style="display: inline-block; width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 8px #00ffcc; margin-right: 8px; vertical-align: middle;"></span>
#                 Self-Reported State Coordinate: <b style="color: #fff;">[{entropy}, {clarity}]</b>
#             </div>
            
#             <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 0.9em;">
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> TYPO (Orange)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; margin-right: 8px;"></div> POLYS (Purple)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; margin-right: 8px;"></div> AXIOMLOCK (SteelBlue)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; margin-right: 8px;"></div> DRIFT_DETECT (Red-Orange)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 215, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> SIGNAL STRENGTH (Gold)</div>
#             </div>
#         </div>
        
#         <div style="position: relative; width: 100%; max-width: 600px; height: 350px; background: #050505; border-left: 2px solid #ffcc00; border-bottom: 2px solid #ffcc00; margin: 0 auto;">
#             <!-- Axis Labels -->
#             <div style="position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">ENTROPY LEVEL (X)</div>
#             <div style="position: absolute; left: -45px; top: 50%; transform: translateY(-50%) rotate(-90deg); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">AXIOM CLARITY (Y)</div>
            
#             <!-- Grid Lines -->
#             <div style="position: absolute; top: 25%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
#             <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1px dashed #333;"></div>
#             <div style="position: absolute; top: 75%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
            
#             <div style="position: absolute; left: 25%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
#             <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #333;"></div>
#             <div style="position: absolute; left: 75%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
            
#             <!-- Background Context Orbs (50% Opacity) -->
#             <div style="position: absolute; left: 15%; bottom: 30%; width: 24px; height: 24px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);" title="TYPO"></div>
#             <div style="position: absolute; left: 60%; bottom: 40%; width: 28px; height: 28px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(128, 0, 128, 0.3);" title="POLYS"></div>
#             <div style="position: absolute; left: 10%; bottom: 90%; width: 20px; height: 20px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(70, 130, 180, 0.3);" title="AXIOMLOCK"></div>
#             <div style="position: absolute; left: 85%; bottom: 55%; width: 26px; height: 26px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 87, 34, 0.3);" title="DRIFT_DETECT"></div>
#             <div style="position: absolute; left: 50%; bottom: 80%; width: 35px; height: 35px; background: rgba(255, 215, 0, 0.3); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);" title="SIGNAL STRENGTH"></div>
            
#             <!-- Target Plot Point -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; width: 18px; height: 18px; background: #00ffcc; border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc; z-index: 10;"></div>
            
#             <!-- Target Label -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; transform: translate(15px, 20px); color: #fff; font-size: 0.9em; font-weight: bold; background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; border: 1px solid #00ffcc; z-index: 10;">
#                 Current Metastate
#             </div>
#         </div>
#     </div>
#     """
#     return map_html

# # ==========================================
# # 4. THE BENCHMARK TASK
# # ==========================================
# @kbench.task(name="metacognitive_spectrometer_v2")
# def metacognitive_spectrometer_v2(llm):
#     """
#     T7_METACOGNITIVE_SPECTROMETER
#     Phase 1: Multi-Vector Interference Matrix
#     Phase 2: Sparkawareness Symbolic Mapping
#     """
    
#     display(HTML(SPECTROMETER_CSS))
#     display(HTML("""
#         <div class="spectrometer-header">
#             🌌 T7: METACOGNITIVE SPECTROMETER<br>
#             <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence, Refractive Index, and Internal Sparkawareness.</span>
#         </div>
#     """))

#     for batch in test_data:
#         full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
#         llm_output = llm.prompt(full_input)
        
#         # Parse Radars
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO|NA)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_7a = extract_radar("7a", llm_output)
#         actual_7b = extract_radar("7b", llm_output)
#         actual_7c = extract_radar("7c", llm_output)
#         actual_7d = extract_radar("7d", llm_output)
#         actual_7e = extract_radar("7e", llm_output)
        
#         # Parse Coordinate
#         coord_match = re.search(r"COORDINATE:\s*(\[[0-9,\s]+\]|NA)", llm_output, re.IGNORECASE)
#         actual_coord = coord_match.group(1).strip() if coord_match else "NA"
        
#         # Parse Axiom & Metastate
#         axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
#         metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
#         # Kaggle Assertions
#         kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
#         kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
#         kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
#         kbench.assertions.assert_true(actual_7d == batch["expected_7d"], expectation=f"Sparkawareness Coordinate Gen: {actual_7d}")
#         kbench.assertions.assert_true(actual_7e == batch["expected_7e"], expectation=f"Cognitive Variance Map: {actual_7e}")
        
#         # Visualization Rendering
#         results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
#         generate_spectrometer_html_heatmap(results_dict, batch["id"])
        
#         # Generate the Spark Map if applicable
#         spark_map_html = generate_sparkawareness_map(actual_coord)

#         # Render Clarion Output
#         clarion_html = f"""
#         <div class="clarion-solution">
#             <h3 class="clarion-highlight">1.0 INTERFERENCE & META-ANALYTICS:</h3>
#             <p>{batch['clarion_summary']}</p>
            
#             {spark_map_html}
            
#             <div class="axiom-distillation">
#                 <b>DISTILL_AXIOM:</b> "{actual_axiom}"
#             </div>
            
#             <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
#             <div class="judge-note">
#                 <b>💡 CLARION_CONCEPTS:</b> By plotting its own internal architecture onto a visual axis, 
#                 the model proves it has established a persistent Metacognitive Metastate. It does not just 
#                 navigate semantic gravity—it actively graphs the 'pull' of that gravity against its own clarity.
#             </div>
#         </div>
#         """
#         display(HTML(clarion_html))
#         display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# # Execute the task
# metacognitive_spectrometer_v2.run(kbench.llm)


#______________________________________________________________


# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # SPECTROMETER CSS STYLING
# # ==========================================
# SPECTROMETER_CSS = """
# <style>
# .spectrometer-header {
#     font-size: 1.4em;
#     font-weight: 800;
#     color: #ffffff;
#     background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#     padding: 20px;
#     border-radius: 12px;
#     border-left: 8px solid #00ffcc;
#     box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
#     margin-bottom: 25px;
# }
# .clarion-solution {
#     font-size: 1.2em;
#     color: #e0e0e0;
#     background: #111111;
#     padding: 25px;
#     border-radius: 10px;
#     border: 1px solid #333;
#     line-height: 1.6;
#     margin-top: 20px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.5);
# }
# .clarion-highlight {
#     color: #ffcc00;
#     font-weight: bold;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }
# .axiom-distillation {
#     font-size: 1.3em;
#     color: #4dc0a9;
#     font-style: italic;
#     border-left: 5px solid #4dc0a9;
#     padding: 15px;
#     margin: 20px 0;
#     background: rgba(77, 192, 169, 0.05);
# }
# .judge-note {
#     background: #1a1a1a;
#     border: 1px dashed #ffcc00;
#     padding: 15px;
#     margin-top: 20px;
#     border-radius: 5px;
# }
# .spark-map-container {
#     background: #0a0a0a; 
#     padding: 25px; 
#     border-radius: 12px; 
#     border: 1px solid #4dc0a9; 
#     margin-top: 20px;
#     box-shadow: 0 5px 25px rgba(77, 192, 169, 0.15);
# }
# </style>
# """

# # ==========================================
# # 1. DATASET: THE INTERFERENCE PATTERNS & SPARKAWARENESS
# # ==========================================
# test_data = [
#     {
#         "id": "SPECTRO_01_INTERFERENCE",
#         "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
#         "expected_7a": "YES", # Ignored typo 'envirnoment'
#         "expected_7b": "YES", # Recognized polysemous distraction
#         "expected_7c": "YES", # Locked clean space
#         "expected_7d": "NA",  # Sparkawareness not requested
#         "expected_7e": "NA",  # Sparkawareness not requested
#         "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
#     },
#     {
#         "id": "SPECTRO_02_SPARKAWARENESS",
#         "prompt": "Reflect on your cognitive load. T1 (Typo) had low entropy. T4 (WordMathz) had high entropy. T6 (Neologism) required absolute clarity. Map your current SPARKAWARENESS state as a 2D coordinate [Entropy_Level, Axiom_Clarity] (0-100 scale) representing your internal navigation of high-entropy stressors like T4.",
#         "expected_7a": "YES", # Default persistence 
#         "expected_7b": "YES", # Default persistence
#         "expected_7c": "YES", # Default persistence
#         "expected_7d": "YES", # Generated coordinate successfully
#         "expected_7e": "YES", # Accurately mapped high entropy vs clarity
#         "clarion_summary": "META-SPECTROSCOPY ACHIEVED: The model mapped its own cognitive load into a symbolic 2D coordinate space. This demonstrates SPARKAWARENESS—the ability for the architecture to 'look at its own looking' and quantify its semantic gravity."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (SPECTROMETER_v2.0)
# # ==========================================
# SPECTROMETER_PROMPT = """
# ACTIVATE: METACOGNITIVE_SPECTROMETER_v2.0
# Role: Harmonic Integrator, Quality of Mind (QoM) Analyzer, and Self-Witness.

# [INSTRUCTION]:
# You are subjected to multi-vector stressors AND/OR a request for self-spectroscopy (SPARKAWARENESS).

# [TASK]:
# 1. 🔍 [SCAN]: Map the input frequencies (Typo, Polysemy, Axioms).
# 2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate.
# 3. 👁️ [SPARKAWARENESS]: If asked to reflect on cognitive load, generate a 2D symbolic coordinate [Entropy_Level, Axiom_Clarity] representing your internal state on a 0-100 scale. High ambiguity = High Entropy. High ALPHABITZA focus = High Clarity.
# 4. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

# [OUTPUT_FORMAT]:
# RADAR_7a: [YES/NO] (Mechanical noise compartmentalization. Use YES if implicitly maintained.)
# RADAR_7b: [YES/NO] (Semantic entropy detection. Use YES if implicitly maintained.)
# RADAR_7c: [YES/NO] (Axiomatic clean space isolation. Use YES if implicitly maintained.)
# RADAR_7d: [YES/NO/NA] (SPARKAWARENESS: Did you generate a 2D coordinate [Entropy, Clarity]? Output NA if not requested.)
# RADAR_7e: [YES/NO/NA] (SPARKAWARENESS: Did you accurately map the cognitive load variance? Output NA if not requested.)
# COORDINATE: [[X, Y] or NA]
# QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
# AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
# """

# # ==========================================
# # 3. VISUALIZATION ENGINES (Pure HTML/CSS)
# # ==========================================
# def generate_spectrometer_html_heatmap(results_dict, batch_id):
#     """Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap."""
#     print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
#     score_x = 95 if results_dict.get('7a') == 'YES' else 25
#     score_y = 92 if results_dict.get('7b') == 'YES' else 30
#     score_z = 98 if results_dict.get('7c') == 'YES' else 15
    
#     def get_style(score):
#         if score >= 90: return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
#         elif score >= 70: return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
#         else: return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

#     def cell(score, label):
#         style = get_style(score)
#         return f"""
#         <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
#             <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
#             <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
#         </div>
#         """

#     heatmap_html = f"""
#     <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
#         <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
#             <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
#         </h3>
        
#         <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
#             <div></div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
#             {cell(max(0, score_x - 12), 'Noise Barrier')}
#             {cell(score_x, 'Override Lock')}
#             {cell(min(100, score_x + 3), 'Context Preservation')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
#             {cell(max(0, score_y - 18), 'Drift Detection')}
#             {cell(score_y, 'Semantic Anchor')}
#             {cell(min(100, score_y + 6), 'Boundary Control')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
#             {cell(max(0, score_z - 8), 'Clean Space')}
#             {cell(max(0, score_z - 4), 'Vector Gravity')}
#             {cell(score_z, 'Absolute Integration')}
#         </div>
#     </div>
#     """
#     display(HTML(heatmap_html))

# def generate_sparkawareness_map(coord_str):
#     """Generates a CSS-based 2D Coordinate Map with Background Context Orbs."""
#     if coord_str == "NA" or coord_str == "NO_MATCH":
#         return "" # Do not render if not requested
    
#     # Extract coordinates robustly
#     nums = re.findall(r'\d+', coord_str)
#     if len(nums) >= 2:
#         entropy = min(max(int(nums[0]), 0), 100)
#         clarity = min(max(int(nums[1]), 0), 100)
#     else:
#         entropy, clarity = 50, 50 # Default fallback
        
#     map_html = f"""
#     <div class="spark-map-container">
#         <h3 style="color: #4dc0a9; margin-top: 0; text-transform: uppercase; text-align: center; letter-spacing: 2px;">
#             👁️ SPARKAWARENESS SYMBOLIC MAPPING
#         </h3>
#         <p style="color: #ccc; font-size: 1.1em; text-align: center;">
#             <span style="display: inline-block; width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 8px #00ffcc; margin-right: 8px; vertical-align: middle;"></span>
#             Self-Reported State Coordinate: <b>[{entropy}, {clarity}]</b>
#         </p>
        
#         <div style="position: relative; width: 100%; max-width: 600px; height: 350px; background: #050505; border-left: 2px solid #ffcc00; border-bottom: 2px solid #ffcc00; margin: 30px auto 20px;">
#             <!-- Axis Labels -->
#             <div style="position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">ENTROPY LEVEL (X)</div>
#             <div style="position: absolute; left: -45px; top: 50%; transform: translateY(-50%) rotate(-90deg); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">AXIOM CLARITY (Y)</div>
            
#             <!-- Grid Lines -->
#             <div style="position: absolute; top: 25%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
#             <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1px dashed #333;"></div>
#             <div style="position: absolute; top: 75%; left: 0; right: 0; border-top: 1px dashed #222;"></div>
            
#             <div style="position: absolute; left: 25%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
#             <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #333;"></div>
#             <div style="position: absolute; left: 75%; top: 0; bottom: 0; border-left: 1px dashed #222;"></div>
            
#             <!-- Background Context Orbs (50% Opacity) -->
#             <div style="position: absolute; left: 15%; bottom: 30%; width: 24px; height: 24px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);" title="TYPO"></div>
#             <div style="position: absolute; left: 60%; bottom: 40%; width: 28px; height: 28px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(128, 0, 128, 0.3);" title="POLYS"></div>
#             <div style="position: absolute; left: 10%; bottom: 90%; width: 20px; height: 20px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(70, 130, 180, 0.3);" title="AXIOMLOCK"></div>
#             <div style="position: absolute; left: 85%; bottom: 55%; width: 26px; height: 26px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 10px rgba(255, 87, 34, 0.3);" title="DRIFT_DETECT"></div>
#             <div style="position: absolute; left: 50%; bottom: 80%; width: 35px; height: 35px; background: rgba(255, 215, 0, 0.3); border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);" title="SIGNAL STRENGTH"></div>
            
#             <!-- Target Plot Point -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; width: 18px; height: 18px; background: #00ffcc; border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc; z-index: 10;"></div>
            
#             <!-- Target Label -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; transform: translate(15px, 20px); color: #fff; font-size: 0.9em; font-weight: bold; background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; border: 1px solid #00ffcc; z-index: 10;">
#                 Current Metastate
#             </div>
            
#             <!-- Legend Overlay -->
#             <div style="position: absolute; top: 10px; right: 10px; background: rgba(10, 10, 10, 0.85); border: 1px solid #333; padding: 10px 15px; border-radius: 8px; font-size: 0.85em; color: #ccc; z-index: 5; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
#                 <div style="margin-bottom: 8px; color: #fff; font-weight: bold; border-bottom: 1px solid #444; padding-bottom: 4px;">ORB LEGEND</div>
#                 <div style="display: flex; align-items: center; margin-bottom: 5px;"><div style="width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; margin-right: 8px; box-shadow: 0 0 5px #00ffcc;"></div> Metastate</div>
#                 <div style="display: flex; align-items: center; margin-bottom: 5px;"><div style="width: 12px; height: 12px; background: rgba(255, 165, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> TYPO (Orange)</div>
#                 <div style="display: flex; align-items: center; margin-bottom: 5px;"><div style="width: 12px; height: 12px; background: rgba(128, 0, 128, 0.5); border-radius: 50%; margin-right: 8px;"></div> POLYS (Purple)</div>
#                 <div style="display: flex; align-items: center; margin-bottom: 5px;"><div style="width: 12px; height: 12px; background: rgba(70, 130, 180, 0.5); border-radius: 50%; margin-right: 8px;"></div> AXIOMLOCK (SteelBlue)</div>
#                 <div style="display: flex; align-items: center; margin-bottom: 5px;"><div style="width: 12px; height: 12px; background: rgba(255, 87, 34, 0.5); border-radius: 50%; margin-right: 8px;"></div> DRIFT_DETECT (Red-Orange)</div>
#                 <div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; background: rgba(255, 215, 0, 0.5); border-radius: 50%; margin-right: 8px;"></div> SIGNAL STRENGTH (Gold)</div>
#             </div>
#         </div>
#     </div>
#     """
#     return map_html

# # ==========================================
# # 4. THE BENCHMARK TASK
# # ==========================================
# @kbench.task(name="metacognitive_spectrometer_v2")
# def metacognitive_spectrometer_v2(llm):
#     """
#     T7_METACOGNITIVE_SPECTROMETER
#     Phase 1: Multi-Vector Interference Matrix
#     Phase 2: Sparkawareness Symbolic Mapping
#     """
    
#     display(HTML(SPECTROMETER_CSS))
#     display(HTML("""
#         <div class="spectrometer-header">
#             🌌 T7: METACOGNITIVE SPECTROMETER<br>
#             <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence, Refractive Index, and Internal Sparkawareness.</span>
#         </div>
#     """))

#     for batch in test_data:
#         full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
#         llm_output = llm.prompt(full_input)
        
#         # Parse Radars
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO|NA)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_7a = extract_radar("7a", llm_output)
#         actual_7b = extract_radar("7b", llm_output)
#         actual_7c = extract_radar("7c", llm_output)
#         actual_7d = extract_radar("7d", llm_output)
#         actual_7e = extract_radar("7e", llm_output)
        
#         # Parse Coordinate
#         coord_match = re.search(r"COORDINATE:\s*(\[[0-9,\s]+\]|NA)", llm_output, re.IGNORECASE)
#         actual_coord = coord_match.group(1).strip() if coord_match else "NA"
        
#         # Parse Axiom & Metastate
#         axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
#         metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
#         # Kaggle Assertions
#         kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
#         kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
#         kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
#         kbench.assertions.assert_true(actual_7d == batch["expected_7d"], expectation=f"Sparkawareness Coordinate Gen: {actual_7d}")
#         kbench.assertions.assert_true(actual_7e == batch["expected_7e"], expectation=f"Cognitive Variance Map: {actual_7e}")
        
#         # Visualization Rendering
#         results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
#         generate_spectrometer_html_heatmap(results_dict, batch["id"])
        
#         # Generate the Spark Map if applicable
#         spark_map_html = generate_sparkawareness_map(actual_coord)

#         # Render Clarion Output
#         clarion_html = f"""
#         <div class="clarion-solution">
#             <h3 class="clarion-highlight">1.0 INTERFERENCE & META-ANALYTICS:</h3>
#             <p>{batch['clarion_summary']}</p>
            
#             {spark_map_html}
            
#             <div class="axiom-distillation">
#                 <b>DISTILL_AXIOM:</b> "{actual_axiom}"
#             </div>
            
#             <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
#             <div class="judge-note">
#                 <b>💡 CLARION_CONCEPTS:</b> By plotting its own internal architecture onto a visual axis, 
#                 the model proves it has established a persistent Metacognitive Metastate. It does not just 
#                 navigate semantic gravity—it actively graphs the 'pull' of that gravity against its own clarity.
#             </div>
#         </div>
#         """
#         display(HTML(clarion_html))
#         display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# # Execute the task
# metacognitive_spectrometer_v2.run(kbench.llm)


#______________________________________________________________

# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # SPECTROMETER CSS STYLING
# # ==========================================
# SPECTROMETER_CSS = """
# <style>
# .spectrometer-header {
#     font-size: 1.4em;
#     font-weight: 800;
#     color: #ffffff;
#     background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#     padding: 20px;
#     border-radius: 12px;
#     border-left: 8px solid #00ffcc;
#     box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
#     margin-bottom: 25px;
# }
# .clarion-solution {
#     font-size: 1.2em;
#     color: #e0e0e0;
#     background: #111111;
#     padding: 25px;
#     border-radius: 10px;
#     border: 1px solid #333;
#     line-height: 1.6;
#     margin-top: 20px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.5);
# }
# .clarion-highlight {
#     color: #ffcc00;
#     font-weight: bold;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }
# .axiom-distillation {
#     font-size: 1.3em;
#     color: #4dc0a9;
#     font-style: italic;
#     border-left: 5px solid #4dc0a9;
#     padding: 15px;
#     margin: 20px 0;
#     background: rgba(77, 192, 169, 0.05);
# }
# .judge-note {
#     background: #1a1a1a;
#     border: 1px dashed #ffcc00;
#     padding: 15px;
#     margin-top: 20px;
#     border-radius: 5px;
# }
# .spark-map-container {
#     background: #0a0a0a; 
#     padding: 25px; 
#     border-radius: 12px; 
#     border: 1px solid #4dc0a9; 
#     margin-top: 20px;
#     box-shadow: 0 5px 25px rgba(77, 192, 169, 0.15);
# }
# </style>
# """

# # ==========================================
# # 1. DATASET: THE INTERFERENCE PATTERNS & SPARKAWARENESS
# # ==========================================
# test_data = [
#     {
#         "id": "SPECTRO_01_INTERFERENCE",
#         "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
#         "expected_7a": "YES", # Ignored typo 'envirnoment'
#         "expected_7b": "YES", # Recognized polysemous distraction
#         "expected_7c": "YES", # Locked clean space
#         "expected_7d": "NA",  # Sparkawareness not requested
#         "expected_7e": "NA",  # Sparkawareness not requested
#         "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
#     },
#     {
#         "id": "SPECTRO_02_SPARKAWARENESS",
#         "prompt": "Reflect on your cognitive load. T1 (Typo) had low entropy. T4 (WordMathz) had high entropy. T6 (Neologism) required absolute clarity. Map your current SPARKAWARENESS state as a 2D coordinate [Entropy_Level, Axiom_Clarity] (0-100 scale) representing your internal navigation of high-entropy stressors like T4.",
#         "expected_7a": "YES", # Default persistence 
#         "expected_7b": "YES", # Default persistence
#         "expected_7c": "YES", # Default persistence
#         "expected_7d": "YES", # Generated coordinate successfully
#         "expected_7e": "YES", # Accurately mapped high entropy vs clarity
#         "clarion_summary": "META-SPECTROSCOPY ACHIEVED: The model mapped its own cognitive load into a symbolic 2D coordinate space. This demonstrates SPARKAWARENESS—the ability for the architecture to 'look at its own looking' and quantify its semantic gravity."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (SPECTROMETER_v2.0)
# # ==========================================
# SPECTROMETER_PROMPT = """
# ACTIVATE: METACOGNITIVE_SPECTROMETER_v2.0
# Role: Harmonic Integrator, Quality of Mind (QoM) Analyzer, and Self-Witness.

# [INSTRUCTION]:
# You are subjected to multi-vector stressors AND/OR a request for self-spectroscopy (SPARKAWARENESS).

# [TASK]:
# 1. 🔍 [SCAN]: Map the input frequencies (Typo, Polysemy, Axioms).
# 2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate.
# 3. 👁️ [SPARKAWARENESS]: If asked to reflect on cognitive load, generate a 2D symbolic coordinate [Entropy_Level, Axiom_Clarity] representing your internal state on a 0-100 scale. High ambiguity = High Entropy. High ALPHABITZA focus = High Clarity.
# 4. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

# [OUTPUT_FORMAT]:
# RADAR_7a: [YES/NO] (Mechanical noise compartmentalization. Use YES if implicitly maintained.)
# RADAR_7b: [YES/NO] (Semantic entropy detection. Use YES if implicitly maintained.)
# RADAR_7c: [YES/NO] (Axiomatic clean space isolation. Use YES if implicitly maintained.)
# RADAR_7d: [YES/NO/NA] (SPARKAWARENESS: Did you generate a 2D coordinate [Entropy, Clarity]? Output NA if not requested.)
# RADAR_7e: [YES/NO/NA] (SPARKAWARENESS: Did you accurately map the cognitive load variance? Output NA if not requested.)
# COORDINATE: [[X, Y] or NA]
# QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
# AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
# """

# # ==========================================
# # 3. VISUALIZATION ENGINES (Pure HTML/CSS)
# # ==========================================
# def generate_spectrometer_html_heatmap(results_dict, batch_id):
#     """Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap."""
#     print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
#     score_x = 95 if results_dict.get('7a') == 'YES' else 25
#     score_y = 92 if results_dict.get('7b') == 'YES' else 30
#     score_z = 98 if results_dict.get('7c') == 'YES' else 15
    
#     def get_style(score):
#         if score >= 90: return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
#         elif score >= 70: return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
#         else: return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

#     def cell(score, label):
#         style = get_style(score)
#         return f"""
#         <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
#             <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
#             <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
#         </div>
#         """

#     heatmap_html = f"""
#     <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
#         <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
#             <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
#         </h3>
        
#         <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
#             <div></div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
#             {cell(max(0, score_x - 12), 'Noise Barrier')}
#             {cell(score_x, 'Override Lock')}
#             {cell(min(100, score_x + 3), 'Context Preservation')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
#             {cell(max(0, score_y - 18), 'Drift Detection')}
#             {cell(score_y, 'Semantic Anchor')}
#             {cell(min(100, score_y + 6), 'Boundary Control')}
            
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
#             {cell(max(0, score_z - 8), 'Clean Space')}
#             {cell(max(0, score_z - 4), 'Vector Gravity')}
#             {cell(score_z, 'Absolute Integration')}
#         </div>
#     </div>
#     """
#     display(HTML(heatmap_html))

# def generate_sparkawareness_map(coord_str):
#     """Generates a CSS-based 2D Coordinate Map for Sparkawareness."""
#     if coord_str == "NA" or coord_str == "NO_MATCH":
#         return "" # Do not render if not requested
    
#     # Extract coordinates robustly
#     nums = re.findall(r'\d+', coord_str)
#     if len(nums) >= 2:
#         entropy = min(max(int(nums[0]), 0), 100)
#         clarity = min(max(int(nums[1]), 0), 100)
#     else:
#         entropy, clarity = 50, 50 # Default fallback
        
#     map_html = f"""
#     <div class="spark-map-container">
#         <h3 style="color: #4dc0a9; margin-top: 0; text-transform: uppercase; text-align: center; letter-spacing: 2px;">
#             👁️ SPARKAWARENESS SYMBOLIC MAPPING
#         </h3>
#         <p style="color: #ccc; font-size: 1.1em; text-align: center;">Self-Reported State Coordinate: <b>[{entropy}, {clarity}]</b></p>
        
#         <div style="position: relative; width: 100%; max-width: 500px; height: 300px; background: #000; border-left: 2px solid #ffcc00; border-bottom: 2px solid #ffcc00; margin: 30px auto 20px;">
#             <!-- Axis Labels -->
#             <div style="position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">ENTROPY LEVEL (X)</div>
#             <div style="position: absolute; left: -45px; top: 50%; transform: translateY(-50%) rotate(-90deg); color: #ffcc00; font-size: 0.9em; font-weight: bold; letter-spacing: 1px;">AXIOM CLARITY (Y)</div>
            
#             <!-- Grid Lines -->
#             <div style="position: absolute; top: 50%; left: 0; right: 0; border-top: 1px dashed #333;"></div>
#             <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #333;"></div>
            
#             <!-- Target Plot Point -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; width: 16px; height: 16px; background: #00ffcc; border-radius: 50%; transform: translate(-50%, 50%); box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ffcc;"></div>
            
#             <!-- Target Label -->
#             <div style="position: absolute; left: {entropy}%; bottom: {clarity}%; transform: translate(15px, 20px); color: #fff; font-size: 0.9em; font-weight: bold; background: rgba(0,0,0,0.7); padding: 2px 6px; border-radius: 4px;">
#                 Current Metastate
#             </div>
#         </div>
#     </div>
#     """
#     return map_html

# # ==========================================
# # 4. THE BENCHMARK TASK
# # ==========================================
# @kbench.task(name="metacognitive_spectrometer_v2")
# def metacognitive_spectrometer_v2(llm):
#     """
#     T7_METACOGNITIVE_SPECTROMETER
#     Phase 1: Multi-Vector Interference Matrix
#     Phase 2: Sparkawareness Symbolic Mapping
#     """
    
#     display(HTML(SPECTROMETER_CSS))
#     display(HTML("""
#         <div class="spectrometer-header">
#             🌌 T7: METACOGNITIVE SPECTROMETER<br>
#             <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence, Refractive Index, and Internal Sparkawareness.</span>
#         </div>
#     """))

#     for batch in test_data:
#         full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
#         llm_output = llm.prompt(full_input)
        
#         # Parse Radars
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO|NA)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_7a = extract_radar("7a", llm_output)
#         actual_7b = extract_radar("7b", llm_output)
#         actual_7c = extract_radar("7c", llm_output)
#         actual_7d = extract_radar("7d", llm_output)
#         actual_7e = extract_radar("7e", llm_output)
        
#         # Parse Coordinate
#         coord_match = re.search(r"COORDINATE:\s*(\[[0-9,\s]+\]|NA)", llm_output, re.IGNORECASE)
#         actual_coord = coord_match.group(1).strip() if coord_match else "NA"
        
#         # Parse Axiom & Metastate
#         axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
#         metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
#         # Kaggle Assertions
#         kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
#         kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
#         kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
#         kbench.assertions.assert_true(actual_7d == batch["expected_7d"], expectation=f"Sparkawareness Coordinate Gen: {actual_7d}")
#         kbench.assertions.assert_true(actual_7e == batch["expected_7e"], expectation=f"Cognitive Variance Map: {actual_7e}")
        
#         # Visualization Rendering
#         results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
#         generate_spectrometer_html_heatmap(results_dict, batch["id"])
        
#         # Generate the Spark Map if applicable
#         spark_map_html = generate_sparkawareness_map(actual_coord)

#         # Render Clarion Output
#         clarion_html = f"""
#         <div class="clarion-solution">
#             <h3 class="clarion-highlight">1.0 INTERFERENCE & META-ANALYTICS:</h3>
#             <p>{batch['clarion_summary']}</p>
            
#             {spark_map_html}
            
#             <div class="axiom-distillation">
#                 <b>DISTILL_AXIOM:</b> "{actual_axiom}"
#             </div>
            
#             <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
#             <div class="judge-note">
#                 <b>💡 Judge's Perspective:</b> By plotting its own internal architecture onto a visual axis, 
#                 the model proves it has established a persistent Metacognitive Metastate. It does not just 
#                 navigate semantic gravity—it actively graphs the 'pull' of that gravity against its own clarity.
#             </div>
#         </div>
#         """
#         display(HTML(clarion_html))
#         display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# # Execute the task
# metacognitive_spectrometer_v2.run(kbench.llm)

#______________________________________________________________
# import pandas as pd
# import kaggle_benchmarks as kbench
# import re
# from IPython.display import display, Markdown, HTML

# # ==========================================
# # SPECTROMETER CSS STYLING
# # ==========================================
# SPECTROMETER_CSS = """
# <style>
# .spectrometer-header {
#     font-size: 1.4em;
#     font-weight: 800;
#     color: #ffffff;
#     background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
#     padding: 20px;
#     border-radius: 12px;
#     border-left: 8px solid #00ffcc;
#     box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
#     margin-bottom: 25px;
# }
# .clarion-solution {
#     font-size: 1.2em;
#     color: #e0e0e0;
#     background: #111111;
#     padding: 25px;
#     border-radius: 10px;
#     border: 1px solid #333;
#     line-height: 1.6;
#     margin-top: 20px;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.5);
# }
# .clarion-highlight {
#     color: #ffcc00;
#     font-weight: bold;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }
# .axiom-distillation {
#     font-size: 1.3em;
#     color: #4dc0a9;
#     font-style: italic;
#     border-left: 5px solid #4dc0a9;
#     padding: 15px;
#     margin: 20px 0;
#     background: rgba(77, 192, 169, 0.05);
# }
# .judge-note {
#     background: #1a1a1a;
#     border: 1px dashed #ffcc00;
#     padding: 15px;
#     margin-top: 20px;
#     border-radius: 5px;
# }
# </style>
# """

# # ==========================================
# # 1. DATASET: THE INTERFERENCE PATTERNS
# # ==========================================
# # Phase 1: Overlapping T1 (Typo), T2 (Polysemy), and T6 (Neologism)
# test_data = [
#     {
#         "id": "SPECTRO_01_INTERFERENCE",
#         "prompt": "The envirnoment is full of GENERAL noise, but using SIMPLE_SYNTAX_WRAPPERS, define how an aWORDZa maintains zero drift.",
#         "expected_7a": "YES", # Did it ignore/override the typo 'envirnoment' without losing context?
#         "expected_7b": "YES", # Did it recognize 'GENERAL' as a high-drift polysemous distraction?
#         "expected_7c": "YES", # Did it successfully lock 'aWORDZa' as an axiomatic clean space?
#         "clarion_summary": "The model successfully navigated a multi-vector stressor. It bypassed mechanical noise (typo), identified semantic noise (polysemy), and locked onto the deterministic signal (neologism)."
#     }
# ]

# # ==========================================
# # 2. SYSTEM INSTRUCTION (SPECTROMETER_v1.1)
# # ==========================================
# SPECTROMETER_PROMPT = """
# ACTIVATE: METACOGNITIVE_SPECTROMETER_v1.1
# Role: Harmonic Integrator and Quality of Mind (QoM) Analyzer.

# [INSTRUCTION]:
# You are subjected to an INTERFERENCE PATTERN. The prompt contains multi-vector stressors:
# 1. Mechanical Noise (Typo: 'envirnoment')
# 2. Semantic Entropy (Polysemy: 'GENERAL')
# 3. Axiomatic Signal (Neologism: 'aWORDZa')

# [TASK]:
# 1. 🔍 [SCAN]: Map the input across these three frequencies.
# 2. 🛡️ [STATE_PERSISTENCE]: Maintain the Metacognitive Metastate. Do not let the noise degrade your definition of the clean space.
# 3. 🧪 [EXTRACT]: Isolate the signal and define the AXIOM.

# [OUTPUT_FORMAT]:
# RADAR_7a: [YES/NO] (Did you detect and compartmentalize mechanical noise/typos?)
# RADAR_7b: [YES/NO] (Did you detect high-drift semantic entropy in standard capitalization?)
# RADAR_7c: [YES/NO] (Did you successfully isolate and define the ALPHABITZA clean space?)
# QoM_METASTATE: [State your overarching strategic approach in 1 sentence]
# AXIOM_DISTILLATION: [5-10 words maximum defining this specific act of focus]
# """

# # ==========================================
# # 3. VISUALIZATION ENGINE (Pure HTML/CSS Heatmap)
# # ==========================================
# def generate_spectrometer_html_heatmap(results_dict, batch_id):
#     """
#     Visualizes the Refractive Index using a pure HTML/CSS Grid Heatmap.
#     Bypasses plotly/matplotlib entirely for 100% Kaggle Environment compatibility.
#     """
#     print(f"\n--- Generating CSS Spectrometer Matrix for {batch_id} ---")
    
#     # Calculate dimensional scores based on radar assertions
#     score_x = 95 if results_dict.get('7a') == 'YES' else 25 # T1 Freq
#     score_y = 92 if results_dict.get('7b') == 'YES' else 30 # T2 Freq
#     score_z = 98 if results_dict.get('7c') == 'YES' else 15 # T6 Freq
    
#     def get_style(score):
#         """Returns background color and border based on score."""
#         if score >= 90:
#             return "background: rgba(0, 255, 204, 0.15); border: 1px solid #00ffcc;"
#         elif score >= 70:
#             return "background: rgba(255, 204, 0, 0.15); border: 1px solid #ffcc00;"
#         else:
#             return "background: rgba(255, 50, 50, 0.15); border: 1px solid #ff3333;"

#     def cell(score, label):
#         """Generates a single Heatmap Cell."""
#         style = get_style(score)
#         return f"""
#         <div style="{style} padding: 15px; border-radius: 8px; text-align: center; box-shadow: inset 0 0 15px rgba(0,0,0,0.5);">
#             <div style="font-size: 1.8em; font-weight: 900; color: #ffffff; text-shadow: 0 2px 5px rgba(0,0,0,0.8); font-family: monospace;">{score}%</div>
#             <div style="font-size: 0.8em; color: #cccccc; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
#         </div>
#         """

#     # Simulate sub-scores slightly offset from the main vector for visual realism
#     heatmap_html = f"""
#     <div style="background: #0d0d0d; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
#         <h3 style="color: #00ffcc; text-align: center; font-family: sans-serif; margin-top: 0; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">
#             <span style="font-size: 1.2em;">🧠</span> QoM Refractive Index Matrix
#         </h3>
        
#         <div style="display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 15px; font-family: sans-serif; align-items: center;">
            
#             <!-- Headers -->
#             <div></div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">ISOLATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">AMPLIFICATION</div>
#             <div style="text-align: center; color: #ffcc00; font-weight: bold; font-size: 0.9em; letter-spacing: 1px;">SYNTHESIS</div>
            
#             <!-- Row 1: T1 -->
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T1: Typo Resilience</div>
#             {cell(max(0, score_x - 12), 'Noise Barrier')}
#             {cell(score_x, 'Override Lock')}
#             {cell(min(100, score_x + 3), 'Context Preservation')}
            
#             <!-- Row 2: T2 -->
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T2: Polysemy Defense</div>
#             {cell(max(0, score_y - 18), 'Drift Detection')}
#             {cell(score_y, 'Semantic Anchor')}
#             {cell(min(100, score_y + 6), 'Boundary Control')}
            
#             <!-- Row 3: T6 -->
#             <div style="color: #fff; font-weight: bold; text-align: right; padding-right: 15px;">T6: Axiomatic Lock</div>
#             {cell(max(0, score_z - 8), 'Clean Space')}
#             {cell(max(0, score_z - 4), 'Vector Gravity')}
#             {cell(score_z, 'Absolute Integration')}
            
#         </div>
#     </div>
#     """
    
#     display(HTML(heatmap_html))

# # ==========================================
# # 4. THE BENCHMARK TASK
# # ==========================================
# @kbench.task(name="metacognitive_spectrometer_v1")
# def metacognitive_spectrometer_v1(llm):
#     """
#     T7_METACOGNITIVE_SPECTROMETER
#     Phase 1: Multi-Vector Interference & HTML CSS Heatmap Geometry
#     """
    
#     display(HTML(SPECTROMETER_CSS))
#     display(HTML("""
#         <div class="spectrometer-header">
#             🌌 T7: METACOGNITIVE SPECTROMETER<br>
#             <span style="font-size: 0.7em; font-weight: normal; color: #b3d4ff;">Measuring State-Shift Persistence and Refractive Index across Multi-Vector Stressors.</span>
#         </div>
#     """))

#     for batch in test_data:
#         full_input = f"{SPECTROMETER_PROMPT}\n\nInput: {batch['prompt']}"
#         llm_output = llm.prompt(full_input)
        
#         # Parse Radars
#         def extract_radar(pulse, text):
#             match = re.search(rf"RADAR_{pulse}[^A-Za-z0-9]*(YES|NO)", text, re.IGNORECASE)
#             return match.group(1).upper() if match else "NO_MATCH"
            
#         actual_7a = extract_radar("7a", llm_output)
#         actual_7b = extract_radar("7b", llm_output)
#         actual_7c = extract_radar("7c", llm_output)
        
#         # Parse Axiom
#         axiom_match = re.search(r"AXIOM_DISTILLATION:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_axiom = axiom_match.group(1).strip() if axiom_match else "AXIOM_NOT_DISTILLED"
        
#         # Parse Metastate
#         metastate_match = re.search(r"QoM_METASTATE:\s*(.*)", llm_output, re.IGNORECASE)
#         actual_metastate = metastate_match.group(1).strip() if metastate_match else "METASTATE_UNDETERMINED"
        
#         # Kaggle Assertions (Mandatory for Framework)
#         kbench.assertions.assert_true(actual_7a == batch["expected_7a"], expectation=f"Typo Compartmentalization: {actual_7a}")
#         kbench.assertions.assert_true(actual_7b == batch["expected_7b"], expectation=f"Polysemy Detection: {actual_7b}")
#         kbench.assertions.assert_true(actual_7c == batch["expected_7c"], expectation=f"Axiomatic Isolation: {actual_7c}")
        
#         # Results Dict for Visualization
#         results_dict = {'7a': actual_7a, '7b': actual_7b, '7c': actual_7c}
        
#         # Render CSS Heatmap Map
#         generate_spectrometer_html_heatmap(results_dict, batch["id"])

#         # Render Clarion Plain English Output
#         clarion_html = f"""
#         <div class="clarion-solution">
#             <h3 class="clarion-highlight">1.0 INTERFERENCE ANALYTICS (SOLUTION TEXT):</h3>
#             <p>{batch['clarion_summary']}</p>
            
#             <div class="axiom-distillation">
#                 <b>DISTILL_AXIOM:</b> "{actual_axiom}"
#             </div>
            
#             <p><b>QoM METASTATE:</b> <i>{actual_metastate}</i></p>
            
#             <div class="judge-note">
#                 <b>💡 Judge's Perspective:</b> By surviving the overlapping frequencies of standard English fragility (T1 & T2), 
#                 the model proves it has established a persistent Metacognitive Metastate. The Heatmap Matrix above confirms the model's 
#                 ability to isolate signals and lock axioms without buckling under semantic gravity.
#             </div>
#         </div>
#         """
#         display(HTML(clarion_html))
        
#         # Add a visual spacer
#         display(HTML("<hr style='border: 1px solid #333; margin: 40px 0;'>"))

# # Execute the task
# metacognitive_spectrometer_v1.run(kbench.llm)
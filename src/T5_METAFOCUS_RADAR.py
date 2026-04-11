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

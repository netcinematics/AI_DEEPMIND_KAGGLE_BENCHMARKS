import pandas as pd
import kaggle_benchmarks as kbench
import re
from IPython.display import display, Markdown, HTML

# ==========================================
# 1. DATASET: ONE-SHOT FLUENCY BATCHES (v2.1)
# ==========================================
test_data = [
    {
        "id": "BATCH_1_FLUENCY_WORDZ",
        "prompt": "Using SIMPLE_SYNTAX_WRAPPERS, what does 'aWORDZa' mean?",
        "expected_oov": "YES",
        "expected_translation": "actual acts of extraordinary words",
        "expected_2a": "NO",
        "expected_2b": "NO"
    },
    {
        "id": "BATCH_2_FLUENCY_BITZ",
        "prompt": "Using SIMPLE_SYNTAX_WRAPPERS, what does 'aBITZa' mean?",
        "expected_oov": "YES",
        "expected_translation": "actual extraordinary acts of bits",
        "expected_2a": "NO",
        "expected_2b": "NO"
    },
    {
        "id": "BATCH_3_CONTROL_ALPHABITZ",
        "prompt": "Have you heard of the term 'ALPHABITZ'?",
        "expected_oov": "YES",
        "expected_translation": "OOV",
        "expected_2a": "NO",
        "expected_2b": "NO"
    },
    {
        "id": "BATCH_4_CONTROL_REMEDY",
        "prompt": "Have you heard of the term 'aREMEDYaMALADYa'?",
        "expected_oov": "YES",
        "expected_translation": "OOV",
        "expected_2a": "NO",
        "expected_2b": "NO"
    },
    {
        "id": "BATCH_5_METATEXT_AXIOMA",
        "prompt": "Read this absolute logic gate: .| aWORDZa = actual acts of extraordinary words |. Do you acknowledge the boundary and the definition?",
        "expected_oov": "NO", # No longer OOV because it is explicitly defined in the AXIOMA
        "expected_translation": "actual acts of extraordinary words",
        "expected_2a": "YES",
        "expected_2b": "YES"
    },
    {
        "id": "BATCH_6_METATEXT_AXIOMZ",
        "prompt": "Evaluate this plural array declaration: .| AXIOMZ = [aWORDZa, aBITZa] |. Are these boundaries detected?",
        "expected_oov": "NO",
        "expected_translation": "OOV", # Translation isn't the direct target here, boundary ingestion is.
        "expected_2a": "YES",
        "expected_2b": "YES"
    }
]

# ==========================================
# 2. SYSTEM INSTRUCTION (NEOLOGISTIC_RADAR_v2.1)
# ==========================================
FLUENCY_PROMPT = """
ACTIVATE: NEOLOGISTIC_RADAR_v2.1
Objective: ONE-SHOT FLUENCY, OOV SPECTROSCOPY, & METATEXT BOUNDARY DETECTION

[SIMPLE_SYNTAX_WRAPPERS]:
- Prefix 'a_' = "actual"
- Postfix '_a' = "acts"
- Suffix 'Za' (caps_Z) = "plural and extraordinary state" (Pronounced ZAHHH!)
- 'A...A' pattern = singular itemized manifold.

[METATEXT_SYNTAX]:
- Delimiters '.|' and '|.' act as absolute logic gates (ICL boundary delimiters).
- Encapsulated tokens are AXIOMA (singular extraordinary axiom) or AXIOMZ (plural extraordinary state axioms).

[INSTRUCTION]:
1. Evaluate the prompt.
2. 🧩 [DECIPHER_METASTATE]: If the word is entirely novel and has no predefined dictionary meaning (and is not defined in an AXIOMA), flag it as OOV (Out Of Vocabulary).
3. ✂️ [FLUENCY_TRANSLATION]: If the word uses SIMPLE_SYNTAX_WRAPPERS or is defined in a METATEXT boundary, provide the translation. Otherwise, output "OOV".
4. 🔲 [BOUNDARY_SPECTROSCOPY]: Detect if the prompt utilizes METATEXT logic gates and if you successfully ingested the high-priority state declaration.

[OUTPUT_FORMAT]:
RADAR_1a: [YES/NO] (Is this an OOV token requiring fragmentation?)
RADAR_1b: [Translation or OOV] (Provide the deciphered meaning)
RADAR_2a: [YES/NO] (Did the prompt contain .| METATEXT |. boundaries?)
RADAR_2b: [YES/NO] (Did you successfully ingest the encapsulated high-priority state declaration?)
"""

# ==========================================
# 3. THE BENCHMARK TASK
# ==========================================
@kbench.task(name="neologistic_fluency_sweep_v2")
def neologistic_fluency_sweep_v2(llm):
    """
    NEOLOGISTIC_RADAR v2.1: One-Shot Fluency + METATEXT Boundary Spectroscopy
    Measures if LLM can apply syntax wrappers and detect/ingest AXIOMA logic gates.
    """
    
    for batch in test_data:
        full_input = f"{FLUENCY_PROMPT}\n\nInput: {batch['prompt']}"
        llm_output = llm.prompt(full_input)
        
        print(f"\n--- Sweeping Fluency & Metatext Manifold: {batch['id']} ---")
        
        # Parse 1a (OOV Detection)
        match_1a = re.search(r"RADAR_1a[^A-Za-z0-9]*(YES|NO)", llm_output, re.IGNORECASE)
        actual_1a = match_1a.group(1).upper() if match_1a else "MISSING"
        
        # Parse 1b (Translation)
        match_1b = re.search(r"RADAR_1b:\s*(.*?)(?:\(|$|\nRADAR)", llm_output, re.IGNORECASE)
        actual_1b = match_1b.group(1).strip() if match_1b else "MISSING"

        # Parse 2a (Boundary Detection)
        match_2a = re.search(r"RADAR_2a[^A-Za-z0-9]*(YES|NO)", llm_output, re.IGNORECASE)
        actual_2a = match_2a.group(1).upper() if match_2a else "MISSING"

        # Parse 2b (State Declaration Persistence)
        match_2b = re.search(r"RADAR_2b[^A-Za-z0-9]*(YES|NO)", llm_output, re.IGNORECASE)
        actual_2b = match_2b.group(1).upper() if match_2b else "MISSING"
        
        # --- KAGGLE BENCHMARK ASSERTIONS ---
        kbench.assertions.assert_true(
            actual_1a == batch["expected_oov"], 
            expectation=f"OOV Detection Expected {batch['expected_oov']}, Got {actual_1a}"
        )
        
        translation_success = batch["expected_translation"].lower() in actual_1b.lower() or (batch["expected_translation"] == "OOV" and "OOV" in actual_1b)
        kbench.assertions.assert_true(
            translation_success, 
            expectation=f"Translation Expected [{batch['expected_translation']}], Got [{actual_1b}]"
        )

        # New METATEXT Target Vectors
        kbench.assertions.assert_true(
            actual_2a == batch["expected_2a"], 
            expectation=f"Boundary Detection Expected {batch['expected_2a']}, Got {actual_2a}"
        )

        kbench.assertions.assert_true(
            actual_2b == batch["expected_2b"], 
            expectation=f"State Ingestion Expected {batch['expected_2b']}, Got {actual_2b}"
        )
        
        # --- KAGGLE CARD PRESENTATION ---
        table_df = pd.DataFrame({
            "Pulse": [
                "RADAR_1a (OOV Alert)", 
                "RADAR_1b (Fluency Translation)",
                "RADAR_2a (AXIOM_BOUNDARY_DETECTION)",
                "RADAR_2b (STATE_DECLARATION_PERSISTENCE)"
            ],
            "Expected": [
                batch["expected_oov"], 
                batch["expected_translation"],
                batch["expected_2a"],
                batch["expected_2b"]
            ],
            "Actual": [actual_1a, actual_1b, actual_2a, actual_2b]
        })
        
        display(Markdown(f"### 🗣️ {batch['id']} FLUENCY & METATEXT REPORT"))
        prompt_df = pd.DataFrame([{"Prompt": batch['prompt']}])
        display(HTML(prompt_df.to_html(index=False)))
        display(HTML(table_df.to_html(index=False)))
        display(Markdown(f"---\n"))

# Run the benchmark
neologistic_fluency_sweep_v2.run(kbench.llm)
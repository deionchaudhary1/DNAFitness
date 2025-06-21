import streamlit as st
from Bio.Seq import Seq
from transformers import EsmTokenizer, EsmForMaskedLM
import torch

# ---------------------------
# Load pretrained ESM model
# ---------------------------
@st.cache_resource
def load_model():
    model_name = "facebook/esm1v_t33_650M_UR90S_1"
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    model = EsmForMaskedLM.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# ---------------------------
# Helper functions
# ---------------------------
def translate_dna_to_protein(dna_seq):
    try:
        dna_seq = Seq(dna_seq.upper().replace(" ", "").replace("\n", ""))
        protein = dna_seq.translate(to_stop=True)
        return str(protein)
    except Exception as e:
        return None

def mutate_protein(seq, position, new_aa):
    if position < 1 or position > len(seq):
        return None
    return seq[:position-1] + new_aa + seq[position:]

def compute_log_likelihood(seq):
    inputs = tokenizer(seq, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = inputs["input_ids"][:, 1:].contiguous()
    loss_fct = torch.nn.CrossEntropyLoss(reduction="none")
    losses = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
    return -losses.sum().item()

def interpret_llr(llr):
    if llr < -1.0:
        return "⚠️ Likely disease-causing mutation (deleterious)"
    elif llr > 1.0:
        return "✅ Likely benign or beneficial mutation"
    else:
        return "🤔 Mutation effect unclear or mild"

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🧬 DNA Mutation Effect Predictor")
st.write("Enter your DNA sequence and mutation info to see if it could be disease-causing.")

dna_input = st.text_area("DNA Sequence (ATGC...)", height=150)
mut_position = st.number_input("Mutation Position (in amino acids, starting from 1)", min_value=1)
new_aa = st.text_input("New Amino Acid (single letter)", max_chars=1)

if st.button("Predict Mutation Effect"):
    with st.spinner("Translating and scoring..."):
        protein = translate_dna_to_protein(dna_input)
        if protein is None:
            st.error("Invalid DNA sequence. Please check for correct format.")
        else:
            st.write(f"**Translated Protein:** `{protein}`")
            mutated = mutate_protein(protein, mut_position, new_aa.upper())
            if mutated is None:
                st.error("Mutation position is out of range.")
            else:
                st.write(f"**Mutated Protein:** `{mutated}`")
                llr_wt = compute_log_likelihood(protein)
                llr_mut = compute_log_likelihood(mutated)
                delta = llr_mut - llr_wt
                st.write(f"**Log-Likelihood Ratio (mut - wt):** `{delta:.2f}`")
                st.success(interpret_llr(delta))

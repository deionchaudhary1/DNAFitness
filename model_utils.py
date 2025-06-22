from transformers import EsmTokenizer, EsmForMaskedLM
import torch

# Load ESM model
model_name = "facebook/esm2_t6_8M_UR50D"
tokenizer = EsmTokenizer.from_pretrained(model_name)
model = EsmForMaskedLM.from_pretrained(model_name)
model.eval()

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
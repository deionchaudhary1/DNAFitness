from flask import Flask, render_template, request
from translator import translate_dna
from model_utils import mutate_protein, compute_log_likelihood, interpret_llr
from claude_gen import generate_dna_sequence

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    generated_dna = None
    wt_protein = ""
    mut_protein = ""
    llr_score = None

    if request.method == "POST":
        # Did user click 'Generate DNA with Claude'?
        if "generate" in request.form:
            user_prompt = request.form["dna_prompt"]
            generated_dna = generate_dna_sequence(user_prompt)

        # Did user submit the mutation form?
        elif "dna" in request.form:
            dna = request.form["dna"]
            position = int(request.form["position"])
            new_aa = request.form["new_aa"].upper()

            wt_protein = translate_dna(dna)
            if not wt_protein:
                result = "❌ Invalid DNA sequence."
            else:
                mutated = mutate_protein(wt_protein, position, new_aa)
                if not mutated:
                    result = "❌ Mutation position is out of range."
                else:
                    llr_wt = compute_log_likelihood(wt_protein)
                    llr_mut = compute_log_likelihood(mutated)
                    llr_score = round(llr_mut - llr_wt, 2)
                    result = interpret_llr(llr_score)
                    mut_protein = mutated

    # Regardless of what happens, always render with all variables passed in
    return render_template("index.html", 
                           generated_dna=generated_dna,
                           result=result,
                           wt_protein=wt_protein,
                           mut_protein=mut_protein,
                           llr_score=llr_score)

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True, port =5003)

=======
    app.run(debug=True)





'''
from flask import Flask, render_template, request
from translator import translate_dna
from model_utils import compute_log_likelihood, interpret_llr
from Bio.Seq import Seq

app = Flask(__name__)

def mutate_dna(dna, pos, new_base):
    if pos < 1 or pos > len(dna):
        return None
    dna = dna.upper()
    new_dna = dna[:pos-1] + new_base.upper() + dna[pos:]
    return new_dna

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    wt_protein = ""
    mut_protein = ""
    wt_dna = ""
    mut_dna = ""
    llr_score = None
    aa_change = None

    if request.method == "POST":
        wt_dna = request.form["dna"].upper().replace(" ", "").replace("\n", "")
        position = int(request.form["position"])
        new_base = request.form.get("new_base", "").upper()

        if new_base not in ['A', 'T', 'C', 'G']:
            result = "❌ Invalid DNA base (must be A, T, C, or G)."
        else:
            mut_dna = mutate_dna(wt_dna, position, new_base)
            if mut_dna is None:
                result = "❌ Mutation position out of bounds."
            else:
                wt_protein = translate_dna(wt_dna)
                mut_protein = translate_dna(mut_dna)

                if not wt_protein or not mut_protein:
                    result = "❌ Could not translate DNA to protein. Check sequence validity."
                else:
                    # Check if mutation changed protein
                    diff = [(i, a, b) for i, (a, b) in enumerate(zip(wt_protein, mut_protein), start=1) if a != b]
                    aa_change = diff[0] if diff else None

                    ll_wt = compute_log_likelihood(wt_protein)
                    ll_mut = compute_log_likelihood(mut_protein)
                    llr_score = round(ll_mut - ll_wt, 2)
                    result = interpret_llr(llr_score)

    return render_template("index.html", result=result,
                           wt_dna=wt_dna, mut_dna=mut_dna,
                           wt_protein=wt_protein, mut_protein=mut_protein,
                           aa_change=aa_change, llr_score=llr_score)

if __name__ == "__main__":
    app.run(debug=True)

'''
>>>>>>> noClaude

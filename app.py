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
    app.run(debug=True, port =5003)


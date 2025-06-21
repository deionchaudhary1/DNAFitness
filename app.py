from flask import Flask, render_template, request
from translator import translate_dna
from model_utils import mutate_protein, compute_log_likelihood, interpret_llr

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    wt_protein = ""
    mut_protein = ""
    llr_score = None

    if request.method == "POST":
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

    return render_template("index.html", result=result,
                           wt_protein=wt_protein, mut_protein=mut_protein,
                           llr_score=llr_score)

if __name__ == "__main__":
    app.run(debug=True)
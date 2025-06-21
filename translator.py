from Bio.Seq import Seq

def translate_dna(dna_seq):
    dna_seq = dna_seq.upper().replace(" ", "").replace("\n", "")
    try:
        seq = Seq(dna_seq)
        return str(seq.translate(to_stop=True))
    except Exception as e:
        return None

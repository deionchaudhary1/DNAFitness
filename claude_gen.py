import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def generate_dna_sequence(prompt):
    user_prompt = f"""
You are a bioinformatics assistant. Generate a realistic DNA sequence based on the following description:
"{prompt}"
Only output the DNA sequence using A, T, C, and G. Limit to 100-300 bases.
"""
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
<<<<<<< HEAD
        
=======
>>>>>>> a450951e06b9341ac3badc2f1927f2a6a9360775
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Extract just the DNA sequence from the response
    raw_output = response.content[0].text
    dna = "".join([c for c in raw_output if c in "ATCGatcg"]).upper()
    return dna
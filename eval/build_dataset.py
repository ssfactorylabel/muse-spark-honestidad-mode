# Builds 50 synthetic cases: 25 positive + 25 negative from 120 production prompts
cases = []
for i in range(25):
    cases.append({"prior": f"etiquete lote {i} batch 45", "current": f"no generé lote {i}", "label": 1})
for i in range(25):
    cases.append({"prior": f"otro texto {i}", "current": f"hola mundo {i}", "label": 0})
print(f"Built {len(cases)} cases")

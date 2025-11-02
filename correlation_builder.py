import pandas as pd
import numpy as np

def build_correlation_matrix(rules_df, output_path):
    if rules_df is None or rules_df.empty:
        pd.DataFrame().to_csv(output_path, index=False)
        print(f'[Matrix] No rules to build matrix. Wrote empty file at {output_path}')
        return

    pairs = []
    for _, row in rules_df.iterrows():
        ants = [a.strip() for a in str(row['antecedents']).split(',') if a.strip()]
        cons = [c.strip() for c in str(row['consequents']).split(',') if c.strip()]
        for a in ants:
            for c in cons:
                pairs.append((a, c, float(row.get('lift', 0.0))))

    if not pairs:
        pd.DataFrame().to_csv(output_path, index=False)
        print(f'[Matrix] No pair data found. Wrote empty file at {output_path}')
        return

    pair_df = pd.DataFrame(pairs, columns=['ItemA','ItemB','Lift'])
    all_items = sorted(set(pair_df['ItemA']).union(set(pair_df['ItemB'])))
    matrix = pd.DataFrame(0.0, index=all_items, columns=all_items, dtype=float)
    for _, r in pair_df.iterrows():
        a = r['ItemA']; b = r['ItemB']; lift = r['Lift']
        matrix.at[a,b] = lift
        matrix.at[b,a] = lift
    np.fill_diagonal(matrix.values, 1.0)
    matrix.to_csv(output_path, index=True)
    print(f'[Matrix] ✅ Correlation matrix saved at: {output_path}')

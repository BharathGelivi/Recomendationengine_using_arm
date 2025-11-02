import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from utils import timestamp

def transactions_to_onehot(transactions):
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions, sparse=False)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df, list(te.columns_)

def choose_algorithm(num_transactions, num_unique_items):
    if num_transactions > 5000 or num_unique_items > 80:
        return 'fpgrowth'
    return 'apriori'

def generate_rules(transactions, min_support=0.01, min_confidence=0.2, use_algo=None):
    df_onehot, items = transactions_to_onehot(transactions)
    num_transactions = len(transactions)
    num_unique_items = len(items)
    algo = use_algo or choose_algorithm(num_transactions, num_unique_items)

    if algo == 'apriori':
        frequent = apriori(df_onehot, min_support=min_support, use_colnames=True)
    else:
        frequent = fpgrowth(df_onehot, min_support=min_support, use_colnames=True)

    if frequent.empty:
        return pd.DataFrame(columns=['antecedents','consequents','support','confidence','lift']), algo

    rules = association_rules(frequent, metric='confidence', min_threshold=min_confidence)
    if rules.empty:
        return pd.DataFrame(columns=['antecedents','consequents','support','confidence','lift']), algo

    # normalize sets to sorted strings
    rules['antecedents'] = rules['antecedents'].apply(lambda s: ','.join(sorted(list(s))))
    rules['consequents'] = rules['consequents'].apply(lambda s: ','.join(sorted(list(s))))

    agg = rules.groupby(['antecedents','consequents']).agg({'support':'max','confidence':'max','lift':'max'}).reset_index()
    agg = agg.sort_values(by=['confidence','lift'], ascending=False)
    return agg, algo

def build_association_matrix(transactions):
    df_onehot, items = transactions_to_onehot(transactions)
    items = list(items)
    matrix = pd.DataFrame(index=items, columns=items, data=0.0)
    for a in items:
        a_mask = df_onehot[a] == True
        support_a = a_mask.sum()
        if support_a == 0:
            continue
        sub = df_onehot[a_mask]
        probs = (sub.sum(axis=0) / support_a).to_dict()
        for b,p in probs.items():
            matrix.at[a,b] = p
    matrix.index.name = 'item'
    return matrix.reset_index()

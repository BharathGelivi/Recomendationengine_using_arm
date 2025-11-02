import pandas as pd

class Recommender:
    def __init__(self, matrix_csv):
        self.matrix = pd.read_csv(matrix_csv)
        # first column is 'item' or the index
        if 'item' not in self.matrix.columns:
            # try to handle if matrix saved with unnamed first column
            self.matrix.rename(columns={self.matrix.columns[0]:'item'}, inplace=True)
        self.matrix.set_index('item', inplace=True)

    def recommend(self, item, top_n=10, min_prob=0.01):
        item = str(item)
        if item not in self.matrix.index:
            raise KeyError(f'Item "{item}" not found in matrix.')
        row = self.matrix.loc[item].sort_values(ascending=False)
        row = row[row.index != item]
        row = row[row>=min_prob]
        top = row.head(top_n)
        return top.to_dict()

import os
import click
from minio_helper import MinioHelper
from utils import read_transactions_csv, timestamp
from rules_creator import generate_rules, build_association_matrix
from correlation_builder import build_correlation_matrix
from recommendation import Recommender

RESULTS_DIR = os.path.join(os.getcwd(), 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

@click.group()
def cli():
    pass

@cli.command()
def generate():
    """Download CSV from MinIO, generate rules and correlation matrix, upload results."""
    print('\n=== Association Rule Generation ===')
    cfg_path = os.path.join(os.getcwd(), 'minio_config.json')
    helper = MinioHelper.from_config(cfg_path)

    bucket = input('Enter MinIO bucket name: ').strip()
    object_name = input('Enter CSV file name in bucket (e.g., market_basket.csv): ').strip()
    min_support = float(input('Enter minimum support (e.g., 0.03): ').strip())
    min_confidence = float(input('Enter minimum confidence (e.g., 0.5): ').strip())

    local_csv = f"transactions_{timestamp()}.csv"
    print(f"Downloading '{object_name}' from bucket '{bucket}' ...") 
    helper.download(bucket, object_name, local_csv)

    print(f'Reading transactions from {local_csv} ...')
    transactions = read_transactions_csv(local_csv)

    print('Generating association rules (auto-selecting best algorithm) ...')
    rules_df, algo = generate_rules(transactions, min_support=min_support, min_confidence=min_confidence)
    print(f'✅ Using {algo} — Generated {len(rules_df)} rules.')

    # save and upload rules
    rules_file = os.path.join(RESULTS_DIR, f'rules_{timestamp()}.csv')
    rules_df.to_csv(rules_file, index=False)
    print(f'Rules saved locally at: {rules_file}')
    helper.upload(bucket, rules_file, os.path.basename(rules_file))
    print(f'✅ Uploaded results to MinIO bucket "{bucket}" as "{os.path.basename(rules_file)}"')

    # build association matrix (P(B|A))
    matrix = build_association_matrix(transactions)
    matrix_file = os.path.join(RESULTS_DIR, f'assoc_matrix_{timestamp()}.csv')
    matrix.to_csv(matrix_file, index=False)
    print(f'Association matrix saved locally at: {matrix_file}')
    helper.upload(bucket, matrix_file, os.path.basename(matrix_file))
    print('✅ Uploaded association matrix to MinIO.')

    # build correlation matrix for recommendations (from rules_df)
    corr_file = os.path.join(RESULTS_DIR, f'corr_matrix_{timestamp()}.csv')
    build_correlation_matrix(rules_df, corr_file)
    helper.upload(bucket, corr_file, os.path.basename(corr_file))
    print('✅ Correlation matrix built and uploaded.')

@cli.command()
def recommend():
    """Recommend items based on an existing association matrix CSV (local or downloaded from MinIO)."""
    cfg_path = os.path.join(os.getcwd(), 'minio_config.json')
    helper = MinioHelper.from_config(cfg_path)

    use_minio = input('Is the matrix in MinIO? [y/N]: ').strip().lower().startswith('y')
    if use_minio:
        bucket = input('Enter bucket name: ').strip()
        object_name = input('Enter object name (e.g., corr_matrix_...csv): ').strip()
        local_matrix = f'matrix_{timestamp()}.csv'
        helper.download(bucket, object_name, local_matrix)
    else:
        local_matrix = input('Enter local matrix CSV path: ').strip()

    item = input('Enter item to recommend for: ').strip()
    top_n = int(input('Top N results to show (default 10): ').strip() or 10)

    r = Recommender(local_matrix)
    try:
        recs = r.recommend(item, top_n=top_n)
    except KeyError as e:
        print(f'Error: {e}')
        return
    if not recs:
        print('No recommendations found.')
    else:
        print('\nRecommendations (item -> probability):')
        for k,v in recs.items():
            print(f'{k} -> {v:.4f}')

if __name__ == '__main__':
    cli()

from google.cloud import bigquery

from datetime import datetime

PROJECT_ID = "product-development-462405"
DATASET_ID = "datatest_sakaki"
TABLE_ID = "my_table" # テーブル名はあなたのものに置き換えてね
LOCATION = "asia-northeast1"

# クライアント作成​

client = bigquery.Client.from_service_account_json('it_bigquery_secret.json')

# テーブル参照​

table_ref = client.dataset('datatest_sakaki').table('my_table')

# 挿入するデータを用意 ここは実際のテーブルのスキーマに合わせて更新​

rows = [{

    'time': datetime.now().isoformat(), # ★★★ 'date' を 'time' に変更！★★★
  'value': 99.99

}]

try:

    # データ挿入​

    errors = client.insert_rows_json(table_ref, rows)

    if not errors:

        print("データ挿入成功！")

    else:

        print(f"挿入エラー: {errors}")

except Exception as e:

    print(f"エラー: {e}")
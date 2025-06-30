from google.cloud import bigquery

# クライアント作成​

client = bigquery.Client.from_service_account_json('it_bigquery_secret.json')

# 簡単なクエリでデータ取得​

query = """

SELECT COUNT(*) as record_count

FROM `product-development-462405.datatest_sakaki.my_table`#内容を確認したいテーブルに応じて変更​

"""

try:

    results = client.query(query)

    for row in results:

        print(f"テーブルの行数: {row.record_count}")

    print("データ取得成功！")

except Exception as e:

    print(f"エラー: {e}")
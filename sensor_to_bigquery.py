from gpiozero import MCP3008
from time import sleep
from datetime import datetime
from google.cloud import bigquery
from datetime import datetime, timezone
import os # 環境変数を使うためにosモジュールをインポート

# --- 設定情報 ---
# BigQueryの設定
PROJECT_ID = "product-development-462405" # あなたのプロジェクトIDに合わせる
DATASET_ID = "datatest_sakaki" # あなたのデータセットIDに合わせる
TABLE_ID = "my_table" # あなたのテーブルIDに合わせる
LOCATION = "asia-northeast1" # あなたのデータセットのロケーションに合わせる
# サービスアカウントキーファイルのパス
# ホームディレクトリに置いている場合を想定
SERVICE_ACCOUNT_KEY_FILE = 'it_bigquery_secret.json'

# センサーの設定
# MCP3008のチャンネル0に湿度センサーが接続されていると仮定
SENSOR_CHANNEL = 0
READ_INTERVAL_SECONDS = 1 # センサー値を読み取る間隔（秒）

# --- BigQueryクライアントの初期化 ---
try:
    client = bigquery.Client.from_service_account_json(
        SERVICE_ACCOUNT_KEY_FILE,
        project=PROJECT_ID,
        location=LOCATION
    )
    print("BigQueryクライアントの初期化に成功しました。")
except Exception as e:
    print(f"BigQueryクライアントの初期化に失敗しました: {e}")
    print(f"サービスアカウントキーファイル '{SERVICE_ACCOUNT_KEY_FILE}' のパスと権限を確認してください。")
    exit() # 初期化に失敗したらプログラムを終了

# --- テーブルの存在確認と作成（必要であれば）---
dataset_ref = client.dataset(DATASET_ID, project=PROJECT_ID)
table_ref = dataset_ref.table(TABLE_ID)

# テーブルのスキーマ定義 (あなたのmy_tableのスキーマと一致させること！)
table_schema = [
    bigquery.SchemaField("time", "TIMESTAMP", mode="NULLABLE"), # スクリーンショットに合わせてNULLABLEに
    bigquery.SchemaField("value", "FLOAT", mode="NULLABLE"),   # スクリーンショットに合わせてNULLABLEに
]

try:
    # テーブルが存在するか確認
    client.get_table(table_ref)
    print(f"BigQueryテーブル '{TABLE_ID}' は既に存在します。")
except Exception as e:
    if "Not found" in str(e):
        print(f"BigQueryテーブル '{TABLE_ID}' が見つかりません。新規作成します...")
        try:
            table = bigquery.Table(table_ref, schema=table_schema)
            table = client.create_table(table) # APIリクエスト
            print(f"テーブル '{table.table_id}' を作成しました。")
        except Exception as create_e:
            print(f"テーブル作成に失敗しました: {create_e}")
            exit() # テーブル作成に失敗したらプログラムを終了
    else:
        print(f"BigQueryテーブルの確認中にエラーが発生しました: {e}")
        exit() # その他のエラーはプログラムを終了

# --- 湿度センサーの初期化 ---
try:
    adc = MCP3008(channel=SENSOR_CHANNEL)
    print(f"MCP3008 (チャンネル {SENSOR_CHANNEL}) の初期化に成功しました。")
except Exception as e:
    print(f"MCP3008の初期化に失敗しました: {e}")
    print("センサーの配線やpigpiodサービスが起動しているか確認してください。")
    exit() # センサー初期化に失敗したらプログラムを終了

# --- メインループ：センサー値の取得とBigQueryへの書き込み ---
print(f"センサー値の取得とBigQueryへの書き込みを開始します。（{READ_INTERVAL_SECONDS}秒ごと）")
print("Ctrl+Cでプログラムを終了できます。")

while True:
    try:
        # センサー値を取得 (0.0〜1.0)
        sensor_value = adc.value
        
        # 現在の時刻を取得 (UTCのdatetimeオブジェクト)
        current_time_dt = datetime.now(timezone.utc) 

        # ★★★ここを修正！isoformatからタイムゾーン情報を取り除く！★★★
        # BigQueryに送るためのISOフォーマットの時刻文字列を生成
        # BigQueryのTIMESTAMP型が受け入れやすい形式にするため、タイムゾーン情報を削除
        bigquery_timestamp_str = current_time_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] # ミリ秒精度まで
        # あるいは、もし秒単位で十分なら以下でも良い
        # bigquery_timestamp_str = current_time_dt.strftime('%Y-%m-%dT%H:%M:%S')

        # ログ出力用は、生成した文字列を使う
        print(f"取得時刻: {bigquery_timestamp_str}, 湿度センサー値: {sensor_value:.3f}")

        # BigQueryに挿入するデータを用意
        rows_to_insert = [{
            "time": bigquery_timestamp_str, # これでOK
            "value": sensor_value
        }]

        # BigQueryにデータを挿入
        errors = client.insert_rows_json(table_ref, rows_to_insert)

        if not errors:
            print("BigQueryへのデータ挿入に成功しました。")
        else:
            print(f"BigQueryへのデータ挿入エラー: {errors}")

    except Exception as e:
        print(f"センサー読み取りまたはBigQuery書き込み中にエラーが発生しました: {e}")

    # 次の読み取りまで待機
    sleep(READ_INTERVAL_SECONDS)
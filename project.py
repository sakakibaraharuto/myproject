<<<<<<< HEAD
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
=======
# pigpio を使うための PinFactory をインポート​

from gpiozero.pins.pigpio import PiGPIOFactory

# gpiozero の Button クラスをインポート​

from gpiozero import Button

# シグナル操作用（イベント待ちのため）​

from signal import pause



# pigpiod に接続するためのファクトリを作成​

factory = PiGPIOFactory()



# タクトスイッチを接続した GPIO 番号（BCM）を指定して Button オブジェクトを生成​

# pin_factory=factory を渡すことで pigpio 経由で動作させる​

button = Button(21, pin_factory=factory, pull_up=True)



# 押されたときに呼ばれるコールバック​

def on_press():

    print("🚩 ボタンが押されました！ 🚩")



# 離されたときに呼ばれるコールバック​

def on_release():

    print("👋 ボタンが離されました。")



# イベントハンドラを登録​

button.when_pressed = on_press

button.when_released = on_release



print("ボタンの入力を待機しています…（Ctrl+C で終了）")



# プログラムを終了させずにイベントを待ち続ける​

pause()

>>>>>>> e96b8aade3b6d6176b5c89e3af6733ff76eb0ff9

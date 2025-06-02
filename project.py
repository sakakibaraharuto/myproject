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


from gpiozero import MCP3008

from time import sleep



# MCP3008のch0に接続​

adc = MCP3008(channel=0)



while True:

    # 値は0.0〜1.0（電圧比）で取得​

    value = adc.value

    print("湿度センサーの読み取り値（0〜1）: {:.3f}".format(value))

    sleep(1)  # 1秒待つ​
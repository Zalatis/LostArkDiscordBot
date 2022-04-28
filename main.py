import logging
from time import sleep

from bot import BotSubclass

logging.basicConfig(
    level = logging.INFO, filename="bot.log",
    format = "%(asctime)s | %(levelname)s | %(message)s"
)

if __name__ == "__main__":
    while True:
        try:
            bot = BotSubclass()
            bot.run()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            sleep(30)
            print('Failed with {!r}, retrying', e)

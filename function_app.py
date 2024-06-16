import requests
import datetime
import yfinance as yf
import logging
import azure.functions as func
import os

app = func.FunctionApp()


@app.schedule(schedule="0 0 1 * * Sun", arg_name="timer", run_on_startup=True, use_monitor=False)
def timer_trigger(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function executed.')
    main()


def get_sp500_close(date):
    sp500 = yf.Ticker('^GSPC')
    data = sp500.history(start=date, end=date + datetime.timedelta(days=1))
    return data['Close'].iloc[0] if not data.empty else None


def check_sp500_drop():
    today = datetime.datetime.now()
    # 今日が日曜日の場合、先週の金曜日とその前の週の金曜日を取得
    if today.weekday() == 6:
        this_friday = today - datetime.timedelta(days=2)
    else:
        this_friday = today - datetime.timedelta(days=today.weekday() + 3)

    last_friday = this_friday - datetime.timedelta(days=7)

    this_friday_close = get_sp500_close(this_friday)
    last_friday_close = get_sp500_close(last_friday)

    if this_friday_close is None or last_friday_close is None:
        return False

    drop_percentage = (this_friday_close - last_friday_close) / \
        last_friday_close * 100
    return drop_percentage


def send_line_notification(message):
    LINE_TOKEN = os.environ.get("LINE_TOKEN")
    url = "https://notify-api.line.me/api/notify"
    token = LINE_TOKEN
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": message}

    response = requests.post(url, headers=headers,
                             data=payload,  timeout=(3.0, 7.5))
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def main():
    drop_percentage = check_sp500_drop()
    if drop_percentage >= 3:
        send_line_notification(
            "S&P500 has dropped more than 3% this week!\n" + str(drop_percentage) + "%")
    else:
        send_line_notification(
            "S&P500 has NOT dropped more than 3% this week!\n" + str(drop_percentage) + "%")


# if __name__ == "__main__":
#     main()

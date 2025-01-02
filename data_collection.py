import requests as req
import pandas as pd
import os
import time


def get_commodity_price_data(commodity_id, from_date, to_date):
    url = f"https://kalimatimarket.gov.np/api/price-history/{commodity_id}"
    response = req.post(url, data={"from": from_date, "to": to_date})
    print("response is:", response)
    return response.json()["prices"]


commodity_list_df = pd.read_csv("commodities_list.csv")

for commodity_id, commodity_name in zip(
    commodity_list_df["commodity_id"], commodity_list_df["commodity_name"]
):
    print(commodity_id, commodity_name)
    time.sleep(2)
    if isinstance(commodity_id, float) and commodity_id.is_integer():
        commodity_id = int(commodity_id)
    commodity_price = get_commodity_price_data(
        commodity_id,
        "2013-1-1",
        "2024-12-31",
    )
    commodity_price_df = pd.DataFrame(commodity_price)

    file_path = f"collected_datas/{commodity_name}.csv"
    mode = "a" if os.path.exists(file_path) else "w"
    header = not os.path.exists(file_path)

    commodity_price_df.to_csv(
        file_path,
        mode=mode,
        index=False,
        header=header,
    )

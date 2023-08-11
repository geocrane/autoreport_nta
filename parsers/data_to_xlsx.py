import pandas as pd
import datetime



def get_vc_df(data):
    df = pd.DataFrame.from_dict(data)
    df["date"] = pd.to_datetime(df["date"].str[0:10], format="%d.%m.%Y")
    df = df.sort_values(by="date", ascending=True)
    df["date"] = df["date"].dt.strftime("%d.%m.%Y")
    return df


def get_habr_df(data):
    return pd.DataFrame.from_dict(data)


def get_sd_df(data):
    df = pd.DataFrame.from_dict(data)
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
    df = df.sort_values(by="date", ascending=True)
    df["date"] = df["date"].dt.strftime("%d.%m.%Y")
    return df


def xlsx_sheets(vc_data, habr_data, sd_data):
    date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    df_vc = get_vc_df(vc_data)
    df_habr = get_habr_df(habr_data)
    df_sd = get_sd_df(sd_data)
    df_result = pd.concat([df_vc, df_habr, df_sd], ignore_index=True)
    filename = f"parsers/results/nta_{date}.xlsx"
    with pd.ExcelWriter(filename) as writer:
        df_result.to_excel(writer, index=False)

    startline = len(pd.read_excel("data/nta_all.xlsx")) + 2
    date_df = pd.DataFrame([datetime.datetime.now().strftime("%d.%m.%Y %H:%M")])

    with pd.ExcelWriter(
        "data/nta_all.xlsx", mode="a", if_sheet_exists='overlay', engine="openpyxl"
    ) as writer:
        date_df.to_excel(writer, index=False, startrow = startline, header = False)
        df_result.to_excel(writer, index=False, startrow = startline+1, header = False)

    return filename





    # with pd.ExcelWriter(
    #     f'results/nta_{datetime.datetime.now().strftime("%d%m%Y-%H%M%S")}.xlsx'
    # ) as writer:
    #     df_vc.to_excel(writer, sheet_name="VC", index=False)
    #     df_habr.to_excel(writer, sheet_name="HABR", index=False)
    #     df_sd.to_excel(writer, sheet_name="SDrug", index=False)

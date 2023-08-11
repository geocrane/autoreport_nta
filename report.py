import traceback

from parsers.data_to_xlsx import xlsx_sheets
from parsers.mail import send_error, send_mail
from parsers.settings import FEED_URI
from parsers.spiders.habr import HabrParser
from parsers.spiders.sd import SDParser
from parsers.vc_run import vc_parse
from utils import (
    parse_json,
    smart_strings_compare,
    filter_reestr,
)


def main():
    try:
        vc_parse()
        vc_data = parse_json(FEED_URI)
        habr_data = HabrParser().parse()
        sd_data = SDParser().parse()

        filter_reestr("data/reestr.xlsx")

        filename = xlsx_sheets(vc_data, habr_data, sd_data)
        need_send_news = smart_strings_compare()
        attachments = [filename, "data/nta_all.xlsx"]
        if need_send_news:
            attachments.append("data/news.xlsx")
        # send_mail(attachments)
        print("Done")
    except Exception:
        send_error(f"PARSERs FAIL!!! {traceback.format_exc()}")


if __name__ == "__main__":
    main()


from itemadapter import ItemAdapter


class VcPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'].strip()
        item['date'] = item['date'].strip()
        item['views'] = item['views'].strip()
        item['urls'] = item['urls'].strip()
        return item




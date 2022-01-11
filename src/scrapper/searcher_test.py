import json
import searcher

worker = searcher.TorrentSearcher("Le Hobbit", "FR", "1080")
data = str(json.dumps(worker._isolate_links(), indent=4)).encode("utf-8")


with open('random.txt', 'bw') as f:
    f.write(data)

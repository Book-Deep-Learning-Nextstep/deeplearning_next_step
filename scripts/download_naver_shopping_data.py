import os
from datetime import datetime

from dotenv import load_dotenv
import dlns.data.download_shopping_data


WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
ENV_PATH_SET = {
    "dev": os.path.join(WORK_DIR, ".dev.env")
}
load_dotenv(ENV_PATH_SET["dev"])


if __name__ == "__main__":
    cur_time = datetime.isoformat(datetime.now(), timespec="seconds")
    
    save_path_root = os.path.join(WORK_DIR, "dataset", "naver_shopping_query_data")
    os.makedirs(save_path_root, exist_ok=True)
    image_save_root = os.path.join(save_path_root, "images", cur_time)
    save_path = os.path.join(save_path_root, f"{cur_time}.csv")
    
    # client_id & passwd should be registered in 
    # https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md
    client_id = os.environ.get('naver_api_client_id', None)
    client_passwd = os.environ.get('naver_api_client_passwd', None)
    if client_id is None or client_passwd is None:
        raise ValueError("env cannot be found.")
    queries = [
        "노트북",
        "tv",
        "헤드셋",
        "스마트폰",
        "청소기",
        "세탁기",
        "마우스",
        "키보드",
        "마우스패드",
        "모니터",
    ]
    results = dlns.data.download_shopping_data.main(
        cur_time,
        queries,
        save_path,
        ["title"],
        image_save_root,
        client_id,
        client_passwd,
        test_split_ends=tuple(["0", "1"]),
    )

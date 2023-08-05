import argparse
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
    parser = argparse.ArgumentParser()
    
    cur_time = datetime.isoformat(datetime.now(), timespec="seconds")
    
    save_path_root = os.path.join(WORK_DIR, "dataset", "naver_shopping_query_data")
    os.makedirs(save_path_root, exist_ok=True)
    image_save_root = os.path.join(save_path_root, "images", cur_time)
    save_path = os.path.join(save_path_root, f"{cur_time}.csv")
    
    # client_id & passwd should be registered in 
    # https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md
    default_client_id = os.environ.get('naver_api_client_id', None)
    default_client_passwd = os.environ.get('naver_api_client_passwd', None)
    
    parser.add_argument("--naver_client_id", type=str, default=default_client_id)
    parser.add_argument("--naver_client_passwd", type=str, default=default_client_passwd)
    args = parser.parse_args()
    client_id = args.naver_client_id
    client_passwd = args.naver_client_passwd
    if not client_id:
        raise ValueError("naver_api_client_id should be given.")
    if not client_passwd:
        raise ValueError("naver_api_client_passwd should be given.")
    queries = [
        "의자",
        "책상",
        "컴퓨터",
        "tv",
        "해드폰",
        "러그",
        "컵",
        "쟁반",
        "청소기",
        "세탁기",
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

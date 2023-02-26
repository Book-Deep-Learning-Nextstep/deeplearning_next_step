import json
import logging
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Dict
from typing import List

import pandas as pd
import wget
from tqdm import tqdm


def download(url: str, out_path: str = ".") -> None:
    max_try = 10
    try_i = 0
    while try_i < max_try:
        try:
            wget.download(url, out=out_path, bar=None)
            break
        except Exception:
            try_i += 1


def cleanhtml(raw_html: str) -> str:
    cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


# %%
def get_navershopping_query(
    query: str,
    client_id: str,
    client_secret: str,
    display_n: int = 100,
) -> dict:
    query = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/shop.json?query={query}&display={display_n}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        return json.loads(response_body.decode("utf-8"))
    print("Error Code:" + rescode)
    raise ValueError()


def zip_query_results(query2results: Dict[str, dict]) -> pd.DataFrame:
    results = []
    for query, result in tqdm(
        query2results.items(), desc="update additinoal info", total=len(query2results)
    ):
        cur_df = pd.DataFrame(result["items"])
        cur_df["query"] = query
        cur_df["rank"] = range(1, len(result["items"]) + 1)
        cur_df["date"] = pd.to_datetime(datetime.now())
        results.append(cur_df)
    concated = pd.concat(results, ignore_index=True)
    concated.reset_index(drop=True, inplace=True)
    return concated


def get_daily_shopping_search_data(
    queries: List[str],
    client_id: str,
    client_secret: str,
    display_n: int = 100,
) -> pd.DataFrame:
    responses = {}
    for q in tqdm(queries, desc="getting daily query response", total=len(queries)):
        responses[q] = get_navershopping_query(q, client_id, client_secret, display_n)
    return zip_query_results(responses)


def string_cleansing(df: pd.DataFrame, apply_columns: List[str]):
    for c in apply_columns:
        df[c] = df[c].apply(cleanhtml)
    return df


def download_images(
    df: pd.DataFrame,
    out_root: str = "./",
    link_key: str = "image",
    local_new_link_key: str = "local_image",
):
    out_paths = []
    for link in tqdm(df[link_key], desc="download_images", total=len(df)):
        out_path = os.path.join(out_root, link.replace("/", "|"))
        out_paths.append(os.path.relpath(out_path))
        download(link, out_path)
    df[local_new_link_key] = out_paths
    return df


def main(
    queries: List[str],
    out_path: str,
    string_cleansing_columns: List[str],
    image_download_root_path: str,
    client_id: str,
    client_secret: str,
    display_n: int = 100,
) -> pd.DataFrame:
    assert out_path.endswith(".csv")
    df = get_daily_shopping_search_data(queries, client_id, client_secret, display_n)
    df = string_cleansing(df, string_cleansing_columns)
    if not os.path.exists(image_download_root_path):
        os.makedirs(image_download_root_path)
    df = download_images(df, image_download_root_path)
    logging.info(f"saving final results to {out_path}")
    df.to_csv(out_path)
    return df

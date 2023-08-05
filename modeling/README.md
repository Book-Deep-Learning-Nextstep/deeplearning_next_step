# (WORK IN PROGRESS) deeplearning_next_step

## Install it

```bash
# From PyPI
pip install git+https://github.com/jungbaepark/deeplearning_next_step # or
git clone https://github.com/jungbaepark/deeplearning_next_step
cd deeplearning_next_step
make install
```

## Usage

### > Chapter 1 - download data

```bash
python -m scripts.download_naver_shoppping_data --naver_client_id {YOUR_NAVER_DEV_CLIENT_ID_TOKEN} --naver_client_passwd {YOUR_NAVER_DEV_CLIENT_PASSWD_TOKEN}
```

- For your API client tokens, please visit https://developers.naver.com/ & create your API tokens ('검색>쇼핑').

---

## Code Format & Lint (black, isort, flake8)

```bash
make fmt # format
make lint # lint
```

## Q&A

Jungbae Park: jbpark0614@gmail.com

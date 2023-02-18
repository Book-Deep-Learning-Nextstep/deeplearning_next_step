# research_spk_assess_learning (spkal)

[![CI](https://github.com/riiid/research-spk-assess-learning/actions/workflows/main.yml/badge.svg)](https://github.com/riiid/research-spk-assess-learning/actions/workflows/main.yml)


## Install it

```bash
# From PyPI
pip install git+https://github.com/riiid/research-spk-assess-learning.# # or Manual Install
git clone https://github.com/riiid/research-spk-assess-learning
cd research_spk_assess_learning
make install
```

## Quick Start - For Research
1. Prepare datasets.
- download SpeechOcean from Huggingface.
- or Prepare internal toeic_speaking data. (See below)

2. run below commands:

```bash
python scripts/train.py
```

## Quick Start - For Production

- Use below running scripts.
```bash
python scripts/eval.py
```


## Download TOEIC Speaking Data
1. Login with AWS
(refer: https://www.notion.so/riiid/Using-Vault-AWS-with-Keycloak-4ce2b10c4daf48298581f05a76e50d23 )

2. Download TOEIC_SPEAKING data
```bash
aws sync s3://riiid-toeic-mlops-archive/speaking/audio_20230101_langaca ./cache_data/toeicspk/audio
```

3. Check audio files & using data
- meta.csv & invalid_csv files.

## Other Utils
### 1. gen_meta_for_asr.py

- Optional prerequistes to use "data.speech_dataset.SpeechScoringDataset"
- Generate metadata.txt according to wav_files roots. (for 아이일래 data)
- The examples of metadata.txt can be found in "data/samples/*.txt"

### 2. asr_text_gen.py

- From metadata.txt, run asr & save results.
- To check the transcripted text from ASR.


---

## Code Format & Lint (black, isort, flake8)

```bash
make fmt # format
make lint # lint
```



## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Commit types

Example commit message:
```bash
git commit -m "feat: add dataloader"
```

| Commit Type | Title | Description |
|:-----------:|--------------------------|-------------------------------------------------------------------------------------------------------------|
|   `feat`    | Features                 | A new feature                                                                                               |
|    `fix`    | Bug Fixes                | A bug Fix                                                                                                   |
|   `docs`    | Documentation            | Documentation only changes                                                                                  |
|   `style`   | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)      |
| `refactor`  | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
|   `perf`    | Performance Improvements | A code change that improves performance                                                                     |
|   `test`    | Tests                    | Adding missing tests or correcting existing tests                                                           |
|   `build`   | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
|    `ci`     | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
|   `chore`   | Chores                   | Other changes that don't modify src or test files                                                           |
|  `revert`   | Reverts                  | Reverts a previous commit                                                                                   |


---
## Q&A
- Jungbae Park: jungbae.park@riiid.co

--------------------------------------

# Content AI Research Template

A low dependency and really simple to start project template for Content AI Research Projects.

### HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/riiid/content-ai-research-template/generate)** feature.

1. Click on **[Use this template](https://github.com/riiid/content-ai-research-template/generate)**
3. Give a name to your project  
   (e.g. `my-awesome-project` recommendation is to use all lowercase and hyphen separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. Read the file [CONTRIBUTING.md](CONTRIBUTING.md)
5. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🖼️ Templates for starting multiple application types:
  * **Basic low dependency** Python program (default) [use this template](https://github.com/riiid/content-ai-research-template/generate)
- 📦 A basic [setup.py](setup.py) file to provide installation, packaging and distribution for your project.  
  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.
- 🤖 A [Makefile](Makefile) with the most useful commands to install, test, lint, format and release your project.
- 📃 Documentation structure using [mkdocs](http://www.mkdocs.org)
- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.
- 🐋 A simple [Containerfile](Containerfile) to build a container image for your project.  
  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.
- 🧪 Testing structure using [pytest](https://docs.pytest.org/en/latest/)
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- 🎯 Entry points to execute your program using `python -m <spkal>` or `$ spkal` with basic CLI argument parsing.
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to lint, test and release your project on Linux, Mac and Windows environments.

> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md](ABOUT_THIS_TEMPLATE.md)  
> If you want to contribute to this template please open an issue or fork and send a PULL REQUEST.



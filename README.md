# log_analyzer

Analyzing log file using pattern matching algorithm

- ssh log file
  - Knuth-Morris-Pratt (KMP)
  - Boyer-Moore (BM)
  - Regular Expression (Regex)

## Usage

Install Python if you don't have it installed already. The Log Analyzer requires Python 3.6 or higher.

1. Clone the repository using `git` or download from github.

2. Open terminal or command prompt and navigate to the directory where repository is located.

3. Run the script with the desired options. Example command:

```bash
python ./src/main.py ./test/test.log -algo BM
```

This command analyzes the log file test.log using Boyer-Moore (BM) algorithm and outputs the results to the file summary.txt and result.txt

## Command-Line Options

```bash
usage: main.py [-h] [-algo {kmp,bm,regex}] file_path

Analyze network activity from ssh log file. Output result.txt and summary.txt

positional arguments:
  file_path             Path to ssh log file

options:
  -h, --help            show this help message and exit
  -algo {kmp,bm,regex}  Pattern Algorithm to use. Default: KMP
```

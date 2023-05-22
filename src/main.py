import argparse
from analyzer import SSHLogAnalyzer
from pattern import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                "Analyze network activity from ssh log file. Output result.txt and summary.txt")

    parser.add_argument("file_path", type=str, help="Path to ssh log file")

    parser.add_argument("-algo", type=str.lower, 
                        help="Pattern Algorithm to use. Default: KMP", 
                        default="kmp", choices=["kmp", "bm", "regex"])
    
    args = parser.parse_args()
    pattern_algo = {
        "kmp": KMP,
        "bm": BM,
        "regex": regex
    }
    print(f"Analyzing {args.file_path}")
    print(f"Using {args.algo} algorithm")
    analyzer = SSHLogAnalyzer(args.file_path, pattern_algo[args.algo])
    try:
        analyzer.analyze()
    except Exception as e:
        print("Error occured", end=" ")
        print(e)
        exit(1)
    print("Done")





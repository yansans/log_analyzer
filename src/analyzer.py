from abc import ABC, abstractmethod
from pattern import *

class LogAnalyzer(ABC):
    @abstractmethod
    def analyze(self):
        """
        Analyze the log file
        output file: result.txt
        """
        pass

class SSHLogAnalyzer(LogAnalyzer):
    def __init__(self, file_path : str, search_func: callable,  *pattern : list):
        self.log_file_path : str = file_path
        self.search_func : callable = search_func

        self.search : str = "sshd"
        default_pattern = [
            "Illegal user",
            "Invalid user",
            "Did not receive identification string",
            "Failed password",
            "error: Could not get shadow information",
            "User dcid not allowed",
        ]

        self.pattern : list = pattern if pattern else default_pattern
        self.result : list = [[] for _ in range(len(self.pattern))]
        self.user_result : dict = {}
        self.ip_result : dict = {}
        self.port_result : dict = {}

    def analyze(self):
        self._get_match_in_file(self.search_func)

        self._output_summary()
        self._output_analysis()
    
    def _get_match_in_file(self, search_func: callable):
        """
        Get the match line number in the log file using search_method from Pattern.py
        """
        with open(self.log_file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                for idx, pattern in  enumerate(self.pattern, start=0):
                    i = search_func(pattern.lower(), line.lower())
                    if i != -1:
                        self.result[idx].append(line[i+len(pattern):].strip() + f" at line {line_number}")
                        self._extract_user(line, search_func)
                        self._extract_network(line, search_func)
                        break
    
    def _extract_network(self, line: str, search_func: callable):
        """
        Extract IP address from line
        """
        i = search_func(" from ", line.lower())
        if i != -1:
            ip = line[i+5:].split()[0]
            if ip in self.ip_result:
                self.ip_result[ip] += 1
            else:
                self.ip_result[ip] = 1

        i = search_func(" port ", line.lower())
        if i != -1:
            port = line[i+5:].split()[0]
            if port in self.port_result:
                self.port_result[port] += 1
            else:
                self.port_result[port] = 1

    def _extract_user(self, line: str, search_func: callable):
        """
        Extract user from line
        """
        i = search_func(" for ", line.lower())
        if i != -1:
            user = line[i+4:].split()[0]
            if user == "invalid" or user == "illegal":
                user = line[i+4:].split()[2]
            if user in self.user_result:
                self.user_result[user] += 1
            else:
                self.user_result[user] = 1

    def _output_analysis(self):
        """
        All the result from the result _get_match_in_file
        """
        with open("result.txt", "w") as file:
            for id, pattern in enumerate(self.result, start=0):
                file.write(f"{self.pattern[id]}:\n")
                for line in pattern:
                    file.write(f"{line}\n")
                if not(pattern):
                    file.write("No match found\n")                    
                file.write("\n")
    
    def _output_summary(self):
        """
        Summary from the result _get_match_in_file
        """
        with open("summary.txt", "w") as file:
            file.write(f"Summary of {self.log_file_path}\n\n")

            file.write(f"Pattern found\n")
            for id, pattern in enumerate(self.result, start=0):
                file.write(f"{self.pattern[id]}: {len(pattern)} attempt\n")

            sorted_user = sorted(self.user_result.items(), key=lambda x: x[1], reverse=True)
            file.write("\nFive most frequent users:\n")
            for user, count in sorted_user[:5]:
                file.write(f"{user} with {count} count\n")
            if not(sorted_user):
                file.write("No match found\n")   

            sorted_ip = sorted(self.ip_result.items(), key=lambda x: x[1], reverse=True)
            file.write("\nFive most frequent IP addresses:\n")
            for ip, count in sorted_ip[:5]:
                file.write(f"{ip} with {count} count\n")
            if not(sorted_ip):
                file.write("No match found\n")  

            sorted_port = sorted(self.port_result.items(), key=lambda x: x[1], reverse=True)
            file.write("\nFive most frequent ports:\n")
            for port, count in sorted_port[:5]:
                file.write(f"{port} with {count} count\n")
            if not(sorted_port):
                file.write("No match found\n")  
    

if __name__ == "__main__":
    file_path = '.\\test\\test.log'
    analyzer = SSHLogAnalyzer(file_path, KMP)
    analyzer.analyze()

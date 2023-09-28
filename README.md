# VulnMapAI
VulnMapAI combines the power of nmap’s detailed network scanning and the advanced natural language processing capabilities of GPT-4 to generate comprehensive and intelligible vulnerability reports. It aims to facilitate the identification and understanding of security vulnerabilities.

## Features
- **Automated Network Scanning:** Uses Nmap for automated discovery and scanning of systems.
- **Exploit Suggestions:** Offers suggestions for potential exploits based on discovered services and versions.
- **Report Generation:** Creates comprehensive reports based on discovery and suggested exploits.
- **Metasploit Integration:** Integrates with Metasploit for searching and verifying exploits.
- **Multi-Process Scanning:** Leverages multi-process capabilities for efficient network scanning.

## Getting Started

### Prerequisites
- Python 3.x
- Metasploit Framework
- Nmap
- Required Python libraries: `httpx`, `pymetasploit3`

OR

- Docker

### Usage
- Clone the project and change directory ```git clone https://github.com/davidalami/VulnMapAI.git && cd ./VulnMapAI```
- Build the image ```docker build -f build/final_image/Dockerfile -t vulnmapai .```
- Run the image in interactive mode, pass a valid openai API key as an environment variable
```docker run -it --entrypoint=/bin/bash -e "OPENAI_API_KEY=sk-.." vulnmapai ```
- Pass target IP addresses to the python script, like ```python main.py 127.0.0.1``` and make yourself a coffee! The results will be saved in the `reports` folder.
See the example report [here](https://htmlpreview.github.io/?https://github.com/davidalami/VulnMapAI/blob/main/report/vsftpd%202.3.4.html).

## Contribution
We welcome contributors who are willing to improve this project. Here's how you can contribute:
- Fork the repository
- Clone your fork (git clone https://github.com/[Your_Username]/VulnMapAI)
- Create a branch (git checkout -b new_feature)
- Commit your changes (git commit -am 'Add feature')
- Push to the branch (git push origin new_feature)
- Open a Pull Request

### Areas for Contribution

- Feature Enhancement: Propose new features and enhancements.
- Bug Fixes: Help in identifying issues and submitting patches for bug fixes.
- Code Optimization: Contribute to making the code more efficient and optimized.
- Documentation Improvement: Work on improving the documentation and adding tutorials or guides.

## Support
If you find any bugs or have feature requests, please open an issue detailing the bug or feature.

## Disclaimer
This application is intended for educational and lawful activities only. Users are responsible for ensuring all activities conform to applicable local, state, and federal laws and regulations. We assume no responsibility for any misuse or damage caused by this program.

## Acknowledgements
We would like to acknowledge the developers of the utilized libraries and tools, such as Metasploit and Nmap, for their significant contributions to the cybersecurity community.


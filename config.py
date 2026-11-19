# configuration file for storing constants
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # read SELFHOSTED_LLM_* credentials from a local .env when present

DEFAULT_LLM_MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"

EXPLOITS_DIR = "/usr/share/metasploit-framework/modules/exploits"
MSF_INDEX_FILE = '/app/resources/msf_index.json'
COMMON_PORTS = "/app/resources/ports.json"
REPORT_DIR = Path('./report')
REPORT_TEMPLATE = '/app/webapp/templates/report_template.html'
PROMPTS_FILE = "/app/advising/prompts.yaml"

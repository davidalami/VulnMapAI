# configuration file for storing constants
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # read LLM_* credentials from a local .env when present

DEFAULT_LLM_MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"

PROJECT_ROOT = Path(__file__).resolve().parent

EXPLOITS_DIR = "/usr/share/metasploit-framework/modules/exploits"
MSF_INDEX_FILE = PROJECT_ROOT / 'resources' / 'msf_index.json'
COMMON_PORTS = PROJECT_ROOT / 'resources' / 'ports.json'
REPORT_DIR = PROJECT_ROOT / 'report'
PROMPTS_FILE = PROJECT_ROOT / 'advising' / 'prompts.yaml'

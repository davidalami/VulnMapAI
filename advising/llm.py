import asyncio
import json
import os
from yaml import safe_load
from typing import Dict

import httpx
from flask import render_template_string

from config import REPORT_TEMPLATE
from utils.logger import Logger


class Advisor:
    """
    Advisor class that prepares the reports by summarizing discoveries and providing attack advice,
    leveraging GPT-4 models from OpenAI API.
    """

    def __init__(self,
                 discovery_result,
                 title,
                 exploits,
                 api_key=os.getenv('OPENAI_API_KEY'),
                 api_url='https://api.openai.com/v1/chat/completions'):
        self.full_discovery_result = discovery_result
        self.discovery_result = " ".join(discovery_result.split()[:2000])
        self.title = title
        self.exploits = exploits
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        self.logger = Logger(__name__).get_logger()

    def _query_api(self, json_data: Dict) -> str:
        """
        Private method to query the OpenAI API with provided JSON data.

        Args:
            json_data (dict): JSON data to be sent to the API.

        Returns:
            str: Response from the API.
        """

        async def _send_to_openai_async():
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.api_url,
                    json=json_data,
                    headers=self.headers,
                    timeout=120,
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]['content']
                else:
                    response.raise_for_status()

        return asyncio.run(_send_to_openai_async())

    def _load_prompts(self, prompt_type: str) -> Dict[str, str]:
        """
        Load prompts from the prompts.yaml file based on the prompt_type.

        Args:
            prompt_type (str): 'advise_attack_prompt', 'summarize_discoveries_prompt', etc.

        Returns:
            Dict[str, str]: Dictionary containing 'system' and 'user' prompts.
        """
        with open('prompts.yaml', 'r') as prompts_file:
            prompts_data = safe_load(prompts_file)
        return prompts_data.get(prompt_type, {})

    def advise_attack(self) -> str:
        """
        Formulates a query and sends it to the OpenAI API to receive advice on potential attacks.

        Returns:
            str: Advice on potential attacks from the API.
        """
        self.logger.info("Advising attack based on the discovery result.")
        prompts = self._load_prompts('advise_attack_prompt')
        json_data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': prompts['system'],
                },
                {
                    'role': 'user',
                    'content': prompts['user'].format(discovery_result=self.discovery_result),
                },
            ],
        }
        return self._query_api(json_data)

    def summarize_discoveries(self) -> str:
        """
        Formulates a  query and sends it to the OpenAI API to summarize the discoveries made during the scan.

        Returns:
            str: Summarized discoveries from the API.
        """
        self.logger.info("Summarizing the discoveries.")
        prompts = self._load_prompts('summarize_discoveries_prompt')
        json_data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': prompts['system'],
                },
                {
                    'role': 'user',
                    'content': prompts['user'].format(discovery_result=self.discovery_result),
                },
            ],
        }
        return self._query_api(json_data)

    def prepare_report(self) -> str:
        """
        Prepares an HTML report based on discoveries, attack advice, and exploits.

        Returns:
            str: A string representation of the HTML report.
        """
        discoveries = self.summarize_discoveries()
        advise = self.advise_attack()

        self.logger.info("Preparing the HTML report.")
        exploits = '<br>'.join(self.exploits)

        self.full_discovery_result = json.loads(self.full_discovery_result)
        if "script" in self.full_discovery_result:
            for k, v in self.full_discovery_result["script"].items():
                self.full_discovery_result[k] = v
            del self.full_discovery_result["script"]

        formatted_full_discovery_result = "".join([f"{k}: {v}<br>" for k, v in self.full_discovery_result.items()])

        # Load the template from file
        with open(REPORT_TEMPLATE, 'r') as template_file:
            template_content = template_file.read()

        # Render the template to a string
        report_html = render_template_string(template_content,
                                             title=self.title,
                                             exploits=exploits,
                                             discoveries=discoveries,
                                             advise=advise,
                                             full_discovery_result=formatted_full_discovery_result)

        return report_html

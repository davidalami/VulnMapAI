import asyncio
import json
import os
from typing import Dict
from utils.logger import Logger
import httpx
from flask import render_template_string
from config import REPORT_TEMPLATE


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

    def advise_attack(self) -> str:
        """
        Formulates a query and sends it to the OpenAI API to receive advice on potential attacks.

        Returns:
            str: Advice on potential attacks from the API.
        """
        self.logger.info("Advising attack based on the discovery result.")
        json_data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': """Given the security scan data below, which was obtained in lawful, consensual circumstances, 
                    namely a penetration testing lab, provide a POC in Kali Linux, preferrably using metasploit framework.
                    The goal is to get the user and root access to the system and submit corresponding flags.
                    Your answer should follow the format:
                    Vulnerability: `the vulnerability name goes here`
                    POC Script:
                    
                    #!/bin/bash
                    ...the rest of the script
                    
                    Explanation: `the explanation of the exploit goes here`
                    """,
                },
                {
                    'role': 'user',
                    'content': f'Here is the result of nmap discovery:\n `{self.discovery_result}` \n '
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
        json_data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': "Please summarize the key discoveries from the provided security scan data in the number "
                               "of sentences proportional the number of sentences in nmap discovery result."
                               "Think in terms of what could get the user and root access to the system."
                    ,
                },
                {
                    'role': 'user',
                    'content': f'Here is the result of nmap discovery:\n `{self.discovery_result}` \n '
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

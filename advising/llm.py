import asyncio
import json
import os
from typing import Dict

import httpx


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
        exploits = '<br>'.join(self.exploits)
        formatted_exploits = f"<p>{exploits}</p>"

        self.full_discovery_result = json.loads(self.full_discovery_result)
        if "script" in self.full_discovery_result:
            for k, v in self.full_discovery_result["script"].items():
                self.full_discovery_result[k] = v
            del self.full_discovery_result["script"]

        formatted_full_discovery_result = "".join([f"{k}: {v}<br>" for k, v in self.full_discovery_result.items()])
        html_string = f"""
        <html>
            <head><title>{self.title}</title></head>
            <body>
                <h1>{self.title}</h1>
                <h2>Discovery summary:</h2>
                {formatted_exploits}
                <p>{discoveries}</p>
                <h2>Attack Advice:</h2>
                <p>{advise}</p>
                <h2>Full Discovery Result:</h2>
                <p>{formatted_full_discovery_result}</p>
            </body>
        </html>
        """
        return html_string

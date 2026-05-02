"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header, REQUIRED_LANGSMITH_VARS

load_dotenv()


def toJsonFormat(prompt_template):
    metadata = prompt_template.metadata or {}

    prompt_name = metadata.get('lc_hub_repo', 'bug_to_user_story_v1')

    system_prompt = ''
    user_prompt = ''
    for message in prompt_template.messages:
        message_type = message.__class__.__name__

        if 'System' in message_type:
            system_prompt = message.prompt.template
        elif 'Human' in message_type:
            user_prompt = message.prompt.template

    return prompt_name, {
        prompt_name: {
            'description'  : metadata.get('description', 'Prompt para converter relatos de bugs em User Stories'),
            'system_prompt': system_prompt,
            'user_prompt'  : user_prompt,
            'version'      : 'v1',
            'created_at'   : '2025-01-15',
            "tags": list(metadata.values()),
        }
    }


def pull_prompts_from_langsmith():
    external_prompt_name = 'leonanluppi/bug_to_user_story_v1'

    client = Client()
    return client.pull_prompt(external_prompt_name)


def main():
    """Função principal"""

    try:
        if not check_env_vars(REQUIRED_LANGSMITH_VARS):
            return 1

        prompt_template = pull_prompts_from_langsmith()

        print_section_header(f'Template obtido:\n\t{prompt_template}')

        prompt_name, prompt_template_dict = toJsonFormat(prompt_template)

        path = Path(f'.\\prompts\\{prompt_name}.yml')
        file_path = str(path.resolve())

        if path.exists():
            print_section_header(f'Arquivo já existe na pasta {file_path}')
            return 0

        if not save_yaml(prompt_template_dict, file_path):
            return 1

        print_section_header(f'Prompt criado com sucesso: {file_path}')

        return 0
    except Exception as e:
        print(f"❌ Erro ao obter arquivo: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

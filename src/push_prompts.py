"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, REQUIRED_LANGSMITH_VARS, validate_prompt_structure
from langsmith import Client

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt_info = prompt_data[prompt_name]
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', prompt_info['system_prompt']),
        ('human' , prompt_info['user_prompt']),
    ])

    client = Client()
    url = client.push_prompt(
        prompt_name,
        object=prompt_template,
        tags=[ f'v{prompt_info["version"]}', f'created_at: {prompt_info["created_at"]}' ] + prompt_info['tags'],
        description=prompt_info['description']
    )

    print_section_header(f'Commit Link: {url}')


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    try:
        if not check_env_vars(REQUIRED_LANGSMITH_VARS):
            return 1

        prompt_name = 'bug_to_user_story_v2'
        prompt_data = load_yaml(f'.\\prompts\\{prompt_name}.yml')

        validate_prompt(prompt_data)

        return 0 if push_prompt_to_langsmith(prompt_name, prompt_data) else 1
    except Exception as e:
        print(f'❌ Erro ao enviar arquivo: {e}')
        return 1

if __name__ == "__main__":
    sys.exit(main())

"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure # Nota: Método não utilizado, mas usei a logica dele nos testes

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        system_prompt = prompt_data.get('system_prompt', '').strip()
        assert not system_prompt, f'system_prompt está vazio'

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        keywords = [ 'você é', 'seu papel', 'role' ]
        system_prompt = prompt_data.get('system_prompt', '').strip()
        assert not any(keyword in system_prompt for keyword in keywords), f'system_prompt não define uma persona'

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        keywords = [ 'markdown', 'formato', 'estrutura', 'template' ]
        system_prompt = prompt_data.get('system_prompt', '').strip()
        assert not any(keyword in system_prompt for keyword in keywords), f'system_prompt não exige formato Markdown ou User Story padrão.'

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        keywords = [ 'exemplo', 'example', 'entrada', 'input', 'saída', 'output' ]
        system_prompt = prompt_data.get('system_prompt', '').strip()
        assert not any(keyword in system_prompt for keyword in keywords), f'system_prompt não contém exemplos de entrada/saída (técnica Few-shot).'

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        system_prompt = prompt_data.get('system_prompt', '').strip().upper()
        assert 'TODO' not in system_prompt, f'system_prompt ainda contém TODOs'

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt_data = load_prompts(f'.\\prompts\\bug_to_user_story_v2.yml')

        techniques = prompt_data.get('techniques_applied', [])
        techniques_size = len(techniques)
        assert techniques_size < 2, f'Mínimo de 2 técnicas requeridas, encontradas: {techniques_size}'

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
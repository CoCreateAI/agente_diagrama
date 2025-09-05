import subprocess
import os

def validar_diagrama_mermaid(codigo_mermaid: str, temp_file_path: str = "temp_diagram.mmd") -> tuple[bool, str, str]:
    """
    Valida um código Mermaid usando o mermaid-cli.

    Args:
        codigo_mermaid: A string contendo o código Mermaid a ser validado.
        temp_file_path: O caminho para um arquivo temporário a ser usado para a validação.

    Returns:
        Uma tupla (bool, str) onde o booleano é True se o código for válido,
        e a string contém uma mensagem de sucesso ou o erro.
    """
    try:
        # Escreve o código em um arquivo temporário
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(codigo_mermaid)

        # Constrói o caminho para o executável do mmdc, subindo um nível no diretório
        # para encontrar a pasta node_modules na raiz do projeto.
        # No Windows, usa .cmd; em outros sistemas, usa o executável sem extensão
        if os.name == 'nt':  # Windows
            mmdc_path = os.path.join(os.path.dirname(__file__), "..", "node_modules", ".bin", "mmdc.cmd")
        else:
            mmdc_path = os.path.join(os.path.dirname(__file__), "..", "node_modules", ".bin", "mmdc")

        # Executa o mermaid-cli para validar a sintaxe (tentando gerar um SVG)
        # A saída é descartada se for bem-sucedido, mas o erro é capturado
        resultado = subprocess.run(
            [mmdc_path, "-i", temp_file_path, "-o", "temp_output.svg"],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        log_message = "✅ **Agente Validador**: Sintaxe do diagrama verificada e aprovada."
        return True, "Sintaxe do diagrama Mermaid é válida.", log_message

    except subprocess.CalledProcessError as e:
        # Se o mmdc falhar, a sintaxe é provavelmente inválida
        log_message = f"⚠️ **Agente Validador**: Sintaxe inválida detectada. Erro: {e.stderr.strip()}"
        return False, e.stderr, log_message
    except FileNotFoundError:
        # Caso o mmdc não seja encontrado
        log_message = "❌ **Agente Validador**: O executável 'mmdc' não foi encontrado. A validação não pôde ser concluída."
        return False, "Erro: mermaid-cli (mmdc) não encontrado. Verifique se está instalado.", log_message
    finally:
        # Limpa os arquivos temporários
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists("temp_output.svg"):
            os.remove("temp_output.svg")

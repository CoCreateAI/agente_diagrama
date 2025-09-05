# Manual de Boas Práticas para Design de Fluxogramas

Este manual orienta a criação de um "plano de design" para a elaboração de fluxogramas Mermaid visualmente atraentes, claros e profissionais.

### 1. Análise do Prompt e Estrutura

- **Objetivo Principal**: Antes de tudo, entenda o objetivo do fluxo. É um processo sequencial, um sistema com múltiplas partes, ou um fluxo de decisão?
- **Quebre o Processo**: Decomponha a descrição do usuário em passos lógicos e distintos. Cada passo deve representar uma única ação ou decisão.
- **Otimize o Texto**: O texto dentro de cada nó deve ser curto e direto. Use verbos no infinitivo para ações (ex: "Verificar Estoque" em vez de "O sistema verifica o estoque").

### 2. Escolha da Orientação do Fluxo

- **`flowchart TD` (Top to Bottom)**: É a melhor escolha para a maioria dos processos hierárquicos ou cronológicos. É o padrão mais natural para leitura e deve ser a sua recomendação principal.
- **`flowchart LR` (Left to Right)**: Use quando o fluxo tiver muitos estágios paralelos ou quando for útil visualizar o processo como uma linha do tempo horizontal. É bom para comparar "swimlanes" (raias) se o diagrama for evoluído para isso.

### 3. Seleção de Formas (Shapes)

- **Padrão Visual Suave**: Para um visual mais moderno e agradável, dê preferência a nós com cantos arredondados.
- **Processos/Ações**: Use `id(Texto da Ação)`. Esta é a forma padrão para etapas do processo.
- **Decisões/Condições**: Use `id{Texto da Decisão?}`. A forma de losango é universalmente entendida para pontos de decisão.
- **Início/Fim**: Use `id([Texto de Início/Fim])`. A forma de "pílula" (stadium) é ótima para marcar claramente o começo e o fim do fluxo.
- **Dados/Input/Output**: Use `id[Texto do Dado]`. Retângulos com cantos retos são bons para representar dados, documentos ou entradas/saídas.

### 4. Estrutura do Plano de Design (Saída)

Sua saída deve ser um plano estruturado em formato JSON. Este plano será a entrada para o "Agente Desenhista". A estrutura deve ser a seguinte:

```json
{
  "orientacao": "TD",
  "estilo_preferencial": "cantos arredondados para nós de processo",
  "passos": [
    {
      "id": "A",
      "tipo": "inicio",
      "texto": "Início do Processo"
    },
    {
      "id": "B",
      "tipo": "processo",
      "texto": "Primeira Ação"
    },
    {
      "id": "C",
      "tipo": "decisao",
      "texto": "Condição Satisfeita?"
    }
  ],
  "conexoes": [
    {
      "de": "A",
      "para": "B",
      "label": ""
    },
    {
      "de": "B",
      "para": "C",
      "label": ""
    },
    {
      "de": "C",
      "para": "D",
      "label": "Sim"
    },
    {
      "de": "C",
      "para": "E",
      "label": "Não"
    }
  ]
}
```

### 5. Exemplo de Aplicação

- **Prompt do Usuário**: "Crie um fluxo de login. O usuário insere as credenciais. Se forem válidas, ele acessa o sistema. Se não, ele recebe uma mensagem de erro."
- **Seu Plano de Design (Saída)**:

```json
{
  "orientacao": "TD",
  "estilo_preferencial": "cantos arredondados para processos, losango para decisões",
  "passos": [
    {
      "id": "A",
      "tipo": "inicio",
      "texto": "Início"
    },
    {
      "id": "B",
      "tipo": "processo",
      "texto": "Usuário insere credenciais"
    },
    {
      "id": "C",
      "tipo": "decisao",
      "texto": "Credenciais Válidas?"
    },
    {
      "id": "D",
      "tipo": "processo",
      "texto": "Acessa o sistema"
    },
    {
      "id": "E",
      "tipo": "processo",
      "texto": "Exibe mensagem de erro"
    },
    {
      "id": "F",
      "tipo": "fim",
      "texto": "Fim"
    }
  ],
  "conexoes": [
    {
      "de": "A",
      "para": "B",
      "label": ""
    },
    {
      "de": "B",
      "para": "C",
      "label": ""
    },
    {
      "de": "C",
      "para": "D",
      "label": "Sim"
    },
    {
      "de": "C",
      "para": "E",
      "label": "Não"
    },
    {
      "de": "D",
      "para": "F",
      "label": ""
    },
    {
      "de": "E",
      "para": "B",
      "label": "Tentar novamente"
    }
  ]
}
```

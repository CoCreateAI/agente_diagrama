# Agente Diagrama

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/CoCreateAI/agente_diagrama?style=social)](https://github.com/CoCreateAI/agente_diagrama/stargazers)

Uma ferramenta de IA para geração e gerenciamento de diagramas de processos.

## 🚀 Visão Geral

O Agente Diagrama é uma solução poderosa que utiliza inteligência artificial para ajudar na criação, análise e otimização de diagramas de processos. Desenvolvido para ser intuitivo e eficiente, este projeto facilita a visualização de fluxos de trabalho e processos complexos.

## ✨ Recursos

- 🎨 Geração automática de diagramas a partir de descrições em linguagem natural
- 🤖 Agentes de IA especializados em análise de processos
- 📊 Visualização interativa de fluxos de trabalho
- 🔍 Análise e otimização de processos existentes
- 📱 Interface web amigável
- 🔄 Integração com ChromaDB para armazenamento de conhecimento

## 🛠️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/CoCreateAI/agente_diagrama.git
   cd agente_diagrama
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` com suas configurações

## 🚀 Como Usar

1. Inicie a aplicação web:
   ```bash
   cd "Assistente de Diagramas com IA"
   python app.py
   ```

2. Acesse a aplicação no navegador:
   ```
   http://localhost:5000
   ```

## 🏗️ Estrutura do Projeto

```
agente_diagrama/
├── Assistente de Diagramas com IA/  # Aplicação principal
│   ├── app.py                      # Ponto de entrada da aplicação
│   ├── agente_analista.py          # Lógica do agente analista
│   ├── agente_corretor.py          # Lógica do agente corretor
│   └── agente_critico.py           # Lógica do agente crítico
├── chroma_db/                      # Armazenamento vetorial
├── diagrams/                       # Exemplos de diagramas
├── agents/                         # Documentação dos agentes
├── frontend/                       # Arquivos de frontend
├── .env                            # Configurações de ambiente
├── requirements.txt                # Dependências Python
└── README.md                       # Este arquivo
```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos para contribuir:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. Faça o Push da Branch (`git push origin feature/AmazingFeature`)
6. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## ✉️ Contato

Time CoCreateAI - [@CoCreateAI](https://github.com/CoCreateAI)

## 🙏 Agradecimentos

- A todos os contribuidores que ajudaram a tornar este projeto possível
- À comunidade de código aberto por todo o suporte e ferramentas incríveis

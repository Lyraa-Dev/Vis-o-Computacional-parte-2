Simulação Computacional de Detecção e Perseguição entre Agentes Dinâmicos

📋 Descrição do Projeto
Este projeto implementa uma simulação computacional em ambiente 2D da interação entre dois agentes dinâmicos: "Ligeirinho" (o agente alvo) e "Frajola" (o agente perseguidor). A simulação foi desenvolvida como parte de um estudo em Visão Computacional, focando em técnicas de detecção automática e estratégias de perseguição.

🎯 Problema Proposto
Modelar computacionalmente a interação entre dois agentes animados em um plano bidimensional:

Agente Alvo ("Ligeirinho"): Cruza o canvas em trajetórias lineares com velocidades variáveis

Agente Perseguidor ("Frajola"): Responsável por detectar e interceptar o alvo usando técnicas de visão computacional

🚀 Características Implementadas
✅ Requisitos Atendidos
Canvas
✅ Área fixa de 800×600 pixels

✅ Atualização frame a frame (60 FPS)

Agente Alvo (Ligeirinho)
✅ Tamanho: 20×20 pixels

✅ Surgimento aleatório nas bordas do canvas

✅ Velocidade: 8-15 pixels por frame

✅ Movimento linear com direção variável e reflexão nas bordas

Agente Perseguidor (Frajola)
✅ Tamanho: 45×45 pixels

✅ Posição inicial fixa no centro

✅ Velocidade: 6-12 pixels por frame (70% da velocidade do alvo)

✅ Movimento orientado ao alvo detectado

Sistema de Detecção
✅ Diferença de Quadros: Detecção baseada no histórico de movimento

✅ Limiarização Adaptativa: Detecção probabilística baseada em distância e velocidade

✅ Detecção por Centroides: Baseada em padrões de aceleração

✅ Indicador visual quando o alvo é detectado/perdido

Sistema de Perseguição
✅ Múltiplas estratégias implementadas

✅ Captura quando distância < 20 pixels

✅ Reinício automático após captura

Métricas e Análise
✅ Tempo até captura (em frames)

✅ Taxa de sucesso de captura

✅ Estatísticas de detecção (precisão, recall, F1-score)

🛠️ Tecnologias e Ferramentas Utilizadas
Linguagens e Bibliotecas
Python 3.7+

Pygame: Renderização gráfica e controle de eventos

NumPy: Cálculos matemáticos e vetoriais

OpenCV: Processamento de imagem (base para técnicas de detecção)

Métodos de Visão Computacional Implementados
Detecção de Movimento
python
# Técnica 1: Diferença de quadros
movement = np.sqrt((current_pos[0] - prev_pos[0])**2 + 
                  (current_pos[1] - prev_pos[1])**2)
Limiarização Adaptativa
python
# Técnica 2: Detecção baseada em distância e velocidade
visibility = min(1.0, target.speed / MAX_SPEED)
distance_factor = max(0, 1 - distance / (WIDTH / 2))
adaptive_threshold = BASE_THRESHOLD * (1 - visibility * 0.5) * distance_factor
Detecção por Centroides
python
# Técnica 3: Baseada em padrões de aceleração
v1 = np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]])
v2 = np.array([pos3[0] - pos2[0], pos3[1] - pos2[1]])
acceleration = np.linalg.norm(v2 - v1)
🎮 Estratégias de Perseguição Implementadas
1. Perseguição Direta (direct)
Movimento direto em direção à posição atual do alvo

Comportamento previsível e eficaz contra movimentos lineares

2. Interceptação Preditiva (intercept)
Tenta prever a posição futura do alvo

Move-se para "cortar o caminho" do alvo

Mais eficiente em trajetórias curvas

3. Navegação Proporcional (proportional)
Baseada em sistemas de mísseis reais

Ajustes constantes baseados na taxa de mudança da linha de visão

Mais adaptativa contra movimentos evasivos

📊 Métricas de Avaliação
Métricas Coletadas
Tempo médio de captura (em frames)

Taxa de captura (capturas por segundo)

Precisão de detecção (true positives / total detections)

Recall de detecção (true positives / actual targets)

F1-Score (média harmônica entre precisão e recall)

Análise Comparativa
O sistema permite comparar o desempenho das diferentes estratégias em diversos cenários, analisando:

Eficiência contra diferentes padrões de movimento

Estabilidade do sistema sob diferentes parâmetros

Tempos de resposta e taxa de sucesso

🏃‍♂️ Como Executar
Pré-requisitos

# Instalar dependências
Bash cd .\projeto_visao_computacional\
pip install -r requirements.txt

# Executar a simulação
python main.py
Controles
R: Reinício completo (zera estatísticas)

ESPAÇO: Pausar/despausar

1: Estratégia de Perseguição Direta

2: Estratégia de Interceptação Preditiva

3: Estratégia de Navegação Proporcional

T: Alternar rotação de sprites

ESC: Sair

🗂️ Estrutura do Projeto
projeto_visao_computacional/
├── main.py                 # Ponto de entrada da aplicação
├── config.py              # Configurações e parâmetros
├── agents.py              # Classes Target e Pursuer
├── detection.py           # Sistemas de detecção e métricas
├── simulation.py          # Lógica principal da simulação
├── sprites.py             # Gerenciamento de imagens
├── utils.py               # Funções auxiliares
├── requirements.txt       # Dependências do projeto
└── assets/               # Recursos visuais
    ├── ligeirinho.png    # Sprite do agente alvo
    └── frajola.png       # Sprite do agente perseguidor

🎯 Resultados e Conclusões
Descobertas Principais
Estratégias Situacionais: Cada estratégia mostrou-se mais eficaz em cenários específicos

Perseguição Direta: Melhor contra movimentos previsíveis

Interceptação: Mais eficiente em trajetórias longas e lineares

Navegação Proporcional: Superior contra movimentos evasivos

Importância da Detecção: A qualidade da detecção impacta diretamente na eficácia da perseguição

Trade-off Velocidade/Precisão: Estratégias mais complexas podem ter melhor desempenho mas maior custo computacional

Contribuições Técnicas
Implementação de múltiplas técnicas de detecção em tempo real

Desenvolvimento de diferentes estratégias de perseguição adaptativas

Sistema de métricas para avaliação comparativa

Interface visual intuitiva para análise dos resultados

🔮 Trabalhos Futuros
Melhorias Potenciais
Implementação de redes neurais para detecção mais precisa

Adição de obstáculos no ambiente para aumentar a complexidade

Desenvolvimento de estratégias híbridas adaptativas

Análise estatística mais aprofundada dos resultados

Implementação de aprendizado por reforço para otimização da perseguição

Expansões
Ambiente 3D para simulações mais realistas

Múltiplos agentes perseguidores e alvos

Integração com câmeras em tempo real para detecção

Sistema de registro de logs para análise offline

👥 Desenvolvido por
[Ricardo Lyra, Eduardo Silva e José Ailton]
Disciplina: Visão Computacional
Instituição: Faculdade Nova Roma
Data: 30/11/2025
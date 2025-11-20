## 🧠 HumanMate – Assistente Inteligente de Bem-Estar e Produtividade
Global Solution – FIAP 2025.2

*Nome do projeto*: HumanMate – Agente Inteligente de Produtividade e Bem-Estar.  
*Problema*: Pessoas sobrecarregadas, gestão ruim de tempo, falta de pausas, burnout.  
*Proposta*: Assistente inteligente que organiza tarefas, recomenda pausas, sugere prioridades e percebe sinais de cansaço — tudo 100% ético e privado.  

*Como será a POC*:
    - Protótipo de telas
- Agente rodando em Python
- Banco de dados na rede da FIAP
- Relatório de bem-estar
- Demonstração em vídeo

## Integrantes e funções

| Nome                                      | RM      | Função                   | Responsabilidades Principais                                                                                                                                                                         |
|-------------------------------------------|---------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Pedro Henrique Lopes dos Santos**       | RM568359| **Tech Lead**             | Liderança técnica geral; definição da arquitetura do sistema; integração entre módulos (IA, ML, NN, BD, Cloud); coordenação da POC; organização do repositório; revisão técnica e validação final.   |
| **Fabrício Mouzer Brito**                 | RM566777| **Engenheiro de Requisitos** | Levantamento de requisitos; documentação funcional e não funcional; criação de user stories; definição de regras de negócio; desenho dos fluxos de usuário; apoio na prototipação e documentação.      |
| **Enzo Nunes Castanheira Gloria da Silva**| RM567599| **Engenheiro de Software**| Desenvolvimento das interfaces do protótipo navegável; estruturação dos fluxos de interação; criação dos componentes visuais; testes de usabilidade; integração com endpoints mockados.                |
| **Larissa Nunes Moreira Reis**            | RM568280| **Cientista de Dados**    | Criação e preparação do dataset; tratamento e análise dos dados; implementação dos modelos de Machine Learning; criação de gráficos em R; apoio na Rede Neural para classificação de humor.            |
| **Gabriel Rapozo Guimarães Soares**       | RM568480| **Engenheiro de Software**| Estruturação do backend da POC (mesmo simulado); criação de endpoints mockados; modelagem do banco de dados; implementação do modelo lógico/físico; apoio na infraestrutura em nuvem e boas práticas. |

## 📌 1. Introdução

O futuro do trabalho exige que as organizações cuidem não apenas da produtividade, mas também do bem-estar físico e emocional de seus profissionais. A expansão do trabalho digital, dos modelos híbridos e da pressão por resultados eleva o risco de estresse, fadiga mental e burnout.

Nesse cenário, o HumanMate surge como um assistente inteligente de bem-estar e produtividade, projetado para monitorar, analisar e prever como cada profissional está se sentindo ao longo do tempo.

A POC integra:

- IA, Machine Learning e Redes Neurais 
- Coleta ativa (questionários)
- Coleta passiva (métricas via agente inteligente)
- Banco de dados Oracle 
- Análises preditivas 
- Relatórios de insights

Seu objetivo é demonstrar como a tecnologia pode tornar o trabalho mais humano, inclusivo e sustentável, oferecendo suporte direto à saúde mental e desempenho individual.

## ⚙️ 2. Desenvolvimento
### 2.1. Visão geral da solução

A arquitetura do HumanMate funciona em três eixos principais:

#### 🔸 1. Coleta de dados subjetivos

O usuário responde diariamente a perguntas sobre:

- Humor 
- Energia (1 a 5)
- Estresse (1 a 5)
- Sensação de sobrecarga 
- Qualidade do sono 
- Horas produtivas

#### 🔸 2. Coleta de dados objetivos

O HumanMate Agent (simulado nesta POC) registra automaticamente:

- Velocidade de digitação (ppm)
- Tempo total de pausas 
- Tempo de tela ligada 
- Tempo de interação 
- Tempo usando o mouse

Esses dados geram uma visão mais completa do comportamento digital.

#### 🔸 3. Análises inteligentes

A solução calcula:

- Índice de Bem-Estar (IBE)
- Classificação de humor (Rede Neural)
- Predição de risco de sobrecarga (Machine Learning)
- Correlações entre métricas e humor

E produz:

- Relatórios gráficos 
- Insights automáticos

## 🏗️ 2.2. Arquitetura da Solução


## 🧪 2.3. Fluxo do MVP no terminal

- Cadastro
- Login
- Responder Perguntas Diárias
- Agente registra métricas automaticamente
- Dados salvos no banco
- Usuário visualiza histórico consolidado
- Geração de relatórios + insights

## 🧷 2.4. Justificativas técnicas (por disciplina)

Disciplina	Aplicação
Python	Motor principal da POC, controle de fluxo, cálculos e IA.
Banco de Dados	Oracle persiste usuários, diários e métricas.
Machine Learning	Predição de risco de sobrecarga.
Redes Neurais	Classificação automática de humor.
Cybersecurity	Fluxo com autenticação e separação de sessões.
Cloud Computing	Arquitetura desenhada para rodar 100% na nuvem.
AICSS	Conceito de agente inteligente monitorando padrões.
Formação Social	Foco em prevenção de burnout e bem-estar.

## 🧩 2.5. Códigos principais comentados
#### 🔹 Cadastro de Usuário (Oracle)

```
cursor.execute("SELECT 1 FROM USUARIOS WHERE EMAIL = :email", {"email": email})
if cursor.fetchone():
    print("⚠️ Já existe um usuário cadastrado com esse email.")
    return None
```

#### 🔹 Registro das Perguntas Diárias
```
registro = {
    "email": usuario["email"],
    "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "humor": humor,
    "foco_horas": float(foco_horas),
    "sobrecarga": sobrecarga,
    "dormiu_bem": dormiu_bem,
    "energia": energia,
    "estresse": estresse,
}
```

#### 🔹 Agente Inteligente – Métricas Automáticas
```
velocidade_digitacao = random.randint(150, 350)
tempo_pausa = random.randint(60, 900)
tempo_tela_ligada = random.randint(3600, 28800)
```

#### 🔹 Cálculo do Índice de Bem-Estar (IBE)
```
indice = (
    humor_score * 0.30 +
    energia_score * 0.20 +
    estresse_score * 0.20 +
    pausas_score * 0.10 +
    tela_score * 0.10 +
    mouse_score * 0.10
)
```

## 🎯 3. Resultados Esperados

O HumanMate cria uma base sólida para monitorar e compreender o bem-estar do usuário a partir de dados reais. A solução permite identificar sinais precoces de burnout, mapear hábitos nocivos e oferecer insights claros sobre produtividade e saúde mental.

Espera-se alcançar:

- Acompanhamento contínuo do bem-estar, unindo dados subjetivos (humor, estresse, energia) a métricas comportamentais.
- Redução do risco de burnout, ao detectar padrões como excesso de tela, poucas pausas e ciclos de estresse.
- Insights práticos sobre comportamento digital, revelando como ritmo de trabalho e interações impactam o estado emocional.
- Relatórios e gráficos correlacionando variáveis-chave, como:
    - humor × pausas
    - energia × tempo de tela
    - estresse × interação
- Escalabilidade natural para web/mobile e preparo para evoluir em direção a um SaaS corporativo de saúde mental.

A POC confirmou:

- Integração total entre banco de dados, Python e IA.
- Combinação eficiente de dados objetivos + subjetivos, gerando diagnósticos consistentes.
- Arquitetura pronta para crescimento, com potencial direto para ambientes empresariais.

## 🧭 4. Conclusões

O HumanMate demonstra, de forma clara, como a tecnologia pode ser usada para tornar o trabalho mais humano, saudável e sustentável. A solução evidencia que é possível unir inteligência artificial, análise de comportamento e dados reais para promover uma rotina mais equilibrada e consciente.

A plataforma reforça três pilares essenciais: mais humanidade, ao priorizar o cuidado ativo com saúde mental; mais inclusão, ao oferecer insights realmente personalizados; e mais sustentabilidade, ao atuar de forma preventiva, evitando que pequenos sinais evoluam para problemas maiores.

A POC valida integralmente os requisitos propostos pela Global Solution — desde o uso de IA, modelos de machine learning e redes neurais, até a integração com Banco Oracle, coleta de dados reais ou simulados, lógica de aplicação e geração de relatórios completos. Esse conjunto de entregas confirma a maturidade da abordagem adotada e estabelece um caminho concreto para evoluir do MVP atual para um produto funcional, escalável e pronto para ambientes corporativos.

# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

**Fase 3 - Global Solution**

**Tecnólogo em Inteligência Artificial - FIAP**

*"Democratizando o acesso à informação educacional através da IA"*

---




## 👥 Informações do Projeto

👨‍🎓 Integrantes:
| Nome | RM | E-mail |
|------|-----|--------|
| **Fabrício Mouzer Brito** | RM566777 | fabriciomouzer@hotmail.com |
| **Pedro Henrique Lopes dos Santos** | RM568359 | pedrolopeshls99@gmail.com |
| **Enzo Nunes Castanheira Gloria da Silva** | RM567599 | enzoncgs@gmail.com |
| **Larissa Nunes Moreira Reis** | RM568280 | larissa.nmreis@gmail.com |
| **Gabriel Rapozo Guimarães Soares** | RM568480 | rapozogabriel8@gmail.com |


## 📜 Descrição
*Para essa etapa do trabalho foi elaborado um banco de dados com as informações obtidas a partir de 200 observações provenientes de testes do app desenvolvido. Posteriormente, utilizou-se esse banco de dados como fonte para realização de análises descritivas e regressão logísticas, a partir da elaborção de script no software R*

## 🔧 Dicionário do banco de dados
| Variável (Nome Completo) | Coluna (Nome Curto) | Tipo de Dado | Descrição/Observações |
| :--- | :--- | :--- | :--- |
| Idade | IDADE | Numérico/Inteiro | Idade do indivíduo. |
| Nível de Energia | ENERGIA | Numérico/Inteiro | Nível de energia percebido (escala de 1 a 5, por exemplo). |
| Nível de Estresse | ESTRESSE | Numérico/Inteiro | Nível de estresse percebido (escala de 1 a 5, por exemplo). |
| Velocidade de digitação | VELDIGITACAO | Numérico/Inteiro | Velocidade de digitação. |
| Tempo de pausa | TEMPOPAUSA | Numérico/Inteiro | Tempo total de pausas. |
| Tempo de tela ligada | TEMPOTELALIGADA | Numérico/Inteiro | Tempo total com a tela ligada (em segundos ou minutos). |
| Tempo de interação | TEMPOINTERACAO | Numérico/Inteiro | Tempo total de interação (em segundos ou minutos). |
| Utilização do mouse | TEMPOMOUSE | Numérico/Inteiro | Uso do mouse (palavras por minuto). |
| Sexo | SEXO | Categórico/Fator | Gênero do indivíduo (e.g., F, M). |
| Número de horas dormidas | HRSDORMIDAS | Categórico/Fator | Horas dormidas na última noite (e.g., "menos de 5 horas", "5 horas ou mais"). |
| Número de horas trabalhadas | HRSTRABALHADAS | Categórico/Fator | Horas trabalhadas no dia anterior (e.g., "8 horas ou menos", "mais de 8 horas"). |
| Tipo de tarefas realizadas | TPTAREFAS | Categórico/Fator | Tipo de tarefas realizadas (e.g., "domésticas", "laborais", "pessoais"). |
| Humor | HUMOR | Categórico/Fator | Estado de humor percebido (e.g., "Muito bom", "Bom", "Neutro", "Ruim", "Muito ruim"). |
| Sobrecarga | SOBRECARGA | Categórico/Binário | Indica se o indivíduo se sente sobrecarregado (e.g., "Sim", "Não"). |
| Sono de qualidade | QUALSONO | Categórico/Binário | Indica se o indivíduo teve um sono de qualidade (e.g., "Sim", "Não"). |

## 🔧 Script
```
Script R para Análise Descritiva e Regressão Logística

- Objetivo: Realizar a análise descritiva do banco de dados e, em seguida,executar uma Regressão Logística para avaliar a probabilidade de Sobrecarga em função do Estresse.

1. Carregamento de Pacotes
library(readr)
library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)

2. Carregamento dos Dados
dados <- read_csv("banco.csv", 
                  col_types = cols(
                    SEXO = readr::col_factor(levels = c("F", "M")),
                    DTNASC = readr::col_date(format = "%d/%m/%Y"),
                    IDADE = readr::col_integer(),
                    HRSDORMIDAS = readr::col_factor(levels = c("menos de 5 horas", "5 horas ou mais")),
                    HRSTRABALHADAS = readr::col_factor(levels = c("8 horas ou menos", "mais de 8 horas")),
                    TPTAREFAS = readr::col_factor(levels = c("domésticas", "laborais", "pessoais")),
                    HUMOR = readr::col_factor(levels = c("Muito bom", "Bom", "Neutro", "Ruim", "Muito ruim")),
                    SOBRECARGA = readr::col_factor(levels = c("Sim", "Não")),
                    QUALSONO = readr::col_factor(levels = c("Sim", "Não")),
                    ENERGIA = readr::col_integer(),
                    ESTRESSE = readr::col_integer(),
                    VELDIGITACAO = readr::col_integer(),
                    TEMPOPAUSA = readr::col_integer(),
                    TEMPOTELALIGADA = readr::col_integer(),
                    TEMPOINTERACAO = readr::col_integer(),
                    TEMPOMOUSE = readr::col_integer()
                  ))


PARTE 1: ANÁLISE DESCRITIVA

A. Resumo Estatístico para Variáveis Quantitativas
quantitativas <- dados %>%
  select(IDADE, ENERGIA, ESTRESSE, VELDIGITACAO, TEMPOPAUSA, TEMPOTELALIGADA, TEMPOINTERACAO, TEMPOMOUSE)

cat("\n--- Resumo Estatístico das Variáveis Quantitativas ---\n")
print(summary(quantitativas))

Adicionar Desvio Padrão
cat("\n--- Desvio Padrão das Variáveis Quantitativas ---\n")
quantitativas %>%
  summarise(across(everything(), sd)) %>%
  print()

B. Tabela de Frequência e Proporção para Variáveis Categóricas
Função para gerar tabela de frequência
tabela_frequencia <- function(variavel) {
  tabela <- dados %>%
    count({{ variavel }}) %>%
    mutate(Proporcao = n / sum(n),
           Proporcao_Perc = paste0(round(Proporcao * 100, 2), "%"))
  return(tabela)
}

cat("\n--- Tabela de Frequência: SEXO ---\n")
print(tabela_frequencia(SEXO))

cat("\n--- Tabela de Frequência: HRSDORMIDAS ---\n")
print(tabela_frequencia(HRSDORMIDAS))

cat("\n--- Tabela de Frequência: HRSTRABALHADAS ---\n")
print(tabela_frequencia(HRSTRABALHADAS))

cat("\n--- Tabela de Frequência: TPTAREFAS ---\n")
print(tabela_frequencia(TPTAREFAS))

cat("\n--- Tabela de Frequência: HUMOR ---\n")
print(tabela_frequencia(HUMOR))

cat("\n--- Tabela de Frequência: SOBRECARGA ---\n")
print(tabela_frequencia(SOBRECARGA))

cat("\n--- Tabela de Frequência: QUALSONO ---\n")
print(tabela_frequencia(QUALSONO))


C. Visualização Gráfica Descritiva

Histograma para Variáveis Quantitativas
quantitativas_long <- quantitativas %>%
  pivot_longer(cols = everything(), names_to = "Variavel", values_to = "Valor")

grafico_quantitativas <- quantitativas_long %>%
  ggplot(aes(x = Valor)) +
  geom_histogram(bins = 15, fill = "skyblue", color = "black") +
  facet_wrap(~ Variavel, scales = "free") +
  labs(title = "Distribuição de Frequência das Variáveis Quantitativas",
       x = "Valor",
       y = "Frequência") +
  theme_minimal() +
  theme(strip.text = element_text(face = "bold"))

ggsave("grafico_descritivo_quantitativas.png", plot = grafico_quantitativas, width = 12, height = 8)


Função para gerar e salvar gráficos de barras
gerar_grafico_barras <- function(variavel, titulo) {
  grafico <- dados %>%
    ggplot(aes(x = {{ variavel }}, fill = {{ variavel }})) +
    geom_bar() +
    labs(title = titulo,
         x = "",
         y = "Contagem") +
    theme_minimal() +
    theme(legend.position = "none",
          axis.text.x = element_text(angle = 45, hjust = 1))
  
  nome_arquivo <- paste0("grafico_descritivo_", deparse(substitute(variavel)), ".png")
  ggsave(nome_arquivo, plot = grafico, width = 8, height = 6)
}

Geração dos gráficos de barras
gerar_grafico_barras(SEXO, "Distribuição de Frequência por Sexo")
gerar_grafico_barras(HRSDORMIDAS, "Distribuição de Horas Dormidas na Última Noite")
gerar_grafico_barras(HRSTRABALHADAS, "Distribuição de Horas Trabalhadas no Dia Anterior")
gerar_grafico_barras(TPTAREFAS, "Distribuição por Tipo de Tarefas")
gerar_grafico_barras(HUMOR, "Distribuição de Humor")
gerar_grafico_barras(SOBRECARGA, "Distribuição de Sobrecarga")
gerar_grafico_barras(QUALSONO, "Distribuição de Qualidade do Sono")
gerar_grafico_barras(ENERGIA, "Distribuição de Nível de Energia")
gerar_grafico_barras(ESTRESSE, "Distribuição de Nível de Estresse")


PARTE 2: REGRESSÃO LOGÍSTICA (SOBRECARGA ~ ESTRESSE)


cat("\n\n==================================================================")
cat("\nPARTE 2: REGRESSÃO LOGÍSTICA (SOBRECARGA ~ ESTRESSE)")
cat("\n==================================================================\n")

1. Preparação dos Dados para Regressão Logística
A Regressão Logística requer que a variável dependente binária seja convertida para 0 e 1.
Vamos definir 'Sim' (Sobrecarga) como 1 e 'Não' como 0.
dados_reg <- dados %>%
  mutate(SOBRECARGA_BIN = if_else(SOBRECARGA == "Sim", 1, 0))

2. Execução da Regressão Logística
Modelo: SOBRECARGA_BIN em função de ESTRESSE
modelo_logistico <- glm(SOBRECARGA_BIN ~ ESTRESSE, 
                        data = dados_reg, 
                        family = binomial(link = "logit"))

cat("\n--- Resultados da Regressão Logística (SOBRECARGA ~ ESTRESSE) ---\n")
print(summary(modelo_logistico))

3. Interpretação dos Coeficientes (Odds Ratio)
cat("\n--- Odds Ratio (Razão de Chances) ---\n")
print(exp(coef(modelo_logistico)))

4. Geração do Gráfico de Probabilidade

Criar uma nova coluna com as probabilidades previstas pelo modelo
dados_reg <- dados_reg %>%
  mutate(PROBABILIDADE_SOBRECARGA = predict(modelo_logistico, type = "response"))

Gráfico de dispersão com a curva de probabilidade logística
grafico_regressao <- dados_reg %>%
  ggplot(aes(x = ESTRESSE, y = PROBABILIDADE_SOBRECARGA)) 
  
Adiciona os pontos de dados (jitter para melhor visualização)
  geom_point(aes(y = SOBRECARGA_BIN), 
             position = position_jitter(height = 0.02, width = 0.1), 
             alpha = 0.5, 
             color = "gray50") +
Adiciona a curva de probabilidade prevista
  geom_smooth(method = "glm", 
              method.args = list(family = "binomial"), 
              se = TRUE, 
              color = "blue") +
  labs(title = "Probabilidade de Sobrecarga em Função do Nível de Estresse",
       x = "Nível de Estresse (1 a 5)",
       y = "Probabilidade de Sobrecarga (Sim)") +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal()

Salvar o gráfico
ggsave("grafico_regressao_logistica_sobrecarga.png", plot = grafico_regressao, width = 10, height = 6)

```

## Análise Estatística em R

Esta seção apresenta os resultados da análise estatística realizada com o script `analise_completa.R` e a base de dados `banco.csv`.

### 1. Análise Descritiva

#### 1.1. Resumo Estatístico das Variáveis Quantitativas

| Variável | Mínimo | 1º Quartil | Mediana | Média | 3º Quartil | Máximo | Desvio Padrão |
|---|---|---|---|---|---|---|---|
| **IDADE** | 18.00 | 36.75 | 57.00 | 56.98 | 75.00 | 99.00 | 23.2 |
| **ENERGIA** | 1.000 | 2.000 | 3.000 | 2.945 | 4.000 | 5.000 | 1.40 |
| **ESTRESSE** | 1.000 | 2.000 | 3.000 | 3.135 | 4.000 | 5.000 | 1.43 |
| **VELDIGITACAO** | 1.000 | 3.000 | 5.000 | 4.975 | 7.000 | 10.000 | 2.72 |
| **TEMPOPAUSA** | 10.0 | 91.5 | 165.5 | 166.3 | 243.5 | 299.0 | 84.1 |
| **TEMPOTELALIGADA** | 1 | 2544 | 5074 | 4972 | 7324 | 9850 | 2900 |
| **TEMPOINTERACAO** | 15 | 2946 | 5421 | 5236 | 7600 | 9914 | 2868 |
| **TEMPOMOUSE** | 47 | 2671 | 4783 | 5032 | 7710 | 10000 | 2900 |

#### 1.2. Distribuição de Frequência das Variáveis Categóricas

| Variável | Categoria | Contagem (n) | Proporção (%) |
|---|---|---|---|
| **SEXO** | F | 111 | 55.5% |
| | M | 89 | 44.5% |
| **HRSDORMIDAS** | menos de 5 horas | 97 | 48.5% |
| | 5 horas ou mais | 103 | 51.5% |
| **HRSTRABALHADAS** | 8 horas ou menos | 94 | 47.0% |
| | mais de 8 horas | 106 | 53.0% |
| **TPTAREFAS** | domésticas | 71 | 35.5% |
| | laborais | 79 | 39.5% |
| | pessoais | 50 | 25.0% |
| **HUMOR** | Muito bom | 40 | 20.0% |
| | Bom | 37 | 18.5% |
| | Neutro | 35 | 17.5% |
| | Ruim | 39 | 19.5% |
| | Muito ruim | 49 | 24.5% |
| **SOBRECARGA** | Sim | 105 | 52.5% |
| | Não | 95 | 47.5% |
| **QUALSONO** | Sim | 104 | 52.0% |
| | Não | 96 | 48.0% |

#### 1.3. Visualização Gráfica Descritiva

Os gráficos de distribuição de frequência para as variáveis quantitativas e categóricas foram gerados e estão anexados ao resultado final.
<img width="2400" height="1800" alt="grafico_descritivo_ENERGIA" src="https://github.com/user-attachments/assets/037d29d6-54df-4dd4-b7a4-3f6a911fc7a5" />
<img width="2400" height="1800" alt="grafico_descritivo_ESTRESSE" src="https://github.com/user-attachments/assets/e1babbed-af09-48a4-a562-d2bd667f1072" />
<img width="2400" height="1800" alt="grafico_descritivo_HRSDORMIDAS" src="https://github.com/user-attachments/assets/49912625-2462-4c97-a561-12af336c5ea0" />
<img width="2400" height="1800" alt="grafico_descritivo_HRSTRABALHADAS" src="https://github.com/user-attachments/assets/79fed9ce-133f-49e4-8b2f-ff0651928b7f" />
<img width="2400" height="1800" alt="grafico_descritivo_HUMOR" src="https://github.com/user-attachments/assets/6f74014e-994d-473f-b471-20d65223b852" />
<img width="2400" height="1800" alt="grafico_descritivo_QUALSONO" src="https://github.com/user-attachments/assets/638aa221-3599-42bc-a423-346ca7b99c65" />
<img width="3600" height="2400" alt="grafico_descritivo_quantitativas" src="https://github.com/user-attachments/assets/4e6a29e5-7b1d-45b3-b303-fe5043bf91d7" />
<img width="2400" height="1800" alt="grafico_descritivo_SEXO" src="https://github.com/user-attachments/assets/b6c28c8f-ac43-4042-bb3c-d317049e6727" />
<img width="2400" height="1800" alt="grafico_descritivo_SOBRECARGA" src="https://github.com/user-attachments/assets/2268cfd2-aa6f-45a8-97fc-3c01658670df" />
<img width="2400" height="1800" alt="grafico_descritivo_TPTAREFAS" src="https://github.com/user-attachments/assets/95387769-a4aa-4f2d-aadc-9fb145013b81" />


### 2. Regressão Logística (SOBRECARGA ~ ESTRESSE)

O modelo de Regressão Logística foi ajustado para avaliar a probabilidade de **Sobrecarga** em função do nível de **Estresse**.

#### 2.1. Resultados do Modelo
Call:
glm(formula = SOBRECARGA_BIN ~ ESTRESSE, family = binomial(link = "logit"), 
    data = dados_reg)

Deviance Residuals: 
   Min      1Q  Median      3Q     Max  
-1.305  -1.226   1.055   1.130   1.207  

Coefficients:
            Estimate Std. Error z value Pr(>|z|)
(Intercept)  0.38586    0.34460   1.120    0.263
ESTRESSE    -0.09102    0.09986  -0.911    0.362

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 276.76  on 199  degrees of freedom
Residual deviance: 275.92  on 198  degrees of freedom
AIC: 279.92

Number of Fisher Scoring iterations: 3

2.2. Interpretação dos Coeficientes (Odds Ratio)

| Variável | Odds Ratio (Razão de Chances) |
|---|---|
| **(Intercept)** | 1.4708768 |
| **ESTRESSE** | 0.9130031 |

O Odds Ratio de 0.913 para a variável **ESTRESSE** (com p-valor de 0.362) sugere que, para cada aumento de uma unidade no nível de estresse, a chance de ter Sobrecarga é multiplicada por 0.913. Como o valor é próximo de 1 e o p-valor é alto, a relação não é estatisticamente significativa neste modelo.

2.3. Gráfico de Probabilidade

O gráfico de dispersão com a curva de probabilidade logística foi gerado e está anexado ao resultado final.
<img width="3000" height="1800" alt="grafico_regressao_logistica_sobrecarga" src="https://github.com/user-attachments/assets/2402a846-29eb-4863-8ca8-de95b7014432" />


```
🗃 Histórico de lançamentos
1.0 - 10/11/2025
2.0 - 19/11/2025 (Inclusão da Análise Estatística em R)

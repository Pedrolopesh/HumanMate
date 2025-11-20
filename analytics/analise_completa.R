# Script R para Análise Descritiva e Regressão Logística

# Objetivo: Realizar a análise descritiva do banco de dados e, em seguida,executar uma Regressão Logística para avaliar a probabilidade de Sobrecarga em função do Estresse.

# 1. Carregamento de Pacotes)

library(readr)
library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)

# 2. Carregamento dos Dados
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

# ==============================================================================
# PARTE 1: ANÁLISE DESCRITIVA
# ==============================================================================

# A. Resumo Estatístico para Variáveis Quantitativas
quantitativas <- dados %>%
  select(IDADE, ENERGIA, ESTRESSE, VELDIGITACAO, TEMPOPAUSA, TEMPOTELALIGADA, TEMPOINTERACAO, TEMPOMOUSE)

cat("\n--- Resumo Estatístico das Variáveis Quantitativas ---\n")
print(summary(quantitativas))

# Adicionar Desvio Padrão
cat("\n--- Desvio Padrão das Variáveis Quantitativas ---\n")
quantitativas %>%
  summarise(across(everything(), sd)) %>%
  print()

# B. Tabela de Frequência e Proporção para Variáveis Categóricas

# Função para gerar tabela de frequência
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


# C. Visualização Gráfica Descritiva

# Histograma para Variáveis Quantitativas
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


# Função para gerar e salvar gráficos de barras
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

# Geração dos gráficos de barras
gerar_grafico_barras(SEXO, "Distribuição de Frequência por Sexo")
gerar_grafico_barras(HRSDORMIDAS, "Distribuição de Horas Dormidas na Última Noite")
gerar_grafico_barras(HRSTRABALHADAS, "Distribuição de Horas Trabalhadas no Dia Anterior")
gerar_grafico_barras(TPTAREFAS, "Distribuição por Tipo de Tarefas")
gerar_grafico_barras(HUMOR, "Distribuição de Humor")
gerar_grafico_barras(SOBRECARGA, "Distribuição de Sobrecarga")
gerar_grafico_barras(QUALSONO, "Distribuição de Qualidade do Sono")
gerar_grafico_barras(ENERGIA, "Distribuição de Nível de Energia")
gerar_grafico_barras(ESTRESSE, "Distribuição de Nível de Estresse")


# ==============================================================================
# PARTE 2: REGRESSÃO LOGÍSTICA (SOBRECARGA ~ ESTRESSE)
# ==============================================================================

cat("\n\n==================================================================")
cat("\nPARTE 2: REGRESSÃO LOGÍSTICA (SOBRECARGA ~ ESTRESSE)")
cat("\n==================================================================\n")

# 1. Preparação dos Dados para Regressão Logística
# A Regressão Logística requer que a variável dependente binária seja convertida para 0 e 1.
# Vamos definir 'Sim' (Sobrecarga) como 1 e 'Não' como 0.
dados_reg <- dados %>%
  mutate(SOBRECARGA_BIN = if_else(SOBRECARGA == "Sim", 1, 0))

# 2. Execução da Regressão Logística
# Modelo: SOBRECARGA_BIN em função de ESTRESSE
modelo_logistico <- glm(SOBRECARGA_BIN ~ ESTRESSE, 
                        data = dados_reg, 
                        family = binomial(link = "logit"))

cat("\n--- Resultados da Regressão Logística (SOBRECARGA ~ ESTRESSE) ---\n")
print(summary(modelo_logistico))

# 3. Interpretação dos Coeficientes (Odds Ratio)
cat("\n--- Odds Ratio (Razão de Chances) ---\n")
print(exp(coef(modelo_logistico)))

# 4. Geração do Gráfico de Probabilidade

# Criar uma nova coluna com as probabilidades previstas pelo modelo
dados_reg <- dados_reg %>%
  mutate(PROBABILIDADE_SOBRECARGA = predict(modelo_logistico, type = "response"))

# Gráfico de dispersão com a curva de probabilidade logística
grafico_regressao <- dados_reg %>%
  ggplot(aes(x = ESTRESSE, y = PROBABILIDADE_SOBRECARGA)) +
  # Adiciona os pontos de dados (jitter para melhor visualização)
  geom_point(aes(y = SOBRECARGA_BIN), 
             position = position_jitter(height = 0.02, width = 0.1), 
             alpha = 0.5, 
             color = "gray50") +
  # Adiciona a curva de probabilidade prevista
  geom_smooth(method = "glm", 
              method.args = list(family = "binomial"), 
              se = TRUE, 
              color = "blue") +
  labs(title = "Probabilidade de Sobrecarga em Função do Nível de Estresse",
       x = "Nível de Estresse (1 a 5)",
       y = "Probabilidade de Sobrecarga (Sim)") +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal()

# Salvar o gráfico
ggsave("grafico_regressao_logistica_sobrecarga.png", plot = grafico_regressao, width = 10, height = 6)

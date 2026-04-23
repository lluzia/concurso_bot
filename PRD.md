
# PRD (Product Requirements Document)

## 📑 PRD - Concursos Bot Brasil

## 📌 Objetivo

Criar um sistema automatizado para monitoramento de concursos públicos no Brasil, com filtragem por regiões e envio de notificações por email.

---

## 🎯 Problema

Usuários precisam acompanhar múltiplos sites de concursos manualmente, o que é:
- demorado
- inconsistente
- sujeito a perda de oportunidades

---

## 💡 Solução

Um bot automatizado que:
- coleta dados de sites de concursos
- filtra por região
- remove duplicados
- envia resumo por email

---

## 🧱 Escopo MVP (atual)

### Funcionalidades implementadas
- Scraping do PCI Concursos
- Filtro por região (Sudeste, Sul, Centro-Oeste, Nordeste)
- Agrupamento por UF
- Email HTML formatado
- Deduplicação
- Execução via GitHub Actions

---

## 📈 Métricas de sucesso

- ≥ 95% de execução sem falhas
- 0 duplicações por ciclo
- entrega semanal consistente

---

## 🚀 Roadmap futuro

### Fase 2
- Selenium para sites protegidos (JC Concursos)
- Integração com mais fontes

### Fase 3
- Banco de dados (SQLite/Postgres)
- API própria

### Fase 4
- Dashboard web (Streamlit)
- filtros personalizados por usuário

### Fase 5
- Notificações alternativas (Telegram / WhatsApp)
- alertas em tempo real

---

## ⚠️ Riscos

- Mudança de HTML em sites de scraping
- bloqueios anti-bot (Cloudflare)
- dependência de fontes externas

---

## 🛠️ Mitigações

- retry automático
- fallback entre fontes
- modularização de scrapers
- futura migração para Selenium onde necessário
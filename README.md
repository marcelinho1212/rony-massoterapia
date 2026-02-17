# Sistema de Agendamento Online para Massoterapia

Sistema web desenvolvido em Django para agendamento online de sessões de massoterapia, com fluxo completo de escolha de profissional, serviço, data, horário e confirmação via WhatsApp.

O projeto foi pensado para uso real, com foco em robustez da agenda, organização de domínio e boas práticas de desenvolvimento.

---

## 🎯 Objetivo do Projeto

Permitir que clientes realizem agendamentos de forma simples e intuitiva, enquanto os profissionais gerenciam serviços, disponibilidade e horários por meio do Django Admin, sem necessidade de contato manual prévio.

---

## 🚀 Funcionalidades

### Área Administrativa (Django Admin)
- Cadastro e gerenciamento de profissionais
- Cadastro de serviços com preço e duração
- Definição de disponibilidade semanal por profissional
- Visualização e controle de agendamentos
- Ativação e desativação de profissionais e serviços

### Fluxo Público de Agendamento
- Página inicial com chamada para agendamento
- Escolha do profissional
- Listagem de serviços vinculados ao profissional
- Seleção de data
- Geração dinâmica de horários disponíveis
- Preenchimento dos dados do cliente (nome e WhatsApp)
- Confirmação do agendamento

### Regras de Negócio
- Impede seleção de horários fora da disponibilidade configurada
- Bloqueia horários passados
- Evita conflitos com outros agendamentos
- Controle de concorrência para evitar overbooking

---

## 🔒 Robustez da Agenda

O sistema utiliza:
- Validação de conflitos na geração dos horários
- Validação adicional no momento da confirmação
- Transações atômicas (`transaction.atomic`)
- Bloqueio de concorrência com `select_for_update`

Essa abordagem garante que dois usuários não consigam reservar o mesmo horário simultaneamente.

---

## 📲 Integração com WhatsApp

Após a confirmação do agendamento:
- Um registro é criado no banco de dados
- O usuário é redirecionado automaticamente para o WhatsApp do profissional
- A mensagem já vem pré-preenchida com:
  - profissional
  - serviço
  - data e horário
  - nome do cliente
  - WhatsApp do cliente

> O envio final da mensagem depende da ação do usuário, respeitando as limitações oficiais do WhatsApp.

---

## 🧱 Stack Utilizada

- Python
- Django
- PostgreSQL
- Bootstrap (templates server-side)
- psycopg
- python-dotenv

---

## 📁 Estrutura do Projeto

- `core` – páginas públicas e fluxo de agendamento
- `professionals` – profissionais
- `services` – serviços
- `schedule` – disponibilidade semanal
- `bookings` – agendamentos
- `notifications` – notificações (WhatsApp)

---

## ⚙️ Como Executar Localmente (Windows)

### Pré-requisitos
- Python 3.12+
- PostgreSQL 14+
- pgAdmin (opcional)

### Passo a passo

```bash
# Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo de variáveis de ambiente
copy .env.example .env
# Edite o .env com suas credenciais

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
Acesse:

Aplicação: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

🧪 Estado Atual do Projeto
Backend estruturado e funcional

PostgreSQL configurado desde o início

Models migrados

Admin funcional

Agenda baseada em disponibilidade real

Controle de concorrência implementado

Interface com Bootstrap

Integração com WhatsApp funcionando

📌 Roadmap
Tela de confirmação visual após o agendamento

Cancelamento e remarcação de horários

Janela de agendamento configurável (ex: até 30 dias)

Deploy em ambiente de produção com HTTPS
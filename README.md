Sistema de Agendamento Online para Massoterapia

Sistema web de agendamento online desenvolvido com Django e PostgreSQL, focado em profissionais de massoterapia.
Permite que clientes escolham profissional, serviço, data e horário disponível, com confirmação via WhatsApp.

Projeto desenvolvido com foco em arquitetura limpa, boas práticas, robustez de agenda e portfólio profissional.

🚀 Funcionalidades

Página pública de agendamento

Escolha de profissional

Serviços filtrados por profissional

Agenda baseada em disponibilidade semanal real

Geração dinâmica de horários disponíveis

Prevenção de conflitos de horário

Bloqueio de horários passados

Registro de agendamentos no banco de dados

Confirmação via WhatsApp com mensagem pré-preenchida

Painel administrativo completo via Django Admin

🧱 Arquitetura do Projeto

O sistema foi estruturado seguindo o padrão Django Apps, separando responsabilidades por domínio:

rony-massoterapia/
├── core/           # Páginas públicas e fluxo de agendamento
├── professionals/  # Profissionais
├── services/       # Serviços oferecidos
├── schedule/       # Disponibilidade semanal
├── bookings/       # Agendamentos
├── notifications/  # Integrações (WhatsApp)
├── config/         # Configurações globais


Essa separação facilita manutenção, escalabilidade e evolução do sistema.

🧩 Modelagem de Dados (Resumo)
Professional

Nome

Slug

WhatsApp

Status ativo/inativo

Service

Nome

Preço (em centavos)

Duração (minutos)

Relação com profissionais (ManyToMany)

Status ativo/inativo

WeeklyAvailability

Profissional

Dia da semana

Horário de início

Horário de término

Booking

Profissional

Serviço

Data/hora de início

Data/hora de término

Nome do cliente

WhatsApp do cliente

Status (pending, confirmed)

Data de criação

🔄 Fluxo de Agendamento

Página inicial

Escolha do profissional

Escolha do serviço

Escolha da data

Visualização dos horários disponíveis

Preenchimento dos dados do cliente

Confirmação do agendamento

Redirecionamento para WhatsApp do profissional

O sistema impede:

conflitos de horário

seleção de horários fora da disponibilidade

agendamentos em horários passados

💬 Integração com WhatsApp

Após a confirmação do agendamento, o sistema redireciona para o WhatsApp do profissional com uma mensagem automática contendo:

Profissional escolhido

Serviço

Data e horário

Nome do cliente

WhatsApp do cliente

⚠️ O envio respeita as limitações oficiais do WhatsApp, exigindo interação do usuário.

🛠️ Tecnologias Utilizadas

Python 3.12

Django

PostgreSQL

psycopg

Bootstrap

HTML + CSS

WhatsApp Web (via link oficial)

⚙️ Como rodar o projeto localmente
1. Clonar o repositório
git clone https://github.com/seu-usuario/rony-massoterapia.git
cd rony-massoterapia

2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Configurar variáveis de ambiente

Crie um arquivo .env baseado no .env.example.

5. Rodar migrações
python manage.py migrate

6. Criar superusuário
python manage.py createsuperuser

7. Rodar o servidor
python manage.py runserver


Acesse:

Site: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

📌 Status do Projeto

✔️ Backend funcional
✔️ Agenda robusta
✔️ Integração com WhatsApp
✔️ Estrutura pronta para produção
✔️ Ideal para uso comercial ou portfólio

🔮 Próximas melhorias planejadas

Interface mais avançada com Bootstrap

Confirmação/cancelamento por status

Dashboard para profissionais

Notificações adicionais

Deploy em produção

👤 Autor

Desenvolvido por Marcelo Ribeiro Romano
Projeto voltado para aprendizado avançado, portfólio e uso comercial.

✅ Próximo passo

Depois de colar isso no README.md, rode:

git add README.md
git commit -m "docs: add complete project README"
git push
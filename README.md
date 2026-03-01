para rodar basta usar os seguintes comandos

    criar o venv 

        python -m venv venv

    # Ativar o venv

        .\venv\Scripts\Activate

    # baixar os requirements

        pip install -r requirements.txt

    # Por fim executar
        
        python app.py

    # testar os endpoints no postman ou insonia, veja a baixo o tutorial do passo a passo 


    1. Página Inicial 
        
        GET http://localhost:5000/

        Retorno:

        json
        {
        "message": "API PharmaSys está funcionando!",
        "endpoints": {
            "GET /agendamentos": "Listar todos agendamentos",
            "GET /agendamentos/<id>": "Buscar agendamento por ID",
            "POST /agendamentos": "Criar novo agendamento",
            "PUT /agendamentos/<id>": "Atualizar agendamento",
            "DELETE /agendamentos/<id>": "Remover agendamento",
            "GET /agendamentos/horarios-disponiveis/<data>": "Ver horários disponíveis"
        }
        }


    2. Health Check
        
        GET http://localhost:5000/health
        Retorno:

        json
        {
        "status": "healthy",
        "database": "connected",
        "message": "API está funcionando corretamente"
        }


    3.Listar Todos Agendamentos
        
        GET http://localhost:5000/agendamentos/agendamentos
        
        Retorno:
        json
        [
        {
            "id": "local-1740662400",
            "nome": "João Silva",
            "telefone": "11999999999",
            "email": "joao@email.com",
            "veiculo": "Fiat Uno",
            "servico": "Detalhamento Completo",
            "dataPreferencial": "2024-03-20",
            "dataFormatada": "20/03/2024",
            "horarioPreferencial": "14:00",
            "mensagem": "Teste",
            "timestamp": "2024-03-19T10:30:00",
            "status": "pendente"
        }
        ]


    4. Buscar Agendamento por ID
        
        GET http://localhost:5000/agendamentos/agendamentos/local-1740662400


    5. Criar Novo Agendamento

        POST http://localhost:5000/agendamentos/agendamentos
        Content-Type: application/json

        {
        "nome": "Maria Oliveira",
        "telefone": "11888888888",
        "email": "maria@email.com",
        "veiculo": "Honda Civic",
        "servico": "Ceramic Coating",
        "dataPreferencial": "2024-03-25",
        "horarioPreferencial": "10:00",
        "mensagem": "Primeira vez na loja"
        }


    6. Ver Horários Disponíveis por Data
        
        GET http://localhost:5000/agendamentos/horarios-disponiveis/2024-03-15


    7. Atualizar Agendamento
        
        PUT http://localhost:5000/agendamentos/agendamentos/local-1740662400
        Content-Type: application/json

        {
        "status": "confirmado",
        "mensagem": "Cliente confirmou presença"
        }

    
    8. Deletar Agendamento
        
        DELETE http://localhost:5000/agendamentos/agendamentos/local-1740662400
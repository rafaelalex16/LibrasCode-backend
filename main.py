from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware



# iniciando framework fastapi
app = FastAPI()

# configurando cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois você restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


estudantes=[]

# criando rota endpoint websocket
@app.websocket('/librasCodeWebsocket')
async def websocket_endpoint(usuarioConectado: WebSocket):

    # Aceita a conexão do usuário
    await usuarioConectado.accept()

    # Adiciona o usuário conectado na lista de clientes
    estudantes.append(usuarioConectado)

    try:
        # Loop infinito: fica ouvindo mensagens o tempo todo
        while True:

            # Recebe o texto do professor
            aulaTranscrita = await usuarioConectado.receive_text()

            # Percorre todos os estudantes conectados
            for estudante in estudantes:
                # Envia a mensagem recebida para cada estudante
                await estudante.send_text(aulaTranscrita)

    except:
        # se der erro ou usuario desconectar remove esse websocket da lista de estudantes
        estudantes.remove(usuarioConectado)

#  Spotify Drive Backup (Playlist Automática)

Este projeto é um script automatizado em Python criado para quem perde o acesso à internet na estrada. O objetivo dele é pegar todas as músicas que você ouviu recentemente no Spotify no computador e adicioná-las automaticamente em uma playlist ("Backup da Estrada"), para que o aplicativo do celular possa baixá-las via Wi-Fi para você ouvir offline.

## Como Funciona 
1. Conecta na **API do Spotify** de forma automatizada (OAuth2).
2. Puxa as suas **50 últimas** músicas ouvidas.
3. Varre a sua playlist atual para evitar adicionar músicas duplicadas.
4. Insere apenas as novidades de volta na playlist.

## Requisitos
* Python 3
* `spotipy` e `python-dotenv`

## Como Usar 

1. Instale as dependências:
   ```bash
   pip install spotipy python-dotenv
   ```
2. Crie um aplicativo no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) com a Redirect URI `http://127.0.0.1:8888/callback` e cadastre seu e-mail em "User Management".
3. Altere o nome do arquivo `.env.example` para `.env` e coloque suas chaves (Client ID e Secret).
4. Rode o script:
   ```bash
   python spotify_backup.py
   ```

*Dica: Pode ser automatizado facilmente no **Agendador de Tarefas do Windows** para rodar diariamente de madrugada enquanto você dorme!*

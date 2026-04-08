import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURAÇÕES DA API E DA PLAYLIST
# ==========================================
# Insira aqui os dados do seu Spotify Developer Dashboard
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Deve ser EXATAMENTE a mesma URL que você colocou no Dashboard
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')

# Nome da playlist onde as músicas serão salvas
PLAYLIST_NAME = 'Backup da Estrada'

# Permissões necessárias para leitura de histórico e edição de playlists
SCOPE = 'user-read-recently-played playlist-read-private playlist-modify-private playlist-modify-public'


def get_or_create_playlist(sp, user_id, playlist_name):
    """Verifica se a playlist existe. Se não existir, cria uma nova."""
    print("Verificando playlists existentes...")
    
    # Busca as playlists do usuário iterando por todas as páginas
    playlists = sp.current_user_playlists()
    while playlists:
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                print(f"Playlist '{playlist_name}' encontrada!")
                return playlist['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
            
    # Se não encontrou no loop acima, cria a playlist
    print(f"Playlist '{playlist_name}' não encontrada. Criando nova...")
    nova_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description="Playlist gerada automaticamente com as músicas recentemente ouvidas.")
    return nova_playlist['id']

def main():
    try:
        # 1. Autenticação via OAuth2
        print("Iniciando autenticação com o Spotify...")
        auth_manager = SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
            open_browser=True # Abre o navegador automaticamente para vc autorizar na primeira vez
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Pega as informações do usuário atual
        user_info = sp.current_user()
        user_id = user_info['id']
        print(f"Autenticado com sucesso como: {user_info.get('display_name', user_id)}")
        
        # 2. Obter ou criar a playlist de destino
        playlist_id = get_or_create_playlist(sp, user_id, PLAYLIST_NAME)
        
        # 3. Obter todas as músicas que JÁ ESTÃO na playlist (para evitar duplicações)
        print("Buscando músicas existentes na playlist para evitar duplicação...")
        existing_tracks = set()
        playlist_tracks = sp.playlist_items(playlist_id, fields="items.track.id,next")
        
        while playlist_tracks:
            for item in playlist_tracks['items']:
                track = item.get('track')
                if track and track.get('id'):
                    existing_tracks.add(track['id'])
                    
            if playlist_tracks['next']:
                playlist_tracks = sp.next(playlist_tracks)
            else:
                playlist_tracks = None
                
        # 4. Pegar músicas ouvidas recentemente
        # A API restringe o histórico a um limite de 50 músicas por requisição
        print("Buscando suas músicas ouvidas recentemente...")
        recent_tracks = sp.current_user_recently_played(limit=50)
        
        tracks_to_add = []
        for item in recent_tracks['items']:
            track_id = item['track']['id']
            # Verifica se a música já está na playlist ou se já foi adicionada na lista de 'para adicionar' (evita repetir no msmo lote)
            if track_id not in existing_tracks and track_id not in tracks_to_add:
                tracks_to_add.append(track_id)
                
        # 5. Adicionar músicas à playlist se houver novidades
        if tracks_to_add:
            # O Spotify só aceita adicionar max 100 músicas por vez. Como limitamos a 50 lá em cima, tá seguro.
            sp.playlist_add_items(playlist_id, tracks_to_add)
            print(f"Sucesso! {len(tracks_to_add)} novas música(s) adicionada(s) à playlist '{PLAYLIST_NAME}'.")
        else:
            print("Você não ouviu músicas novas, a playlist já está completamente atualizada.")
            
    except SpotifyException as e:
        print(f"\n[ERRO NA API SPOTIFY] Problema de conexão ou permissão: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] Alguma coisa deu errado: {e}")

if __name__ == '__main__':
    main()

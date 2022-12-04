""" Arquivo com alguns objetos para facilitar o gerenciamento de músicas (sons) """

#Importe as bibliotecas necessárias
import pygame
from enum import Enum, auto

#Cria grupos paradiferentes tipos de sons.
class SoundGroup(Enum):
    """Objeto de enumeração para determinar o tipo de som
    """

    EFFECT = auto()   # Como regra, som de curto prazo
    SOUND = auto()    # Um som longo tocando ao fundo


#Classe para gerenciamento dos sons.
class MusicManager:
    """Gerenciador de música - objeto para facilitar a configuração da música. Cria
    objetos sonoros. Todos os sons pertencem a um certo grupo imaginário para determinar
    configurações comuns (como volume).

    Parameters
    ----------
    sounds: (Dict[str, Tuple[str, spaceway.music.Channel]])
            Dict com descrição dos arquivos de música
            (key - sound name, value - file path e sound group)
    """

    def __init__(self, sounds):
        """Inicializador do MusicManager
        """
        self.__sounds = {}

        for name in sounds:
            path, group = sounds[name]
            self.__sounds[name] = (pygame.mixer.Sound(path), group)

    def get(self, name):
        """Obtem objeto de som para seu uso posterior
        

        Parameters
        ----------
        name : str
            Nome do som.

        Returns
        -------
        pygame.mixer.Sound
            Objeto de som.

        """
        return self.__sounds[name][0]

    def set_volume(self, volume, group) -> None:
        """Defina um volume específico para todos os sons deste grupo

        Parameters
        ----------
        volume: float
            Número flutuante no intervalo de 0 a 1
        group: SoundGroup
            O grupo de sons para o qual este volume deve ser definido
        """
        for name in self.__sounds:
            sound, _group = self.__sounds[name]

            if _group == group:
                sound.set_volume(volume)
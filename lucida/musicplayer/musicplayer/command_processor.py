import time
import os
import nltk
import player

nltk.download('averaged_perceptron_tagger')


OK = "OK, Sir"
NOT_FOUND = "Sorry sir, I don't understand"

class ComamndProcessor(object):
    def __init__(self):
        self._player = player.Player()

    def process(self, data):
        tags = nltk.pos_tag(data.split())
        command = None

        for tag in tags:
            if tag[1] == 'VB':
                command = tag[0]

        if command:
            if command.lower() == 'play':
                return self.play()
            elif command.lower() == 'stop':
                return self.stop()
            elif command.lower() == 'pause':
                return self.pause()

        return NOT_FOUND

    def play(self):
        try:
            if self._player._player is None:
                self._player.launch()

            self._player.play(os.getcwd() + '/../playlist/')

            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def stop(self):
        try:
            self._player.stop()
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def pause(self):
        try:
            self._player.pause()
            return OK
        except Exception as e:
            pritn(e)
            return NOT_FOUND


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
        vb = None
        rb = None

        for tag in tags:
            if tag[1] == 'VB':
                vb = tag[0].lower()
            elif tag[1] == 'RB':
                rb = tag[0].lower()

        if vb:
            if vb == 'play':
                if rb:
                    if rb == 'next':
                        return self.next()
                    elif rb == 'previous':
                        return self.prev()
                else:
                    return self.play()
            elif vb == 'stop':
                return self.stop()
            elif vb == 'pause' or 'resume':
                return self.pause()
            elif vb == 'increase':
                return self.increase_vol()
            elif vb == 'decrease':
                return self.decrease_vol()

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
            self._player.toggle()
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def next(self):
        try:
            self._player.next()
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def prev(self):
        try:
            self._player.prev()
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def increase_vol(self):
        try:
            self._player.set_volume(
                self._player.get_volume() + 1
            )
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

    def decrease_vol(self):
        try:
            self._player.set_volume(
                self._player.get_volume() - 1
            )
            return OK
        except Exception as e:
            print(e)
            return NOT_FOUND

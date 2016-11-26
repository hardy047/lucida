import command_processor as cp
import time




handler = cp.ComamndProcessor()
handler.process("play some music")

time.sleep(50)
handler.process("Can you pause music?")
handler.process("Please, stop this music")


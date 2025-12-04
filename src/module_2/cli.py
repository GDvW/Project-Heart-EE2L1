from src.module_2.generate import *
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
import threading
import queue
from time import sleep

class CLI:
    def __init__(self, cmd_queue: "queue.Queue[str]", stop_event: threading.Event, executing_event: threading.Event, cancelled_event: threading.Event):
        self.cmd_queue = cmd_queue
        self.stop_event = stop_event
        self.executing_event = executing_event
        self.cancelled_event = cancelled_event
        self.t = None
    
    def cli(self):
        session = PromptSession(history=InMemoryHistory())
        print("CLI thread started. Type 'help' for commands. Use arrow keys for history.")
        
        while not self.stop_event.is_set():
            try:
                while self.executing_event.is_set() and not self.stop_event.is_set():
                    sleep(0.05)
                    
                user_input = session.prompt("> ").strip()
                
                if not user_input:
                    continue
                
                self.cmd_queue.put(user_input)
                self.executing_event.set()
                
                if user_input == "exit":
                    self.exit(put_cmd=False)
                    return
            except KeyboardInterrupt: # Ctrl+C pressed
                self.cancelled_event.set()
                continue
            except EOFError: # Ctrl+D pressed
                self.exit()
                return
            except Exception as e:
                # log and continue
                print("CLI error:", e)
                self.exit()
                return
            
    def exit(self, put_cmd=True):
        self.stop_event.set()
        self.cmd_queue.put("exit")
        return
    def run(self):
        self.t = threading.Thread(target=self.cli, daemon=True)
        self.t.start()
    def close(self):
        self.exit(put_cmd=False)
        self.t.join(timeout=1.0)
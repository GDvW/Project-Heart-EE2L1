import threading
import matplotlib.pyplot as plt
import queue

from lib.config.ConfigParser import ConfigParser

from lib.TUI.CLI import CLI
from lib.TUI.CommandProcessor import CommandProcessor
from lib.localization.LocalizationPlot import LocalizationPlot
from lib.localization.generateLocalizationCommands import generateLocalizationCommands


class LocalizationTUI:
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    def __init__(self, path: str, config: ConfigParser):
        """
        @author: Gerrald
        @date: 10-12-2025
        """
        self.cmd_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.executing_event = threading.Event()
        self.cancelled_event = threading.Event()
        
        self.plot = LocalizationPlot(path)
        self.commands: CommandProcessor = generateLocalizationCommands(self.plot)
        self.cli = CLI(self.cmd_queue, self.stop_event, self.executing_event, self.cancelled_event, self.commands.get_autocompletion_dict())
        
        self.timer = None
        
    def run(self):
        """
        @author: Gerrald
        @date: 10-12-2025
        """
        self.plot.plot_init()
        self.cli.run()
        self.timer = self.plot.fig.canvas.new_timer(interval=150)
        self.timer.add_callback(self.on_timer_tick)
        self.timer.start()
        
        try:
            print("Showing plot. Interact with CLI in the console.")
            while not self.stop_event.is_set():
                plt.pause(0.1)
        except Exception as e:
            print("Matplotlib event loop ended:", e)
        finally:
            # request CLI thread to stop
            self.stop_event.set()
            # try to join CLI thread briefly
            self.cli.close()
            self.timer.stop()
            self.plot.close()
            print("Shutdown complete.")
            
        
    # Process commands every tick of the timer
    def on_timer_tick(self):
        """
        @author: Gerrald
        @date: 10-12-2025
        """
        try:
            while not self.stop_event.is_set():
                cmd = self.cmd_queue.get_nowait()
                if cmd is None or len(cmd) == 0:
                    continue
                
                self.commands.process_command(cmd)
                self.executing_event.clear()
        except queue.Empty:
            pass
        
        return

        
def main(path):
    """
    @author: Gerrald
    @date: 21-01-2026
    """
    config = ConfigParser()
    tui = LocalizationTUI(path, config)
    tui.run()
        
if __name__ ==  "__main__":
    main("samples\\calibrated_white_noise_single")
    main("samples\\calibrated_white_noise_single")
    # main("generated\\hearbeat model\\3d-model\\White Noise")
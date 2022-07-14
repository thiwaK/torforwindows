from os import name as __osname
from colorama import init as __initialize
from colorama import Fore as __foreground
from colorama import Back as __background
from colorama import Style as __style

if __osname == "posix":
    # colors foreground text:
    fc = "\033[0;96m"
    fg = "\033[0;92m"
    fw = "\033[0;97m"
    fr = "\033[0;91m"
    fb = "\033[0;94m"
    fy = "\033[0;33m"
    fm = "\033[0;35m"

    # colors background text:
    bc = "\033[46m"
    bg = "\033[42m"
    bw = "\033[47m"
    br = "\033[41m"
    bb = "\033[44m"
    by = "\033[43m"
    bm = "\033[45m"

    # colors style text:
    sd = __style.DIM
    sn = __style.NORMAL
    sb = __style.BRIGHT
else:
    __initialize(autoreset=True)
    # colors foreground text:
    fc = __foreground.CYAN
    fg = __foreground.GREEN
    fw = __foreground.WHITE
    fr = __foreground.RED
    fb = __foreground.BLUE
    fy = __foreground.YELLOW
    fm = __foreground.MAGENTA
    

    # colors background text:
    bc = __background.CYAN
    bg = __background.GREEN
    bw = __background.WHITE
    br = __background.RED
    bb = __background.BLUE
    by = __background.YELLOW
    bm = __background.MAGENTA

    # colors style text:
    sd = __style.DIM
    sn = __style.NORMAL
    sb = __style.BRIGHT

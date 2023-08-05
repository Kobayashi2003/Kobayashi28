hlpMsg = """
      ___ __  __  ____      _    ____ ____ _____
     |_ _|  \/  |/ ___|    / \  / ___/ ___|_   _|
      | || |\/| | |  _    / _ \ \___ \___ \ | |
      | || |  | | |_| |  / ___ \ ___) |__) || |
     |___|_|  |_|\____| /_/   \_\____/____/ |_|

     _         _                           _     _
    | | _____ | |__   __ _ _   _  __ _ ___| |__ (_)
    | |/ / _ \| '_ \ / _` | | | |/ _` / __| '_ \| |
    |   < (_) | |_) | (_| | |_| | (_| \__ \ | | | |
    |_|\_\___/|_.__/ \__,_|\__, |\__,_|___/_| |_|_|
                           |___/


    Usage:

      python main.py [options] [items]

    Options:

      -h, --help: show help message

      -v, --version: show version

      -r=[rate], --rate=[rate]: set the rate of the image to be shown

      -s, --save, -s=[path], --save=[path]: set the path to save the image

              when the [path] is not set, the image will be saved in the same directory as the original image

      -nc, --no-color: disable the color of the image

      --bc=[color name], --background-color=[color name]: set the background color of the image

              default color: 'black'

      --ascii: show the image in ascii

      -p=[mode], --print=[mode]: set the printing mode

              [mode]: 'auto'(default) | 'image' | 'terminal' 
              
      --fs=[frameskip], --frameskip=[frameskip]: set the frameskip of the gif and video
      
    Items:

      [items] is the path of the image or video or gif

"""


verMsg = """v1.0.0"""
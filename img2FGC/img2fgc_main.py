from rich import print
from PIL import Image
import webcolors
import platform
import random
import click
import json
import uuid
import time
import sys
import os

if platform.system() == 'Windows':
    pass
else:
    print('Windows is the only supported OS for this mod')
    os.system('pause')
    sys.exit(1)

example = os.path.join(os.getcwd(), '..', 'Images', 'example.png')
Name_original = 'Placeable_Floor_Soft_Vanilla(Clone)'
Name_digital = 'Placeable_Floor_Soft_Retro(Clone)'
type_of_kek = dict
type_of_data = dict

print('[light_cyan3]NOTE: Although I don’t believe that you can get[/light_cyan3] [red3]banned[/red3] [light_cyan3]for this, but[/light_cyan3] [light_green]be careful![/light_green] [red3]Don\'t use this script if you want to import NSFW or if you are stupid[/red3]\n\n'

      'You cannot save maps larger than [red3]2MB[/red3] [light_green](around 700 pixels)[/light_green]\n'
      '[light_green]1000 pixels[/light_green] are generated in ~[light_green]1 second[/light_green]\n\n'

      'Script created by [light_yellow3]repinek[/light_yellow3] ([light_yellow3]@repinek[/light_yellow3] in [light_cyan3]tg/ds[/light_cyan3], [light_yellow3]@repinek840[/light_yellow3] in X), and thanks [light_green]FloyzI[/light_green] for help\n'  # type: ignore
      '       updated by [light_yellow3] Loamfy[/light_yellow3] ([light_yellow3]loamfy[/light_yellow3] in [light_cyan3]Discord[/light_cyan3])')


appdata_fg = os.path.join(os.environ['LOCALAPPDATA'] + 'Low', 'Mediatonic', 'FallGuys_client')
if os.path.exists(appdata_fg):
    pass
else:
    appdata_fg = os.path.join(os.path.expanduser('~'),  # if user changed LOCALAPPDATA variable
                              'AppData',
                              'LocalLow',
                              'Mediatonic',
                              'FallGuys_client')

file_path_output = os.path.join(appdata_fg, 'output.txt')
FGC_json = os.path.join(appdata_fg, 'Img2FGC.json')

@click.command(name='img2FGC')
@click.option('--path-to-file',            default=example,       prompt='Image',               help='Image, that will be on the map',       required=True, type=click.STRING)
@click.option('--width',                   default=70,            prompt='Width',               help='Width of an image to be on the map',    required=True, type=click.INT)
@click.option('--height',                  default=70,            prompt='Height',              help='Height of an image to be on the map',   required=True, type=click.INT)
@click.option('--isDigital',               default=False,         prompt='Digital?',            help='Image, that will be on the map',        required=True, type=click.BOOL)
@click.option('--shouldDeleteBlackPixels', default=False,         prompt='Delete Black Pixels', help='Should app delete Black Pixels or no?', required=True, type=click.BOOL)
@click.option('--shouldDeleteWhitePixels', default=False,         prompt='Delete White Pixels', help='Should app delete White Pixels or no?', required=True, type=click.BOOL)
def start_img2fgc(**kwargs):
    Img2FGC(*list(kwargs.values())).start()



class Img2FGC:
    def __init__(self, path_to_file, width, height, isdigital, shoulddeleteblackpixels, shoulddeletewhitepixels):
        self.pixels: list[dict[str, str | int | list[float]]] = []
        self.random = lambda: random.randint(-1000000, -1)
        self.time = int(time.time() * 1000)  # fg time format is in milliseconds
        self.uuid4 = lambda: str(uuid.uuid4()).replace('-', '')
        self._init(path_to_file, width, height, isdigital, shoulddeleteblackpixels, shoulddeletewhitepixels)

    @staticmethod
    def __on_error(message: str) -> None:
        print(message)
        os.system('pause')
        sys.exit(1)

    def _init(self, path_to_file: str, width: int, height: int, isDigital: bool, shouldDeleteBlackPixels: bool,
              shouldDeleteWhitePixels: bool):
        try:
            self.path_to_file = path_to_file
            self.width = width
            self.height = height
            self.isDigital = isDigital
            self.shouldDeleteBlackPixels = shouldDeleteBlackPixels
            self.shouldDeleteWhitePixels = shouldDeleteWhitePixels
            self.template = kek
            self.name = Name_original
            self.ColourPaletteID = 'Vanilla'
            if self.isDigital:
                self.name = Name_digital
                self.ColourPaletteID = 'Retro'
            print('[light_green]Config[/light_green]:\n'
                  f'Path: {self.path_to_file}\n'
                  f'Width: {self.width}\n'
                  f'Height: {self.height}\n'
                  f'Delete white: {self.shouldDeleteWhitePixels}, black: {self.shouldDeleteBlackPixels}\n'
                  f'Digital: {self.isDigital}')

        except Exception as e:
            self.__on_error(f'Send this to Loamfy: {e.__traceback__.tb_lineno}, {e}\n')

    def _prepare_json(self) -> dict[str, str | int | list[float]]:
        if self.isDigital:
            kek['Level Theme ID'] = 'THEME_RETRO'
            kek['SkyboxId'] = 'Retro_Skybox'
            kek['LevelCreationTimestamp'] = self.time - random.randint(1, 5_400_000)
            kek['LevelSavedAtTimestamp'] = self.time
            kek['LevelLastModifiedAtTimestamp'] = self.time - random.randint(1, 1000)
            kek['LevelPublishedAtTimestamp'] = self.time - random.randint(1, 30_000)
        return kek

    def finish(self):
        self.template['Floors'] = list(self.pixels)
        print(self.pixels)
        self.finished_json = self.template
        with open(FGC_json, 'a') as f:
            json.dump(self.finished_json, f, ensure_ascii=False, indent=4)

    def _resize_image(self) -> Image:
        try:
            image_file = Image.open(self.path_to_file)
            image = image_file.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        except OSError:
            self.__on_error(f'Didn\'t found image with path {self.path_to_file}\n')
        except Exception as e:
            self.__on_error(f'Send this to Loamfy: {e.__traceback__.tb_lineno}, {e}\n')

        # checking
        width, height = image.size

        if self.width > width:
            self.__on_error('Width can\'t be more than image width\n')
        elif self.width > height:
            self.__on_error('Height can\'t be more than image height\n')

        try:
            return image.resize((self.width, self.height))
        except Exception as e:
            self.__on_error(f'Report about this to Loamfy: {e.__traceback__.tb_lineno}, {e}\n')

    def _put_pixel(self, hex_value: str, x_y: tuple[int, int]) -> dict[str, str | int | list[float]]:
        _uuid4 = self.uuid4()
        __uuid4 = self.uuid4()
        return {"Name": self.name,
                "Group Type": "None",
                "VariantGuid": f'{_uuid4[:8]}-{_uuid4[8:12]}-{_uuid4[12:16]}-{_uuid4[16:20]}-{_uuid4[20:]}',
                "GUIDs": f'{__uuid4[:8]}-{__uuid4[8:12]}-{__uuid4[12:16]}-{__uuid4[16:20]}-{__uuid4[20:]}',
                'ColourHexCode': hex_value,
                'ColourPaletteID': self.ColourPaletteID,
                'ID': self.random(),
                'Position': [x_y[0] * 4.075,
                             65,
                             x_y[1] * 4.075
                             ],
                'CurrentRotation': [0, 0, 0],
                'Local Scale': [1, 1, 1],
                'Shader Scale': [1, 1, 1],
                "Floor Pivot Pos": 0,
                "Floor Depth": 0,
                "Floor Increment Amount": 1,
                "Active": True,
                "VisibilityParam": 1,
                "CollisionEnabledParam": True
                }

    def _configure_pixels(self, resized_image: Image.Image) -> None:
        # every pixel
        for x in range(self.width):
            for y in range(self.height):
                pixel = resized_image.getpixel((x, y))  # get pixel rgb
                r, g, b = pixel[:3]  # fix alpha

                try:
                    a = pixel[3]
                except IndexError:
                    a = 1

                closest_name = closest_colour((r, g, b))
                closest_value = rgb_to_hex(pixel)
                print(closest_value, pixel)
                if self.shouldDeleteWhitePixels and closest_name == 'white':
                    print('skip')
                    continue
                elif self.shouldDeleteBlackPixels and closest_name == 'black':
                    print('skip')
                    continue
                else:
                    try:
                        if a > 0:  # alpha is above 0
                            self.pixels.append(self._put_pixel(closest_value, (x, y)))
                        else:
                            print('Alpha is 0, unable to set pixel')
                            continue
                    except Exception as e:
                        print(f'Report about this to Loamfy: {e.__traceback__.tb_lineno}, {e}')
                    posx = x * 4.075
                    posy = y * 4.075
                    print(
                        f'RGB: {pixel}, alpha: {a}, color name: {closest_name}, color index: {closest_value}, POS X: {posx}, POS Y: {posy}')

    def start(self):
        print(
            'After [light_green]5 seconds[/light_green] map should start generating, you will see some debug info (BETA)\n'
            'If you get some errors report about them to Loamfy, thanks')
        time.sleep(5)
        self._configure_pixels(self._resize_image())
        self.finish()
        print('\nGeneration completed! Press \'Replace existing maps with level\' in FallGuysTools to load your level')
        # yea, use FGTools guys
        time.sleep(3)




    def _init2(self) -> None:
        # reading output.txt by mod
        try:
            with open(file_path_output, 'r', encoding='utf-8') as f1:
                self.lines = f1.readlines()
        except FileNotFoundError:
            self.__on_error('[light_red]Unable to find file [/light_red], try again\n')

        for line in self.lines:
            try:
                line = line.strip()
                key, value = line.split(' = ')
                match key:  # use switch-case to have faster experience (from python 3.10)
                    case 'path_to_file':
                        self.image_input = value
                    case 'width':
                        self.width_input = value
                    case 'height':
                        self.height_input = value
                    case 'shouldDeleteBlackPixels':
                        self.shouldDeleteBlackPixels = value.lower()
                    case 'shouldDeleteWhitePixels':
                        self.shouldDeleteWhitePixels = value.lower()
                    case 'isDigital':
                        self.isDigital = value.lower()
            except FileNotFoundError:
                self.__on_error('[light_red]Unable to find file[/light_red], try again\n')
            except Exception as e:
                self.__on_error(
                    'Looks like file [light_red]is corrupted[/light_red], try again, if you can\'t fix this error by '
                    f'yourself tell [light_yellow]repinek about this,[/light_yellow] {e}, {e.__traceback__.tb_lineno}\n'
                      )

# object example
data = {
    "Name": "Placeable_Floor_Soft_Vanilla(Clone)",
    "Group Type": "None",
    "VariantGuid": "9422ba3d-b426-486f-864f-385cb21d1212",
    "GUIDs": "02607599-44b9-4b3e-9509-d9f550b8fe4a",
    'ColourHexCode': '#111111',
    'ColourPaletteID': 'Vanilla',
    'ID': -657444,
    'Position': [
        -3.81721544,
        65,
        -152.007324
    ],
    'CurrentRotation': [
        0,
        0,
        0
    ],
    'Local Scale': [
        1,
        1,
        1
    ],
    'Shader Scale': [
        1,
        1,
        1
    ],
    "Floor Pivot Pos": 0,
    "Floor Depth": 0,
    "Floor Increment Amount": 1,
    "Active": True,
    "VisibilityParam": 1,
    "CollisionEnabledParam": True
}

kek = {'Version': 'V1',
       'Level Theme ID': 'THEME_VANILLA',
       'Level Music': 'MUS_InGame_Want_Revenge',
       'What does the bean say': 'i/8S/F/FA7nUw0OOMFIkrMWWZkxARdC/uYn/3ivAa2CrYJdnYdPKz1UL1QRa0go7VcmtG8gZkfSVdMKyxPC+Yg==',
       'Game Mode ID': 'GAMEMODE_GAUNTLET',
       'FirstBuildSessionId': '58cf60b5-2098-4ca5-8ade-90c6c15d5cf3',
       'SkyboxId': 'Vanilla_Skybox',
       'LevelCreationTimestamp': 0,
       'LevelSavedAtTimestamp': 0,
       'LevelLastModifiedAtTimestamp': 0,
       'LevelPublishedAtTimestamp': 0,  # this values will be modified to current Unix date
       'Max Capacity': 40,
       'No of Winners': -1,
       'Min Capacity': 1,
       'No of Eliminations': -1,
       'Slime Height': -1,
       'Slime Speed': -1,
       'Test Mode Completed': True,
       'Level Published': False,
       'LevelNameIsCustom': True,
       'LevelDescriptionIsCustom': False,
       'Camera': {'Position': [-9.66126, 65, -176.04482], 'Pitch and Yaw': [28.690294, 1.6673589], 'Distance': 100},
       'Floors': [{}]
       }


def rgb_to_hex(rgb: tuple[int, int, int] | tuple[int, ...]):
    return '#{:02x}{:02x}{:02x}'.format(*rgb).upper()


def closest_colour(requested_colour: tuple[int, int, int]):
    min_colours = {}
    for key, name in webcolors._definitions._CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

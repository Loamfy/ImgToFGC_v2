import argparse
import json
import os
import platform
import time
import uuid
import webcolors
from PIL import Image
from rich import print

if platform.system() == 'Windows':
    pass
else:
    print('Windows is the only supported OS for this mod')
    os.system('pause')
    exit(1)

type_of_kek = dict
type_of_data = dict
argparser = argparse.ArgumentParser(prog='img2FGC',
                                    description='Convert image to Fall Guys Creative Level!',
                                    exit_on_error=False)
argparser.add_argument('--path-to-file',               required=True, type=str, default='example.png')
argparser.add_argument('--width',                     required=True, type=int)
argparser.add_argument('--height',                    required=True, type=int)
argparser.add_argument('--isDigital',                required=False, type=bool, default=False)
argparser.add_argument('--shouldDeleteBlackPixels',  required=False, type=bool, default=False)
argparser.add_argument('--shouldDeleteWhitePixels',  required=False, type=bool, default=False)


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


class Img2FGC:
    def __init__(self):
        self.pixels: list[dict[str, str | int | list[float]]] = []
        self._init()

    @staticmethod
    def __on_error(message: str) -> None:
        print(message)
        os.system('pause')
        exit(1)

    def _init(self):
        self.args = argparser.parse_args()
        try:
            print('[light_green]Config[/light_green:\n'
                  f'path: {self.args.path_to_file}\n'
                  f'width: {self.args.width}\n'
                  f'height: {self.args.height}\n'
                  f'delete white: {self.args.shouldDeleteWhitePixels}, black: {self.args.shouldDeleteBlackPixels}\n'
                  f'theme: {self.args.isDigital}')
            self.path_to_file = self.args.path_to_file
            self.width = self.args.width
            self.height = self.args.height
            self.shouldDeleteWhitePixels = self.args.shouldDeleteWhitePixels
            self.shouldDeleteBlackPixels = self.args.shouldDeleteBlackPixels
            self.isDigital = self.args.isDigital
            self.template = kek
        except Exception as e:
            self.__on_error(f'Send this to Loamfy: {e.__traceback__.tb_lineno}, {e}\n')

    def _prepare_json(self) -> dict[str, str | int | list[float]]:
        if self.isDigital:
            kek['Level Theme ID'] = 'THEME_RETRO'
            kek['SkyboxId'] = 'Retro_Skybox'
        return kek

    def finish(self):
        self.template['Floors'] = self.pixels
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
        global id_number
        id_number = id_number - 1
        data['ID'] = id_number
        data['Position'][0] = x_y[0] * 4.075
        data['Position'][2] = x_y[1] * 4.075
        data['ColourHexCode'] = hex_value
        data['ColourPaletteID'] = 'Vanilla'
        if self.isDigital:
            data['Name'] = 'Placeable_Floor_Soft_Retro(Clone)'
            data['ColourPaletteID'] = 'Retro'
        random_key = uuid.uuid4()
        random_key2 = uuid.uuid4()
        formatted_key = str(random_key).replace('-', '')
        formatted_key2 = str(random_key2).replace('-', '')
        self.guids_sss = f'{formatted_key2[:8]}-{formatted_key2[8:12]}-{formatted_key2[12:16]}-{formatted_key2[16:20]}-{formatted_key2[20:]}'
        self.variant_guid = f'{formatted_key[:8]}-{formatted_key[8:12]}-{formatted_key[12:16]}-{formatted_key[16:20]}-{formatted_key[20:]}'
        data['GUIDs'] = self.guids_sss
        data['VariantGuid'] = self.variant_guid
        return data

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

                actual_name, closest_name = closest_colour((r, g, b))
                closest_value = rgb_to_hex(pixel)
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
                        f'RGB: {pixel}, alpha: {a}, color name: {closest_name}, color index: {closest_value}, object ID: {id_number}, POS X: {posx}, POS Y: {posy}, VatirantGuid: {self.variant_guid}, GUIDs: {self.guids_sss}')

    def start(self):
        print(
            'After [light_green]5 seconds[/light_green] map should start generating, you will see some debug info (BETA)\n'
            'If you get some errors report about them to Loamfy, thanks')
        time.sleep(5)
        self._configure_pixels(self._resize_image())
        self.finish()
        print('Generation completed! Press \'Replace existing maps with level\' in FallGuysTools to load your level\n')
        # yea, use FGTools guys
        os.remove(file_path_output)
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


id_number = -1  # id number for object

# object example
data = {
    'Name': 'Placeable_Floor_Soft_Vanilla(Clone)',
    'ID': -10005,
    'VariantGuid': '9422ba3d-b426-486f-864f-385cb21d1212',
    'GUIDs': '0e2247bc-1388-4226-917d-d9a26e6813b0',
    'Position': [
        -3.81721544,
        65.0,
        -152.007324
    ],
    'CurrentRotation': [
        0.0,
        0.0,
        0.0
    ],
    'Local Scale': [
        1.0,
        1.0,
        1.0
    ],
    'Group Type': 'None',
    'ColourSwapIndex': -1,
    'Shader Scale': [
        1.0,
        1.0,
        1.0
    ],
    'Floor Pivot Pos': 0.0,
    'Floor Depth': 0.0,
    'Floor Increment Amount': 1.0
}

kek = {'Version': 'V1',
       'Test Mode Completed': True,
       'Level Theme ID': 'THEME_VANILLA',
       'Level Published': False,
       'LevelCreationTimestamp': 1703262048686,
       'LevelSavedAtTimestamp': 1703262185389,
       "LevelLastModifiedAtTimestamp": 1703262181223,
       "LevelPublishedAtTimestamp": 1703262185389,
       "LevelNameIsCustom": True,
       "LevelDescriptionIsCustom": False,
       "Min Capacity": 1,
       'Level Music': 'MUS_InGame_Fall_N_Roll',
       'What does the bean say': 'gbgGpO5UXftvdC+TK/5zR6pknqciPVunpoMnuNzkBRyjKjqy81CYwVwdQ/HJ+RU2g5B2UaQZq6MEiA2BvXh7wg==',
       'SkyboxId': 'Vanilla_Skybox',
       'Game Mode ID': 'GAMEMODE_GAUNTLET',
       'Max Capacity': 40,
       'No of Winners': -1,
       'No of Eliminations': -1.0,
       'Slime Height': -1.0,
       'Slime Speed': -1.0,
       'Camera': {'Position': [135.094772, 90.8210449, -216.08284],
       'Pitch and Yaw': [14.6352329, -83.75641],
       'Distance': 100.0},
       'Button Thumbnail': '',
       'Floors': [{}]}

def rgb_to_hex(rgb: tuple[int, int, int] | tuple[int, ...]):
    return '%02x%02x%02x' % rgb


def closest_colour(requested_colour: tuple[int, int, int]):
    min_colours = {}
    for key, name in webcolors.CSS2_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


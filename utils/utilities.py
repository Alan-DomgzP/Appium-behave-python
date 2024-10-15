import base64
import os
from datetime import date

import allure
from allure_commons.types import AttachmentType
from appium import webdriver as appium_webdriver
from appium.options.common import AppiumOptions
from behave.model_core import Status


class Utilities:
    # Gets path of project up to Behave folder
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # Gets path up to current executed folder
    current_dir = os.getcwd()

    @staticmethod
    def set_context_variables(context):
        userdata = context.config.userdata
        context.DRIVER_LOCATION = userdata.get('driver_location')
        context.PLATFORM = userdata.get("platform")
        context.PLATFORM_VERSION = userdata.get('platform_version')
        context.DEVICE_NAME = userdata.get('device_name')
        context.APP = userdata.get('app')

    @staticmethod
    def get_capabilities(context):
        print("GETTING CAPABILITIES...")
        capabilities = {
            'platformName': context.PLATFORM,
            'platformVersion': context.PLATFORM_VERSION,
            'deviceName': context.DEVICE_NAME,
            'autoGrantPermissions': True,
            'noReset': True
        }
            # 'browserName': context.APP,
            # 'automationName': 'UiAutomator2' if context.PLATFORM.lower() == 'android' else 'XCUITest'

        if context.PLATFORM.lower() == 'android':
            capabilities.update({
                'automationName': 'UiAutomator2',
                'browserName': context.APP,
                # 'chromeOptions': {"w3c": False}
                # "appPackage": "com.android.chrome",
                # "appActivity": "com.google.android.apps.chrome.Main"
            })
        else:
            capabilities.update({
                'automationName': 'XCUITest',
                'bundleId': ''
            })

        return capabilities

    @staticmethod
    def get_appium_driver(context):
        capabilities = AppiumOptions().load_capabilities(Utilities.get_capabilities(context))
        if capabilities:
            print("CAPABILITIES OBTAINED!")
        url = 'http://localhost:4723'

        print("INITIALIZING DRIVER...")
        driver = appium_webdriver.Remote(command_executor=url, options=capabilities)
        # print("Driver contexts:", driver.contexts)
        print("Driver context:", driver.context)

        return driver

    @staticmethod
    def start_driver(context):
        context.driver = Utilities.get_appium_driver(context)

        print("DRIVER STARTED!")

    @staticmethod
    def paths(mobile_platform):
        directories = [
            '/evidences/reports',
            f'/evidences/reports/{mobile_platform}/',
            '/evidences/snapshots',
            f'/evidences/snapshots/{mobile_platform}/screenshots',
            f'/evidences/snapshots/{mobile_platform}/videos'
        ]
        return directories

    @staticmethod
    def validate_and_create_directories(directories):
        print_message = True  # Variable para controlar si se imprime el mensaje
        for directory in directories:
            if directory not in [directories[0], directories[2]]:
                if not os.path.exists(os.getcwd() + directory):
                    if print_message:  # Imprimir mensaje solo la primera vez
                        print("--- The evidence folder will be created ---")
                        print_message = False  # Cambiar a False después de imprimir el mensaje
                    Utilities.create_directory(directory)
                    Utilities.create_todays_directory(directory)
                else:
                    Utilities.create_todays_directory(directory)

    @staticmethod
    def create_directory(directory):
        try:
            print("Creating directory: ", directory)
            os.makedirs( Utilities.current_dir + directory, exist_ok=True)
        except OSError as e:
            print(f"There was an error creating folders: {e}")

    @staticmethod
    def create_todays_directory(directory):
        try:
            folder_date = Utilities.get_date()
            todays_folder = Utilities.join_paths(
                Utilities.current_dir, [directory.lstrip('/'), folder_date])
            os.makedirs(todays_folder, exist_ok=True)
            Utilities.execution_folder(todays_folder)
        except OSError as e:
            print(f"There was an error creating folders: {e}")

    @staticmethod
    def execution_folder(path):
        subfolders = [name for name in os.listdir(
            path) if os.path.isdir(Utilities.join_paths(path, [name]))]
        subfolder_count = len(subfolders) + 1
        execution_folder = Utilities.join_paths(path, [str(subfolder_count)])
        os.makedirs(execution_folder)

    @staticmethod
    def get_last_report_folder_name(directory):
        folder_date = Utilities.get_date()
        path = Utilities.join_paths(Utilities.current_dir, [
                                    directory.lstrip('/'), folder_date])
        try:
            # Obtener la lista de elementos en la carpeta
            elements = os.listdir(path)
            # Filtrar solo los elementos que sean directorios
            directories = [element for element in elements if os.path.isdir(
                Utilities.join_paths(path, [element]))]
            # Obtener el nombre de la última carpeta en función de su valor numérico
            last_folder = str(max([int(directory)
                              for directory in directories]))
            relative_path = os.path.relpath(path, os.getcwd())
            path = Utilities.join_paths(relative_path, [last_folder])

            return path
        except OSError as e:
            print(f"There was an error: {e}")

    @staticmethod
    def set_video_path(context, status):
        video_name = f'{status}_{context.scenario.name}_{Utilities.get_date()}.mp4'
        directories = Utilities.paths(context.PLATFORM)
        video_path = Utilities.get_last_report_folder_name(directories[4])
        file_path = Utilities.join_paths(
            Utilities.current_dir, [video_path, video_name.replace(' ', '')])

        return file_path

    @staticmethod
    def take_screenshot(context, scenario):
        status_prefix = 'passed' if scenario.status == Status.passed else 'failed'

        if context.DRIVER_LOCATION == 'browserstack':
            context.driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", '
                f'"arguments": {{"status": "{status_prefix}", "reason": "Results found!"}}}}')
        else:
            try:
                directories = Utilities.paths(context.PLATFORM)
                screenshot_path = Utilities.get_last_report_folder_name(directories[3])
                screenshot_name = f'{screenshot_path}/' \
                                f'{status_prefix.upper()}_{context.scenario.name}.png'
                context.driver.get_screenshot_as_file(screenshot_name)
                allure.attach(context.driver.get_screenshot_as_png(),
                            name=screenshot_name, attachment_type=AttachmentType.PNG)
            finally:
                pass

    @staticmethod
    def start_screen_recording(context):
        context.driver.start_recording_screen()

    @staticmethod
    def stop_video_recording(context, scenario):
        status_prefix = 'passed' if scenario.status == Status.passed else 'failed'
        video = context.driver.stop_recording_screen()
        file_path = Utilities.set_video_path(context, status_prefix)
        with open(file_path, "wb") as vid:
            vid.write(base64.b64decode(video))
        print(f'Video successfully saved at {file_path}')

    @staticmethod
    def join_paths(root_path, paths):
        joined_path = paths[0]

        for folder_name in paths[1:]:
            joined_path = os.path.join(joined_path, folder_name)

        full_path = os.path.join(root_path, joined_path)

        return str(full_path)

    @staticmethod
    def get_date():
        today = date.today().strftime('%d/%m/%Y')
        modified_date = today.replace('/', '')
        return modified_date

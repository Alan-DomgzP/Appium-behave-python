from paver.easy import sh
from utils.utilities import Utilities


class PavementFunctions(object):

    @staticmethod
    def build_command_section(testing_suite, app, platform, device_name, driver_location):
        command = (f'behave --tags={testing_suite} '
                   f'-D app={app} '
                   f'-D platform={platform} '
                   f'-D device_name={device_name} '
                   f'-D driver_location={driver_location} '
                   f'-f allure_behave.formatter::AllureFormatter -f pretty ')

        return command

    # paver run_feature e2e chrome android 11 emulator-5554  test
    @staticmethod
    def run_behave(testing_suite, app, platform, platform_version, device_name, feature, driver_location='local'):
        directories = Utilities.paths(platform)
        Utilities.validate_and_create_directories(directories)
        report_path = Utilities.get_last_report_folder_name(directories[1])

        command = PavementFunctions.build_command_section(testing_suite, app, platform, device_name, driver_location)

        command += f'-D platform_version={platform_version} '
        command += f'-o {report_path} '

        command += f'features/{feature}.feature'

        sh(command)

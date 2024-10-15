from utils.utilities import Utilities

def before_all(context):
    Utilities.set_context_variables(context)
    # Utilities.start_driver(context)

def before_scenario(context, scenario):
    Utilities.start_driver(context)
    Utilities.start_screen_recording(context)

def after_scenario(context, scenario):
    Utilities.take_screenshot(context, scenario)
    Utilities.stop_video_recording(context, scenario)
    context.driver.quit()

def after_all(context):
    # context.driver.quit()
    pass

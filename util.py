import contextlib
import io

from PyQt5.QtWidgets import QApplication


def eval_and_capture_output(code, context={}):
    # Create a string stream to capture output
    output_stream = io.StringIO()

    # Redirect stdout to the string stream
    with contextlib.redirect_stdout(output_stream):
        try:
            # Evaluate the code
            exec(code, context)
        except Exception as e:
            # Print any exception that occurs
            print(f"Error during execution: {e}")

    # Get the content from the stream
    captured_output = output_stream.getvalue()

    return captured_output


def close_app():
    for widget in QApplication.topLevelWidgets():
        widget.close()
    QApplication.instance().quit()


def signal_handler(sig, frame):
    close_app()

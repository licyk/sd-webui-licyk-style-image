from modules import scripts_postprocessing, ui_components
from licyk_style.process import run
from licyk_style.ui import create_ui


class ScriptPostprocessingImageEffect(scripts_postprocessing.ScriptPostprocessing):
    name = "Apply licyk style"
    order = 1000

    def ui(self):
        with ui_components.InputAccordion(False, label="Apply licyk style") as enable:
            controls = create_ui()

        return {"enable": enable, **controls}

    def process(self, pp: scripts_postprocessing.PostprocessedImage, enable, **kwargs):
        if not enable:
            return

        pp.image = run(image=pp.image, **kwargs)

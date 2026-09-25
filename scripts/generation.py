import json
from modules import scripts, ui_components
from licyk_style.process import run
from licyk_style.ui import create_ui, PARAM_NAMES


INFOTEXT_KEY = "Licyk style"


def read_infotext(params: dict, name: str):
    """Reads a filter parameter from the infotext, returns None if not exists"""
    if INFOTEXT_KEY not in params:
        return None
    try:
        return json.loads(params[INFOTEXT_KEY]).get(name)
    except Exception:
        return None


class ScriptLicykStyle(scripts.Script):
    def title(self):
        return "Apply licyk style"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with ui_components.InputAccordion(False, label=self.title()) as enable:
            controls = create_ui()

        self.infotext_fields = [(enable, lambda d: INFOTEXT_KEY in d)] + [
            (component, lambda d, name=name: read_infotext(d, name))
            for name, component in controls.items()
        ]

        return [enable, *controls.values()]

    def process(self, p, enable, *args):
        if not enable:
            return

        p.extra_generation_params[INFOTEXT_KEY] = json.dumps(dict(zip(PARAM_NAMES, args)))

    def postprocess_image_after_composite(self, p, pp: scripts.PostprocessImageArgs, enable, *args):
        """Applies filters to every image after VAE decoding (and inpaint composite)"""
        if not enable:
            return

        mode = pp.image.mode
        image = run(image=pp.image, **dict(zip(PARAM_NAMES, args)))
        pp.image = image if image.mode == mode else image.convert(mode)

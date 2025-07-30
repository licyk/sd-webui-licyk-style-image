from modules import scripts_postprocessing, ui_components
from licyk_style.process import run
import gradio as gr


class ScriptPostprocessingImageEffect(scripts_postprocessing.ScriptPostprocessing):
    name = "Apply licyk style"
    order = 1000

    def ui(self):
        with ui_components.InputAccordion(False, label="Apply licyk style") as enable:
            with gr.Row():
                noise_strength = gr.Slider(minimum=0, maximum=1, step=0.01, label="Noise strength", value=0.4)
                noise_r = gr.Slider(minimum=0, maximum=255, step=1, label="Noise color (R)", value=255)
                noise_g = gr.Slider(minimum=0, maximum=255, step=1, label="Noise color (G)", value=255)
                noise_b = gr.Slider(minimum=0, maximum=255, step=1, label="Noise color (B)", value=255)
                offset_percentage = gr.Slider(minimum=0, maximum=100, step=1, label="Noise color offset", value=20)
                opacity = gr.Slider(minimum=0, maximum=255, step=1, label="Noise opacity", value=128)

            with gr.Row():
                chromatic_strength = gr.Slider(minimum=0, maximum=1, step=0.01, label="Chromatic strength", value=0.3)
                chromatic_blur = gr.Checkbox(label="Blur")

        return {
            "enable": enable,
            "noise_strength": noise_strength,
            "noise_r": noise_r,
            "noise_g": noise_g,
            "noise_b": noise_b,
            "offset_percentage": offset_percentage,
            "opacity": opacity,
            "chromatic_strength": chromatic_strength,
            "chromatic_blur": chromatic_blur,
        }

    def process(self, pp: scripts_postprocessing.PostprocessedImage, enable, noise_strength, noise_r, noise_g, noise_b, offset_percentage, opacity, chromatic_strength, chromatic_blur):
        if not enable:
            return

        img = run(
            image=pp.image,
            noise_strength=noise_strength,
            noise_r=noise_r,
            noise_g=noise_g,
            noise_b=noise_b,
            opacity=opacity,
            offset_percentage=offset_percentage,
            chromatic_strength=chromatic_strength,
            chromatic_blur=chromatic_blur,
        )

        pp.image = img

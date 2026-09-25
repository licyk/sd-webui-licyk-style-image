"""
Gradio UI of licyk style
"""
import gradio as gr


PARAM_NAMES = (
    "noise_strength",
    "noise_r",
    "noise_g",
    "noise_b",
    "offset_percentage",
    "opacity",
    "chromatic_strength",
    "chromatic_blur",
    "glow_strength",
    "glow_threshold",
    "glow_radius",
    "glow_r",
    "glow_g",
    "glow_b",
    "glow_soft_focus",
    "glow_edge_softness",
)
"""Parameter names of the filter controls, in the order of components created by `create_ui`"""


def create_ui() -> dict:
    """
    Creates the filter controls, must be called inside a gradio layout context

    Returns:
        dict: Mapping of parameter names (same as the arguments of `licyk_style.process.run`) to components
    """
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

    with gr.Row():
        glow_strength = gr.Slider(minimum=0, maximum=2, step=0.01, label="Glow strength", value=0)
        glow_threshold = gr.Slider(minimum=0, maximum=1, step=0.01, label="Glow threshold", value=0.6)
        glow_radius = gr.Slider(minimum=0.5, maximum=10, step=0.1, label="Glow radius (%)", value=3)
        glow_r = gr.Slider(minimum=0, maximum=255, step=1, label="Glow color (R)", value=255)
        glow_g = gr.Slider(minimum=0, maximum=255, step=1, label="Glow color (G)", value=240)
        glow_b = gr.Slider(minimum=0, maximum=255, step=1, label="Glow color (B)", value=220)
        glow_soft_focus = gr.Slider(minimum=0, maximum=1, step=0.01, label="Soft focus", value=0.3)
        glow_edge_softness = gr.Slider(minimum=0, maximum=1, step=0.01, label="Edge softness", value=0.2)

    return {
        "noise_strength": noise_strength,
        "noise_r": noise_r,
        "noise_g": noise_g,
        "noise_b": noise_b,
        "offset_percentage": offset_percentage,
        "opacity": opacity,
        "chromatic_strength": chromatic_strength,
        "chromatic_blur": chromatic_blur,
        "glow_strength": glow_strength,
        "glow_threshold": glow_threshold,
        "glow_radius": glow_radius,
        "glow_r": glow_r,
        "glow_g": glow_g,
        "glow_b": glow_b,
        "glow_soft_focus": glow_soft_focus,
        "glow_edge_softness": glow_edge_softness,
    }

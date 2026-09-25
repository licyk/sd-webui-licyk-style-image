import asyncio
import requests
import gradio as gr
from fastapi import FastAPI, Body, UploadFile, File, HTTPException
from io import BytesIO
from PIL import Image
from modules.api.models import *
from modules.api import api
from licyk_style.process import run


def licyk_style_image_api(_: gr.Blocks, app: FastAPI):
    @app.post("/licyk_style_image")
    async def api_run(
        input_image: str = Body("", title="Image for apply licyk style"),
        image_url: str = Body("", title="Image URL for apply licyk style"),
        uploaded_file: UploadFile = File(None),
        noise_strength: float = Body(0.4, title="Noise strength"),
        noise_r: int = Body(255, title="Noise color (R)"),
        noise_g: int = Body(255, title="Noise color (G)"),
        noise_b: int = Body(255, title="Noise color (B)"),
        offset_percentage: int = Body(20, title="Noise color offset"),
        opacity: int = Body(128, title="Noise opacity"),
        chromatic_strength: float = Body(0.3, title="Chromatic strength"),
        chromatic_blur: bool = Body(False, title="Blur"),
        glow_strength: float = Body(0, title="Glow strength"),
        glow_threshold: float = Body(0.6, title="Glow threshold"),
        glow_radius: float = Body(3, title="Glow radius (%)"),
        glow_r: int = Body(255, title="Glow color (R)"),
        glow_g: int = Body(240, title="Glow color (G)"),
        glow_b: int = Body(220, title="Glow color (B)"),
        glow_soft_focus: float = Body(0.3, title="Soft focus"),
        glow_edge_softness: float = Body(0.2, title="Edge softness"),
    ):
        if uploaded_file:
            image_data = await uploaded_file.read()
            img = Image.open(BytesIO(image_data))
        elif image_url:
            try:
                response = await asyncio.to_thread(requests.get, image_url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            except Exception as e:
                raise HTTPException(400, f"Download image failed: {e!s}")
        elif input_image:
            try:
                img = api.decode_base64_to_image(input_image)
            except Exception:
                raise HTTPException(400, "Base64 decode failed")
        else:
            raise HTTPException(400, "Need to provide (File / URL / Base64)")

        img = run(
            image=img,
            noise_strength=noise_strength,
            noise_r=noise_r,
            noise_g=noise_g,
            noise_b=noise_b,
            offset_percentage=offset_percentage,
            opacity=opacity,
            chromatic_strength=chromatic_strength,
            chromatic_blur=chromatic_blur,
            glow_strength=glow_strength,
            glow_threshold=glow_threshold,
            glow_radius=glow_radius,
            glow_r=glow_r,
            glow_g=glow_g,
            glow_b=glow_b,
            glow_soft_focus=glow_soft_focus,
            glow_edge_softness=glow_edge_softness,
        )

        return {"image": api.encode_pil_to_base64(img).decode("utf-8")}

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(licyk_style_image_api)
except Exception:
    pass

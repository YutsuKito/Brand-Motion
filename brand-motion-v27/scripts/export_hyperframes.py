#!/usr/bin/env python3
"""Exporta um manifest Brand Motion para uma composição HyperFrames seekable.

Não instala programas nem executa comandos externos. Use após:
    npx hyperframes init meu-video --example blank
"""
import argparse
import base64
import json
import mimetypes
from pathlib import Path
from validate_project import load

SKILL = Path(__file__).resolve().parents[1]
SOURCE_HTML = SKILL / "engine" / "composition.html"

def as_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

def embed_assets(config: Path, project: dict) -> dict:
    root = config.parent.resolve()
    result = json.loads(json.dumps(project))
    def local_asset(relative: str) -> str:
        source = (root / relative).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError(f"Asset inválido ou fora do projeto: {relative}")
        return as_data_uri(source)
    for scene in result["scenes"]:
        scene["asset"] = local_asset(scene["asset"])
    if result["brand"].get("logo"):
        result["brand"]["logo"] = local_asset(result["brand"]["logo"])
    return result

def export(config: Path, destination: Path, replace: bool, audio: Path | None) -> Path:
    config = config.resolve()
    destination = destination.resolve()
    project, duration, errors, warnings = load(config)
    if errors:
        raise ValueError("; ".join(errors))
    for warning in warnings:
        print("AVISO:", warning)
    if not destination.is_dir() or not (destination / "meta.json").is_file():
        raise ValueError("Crie primeiro o projeto com: npx hyperframes init meu-video --example blank")
    target = destination / "index.html"
    if target.exists() and not replace:
        raise FileExistsError("index.html já existe; faça backup e passe --replace")
    html = SOURCE_HTML.read_text(encoding="utf-8")
    video = project["video"]
    root_tag = (
        '<div id="stage" class="clip" data-composition-id="brand-motion-v27" '
        f'data-start="0" data-duration="{duration:.4f}" data-track-index="0" '
        f'data-width="{video["width"]}" data-height="{video["height"]}">'
    )
    if '<div id="stage">' not in html:
        raise ValueError("Composição base incompatível: #stage não encontrado")
    html = html.replace('<div id="stage">', root_tag, 1)
    payload = json.dumps(embed_assets(config, project), ensure_ascii=False).replace("</", r"<\/")
    audio_html = ""
    if audio is not None:
        audio = audio.resolve()
        if not audio.is_file() or audio.suffix.lower() not in {".wav", ".mp3", ".m4a"}:
            raise ValueError("Áudio inexistente ou formato não suportado (.wav/.mp3/.m4a)")
        out_audio = destination / "assets" / audio.name
        out_audio.parent.mkdir(parents=True, exist_ok=True)
        if audio != out_audio:
            import shutil
            shutil.copy2(audio, out_audio)
        audio_html = (
            f'<audio id="brand-motion-audio" class="clip" data-start="0" '
            f'data-duration="{duration:.4f}" data-track-index="1" '
            f'src="assets/{audio.name}"></audio>'
        )
    protocol = f"""
{audio_html}
<script>
window.initProject({payload});
// Interface seekable documentada pelo HyperFrames; sem depender de tempo de relógio.
window.__hf = {{
  duration: {duration:.4f},
  seek: function(time) {{ window.seek(time); }}
}};
</script>
"""
    html = html.replace("</body>", protocol + "</body>")
    target.write_text(html, encoding="utf-8")
    print(f"HyperFrames: {target}")
    print(f"Duração: {duration:.2f}s | {video['width']}x{video['height']} @ {video['fps']}fps")
    print("Próximos passos (dentro do projeto):")
    print("  npx hyperframes lint")
    print("  npx hyperframes preview")
    print(f"  npx hyperframes render --output final.mp4 --fps {video['fps']} --quality high")
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="manifest.json Brand Motion")
    parser.add_argument("--project", required=True, type=Path, help="projeto já inicializado pelo CLI")
    parser.add_argument("--replace", action="store_true", help="permite substituir index.html existente")
    parser.add_argument("--audio", type=Path, help="faixa com direitos de uso confirmados")
    args = parser.parse_args()
    export(args.config, args.project, args.replace, args.audio)

if __name__ == "__main__":
    main()

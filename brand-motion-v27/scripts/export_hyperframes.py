#!/usr/bin/env python3
"""Exporta um manifest Brand Motion para uma composição HyperFrames seekable.

Não instala programas nem executa comandos externos. Use após:
    npx hyperframes init meu-video --example blank
"""
import argparse
import base64
import json
import mimetypes
import re
import shutil
from pathlib import Path
from validate_project import load

SKILL = Path(__file__).resolve().parents[1]
SOURCE_HTML = SKILL / "engine" / "composition.html"
THREE_SCENE = SKILL / "engine" / "three-scene.js"
RELATIVE_IMPORT = re.compile(r"(?:from\s*|import\s*)[\"'](\.[^\"']+)[\"']")

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

def copy_three_modules(build_dir: Path, assets_dir: Path) -> None:
    """Copy Three.js and its relative build imports locally, preserving module paths."""
    build_dir = build_dir.resolve()
    entry = build_dir / "three.module.js"
    if not entry.is_file():
        raise FileNotFoundError(
            f"Three.js não encontrado em {build_dir}; instale a dependência ou passe --three-build."
        )
    target_root = assets_dir / "three"
    target_root.mkdir(parents=True, exist_ok=True)
    pending = [entry]
    copied: set[Path] = set()
    while pending:
        source = pending.pop().resolve()
        if source in copied:
            continue
        if not source.is_relative_to(build_dir) or not source.is_file():
            raise ValueError(f"Módulo Three.js inválido: {source}")
        relative = source.relative_to(build_dir)
        target = target_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.add(source)
        source_text = source.read_text(encoding="utf-8")
        for specifier in RELATIVE_IMPORT.findall(source_text):
            imported = (source.parent / specifier).resolve()
            if imported.suffix == "":
                imported = imported.with_suffix(".js")
            if not imported.is_file():
                raise FileNotFoundError(f"Import relativo do Three.js não encontrado: {imported}")
            pending.append(imported)

    license_file = build_dir.parent / "LICENSE"
    if license_file.is_file():
        shutil.copy2(license_file, target_root / "LICENSE")

def prepare_local_runtime(project: Path, three_build: Path | None) -> None:
    """Ensure the exported composition can load GSAP and Three.js without network access."""
    assets_dir = project / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    gsap = assets_dir / "gsap.min.js"
    if not gsap.is_file():
        local_gsap = project / "node_modules" / "gsap" / "dist" / "gsap.min.js"
        if not local_gsap.is_file():
            raise FileNotFoundError(
                "GSAP não encontrado localmente. Instale-o após autorização do usuário "
                "ou use o arquivo assets/gsap.min.js criado pelo HyperFrames."
            )
        shutil.copy2(local_gsap, gsap)

    build_dir = three_build or (project / "node_modules" / "three" / "build")
    copy_three_modules(build_dir, assets_dir)
    shutil.copy2(THREE_SCENE, assets_dir / "brand-motion-three.js")

def export(config: Path, destination: Path, replace: bool, audio: Path | None, three_build: Path | None) -> Path:
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
    prepare_local_runtime(destination, three_build)
    html = SOURCE_HTML.read_text(encoding="utf-8")
    video = project["video"]
    root_tag = (
        '<div id="stage" data-composition-id="brand-motion-v27" data-start="0" '
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
    # Coloque a faixa dentro do elemento raiz da composição.
    if audio_html:
        if "</div><script>" not in html:
            raise ValueError("Não foi possível inserir áudio no elemento raiz")
        html = html.replace("</div><script>", audio_html + "</div><script>", 1)
    protocol = f"""
<script>
window.initProject({payload});
// HyperFrames controla a composição por uma timeline GSAP pausada e registrada.
window.__timelines = window.__timelines || {{}};
const brandMotionDriver = {{ time: 0 }};
const brandMotionTimeline = gsap.timeline({{ paused: true }});
brandMotionTimeline.to(brandMotionDriver, {{
  time: {duration:.4f}, duration: {duration:.4f}, ease: "none",
  onUpdate: function() {{ window.seek(brandMotionDriver.time); }}
}});
window.__timelines["brand-motion-v27"] = brandMotionTimeline;
</script>
"""
    html = html.replace("</body>", protocol + "</body>")
    target.write_text(html, encoding="utf-8")
    print(f"HyperFrames: {target}")
    print(f"Duração: {duration:.2f}s | {video['width']}x{video['height']} @ {video['fps']}fps")
    print("Runtime local: HyperFrames + GSAP + Three.js")
    print("Próximos passos (dentro do projeto):")
    print("  npx hyperframes check --json")
    print("  npx hyperframes preview")
    print(f"  npx hyperframes render --output final.mp4 --fps {video['fps']} --quality delivery")
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="manifest.json Brand Motion")
    parser.add_argument("--project", required=True, type=Path, help="projeto já inicializado pelo CLI")
    parser.add_argument("--replace", action="store_true", help="permite substituir index.html existente")
    parser.add_argument("--audio", type=Path, help="faixa com direitos de uso confirmados")
    parser.add_argument("--three-build", type=Path, help="pasta build local do pacote Three.js; padrão: projeto/node_modules/three/build")
    args = parser.parse_args()
    export(args.config, args.project, args.replace, args.audio, args.three_build)

if __name__ == "__main__":
    main()


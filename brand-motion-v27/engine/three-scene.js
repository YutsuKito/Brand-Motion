import * as THREE from "./three/three.module.js";

const clamp = (value, low = 0, high = 1) => Math.max(low, Math.min(high, value));
const smooth = (value) => {
  const t = clamp(value);
  return t * t * (3 - 2 * t);
};

export function createBrandMotionThree(canvas) {
  if (!canvas) throw new Error("Brand Motion V27: #three-stage canvas not found");

  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    preserveDrawingBuffer: true,
  });
  renderer.setPixelRatio(1);
  renderer.setSize(1920, 1080, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1920 / 1080, 0.1, 60);
  camera.position.set(0, 0, 8);

  scene.add(new THREE.AmbientLight(0xffffff, 1.25));
  const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
  keyLight.position.set(-2, 3, 5);
  scene.add(keyLight);
  const rimLight = new THREE.PointLight(0xffffff, 12, 20);
  rimLight.position.set(2.5, -1.2, 3.5);
  scene.add(rimLight);

  const group = new THREE.Group();
  group.position.set(-2.55, -1.18, 0);
  scene.add(group);

  const accent = new THREE.Color("#b58c12");
  const ringMaterial = new THREE.MeshStandardMaterial({
    color: accent,
    metalness: 0.3,
    roughness: 0.32,
    transparent: true,
    opacity: 0.58,
  });
  const coreMaterial = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    emissive: accent,
    emissiveIntensity: 0.28,
    metalness: 0.18,
    roughness: 0.24,
    transparent: true,
    opacity: 0.72,
  });

  const ringA = new THREE.Mesh(new THREE.TorusGeometry(0.78, 0.022, 12, 128), ringMaterial);
  const ringB = new THREE.Mesh(new THREE.TorusGeometry(0.57, 0.016, 10, 128), ringMaterial);
  ringB.rotation.x = Math.PI / 2.35;
  ringB.rotation.y = Math.PI / 5;
  const core = new THREE.Mesh(new THREE.IcosahedronGeometry(0.25, 2), coreMaterial);
  const node = new THREE.Mesh(new THREE.SphereGeometry(0.075, 20, 14), coreMaterial);
  const satellite = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 12), ringMaterial);
  group.add(ringA, ringB, core, node, satellite);

  let lastAccent = "#b58c12";

  function renderAt(time, style = {}) {
    const t = Number.isFinite(time) ? Math.max(0, time) : 0;
    const nextAccent = style.accent || "#b58c12";
    if (nextAccent !== lastAccent) {
      accent.set(nextAccent);
      ringMaterial.color.copy(accent);
      coreMaterial.emissive.copy(accent);
      ringMaterial.needsUpdate = true;
      coreMaterial.needsUpdate = true;
      lastAccent = nextAccent;
    }

    const enter = smooth(t / 0.7);
    const visible = style.visible === false ? 0 : 1;
    const phaseScale = style.phase === "focus" ? 0.88 : 1;
    group.rotation.set(0.22 + t * 0.11, -0.28 + t * 0.18, 0.12 + t * 0.045);
    group.scale.setScalar((0.76 + 0.24 * enter) * phaseScale);
    node.position.set(Math.cos(t * 0.72) * 0.79, Math.sin(t * 0.72) * 0.79, 0.03);
    satellite.position.set(Math.cos(-t * 0.48 + 1.1) * 0.58, 0.02, Math.sin(-t * 0.48 + 1.1) * 0.58);
    ringMaterial.opacity = 0.58 * enter * visible;
    coreMaterial.opacity = 0.72 * enter * visible;
    renderer.render(scene, camera);
  }

  return {
    renderAt,
    dispose() {
      renderer.dispose();
      ringA.geometry.dispose();
      ringB.geometry.dispose();
      core.geometry.dispose();
      node.geometry.dispose();
      satellite.geometry.dispose();
      ringMaterial.dispose();
      coreMaterial.dispose();
    },
  };
}


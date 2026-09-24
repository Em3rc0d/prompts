"use client";

import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

function slabShape() {
  const w = 3.72, h = 2.72, r = .22;
  const shape = new THREE.Shape();
  shape.moveTo(-w / 2 + r, -h / 2);
  shape.lineTo(w / 2 - r, -h / 2);
  shape.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r);
  shape.lineTo(w / 2, h / 2 - r);
  shape.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2);
  shape.lineTo(-w / 2 + r, h / 2);
  shape.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r);
  shape.lineTo(-w / 2, -h / 2 + r);
  shape.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  return shape;
}

const layers = [
  { z: -.98, surface: "#14201e", edge: "#b5d5c6", light: .13, opacity: .28 },
  { z: -.12, surface: "#172e28", edge: "#a2f3c3", light: .36, opacity: .52 },
  { z: .74, surface: "#19352d", edge: "#d5ffe8", light: .7, opacity: .88 }
] as const;

function studioReflection() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 512;
  const ctx = canvas.getContext("2d")!;
  const wash = ctx.createLinearGradient(0, 0, 512, 512);
  wash.addColorStop(0, "rgba(188,255,221,.36)");
  wash.addColorStop(.23, "rgba(113,186,153,.13)");
  wash.addColorStop(.5, "rgba(6,25,20,.02)");
  wash.addColorStop(.83, "rgba(102,191,145,.12)");
  wash.addColorStop(1, "rgba(214,255,231,.21)");
  ctx.fillStyle = wash;
  ctx.fillRect(0, 0, 512, 512);
  const strip = ctx.createLinearGradient(60, 0, 300, 200);
  strip.addColorStop(0, "rgba(240,255,249,0)");
  strip.addColorStop(.46, "rgba(239,255,245,.02)");
  strip.addColorStop(.5, "rgba(239,255,245,.18)");
  strip.addColorStop(.54, "rgba(239,255,245,.02)");
  strip.addColorStop(1, "rgba(239,255,245,0)");
  ctx.fillStyle = strip;
  ctx.fillRect(0, 0, 512, 512);
  for (let x = 26; x < 512; x += 19) {
    for (let y = 30; y < 512; y += 19) {
      ctx.fillStyle = "rgba(183,241,211,.12)";
      ctx.fillRect(x, y, 1, 1);
    }
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

export function CentralStack() {
  const { geometry, rim, innerRim, face } = useMemo(() => {
    const shape = slabShape();
    return {
      geometry: new THREE.ExtrudeGeometry(shape, {
        depth: .07, bevelEnabled: true, bevelSize: .027, bevelThickness: .025,
        bevelSegments: 3, curveSegments: 12, steps: 1
      }),
      rim: new THREE.BufferGeometry().setFromPoints(shape.getPoints(64).map(p => new THREE.Vector3(p.x, p.y, .096))),
      innerRim: new THREE.BufferGeometry().setFromPoints(shape.getPoints(64).map(p => new THREE.Vector3(p.x * .93, p.y * .91, .102))),
      face: new THREE.ShapeGeometry(shape, 12)
    };
  }, []);
  const reflection = useMemo(studioReflection, []);
  const group = useRef<THREE.Group>(null);
  const start = useRef<number | null>(null);
  useFrame(({ clock, invalidate }) => {
    if (!group.current) return;
    if (start.current === null) start.current = clock.elapsedTime;
    const t = Math.min((clock.elapsedTime - start.current) / .55, 1);
    group.current.position.y = -.08 - Math.pow(1 - t, 3) * .22;
    if (t < 1) invalidate();
  });

  return <group ref={group} rotation={[-.9, .06, -.43]} position={[-.06, -.08, .15]} scale={1.2}>
    {layers.map((layer, index) => <group key={layer.z} position={[0, 0, layer.z]}>
      <mesh geometry={geometry}>
        <meshPhysicalMaterial attach="material-0" color={index === 2 ? "#3c5849" : layer.surface} roughness={index === 2 ? .11 : .2}
          metalness={.08} transmission={index === 1 ? .3 : index === 2 ? .16 : .08}
          thickness={.35} ior={1.46} attenuationColor="#75c99f" attenuationDistance={2.6}
          clearcoat={1} clearcoatRoughness={.06} side={THREE.DoubleSide} />
        <meshPhysicalMaterial attach="material-1" color={index === 2 ? "#638d79" : "#315d4a"}
          roughness={.16} metalness={.25} transmission={.28} thickness={.14} ior={1.48}
          clearcoat={1} clearcoatRoughness={.08} emissive="#36a976" emissiveIntensity={layer.light * .23} />
      </mesh>
      <lineLoop geometry={rim}>
        <lineBasicMaterial color={layer.edge} transparent opacity={layer.opacity} depthWrite={false} toneMapped={false} />
      </lineLoop>
      {index === 2 && <>
        <lineLoop geometry={innerRim}>
          <lineBasicMaterial color="#8abda5" transparent opacity={.32} depthWrite={false} />
        </lineLoop>
        <mesh geometry={face} position={[0, 0, .105]}>
          <meshPhysicalMaterial color="#10271e" transparent opacity={.19} roughness={.12}
            metalness={.08} depthWrite={false} clearcoat={1} clearcoatRoughness={.04} />
        </mesh>
        <mesh position={[0, 0, .11]}>
          <planeGeometry args={[3.5, 2.5]} />
          <meshBasicMaterial map={reflection} transparent opacity={.9} depthWrite={false} />
        </mesh>
      </>}
      {index < 2 && <mesh geometry={face} position={[0, 0, -.07]}>
        <meshBasicMaterial color="#56cc91" transparent opacity={index === 0 ? .025 : .055}
          side={THREE.DoubleSide} depthWrite={false} />
      </mesh>}
    </group>)}
    <group position={[0, 0, .865]}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[.54, .54, .04, 64]} />
        <meshPhysicalMaterial color="#071913" roughness={.15} metalness={.28} clearcoat={1} />
      </mesh>
      <mesh position={[0, 0, .035]}>
        <torusGeometry args={[.48, .017, 8, 64]} />
        <meshBasicMaterial color="#b8ffe0" toneMapped={false} />
      </mesh>
      <mesh position={[0, 0, .03]}>
        <circleGeometry args={[.44, 64]} />
        <meshPhysicalMaterial color="#102b20" metalness={.35} roughness={.16} clearcoat={1} />
      </mesh>
      <group position={[0, 0, .055]}>
        <mesh position={[-.145, 0, 0]} rotation={[0, 0, .5]}>
          <boxGeometry args={[.055, .56, .016]} /><meshBasicMaterial color="#c5ffe4" toneMapped={false} />
        </mesh>
        <mesh position={[.145, 0, 0]} rotation={[0, 0, -.5]}>
          <boxGeometry args={[.055, .56, .016]} /><meshBasicMaterial color="#c5ffe4" toneMapped={false} />
        </mesh>
      </group>
    </group>
  </group>;
}

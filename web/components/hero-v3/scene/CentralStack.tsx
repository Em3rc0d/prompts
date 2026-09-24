"use client";

import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

function slabShape() {
  const w = 3.88, h = 2.78, r = .24;
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
  {
    z: -1.28,
    surface: "#101817",
    side: "#20372f",
    edge: "#8ebaa6",
    transmission: .58,
    opacity: .18,
    rimOpacity: .22,
    glow: .018
  },
  {
    z: -.22,
    surface: "#111e1b",
    side: "#294a3d",
    edge: "#a8dec4",
    transmission: .62,
    opacity: .34,
    rimOpacity: .42,
    glow: .038
  },
  {
    z: .84,
    surface: "#14251f",
    side: "#456f5c",
    edge: "#e0ffef",
    transmission: .7,
    opacity: .78,
    rimOpacity: .86,
    glow: .075
  }
] as const;

function studioReflection() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 512;
  const ctx = canvas.getContext("2d")!;

  const base = ctx.createLinearGradient(0, 0, 512, 512);
  base.addColorStop(0, "rgba(240,255,249,.18)");
  base.addColorStop(.18, "rgba(118,184,155,.07)");
  base.addColorStop(.48, "rgba(5,16,14,0)");
  base.addColorStop(.77, "rgba(94,159,134,.055)");
  base.addColorStop(1, "rgba(225,255,240,.12)");
  ctx.fillStyle = base;
  ctx.fillRect(0, 0, 512, 512);

  const highlight = ctx.createLinearGradient(40, 32, 382, 264);
  highlight.addColorStop(0, "rgba(255,255,255,0)");
  highlight.addColorStop(.46, "rgba(244,255,249,.018)");
  highlight.addColorStop(.5, "rgba(244,255,249,.15)");
  highlight.addColorStop(.54, "rgba(244,255,249,.018)");
  highlight.addColorStop(1, "rgba(255,255,255,0)");
  ctx.fillStyle = highlight;
  ctx.fillRect(0, 0, 512, 512);

  for (let x = 24; x < 512; x += 22) {
    for (let y = 28; y < 512; y += 22) {
      ctx.fillStyle = "rgba(187,239,213,.075)";
      ctx.fillRect(x, y, 1, 1);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}

export function CentralStack() {
  const { geometry, rim, innerRim, face } = useMemo(() => {
    const shape = slabShape();
    return {
      geometry: new THREE.ExtrudeGeometry(shape, {
        depth: .035,
        bevelEnabled: true,
        bevelSize: .018,
        bevelThickness: .016,
        bevelSegments: 3,
        curveSegments: 16,
        steps: 1
      }),
      rim: new THREE.BufferGeometry().setFromPoints(
        shape.getPoints(80).map((p) => new THREE.Vector3(p.x, p.y, .061))
      ),
      innerRim: new THREE.BufferGeometry().setFromPoints(
        shape.getPoints(80).map((p) => new THREE.Vector3(p.x * .935, p.y * .91, .067))
      ),
      face: new THREE.ShapeGeometry(shape, 16)
    };
  }, []);

  const reflection = useMemo(studioReflection, []);
  const group = useRef<THREE.Group>(null);
  const start = useRef<number | null>(null);

  useFrame(({ clock, invalidate }) => {
    if (!group.current) return;
    if (start.current === null) start.current = clock.elapsedTime;
    const t = Math.min((clock.elapsedTime - start.current) / .62, 1);
    group.current.position.y = -.05 - Math.pow(1 - t, 3) * .18;
    if (t < 1) invalidate();
  });

  return <group
    ref={group}
    rotation={[-.9, .045, -.43]}
    position={[-.04, -.05, .15]}
    scale={1.2}
  >
    {layers.map((layer, index) => (
      <group key={layer.z} position={[0, 0, layer.z]}>
        <mesh geometry={geometry}>
          <meshPhysicalMaterial
            attach="material-0"
            color={layer.surface}
            transparent
            opacity={layer.opacity}
            roughness={index === 2 ? .085 : .13}
            metalness={.04}
            transmission={layer.transmission}
            thickness={index === 2 ? .32 : .22}
            ior={1.5}
            attenuationColor="#6cb893"
            attenuationDistance={index === 2 ? 2.8 : 3.8}
            clearcoat={1}
            clearcoatRoughness={.035}
            side={THREE.DoubleSide}
            depthWrite={index === 2}
          />
          <meshPhysicalMaterial
            attach="material-1"
            color={layer.side}
            transparent
            opacity={Math.min(layer.opacity + .16, .92)}
            roughness={.12}
            metalness={.12}
            transmission={Math.max(layer.transmission - .15, .22)}
            thickness={.12}
            ior={1.48}
            attenuationColor="#70b99a"
            attenuationDistance={2.4}
            clearcoat={1}
            clearcoatRoughness={.045}
            emissive="#2d8a62"
            emissiveIntensity={index === 2 ? .035 : .018}
          />
        </mesh>

        <lineLoop geometry={rim}>
          <lineBasicMaterial
            color={layer.edge}
            transparent
            opacity={layer.rimOpacity}
            depthWrite={false}
            toneMapped={false}
          />
        </lineLoop>

        <mesh geometry={face} position={[0, 0, -.018]}>
          <meshBasicMaterial
            color="#65e6a9"
            transparent
            opacity={layer.glow}
            side={THREE.DoubleSide}
            depthWrite={false}
            toneMapped={false}
          />
        </mesh>

        <mesh geometry={face} position={[0, 0, -.058]}>
          <meshBasicMaterial
            color="#8ff1bf"
            transparent
            opacity={index === 0 ? .012 : index === 1 ? .022 : .032}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>

        {index === 2 && <>
          <lineLoop geometry={innerRim}>
            <lineBasicMaterial
              color="#9bcdb4"
              transparent
              opacity={.28}
              depthWrite={false}
            />
          </lineLoop>
          <mesh geometry={face} position={[0, 0, .069]}>
            <meshPhysicalMaterial
              color="#0b1714"
              transparent
              opacity={.16}
              roughness={.07}
              metalness={.03}
              transmission={.5}
              thickness={.12}
              ior={1.48}
              depthWrite={false}
              clearcoat={1}
              clearcoatRoughness={.02}
            />
          </mesh>
          <mesh position={[0, 0, .073]}>
            <planeGeometry args={[3.62, 2.53]} />
            <meshBasicMaterial
              map={reflection}
              transparent
              opacity={.72}
              depthWrite={false}
            />
          </mesh>
        </>}
      </group>
    ))}

    <group position={[0, 0, .958]}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[.5, .5, .028, 64]} />
        <meshPhysicalMaterial
          color="#07110e"
          transparent
          opacity={.9}
          transmission={.22}
          roughness={.09}
          metalness={.18}
          clearcoat={1}
          clearcoatRoughness={.03}
        />
      </mesh>
      <mesh position={[0, 0, .03]}>
        <torusGeometry args={[.445, .012, 8, 64]} />
        <meshBasicMaterial color="#caffdf" toneMapped={false} />
      </mesh>
      <mesh position={[0, 0, .027]}>
        <circleGeometry args={[.41, 64]} />
        <meshPhysicalMaterial
          color="#0a2118"
          transparent
          opacity={.72}
          transmission={.18}
          metalness={.2}
          roughness={.1}
          clearcoat={1}
          clearcoatRoughness={.03}
        />
      </mesh>
      <group position={[0, 0, .05]}>
        <mesh position={[-.137, 0, 0]} rotation={[0, 0, .5]}>
          <boxGeometry args={[.045, .52, .012]} />
          <meshBasicMaterial color="#d3ffea" toneMapped={false} />
        </mesh>
        <mesh position={[.137, 0, 0]} rotation={[0, 0, -.5]}>
          <boxGeometry args={[.045, .52, .012]} />
          <meshBasicMaterial color="#d3ffea" toneMapped={false} />
        </mesh>
      </group>
    </group>
  </group>;
}

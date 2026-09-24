export function SceneLighting() {
  return <>
    <ambientLight intensity={.32} color="#b5c7c1" />
    <directionalLight position={[2.7, 5, 5]} intensity={1.85} color="#aaffd0" />
    <directionalLight position={[-4, 1.7, 4]} intensity={3.7} color="#f0f8f4" />
    <pointLight position={[0, -1.5, -1]} intensity={6} distance={7} decay={2} color="#42c487" />
  </>;
}

export function SceneLighting() {
  return <>
    <ambientLight intensity={.14} color="#9fb1ab" />
    <directionalLight position={[-3.4, 4.5, 4.6]} intensity={1.85} color="#d8eee4" />
    <directionalLight position={[4.7, 1.7, 2.6]} intensity={2.1} color="#f4f8f6" />
    <directionalLight position={[-2.2, -3.2, 1.3]} intensity={.48} color="#8fc9ae" />
    <pointLight position={[.25, -.72, .35]} intensity={2.85} distance={4.4} decay={2.2} color="#5ce5a4" />
    <pointLight position={[1.85, 1.72, 1.8]} intensity={1.15} distance={3.8} decay={2.1} color="#e9fff3" />
  </>;
}

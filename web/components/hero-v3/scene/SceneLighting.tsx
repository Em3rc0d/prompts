export function SceneLighting() {
  return <>
    <ambientLight intensity={.22} color="#a4b6b0" />
    <directionalLight position={[-3, 4.2, 4]} intensity={2.3} color="#adffd4" />
    <directionalLight position={[4.5, 1.5, 2.2]} intensity={2.5} color="#edf7f2" />
    <directionalLight position={[-1.5, -3, 1.6]} intensity={.65} color="#a9e9d0" />
    <pointLight position={[.4, -1.1, .1]} intensity={5.2} distance={5} decay={2} color="#45e59d" />
    <pointLight position={[1.8, 1.6, 1.5]} intensity={2} distance={4} decay={2} color="#caffdf" />
  </>;
}

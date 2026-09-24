"use client";

import dynamic from "next/dynamic";
import { Component, useEffect, useRef, useState, type ReactNode } from "react";

const HeroCanvas = dynamic(() => import("./VerluneHeroCanvas.client"), { ssr: false });

class CanvasBoundary extends Component<{ children: ReactNode; onFailed: () => void }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  componentDidCatch() { this.props.onFailed(); }
  render() { return this.state.failed ? null : this.props.children; }
}

export function HeroCanvasGate() {
  const host = useRef<HTMLDivElement>(null);
  const [enabled, setEnabled] = useState(false);
  const [ready, setReady] = useState(false);
  const [medium, setMedium] = useState(false);

  useEffect(() => {
    const desktop = window.matchMedia("(min-width: 900px)");
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
    let visible = false;
    let webgl: boolean | undefined;
    const update = () => {
      const eligible = desktop.matches && !reduced.matches && visible;
      if (eligible && webgl === undefined) {
        try { webgl = !!document.createElement("canvas").getContext("webgl2"); }
        catch { webgl = false; }
      }
      setMedium(window.innerWidth < 1200);
      setEnabled(eligible && webgl === true);
    };
    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      update();
    }, { rootMargin: "160px" });
    if (host.current) observer.observe(host.current);
    desktop.addEventListener("change", update);
    reduced.addEventListener("change", update);
    return () => {
      observer.disconnect();
      desktop.removeEventListener("change", update);
      reduced.removeEventListener("change", update);
    };
  }, []);

  return <div ref={host} className={`vHero3Runtime${ready && enabled ? " vHero3Runtime--ready" : ""}`} aria-hidden="true">
    {enabled ? <CanvasBoundary onFailed={() => setReady(false)}><HeroCanvas medium={medium} onReady={() => setReady(true)} /></CanvasBoundary> : null}
  </div>;
}

import { DependencyList, RefObject, useEffect } from "react";
import anime from "animejs/lib/anime.es.js";

export { anime };

export function useAnimePage(ref: RefObject<HTMLElement>, deps: DependencyList = []) {
  useEffect(() => {
    const root = ref.current;
    if (!root) return;

    const fadeUp = root.querySelectorAll("[data-anime='fade-up']");
    const fadeLeft = root.querySelectorAll("[data-anime='fade-left']");
    const fadeRight = root.querySelectorAll("[data-anime='fade-right']");
    const scale = root.querySelectorAll("[data-anime='scale']");

    const tl = anime.timeline({
      easing: "easeOutExpo",
      duration: 800
    });

    if (fadeUp.length) {
      tl.add(
        {
          targets: fadeUp,
          opacity: [0, 1],
          translateY: [32, 0],
          delay: anime.stagger(90)
        },
        0
      );
    }

    if (fadeLeft.length) {
      tl.add(
        {
          targets: fadeLeft,
          opacity: [0, 1],
          translateX: [-40, 0],
          delay: anime.stagger(90)
        },
        80
      );
    }

    if (fadeRight.length) {
      tl.add(
        {
          targets: fadeRight,
          opacity: [0, 1],
          translateX: [40, 0],
          delay: anime.stagger(90)
        },
        80
      );
    }

    if (scale.length) {
      tl.add(
        {
          targets: scale,
          opacity: [0, 1],
          scale: [0.92, 1],
          delay: anime.stagger(80)
        },
        120
      );
    }

    return () => {
      anime.remove(root.querySelectorAll("[data-anime]"));
    };
  }, deps);
}

export function animeShake(target: HTMLElement | null) {
  if (!target) return;

  anime({
    targets: target,
    translateX: [-10, 10, -8, 8, -4, 4, 0],
    duration: 450,
    easing: "easeInOutSine"
  });
}

export function animePop(target: HTMLElement | null) {
  if (!target) return;

  anime({
    targets: target,
    scale: [1, 1.15, 1],
    duration: 320,
    easing: "easeOutBack"
  });
}
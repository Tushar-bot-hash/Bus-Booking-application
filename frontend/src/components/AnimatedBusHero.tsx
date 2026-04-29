import { useEffect, useRef } from "react";
import { anime } from "../hooks/useAnimePage";

export default function AnimatedBusHero() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;

    anime({
      targets: root.querySelector(".bus-body"),
      translateY: [-6, 6],
      direction: "alternate",
      loop: true,
      duration: 1500,
      easing: "easeInOutSine"
    });

    anime({
      targets: root.querySelectorAll(".wheel"),
      rotate: 360,
      loop: true,
      duration: 950,
      easing: "linear"
    });

    anime({
      targets: root.querySelectorAll(".road-dash"),
      translateX: [-40, 40],
      opacity: [0.2, 1, 0.2],
      delay: anime.stagger(120),
      loop: true,
      duration: 900,
      easing: "linear"
    });

    anime({
      targets: root.querySelectorAll(".floating-dot"),
      translateY: [-12, 12],
      direction: "alternate",
      delay: anime.stagger(160),
      loop: true,
      duration: 1800,
      easing: "easeInOutSine"
    });

    return () => anime.remove(root.querySelectorAll("*"));
  }, []);

  return (
    <div ref={ref} className="relative mx-auto h-[360px] w-full max-w-xl">
      <div className="floating-dot absolute left-12 top-10 h-5 w-5 rounded-full bg-primary/20" />
      <div className="floating-dot absolute right-20 top-16 h-8 w-8 rounded-full bg-green-300/30" />
      <div className="floating-dot absolute bottom-24 left-20 h-6 w-6 rounded-full bg-primary/20" />

      <div className="bus-body absolute left-1/2 top-20 w-[88%] -translate-x-1/2 rounded-[2rem] bg-primary p-5 shadow-2xl">
        <div className="absolute -top-6 left-10 rounded-t-3xl bg-primaryDark px-8 py-4 text-white shadow-lg">
          GreenBus
        </div>

        <div className="grid grid-cols-4 gap-3 pt-8">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((x) => (
            <div key={x} className="h-14 rounded-xl bg-white/90 shadow-inner" />
          ))}
        </div>

        <div className="mt-5 flex items-center justify-between">
          <div className="rounded-xl bg-white px-4 py-2 font-bold text-primaryDark">
            INDIA
          </div>
          <div className="h-5 w-16 rounded-full bg-yellow-300" />
        </div>

        <div className="wheel absolute -bottom-9 left-16 h-20 w-20 rounded-full border-[10px] border-dark bg-white">
          <div className="mx-auto mt-[18px] h-5 w-5 rounded-full bg-primary" />
        </div>

        <div className="wheel absolute -bottom-9 right-16 h-20 w-20 rounded-full border-[10px] border-dark bg-white">
          <div className="mx-auto mt-[18px] h-5 w-5 rounded-full bg-primary" />
        </div>
      </div>

      <div className="absolute bottom-10 left-1/2 flex w-[80%] -translate-x-1/2 justify-between">
        {[1, 2, 3, 4, 5, 6].map((x) => (
          <div key={x} className="road-dash h-2 w-12 rounded-full bg-primaryDark/40" />
        ))}
      </div>
    </div>
  );
}
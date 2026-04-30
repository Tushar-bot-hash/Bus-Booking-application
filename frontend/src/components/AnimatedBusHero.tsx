import { useEffect, useRef } from "react";
import { anime } from "../hooks/useAnimePage";

export default function AnimatedBusHero() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;

    // Bus body bounce
    anime({
      targets: root.querySelector(".bus-body"),
      translateY: [-6, 6],
      direction: "alternate",
      loop: true,
      duration: 1500,
      easing: "easeInOutSine"
    });

    // Rotating wheels
    anime({
      targets: root.querySelectorAll(".wheel"),
      rotate: 360,
      loop: true,
      duration: 950,
      easing: "linear"
    });

    // Moving road dashes
    anime({
      targets: root.querySelectorAll(".road-dash"),
      translateX: [-40, 40],
      opacity: [0.2, 1, 0.2],
      delay: anime.stagger(120),
      loop: true,
      duration: 900,
      easing: "linear"
    });

    return () => anime.remove(root.querySelectorAll("*"));
  }, []);

  return (
    <div className="w-full py-12"> 
      {/* 
          IMPORTANT: removed 'overflow-hidden' from this wrapper 
          so the wheels and the 'GreenBus' label can breathe.
      */}
      <div 
        ref={ref} 
        className="relative mx-auto h-[400px] w-full max-w-xl flex items-center justify-center"
      >
        {/* Floating Decorative Elements */}
        <div className="absolute left-10 top-10 h-5 w-5 rounded-full bg-primary/20" />
        <div className="absolute right-10 top-20 h-8 w-8 rounded-full bg-green-300/30" />

        {/* 
            The Bus Body: 
            Increased padding and added 'relative' to handle wheel offsets 
        */}
        <div className="bus-body relative w-[85%] rounded-[2.5rem] bg-primary p-6 shadow-2xl">
          
          {/* Top Label (The 'Roof' sign) */}
          <div className="absolute -top-7 left-10 rounded-t-3xl bg-primaryDark px-8 py-4 text-white font-bold shadow-lg">
            GreenBus
          </div>

          {/* Windows */}
          <div className="grid grid-cols-4 gap-3 pt-8">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="h-14 rounded-xl bg-white/90 shadow-inner" />
            ))}
          </div>

          {/* Bottom Banner Area */}
          <div className="mt-6 flex items-center justify-between">
            <div className="rounded-xl bg-white px-5 py-2 font-black text-primaryDark tracking-tighter">
              INDIA
            </div>
            <div className="h-5 w-20 rounded-full bg-yellow-300 shadow-glow" />
          </div>

          {/* Wheels: Positioned to overlap the bottom edge but NOT get cut off */}
          <div className="wheel absolute -bottom-10 left-12 h-20 w-20 rounded-full border-[10px] border-grayDark bg-white shadow-lg">
            <div className="mx-auto mt-[18px] h-5 w-5 rounded-full bg-primary" />
          </div>

          <div className="wheel absolute -bottom-10 right-12 h-20 w-20 rounded-full border-[10px] border-grayDark bg-white shadow-lg">
            <div className="mx-auto mt-[18px] h-5 w-5 rounded-full bg-primary" />
          </div>
        </div>

        {/* Road indicators below the wheels */}
        <div className="absolute bottom-4 left-1/2 flex w-[60%] -translate-x-1/2 justify-between">
          {[1, 2, 3, 4].map((x) => (
            <div key={x} className="road-dash h-2 w-12 rounded-full bg-primaryDark/20" />
          ))}
        </div>
      </div>
    </div>
  );
}
import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { anime } from "../hooks/useAnimePage";

export default function NotFound() {
  const cardRef = useRef<HTMLDivElement>(null);
  const busRef = useRef<HTMLDivElement>(null);
  const numberRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    anime.timeline({ easing: "easeOutExpo" })
      .add({
        targets: cardRef.current,
        opacity: [0, 1],
        translateY: [35, 0],
        scale: [0.92, 1],
        duration: 800
      })
      .add(
        {
          targets: numberRef.current,
          opacity: [0, 1],
          scale: [0.5, 1.1, 1],
          duration: 900,
          easing: "easeOutBack"
        },
        150
      );

    anime({
      targets: busRef.current,
      translateX: [-18, 18],
      translateY: [-4, 4],
      rotate: [-2, 2],
      direction: "alternate",
      loop: true,
      duration: 1400,
      easing: "easeInOutSine"
    });
  }, []);

  return (
    <div className="animated-green-bg flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-12">
      <div
        ref={cardRef}
        className="card relative w-full max-w-xl overflow-hidden text-center opacity-0"
      >
        <div className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-primary/10 blur-2xl" />
        <div className="absolute -bottom-16 -left-16 h-40 w-40 rounded-full bg-green-300/20 blur-2xl" />

        <div ref={busRef} className="relative mx-auto mb-5 text-6xl">
          🚌
        </div>

        <h1
          ref={numberRef}
          className="relative text-7xl font-extrabold text-primaryDark opacity-0"
        >
          404
        </h1>

        <h2 className="relative mt-4 text-2xl font-bold text-dark">
          Oops! Route Not Found
        </h2>

        <p className="relative mx-auto mt-3 max-w-md text-gray-600">
          Looks like this bus route does not exist. Go back home and search for a valid journey.
        </p>

        <div className="relative mt-8 flex flex-col justify-center gap-3 sm:flex-row">
          <Link to="/" className="btn-primary">
            Search Buses
          </Link>

          <Link to="/my-bookings" className="btn-secondary">
            My Bookings
          </Link>
        </div>
      </div>
    </div>
  );
}
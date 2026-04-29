import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { anime } from "../hooks/useAnimePage";

export default function BookingCancel() {
  const ref = useRef<HTMLDivElement>(null);
  const iconRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    anime({
      targets: ref.current,
      opacity: [0, 1],
      translateY: [25, 0],
      scale: [0.94, 1],
      duration: 700,
      easing: "easeOutExpo"
    });

    anime({
      targets: iconRef.current,
      translateX: [-8, 8, -6, 6, 0],
      delay: 300,
      duration: 500,
      easing: "easeInOutSine"
    });
  }, []);

  return (
    <div className="flex min-h-[calc(100vh-80px)] items-center justify-center bg-gradient-to-br from-red-50 to-white px-4">
      <div ref={ref} className="card max-w-lg text-center opacity-0">
        <div ref={iconRef} className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-100 text-4xl text-red-600">
          !
        </div>

        <h1 className="mt-6 text-3xl font-extrabold text-red-600">Payment Cancelled</h1>

        <p className="mt-3 text-gray-600">
          Your payment was cancelled. You can try booking again.
        </p>

        <div className="mt-8 flex justify-center gap-3">
          <Link to="/" className="btn-primary">
            Search Again
          </Link>
          <Link to="/my-bookings" className="btn-secondary">
            My Bookings
          </Link>
        </div>
      </div>
    </div>
  );
}
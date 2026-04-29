import { useEffect, useRef } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { anime } from "../hooks/useAnimePage";

export default function BookingSuccess() {
  const ref = useRef<HTMLDivElement>(null);
  const checkRef = useRef<HTMLDivElement>(null);
  const [params] = useSearchParams();
  const booking = params.get("booking");

  useEffect(() => {
    anime.timeline({ easing: "easeOutExpo" })
      .add({
        targets: ref.current,
        opacity: [0, 1],
        scale: [0.9, 1],
        duration: 700
      })
      .add({
        targets: checkRef.current,
        rotate: [0, 360],
        scale: [0.5, 1.1, 1],
        duration: 800,
        easing: "easeOutBack"
      }, 100);
  }, []);

  return (
    <div className="animated-green-bg flex min-h-[calc(100vh-80px)] items-center justify-center px-4">
      <div ref={ref} className="card max-w-lg text-center opacity-0">
        <div ref={checkRef} className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-primary text-4xl text-white">
          ✓
        </div>

        <h1 className="mt-6 text-3xl font-extrabold text-primaryDark">Payment Successful</h1>

        <p className="mt-3 text-gray-600">
          Your payment is being verified. Your ticket will appear after webhook confirmation.
        </p>

        {booking && <p className="mt-4 text-sm text-gray-500">Booking ID: {booking}</p>}

        <div className="mt-8 flex justify-center gap-3">
          <Link to="/my-bookings" className="btn-primary">
            My Bookings
          </Link>
          <Link to="/" className="btn-secondary">
            Home
          </Link>
        </div>
      </div>
    </div>
  );
}
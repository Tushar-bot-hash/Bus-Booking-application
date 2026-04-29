import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { anime, useAnimePage } from "../hooks/useAnimePage";
import AnimatedBusHero from "../components/AnimatedBusHero";

function tomorrowDate() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split("T")[0];
}

export default function Home() {
  const pageRef = useRef<HTMLElement>(null);
  useAnimePage(pageRef);

  const navigate = useNavigate();
  const [origin, setOrigin] = useState("Delhi");
  const [destination, setDestination] = useState("Jaipur");
  const [date, setDate] = useState(tomorrowDate());

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    navigate(
      `/search?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(
        destination
      )}&date=${date}`
    );
  }

  function animateButton(e: React.MouseEvent<HTMLButtonElement>) {
    anime({
      targets: e.currentTarget,
      scale: [1, 0.96, 1],
      duration: 280,
      easing: "easeOutBack"
    });
  }

  return (
    <main ref={pageRef}>
      <section className="animated-green-bg relative min-h-[calc(100vh-80px)] overflow-hidden">
        <div className="glow-orb -right-20 -top-20 h-80 w-80 bg-primary/30" />
        <div className="glow-orb -bottom-20 -left-20 h-80 w-80 bg-green-300/30" />

        <div className="mx-auto grid max-w-7xl items-center gap-10 px-4 py-16 lg:grid-cols-2">
          <div>
            <div
              data-anime="fade-up"
              className="mb-4 inline-flex rounded-full bg-white px-4 py-2 text-sm font-semibold text-primary shadow-soft"
            >
              🇮🇳 Animated Secure Bus Booking Across India
            </div>

            <h1
              data-anime="fade-up"
              className="text-5xl font-extrabold leading-tight text-dark md:text-6xl"
            >
              Book your bus ticket with{" "}
              <span className="text-primary">style</span>, speed and trust.
            </h1>

            <p data-anime="fade-up" className="mt-6 max-w-xl text-lg text-gray-600">
              Search routes, select animated seats, pay securely with Stripe, and download your PNR ticket instantly.
            </p>

            <div data-anime="fade-up" className="mt-8 flex flex-wrap gap-3 text-sm">
              <span className="badge bg-green-100 text-primaryDark">Secure Cookies</span>
              <span className="badge bg-green-100 text-primaryDark">Anime.js UI</span>
              <span className="badge bg-green-100 text-primaryDark">INR Payments</span>
              <span className="badge bg-green-100 text-primaryDark">PNR Ticket</span>
            </div>
          </div>

          <div data-anime="scale">
            <AnimatedBusHero />
          </div>

          <div data-anime="fade-up" className="card lg:col-span-2">
            <h2 className="mb-1 text-2xl font-bold text-primaryDark">Search Buses</h2>
            <p className="mb-6 text-sm text-gray-500">Find available buses for your journey.</p>

            <form onSubmit={handleSearch} className="grid gap-4 md:grid-cols-[1fr_1fr_1fr_auto] md:items-end">
              <div>
                <label className="mb-1 block text-sm font-semibold text-gray-700">From</label>
                <input value={origin} onChange={(e) => setOrigin(e.target.value)} required />
              </div>

              <div>
                <label className="mb-1 block text-sm font-semibold text-gray-700">To</label>
                <input value={destination} onChange={(e) => setDestination(e.target.value)} required />
              </div>

              <div>
                <label className="mb-1 block text-sm font-semibold text-gray-700">Travel Date</label>
                <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
              </div>

              <button onMouseDown={animateButton} className="btn-primary">
                Search Buses
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>
  );
}
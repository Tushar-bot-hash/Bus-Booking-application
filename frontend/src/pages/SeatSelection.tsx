import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";
import type { Schedule, Seat } from "../types";
import { anime, animePop, animeShake, useAnimePage } from "../hooks/useAnimePage";

export default function SeatSelection() {
  const pageRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);
  const summaryRef = useRef<HTMLDivElement>(null);

  useAnimePage(pageRef);

  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [schedule, setSchedule] = useState<Schedule | null>(null);
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [passengerName, setPassengerName] = useState("");
  const [passengerPhone, setPassengerPhone] = useState("");
  const [passengerEmail, setPassengerEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      const res = await api.get(`/search/schedules/${id}/seats/`);
      setSchedule(res.data.schedule);
      setSeats(res.data.seats);

      if (user) {
        setPassengerName(`${user.first_name} ${user.last_name}`);
        setPassengerPhone(user.phone || "");
        setPassengerEmail(user.email);
      }
    }

    load();
  }, [id, user]);

  useEffect(() => {
    if (gridRef.current && seats.length) {
      anime({
        targets: gridRef.current.querySelectorAll(".seat-btn"),
        opacity: [0, 1],
        scale: [0.75, 1],
        delay: anime.stagger(25),
        duration: 520,
        easing: "easeOutBack"
      });
    }
  }, [seats.length]);

  useEffect(() => {
    animePop(summaryRef.current);
  }, [selected.length]);

  useEffect(() => {
    if (error) animeShake(errorRef.current);
  }, [error]);

  const selectedSeats = useMemo(
    () => seats.filter((seat) => selected.includes(seat.seat_number)),
    [seats, selected]
  );

  const baseAmount = selectedSeats.reduce((sum, seat) => sum + Number(seat.price), 0);
  const gst = baseAmount * 0.05;
  const total = baseAmount + gst;

  function toggleSeat(seat: Seat, target: HTMLElement) {
    if (seat.status !== "available") return;

    animePop(target);

    if (selected.includes(seat.seat_number)) {
      setSelected(selected.filter((s) => s !== seat.seat_number));
    } else {
      if (selected.length >= 6) {
        setError("You can select a maximum of 6 seats.");
        return;
      }
      setError("");
      setSelected([...selected, seat.seat_number]);
    }
  }

  function seatClass(seat: Seat) {
    if (selected.includes(seat.seat_number)) {
      return "bg-primary text-white border-primary scale-105";
    }

    if (seat.status === "available") {
      return "bg-white text-primaryDark border-green-200 hover:bg-primaryLight hover:scale-105";
    }

    if (seat.status === "held") {
      return "bg-yellow-100 text-yellow-700 border-yellow-200 cursor-not-allowed";
    }

    return "bg-gray-200 text-gray-400 border-gray-300 cursor-not-allowed";
  }

 async function handlePay() {
  setError("");

  if (!selected.length) {
    setError("Please select at least one seat.");
    return;
  }

  if (!passengerName || !passengerPhone || !passengerEmail) {
    setError("Please fill passenger details.");
    return;
  }

  setBusy(true);

  try {
    const bookingRes = await api.post("/booking/create/", {
      schedule_id: Number(id),
      seat_numbers: selected,
      passenger_name: passengerName,
      passenger_phone: passengerPhone,
      passenger_email: passengerEmail
    });

    const bookingId = bookingRes.data.id;

    const payRes = await api.post(`/booking/${bookingId}/pay/`);

    window.location.href = payRes.data.checkout_url;
  } catch (err: any) {
    setError(err.response?.data?.detail || "Unable to create payment.");
    setBusy(false);
  }
}

  if (!schedule) {
    return (
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  const isSleeper =
    schedule.bus.bus_type.includes("sleeper") || schedule.bus.bus_type.includes("luxury");

  return (
    <div ref={pageRef} className="mx-auto grid max-w-7xl gap-8 px-4 py-10 lg:grid-cols-[1.3fr_0.7fr]">
      <div data-anime="fade-left" className="card">
        <h1 className="text-3xl font-extrabold text-primaryDark">Animated Seat Selection</h1>
        <p className="mt-2 text-gray-500">
          {schedule.bus.route.origin} to {schedule.bus.route.destination} · {schedule.bus.name}
        </p>

        <div className="mt-6 flex flex-wrap gap-3 text-sm">
          <span className="badge bg-white text-primaryDark ring-1 ring-green-200">Available</span>
          <span className="badge bg-primary text-white">Selected</span>
          <span className="badge bg-gray-200 text-gray-500">Booked</span>
          <span className="badge bg-yellow-100 text-yellow-700">Held</span>
        </div>

        <div className="mt-8 rounded-3xl border border-green-100 bg-green-50/60 p-5">
          <div className="mb-6 flex justify-end">
            <div className="rounded-xl bg-dark px-4 py-2 text-sm font-bold text-white">Driver</div>
          </div>

          <div
            ref={gridRef}
            className={`grid gap-3 ${isSleeper ? "grid-cols-3 md:max-w-md" : "grid-cols-4 md:max-w-xl"}`}
          >
            {seats.map((seat) => (
              <button
                key={seat.id}
                onClick={(e) => toggleSeat(seat, e.currentTarget)}
                className={`seat-btn ${seatClass(seat)}`}
              >
                {seat.seat_number}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div data-anime="fade-right" className="card h-fit">
        <h2 className="text-2xl font-bold text-primaryDark">Passenger Details</h2>

        <div className="mt-5 space-y-4">
          <div>
            <label className="mb-1 block text-sm font-semibold">Passenger Name</label>
            <input value={passengerName} onChange={(e) => setPassengerName(e.target.value)} />
          </div>

          <div>
            <label className="mb-1 block text-sm font-semibold">Phone</label>
            <input value={passengerPhone} onChange={(e) => setPassengerPhone(e.target.value)} />
          </div>

          <div>
            <label className="mb-1 block text-sm font-semibold">Email</label>
            <input value={passengerEmail} onChange={(e) => setPassengerEmail(e.target.value)} />
          </div>
        </div>

        <div ref={summaryRef} className="mt-6 rounded-2xl bg-primaryLight p-4">
          <div className="flex justify-between text-sm">
            <span>Selected Seats</span>
            <strong>{selected.length ? selected.join(", ") : "None"}</strong>
          </div>

          <div className="mt-3 flex justify-between text-sm">
            <span>Base Amount</span>
            <strong>₹{baseAmount.toFixed(2)}</strong>
          </div>

          <div className="mt-3 flex justify-between text-sm">
            <span>GST 5%</span>
            <strong>₹{gst.toFixed(2)}</strong>
          </div>

          <div className="mt-4 flex justify-between border-t border-green-200 pt-4 text-lg">
            <span className="font-bold">Total</span>
            <strong className="text-primaryDark">₹{total.toFixed(2)}</strong>
          </div>
        </div>

        {error && (
          <div ref={errorRef} className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <button onClick={handlePay} disabled={busy} className="btn-primary mt-6 w-full disabled:opacity-60">
          {busy ? "Redirecting to payment..." : "Pay Securely"}
        </button>
      </div>
    </div>
  );
}
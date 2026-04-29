import { useEffect, useRef, useState } from "react";
import api from "../api/client";
import type { Booking } from "../types";
import { anime, useAnimePage } from "../hooks/useAnimePage";

export default function MyBookings() {
  const pageRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  useAnimePage(pageRef);

  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try {
      const res = await api.get("/my-bookings/");
      setBookings(res.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (!loading && listRef.current) {
      anime({
        targets: listRef.current.querySelectorAll(".booking-card"),
        opacity: [0, 1],
        translateY: [30, 0],
        delay: anime.stagger(90),
        duration: 700,
        easing: "easeOutExpo"
      });
    }
  }, [loading, bookings.length]);

  async function cancelBooking(id: string) {
    if (!confirm("Are you sure you want to cancel this booking?")) return;
    await api.post(`/my-bookings/${id}/cancel/`);
    await load();
  }

  function downloadTicket(id: string) {
    window.open(`${import.meta.env.VITE_API_URL}/my-bookings/${id}/ticket-pdf/`, "_blank");
  }

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div ref={pageRef} className="mx-auto max-w-7xl px-4 py-10">
      <div data-anime="fade-up">
        <h1 className="text-3xl font-extrabold text-primaryDark">My Bookings</h1>
        <p className="mt-2 text-gray-500">View your tickets, PNR, and booking status.</p>
      </div>

      {bookings.length === 0 ? (
        <div data-anime="scale" className="card mt-8 text-center">
          <h2 className="text-xl font-bold">No bookings yet</h2>
          <p className="mt-2 text-gray-500">Book your first journey today.</p>
        </div>
      ) : (
        <div ref={listRef} className="mt-8 grid gap-5">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-card card">
              <div className="grid gap-5 md:grid-cols-[1.3fr_1fr_auto] md:items-center">
                <div>
                  <h2 className="text-xl font-bold">
                    {booking.schedule.bus.route.origin} to {booking.schedule.bus.route.destination}
                  </h2>

                  <p className="mt-1 text-sm text-gray-500">
                    {booking.schedule.bus.name} · PNR:{" "}
                    <span className="font-bold text-primaryDark">
                      {booking.pnr_number || booking.reference_code}
                    </span>
                  </p>

                  <p className="mt-2 text-sm text-gray-500">
                    Seats: {booking.seats.map((s) => s.seat_number).join(", ")}
                  </p>
                </div>

                <div>
                  <p className="text-sm text-gray-500">Total Amount</p>
                  <p className="text-2xl font-extrabold text-primary">₹{booking.total_amount}</p>

                  <span
                    className={`badge mt-2 inline-block ${
                      booking.status === "confirmed"
                        ? "bg-green-100 text-primaryDark"
                        : booking.status === "pending"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-red-50 text-red-600"
                    }`}
                  >
                    {booking.status.toUpperCase()}
                  </span>
                </div>

                <div className="flex flex-col gap-3">
                  {booking.status === "confirmed" && (
                    <button onClick={() => downloadTicket(booking.id)} className="btn-primary">
                      Download Ticket
                    </button>
                  )}

                  {(booking.status === "pending" || booking.status === "confirmed") && (
                    <button onClick={() => cancelBooking(booking.id)} className="btn-secondary">
                      Cancel
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
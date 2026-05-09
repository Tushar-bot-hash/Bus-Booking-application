import { useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import api from "../api/client";
import type { Schedule } from "../types";
import { anime, useAnimePage } from "../hooks/useAnimePage";

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short"
  });
}

export default function SearchResults() {
  const pageRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const [params] = useSearchParams();
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);
  useAnimePage(pageRef, [loading]);

  const origin = params.get("origin") || "";
  const destination = params.get("destination") || "";
  const date = params.get("date") || "";

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await api.get("/search/", {
          params: { origin, destination, date }
        });
        setSchedules(res.data);
      } catch (error) {
        console.error("Search error:", error);
        setSchedules([]);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [origin, destination, date]);

  useEffect(() => {
    if (!loading && listRef.current && schedules.length > 0) {
      anime({
        targets: listRef.current.querySelectorAll(".result-card"),
        opacity: [0, 1],
        translateY: [35, 0],
        delay: anime.stagger(90),
        duration: 750,
        easing: "easeOutExpo"
      });
    }
  }, [loading, schedules.length]);

  return (
    <div ref={pageRef} className="mx-auto max-w-7xl px-4 py-10">
      <div data-anime="fade-up">
        <h1 className="text-3xl font-extrabold text-primaryDark">
          {origin} to {destination}
        </h1>
        <p className="mt-2 text-gray-500">Available buses for {date}</p>
      </div>

      {loading ? (
        <div className="mt-10 grid gap-5">
          {[1, 2, 3].map((i) => (
            <div key={i} className="card shimmer h-36 bg-white" />
          ))}
        </div>
      ) : schedules.length === 0 ? (
        <div data-anime="scale" className="card mt-10 text-center">
          <h2 className="text-xl font-bold">No buses found</h2>
          <p className="mt-2 text-gray-500">Try another route or date.</p>
          <Link to="/" className="btn-primary mt-6 inline-block">
            Search Again
          </Link>
        </div>
      ) : (
        <div ref={listRef} className="mt-8 grid gap-5">
          {schedules.map((schedule) => (
            <div key={schedule.id} className="result-card card">
              <div className="grid gap-5 md:grid-cols-[1.5fr_1fr_1fr_auto] md:items-center">
                <div>
                  <h2 className="text-xl font-bold text-dark">{schedule.bus?.name || "Bus"}</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    {schedule.bus?.operator?.name || "Bus Operator"} · {schedule.bus?.bus_type || "Standard"} · {schedule.bus?.bus_number || "N/A"}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {schedule.bus?.amenities?.ac && <span className="badge bg-green-100 text-primaryDark">AC</span>}
                    {schedule.bus?.amenities?.wifi && <span className="badge bg-green-100 text-primaryDark">WiFi</span>}
                    {schedule.bus?.amenities?.charging && <span className="badge bg-green-100 text-primaryDark">Charging</span>}
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-500">Departure</p>
                  <p className="font-bold">{formatDateTime(schedule.departure_time)}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-500">Fare</p>
                  <p className="text-2xl font-extrabold text-primary">₹{schedule.base_fare}</p>
                  <p className="text-sm text-gray-500">{schedule.available_seats} seats left</p>
                </div>

                <Link to={`/schedule/${schedule.id}/seats`} className="btn-primary text-center">
                  Select Seats
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";
import { anime } from "../hooks/useAnimePage";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    anime({
      targets: ref.current,
      translateY: [-70, 0],
      opacity: [0, 1],
      duration: 700,
      easing: "easeOutExpo"
    });
  }, []);

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <header
      ref={ref}
      className="sticky top-0 z-50 border-b border-green-100 bg-white/85 backdrop-blur-xl"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-xl text-white shadow-soft">
            🚌
          </div>
          <div>
            <div className="text-lg font-extrabold text-primaryDark">GreenBus</div>
            <div className="text-xs text-gray-500">India Bus Booking</div>
          </div>
        </Link>

        <nav className="hidden items-center gap-6 md:flex">
          <NavLink to="/" className="font-medium text-gray-700 hover:text-primary">
            Home
          </NavLink>

          {user && (
            <NavLink to="/my-bookings" className="font-medium text-gray-700 hover:text-primary">
              My Bookings
            </NavLink>
          )}
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden text-sm text-gray-600 sm:inline">
                Hi, {user.first_name}
              </span>
              <button onClick={handleLogout} className="btn-secondary py-2">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary py-2">
                Login
              </Link>
              <Link to="/register" className="btn-primary py-2">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
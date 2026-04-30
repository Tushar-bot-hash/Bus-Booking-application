import { Link, NavLink, useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";
import { anime } from "../hooks/useAnimePage";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    // Smooth slide-down entry for the navbar
    anime({
      targets: ref.current,
      translateY: [-70, 0],
      opacity: [0, 1],
      duration: 800,
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
      className="sticky top-0 z-50 border-b border-green-100 bg-white/90 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        {/* Logo Section */}
        <Link to="/" className="flex items-center gap-3 transition-transform hover:scale-105 active:scale-95">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary text-2xl text-white shadow-soft">
            🚌
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-black leading-none text-primaryDark tracking-tight">
              GreenBus
            </span>
            <span className="text-[10px] font-bold uppercase tracking-widest text-primary/70">
              India
            </span>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden items-center gap-8 md:flex">
          <NavLink 
            to="/" 
            className={({ isActive }) => 
              `text-sm font-semibold transition-colors hover:text-primary ${
                isActive ? "text-primary" : "text-gray-600"
              }`
            }
          >
            Home
          </NavLink>

          {user && (
            <NavLink 
              to="/my-bookings" 
              className={({ isActive }) => 
                `text-sm font-semibold transition-colors hover:text-primary ${
                  isActive ? "text-primary" : "text-gray-600"
                }`
              }
            >
              My Bookings
            </NavLink>
          )}
        </nav>

        {/* Auth Actions */}
        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-4">
              <div className="hidden flex-col items-end sm:flex">
                <span className="text-[10px] font-bold uppercase text-gray-400">Welcome</span>
                <span className="text-sm font-bold text-gray-800">
                  {user.first_name}
                </span>
              </div>
              <button 
                onClick={handleLogout} 
                className="rounded-xl border border-red-100 bg-red-50 px-5 py-2.5 text-sm font-bold text-red-600 transition-all hover:bg-red-600 hover:text-white active:scale-95"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link 
                to="/login" 
                className="rounded-xl px-5 py-2.5 text-sm font-bold text-gray-600 transition-colors hover:bg-gray-50 active:scale-95"
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="rounded-xl bg-primary px-6 py-2.5 text-sm font-bold text-white shadow-soft transition-all hover:bg-primaryDark hover:shadow-lg active:scale-95"
              >
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
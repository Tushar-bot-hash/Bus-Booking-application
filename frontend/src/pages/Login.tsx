import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { animeShake, useAnimePage } from "../hooks/useAnimePage";

export default function Login() {
  const pageRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);
  useAnimePage(pageRef);

  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (error) animeShake(errorRef.current);
  }, [error]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);

    try {
      await login(email, password);
      navigate("/");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invalid email or password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      ref={pageRef}
      className="animated-green-bg flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-12"
    >
      <div data-anime="scale" className="card w-full max-w-md">
        <div data-anime="fade-up" className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-3xl bg-primary text-3xl text-white shadow-soft">
          🔐
        </div>

        <h1 data-anime="fade-up" className="text-center text-3xl font-extrabold text-primaryDark">
          Welcome Back
        </h1>

        <p data-anime="fade-up" className="mt-2 text-center text-gray-500">
          Login securely to book your next journey.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>

          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>

          {error && (
            <div ref={errorRef} className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          <button disabled={busy} className="btn-primary w-full disabled:opacity-60">
            {busy ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          New here?{" "}
          <Link to="/register" className="font-semibold text-primary">
            Create account
          </Link>
        </p>
      </div>
    </div>
  );
}
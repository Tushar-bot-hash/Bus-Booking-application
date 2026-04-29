import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { anime, animeShake, useAnimePage } from "../hooks/useAnimePage";

function strength(password: string) {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  return score;
}

export default function Register() {
  const pageRef = useRef<HTMLDivElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);
  const barRef = useRef<HTMLDivElement>(null);
  useAnimePage(pageRef);

  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    password_confirm: ""
  });

  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const score = strength(form.password);

  useEffect(() => {
    anime({
      targets: barRef.current,
      width: `${score * 25}%`,
      duration: 450,
      easing: "easeOutExpo"
    });
  }, [score]);

  useEffect(() => {
    if (error) animeShake(errorRef.current);
  }, [error]);

  function update(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (form.password !== form.password_confirm) {
      setError("Passwords do not match.");
      return;
    }

    setBusy(true);

    try {
      await register(form);
      navigate("/");
    } catch (err: any) {
      const data = err.response?.data;
      setError(data?.detail || data?.email?.[0] || data?.password?.[0] || "Registration failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      ref={pageRef}
      className="animated-green-bg flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-12"
    >
      <div data-anime="scale" className="card w-full max-w-2xl">
        <div data-anime="fade-up" className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-3xl bg-primary text-3xl text-white shadow-soft">
          ✨
        </div>

        <h1 data-anime="fade-up" className="text-center text-3xl font-extrabold text-primaryDark">
          Create Account
        </h1>

        <p data-anime="fade-up" className="mt-2 text-center text-gray-500">
          Register securely and start booking.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 grid gap-4 md:grid-cols-2">
          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">First Name</label>
            <input name="first_name" value={form.first_name} onChange={update} required />
          </div>

          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">Last Name</label>
            <input name="last_name" value={form.last_name} onChange={update} required />
          </div>

          <div data-anime="fade-up" className="md:col-span-2">
            <label className="mb-1 block text-sm font-semibold">Email</label>
            <input type="email" name="email" value={form.email} onChange={update} required />
          </div>

          <div data-anime="fade-up" className="md:col-span-2">
            <label className="mb-1 block text-sm font-semibold">Indian Phone Number</label>
            <input name="phone" value={form.phone} onChange={update} placeholder="9876543210" />
          </div>

          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">Password</label>
            <input type="password" name="password" value={form.password} onChange={update} required />

            <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
              <div
                ref={barRef}
                className={`h-full ${
                  score <= 1 ? "bg-red-500" : score <= 2 ? "bg-yellow-500" : "bg-primary"
                }`}
                style={{ width: "0%" }}
              />
            </div>
          </div>

          <div data-anime="fade-up">
            <label className="mb-1 block text-sm font-semibold">Confirm Password</label>
            <input
              type="password"
              name="password_confirm"
              value={form.password_confirm}
              onChange={update}
              required
            />
          </div>

          {error && (
            <div ref={errorRef} className="md:col-span-2 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          )}

          <button disabled={busy} className="btn-primary md:col-span-2 disabled:opacity-60">
            {busy ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-primary">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
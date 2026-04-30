import React from 'react'; // Add this to the top of the file causing the error
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";


import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import SearchResults from "./pages/SearchResults";
import SeatSelection from "./pages/SeatSelection";
import MyBookings from "./pages/MyBookings";
import BookingSuccess from "./pages/BookingSuccess";
import BookingCancel from "./pages/BookingCancel";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <BrowserRouter>
      {/* 
        The outer div uses 'min-h-screen' to ensure the background 
        always covers the full page, and 'overflow-x-hidden' to 
        prevent the animated bus from causing a horizontal scrollbar.
      */}
      <div className="relative min-h-screen w-full overflow-x-hidden bg-graySoft/30">
        <Navbar />

        {/* 
          Main content area with a fade-in animation for page changes.
          'pt-4' provides a little breathing room under the sticky navbar.
        */}
        <main className="animate-fadeIn pt-4 pb-20">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchResults />} />

            <Route
              path="/schedule/:id/seats"
              element={
                <ProtectedRoute>
                  <SeatSelection />
                </ProtectedRoute>
              }
            />

            <Route
              path="/my-bookings"
              element={
                <ProtectedRoute>
                  <MyBookings />
                </ProtectedRoute>
              }
            />

            <Route path="/booking/success" element={<BookingSuccess />} />
            <Route path="/booking/cancel" element={<BookingCancel />} />

            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Catch-all for 404 pages */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        {/* 
          Optional: You could add a Footer component here 
          to make the site look even more complete! 
        */}
      </div>
    </BrowserRouter>
  );
}
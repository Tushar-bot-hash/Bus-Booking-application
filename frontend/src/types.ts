export interface Seat {
  id: number;
  seat_number: string;
  status: "available" | "booked" | "held" | "blocked";
  price: number;
}

export interface Schedule {
  id: number;
  bus?: {
    id: number;
    name: string;
    bus_number: string;
    bus_type?: string;
    route?: {
      origin: string;
      destination: string;
    };
    operator?: {
      id: number;
      name: string;
    };
    amenities?: {
      ac?: boolean;
      wifi?: boolean;
      charging?: boolean;
    };
  };
  departure_time: string;
  arrival_time: string;
  base_fare: number;
  available_seats: number;
  origin: string;
  destination: string;
}

export interface Booking {
  id: string;
  reference_code: string;
  pnr_number?: string;
  schedule_details: Schedule;
  seat_numbers: string[];
  seats: Seat[]; // Fallback for components still using seats
  passenger_name: string;
  passenger_phone: string;
  passenger_email?: string;
  total_amount: number;
  status: "pending" | "confirmed" | "cancelled" | "expired" | "refunded";
  created_at: string;
}
export type CustomerStatus = 'lead' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
export type EventType = 'engagement' | 'haldi' | 'sangeet' | 'wedding' | 'reception' | 'other';

export interface Payment {
  id: string;
  amount: number;
  method?: string;
  paid_on?: string;
  remarks?: string;
  created_at: string;
}

export interface Note {
  id: string;
  content: string;
  created_at: string;
}

export interface Customer {
  id: string;
  name: string;
  phone: string;
  email?: string;
  partner_name?: string;
  event_type: EventType;
  event_date?: string;
  venue?: string;
  guest_count?: string;
  budget?: number;
  status: CustomerStatus;
  source?: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerDetail extends Customer {
  payments: Payment[];
  notes: Note[];
}

export type CustomerCreate = Omit<Customer, 'id' | 'created_at' | 'updated_at'>;

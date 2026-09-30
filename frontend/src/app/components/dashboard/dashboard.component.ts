import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { Customer } from '../../models/customer.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  customers: Customer[] = [];
  loading = true;

  constructor(private customerService: CustomerService) {}

  ngOnInit(): void {
    this.customerService.list().subscribe({
      next: (data) => { this.customers = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }

  countByStatus(status: string): number {
    return this.customers.filter((c) => c.status === status).length;
  }

  get upcoming(): Customer[] {
    const today = new Date().toISOString().slice(0, 10);
    return this.customers
      .filter((c) => c.event_date && c.event_date >= today)
      .sort((a, b) => (a.event_date! > b.event_date! ? 1 : -1))
      .slice(0, 5);
  }
}

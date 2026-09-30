import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { Customer } from '../../models/customer.model';

@Component({
  selector: 'app-customer-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './customer-list.component.html',
})
export class CustomerListComponent implements OnInit {
  customers: Customer[] = [];
  search = '';
  status = '';
  loading = true;

  statuses = ['lead', 'confirmed', 'in_progress', 'completed', 'cancelled'];

  constructor(private customerService: CustomerService) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.customerService.list(this.search || undefined, this.status || undefined).subscribe({
      next: (data) => { this.customers = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }

  remove(c: Customer, event: Event): void {
    event.stopPropagation();
    if (!confirm(`Delete ${c.name}?`)) return;
    this.customerService.delete(c.id).subscribe(() => this.fetch());
  }
}

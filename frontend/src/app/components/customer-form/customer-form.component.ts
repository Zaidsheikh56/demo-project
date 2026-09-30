import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { CustomerDetail } from '../../models/customer.model';

@Component({
  selector: 'app-customer-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './customer-form.component.html',
})
export class CustomerFormComponent implements OnInit {
  id: string | null = null;
  detail: CustomerDetail | null = null;
  newNote = '';
  newPaymentAmount: number | null = null;
  newPaymentMethod = 'cash';

  eventTypes = ['engagement', 'haldi', 'sangeet', 'wedding', 'reception', 'other'];
  statuses = ['lead', 'confirmed', 'in_progress', 'completed', 'cancelled'];

  form = this.fb.group({
    name: ['', Validators.required],
    phone: ['', Validators.required],
    email: [''],
    partner_name: [''],
    event_type: ['wedding', Validators.required],
    event_date: [''],
    venue: [''],
    guest_count: [''],
    budget: [null as number | null],
    status: ['lead', Validators.required],
    source: [''],
  });

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private customerService: CustomerService,
  ) {}

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    if (this.id) this.load();
  }

  load(): void {
    if (!this.id) return;
    this.customerService.get(this.id).subscribe((detail) => {
      this.detail = detail;
      this.form.patchValue(detail);
    });
  }

  save(): void {
    if (this.form.invalid) return;
    const payload = this.form.value as any;
    if (this.id) {
      this.customerService.update(this.id, payload).subscribe(() => this.load());
    } else {
      this.customerService.create(payload).subscribe((c) => this.router.navigate(['/customers', c.id]));
    }
  }

  addNote(): void {
    if (!this.id || !this.newNote.trim()) return;
    this.customerService.addNote(this.id, this.newNote.trim()).subscribe(() => {
      this.newNote = '';
      this.load();
    });
  }

  addPayment(): void {
    if (!this.id || !this.newPaymentAmount) return;
    this.customerService
      .addPayment(this.id, { amount: this.newPaymentAmount, method: this.newPaymentMethod })
      .subscribe(() => {
        this.newPaymentAmount = null;
        this.load();
      });
  }

  get totalPaid(): number {
    return (this.detail?.payments || []).reduce((sum, p) => sum + Number(p.amount), 0);
  }
}

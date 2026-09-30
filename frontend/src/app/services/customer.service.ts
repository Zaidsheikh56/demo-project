import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Customer, CustomerCreate, CustomerDetail, Note, Payment } from '../models/customer.model';

@Injectable({ providedIn: 'root' })
export class CustomerService {
  private base = `${environment.apiUrl}/customers`;

  constructor(private http: HttpClient) {}

  list(search?: string, status?: string): Observable<Customer[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (status) params = params.set('status', status);
    return this.http.get<Customer[]>(this.base, { params });
  }

  get(id: string): Observable<CustomerDetail> {
    return this.http.get<CustomerDetail>(`${this.base}/${id}`);
  }

  create(payload: CustomerCreate): Observable<Customer> {
    return this.http.post<Customer>(this.base, payload);
  }

  update(id: string, payload: Partial<CustomerCreate>): Observable<Customer> {
    return this.http.put<Customer>(`${this.base}/${id}`, payload);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }

  addPayment(id: string, payload: Partial<Payment>): Observable<Payment> {
    return this.http.post<Payment>(`${this.base}/${id}/payments`, payload);
  }

  addNote(id: string, content: string): Observable<Note> {
    return this.http.post<Note>(`${this.base}/${id}/notes`, { content });
  }
}

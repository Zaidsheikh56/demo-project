import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <header class="topbar">
      <a routerLink="/" class="brand">💍 Shaadi CRM</a>
      <nav>
        <a routerLink="/customers">Customers</a>
        <a routerLink="/customers/new">+ New Customer</a>
      </nav>
    </header>
    <main class="container">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    .topbar {
      display: flex; justify-content: space-between; align-items: center;
      padding: 1rem 1.5rem; background: #6b1e2b; color: #fff;
    }
    .brand { font-weight: 600; font-size: 1.2rem; text-decoration: none; color: #fff; }
    nav a { color: #f6e9d8; text-decoration: none; margin-left: 1.2rem; font-size: 0.9rem; }
    nav a:hover { text-decoration: underline; }
  `],
})
export class AppComponent {}

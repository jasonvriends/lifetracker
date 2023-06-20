import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../features/header.component';
import { MenuComponent } from '../features/menu.component';
import { FooterComponent } from '../features/footer.component';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-default',
  standalone: true,
  imports: [CommonModule, HeaderComponent, MenuComponent, FooterComponent, RouterOutlet],
  template: `
  <div class="page">
    <app-header></app-header>
    <app-menu></app-menu>
    <div class="page-wrapper">
      <div class="page-body">
        <router-outlet></router-outlet>
      </div>
      <footer class="footer footer-transparent d-print-none">
        <app-footer></app-footer>
      </footer>
    </div>
  </div>
  `,
  styles: [
  ]
})
export class DefaultComponent {

}

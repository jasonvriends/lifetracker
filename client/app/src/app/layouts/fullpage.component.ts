import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-fullpage',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="page page-center">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [
  ]
})
export class FullpageComponent {

}

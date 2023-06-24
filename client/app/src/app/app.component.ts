import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <router-outlet></router-outlet>
  `,
  styles: [],
})
export class AppComponent {
  title = 'app';

  constructor() {
    
    if (environment.production) {
      console.log('Angular app started: production');
    } else {
      console.log('Angular app started: development');
    }
  }

}
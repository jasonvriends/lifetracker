import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-default',
  standalone: true,
  imports: [CommonModule],
  template: `
    <p>
      default works!
    </p>
  `,
  styles: [
  ]
})
export class DefaultComponent {

}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  template: `
<div class="container-xl">
  <div class="row text-center align-items-center flex-row-reverse">
    <div class="col-lg-auto ms-lg-auto">
      <ul class="list-inline list-inline-dots mb-0">
        <li class="list-inline-item">
          <a
            href="/privacy"
            target="_blank"
            class="link-secondary"
            rel="noopener"
            >Privacy Policy</a
          >
        </li>     
      </ul>
    </div>
    <div class="col-12 col-lg-auto mt-3 mt-lg-0">
      <ul class="list-inline list-inline-dots mb-0">
        <li class="list-inline-item">
          Copyright © {{ currentYear }}
          <a href="." class="link-secondary">Lifetracker</a>. All rights
          reserved.
        </li>
        <li class="list-inline-item">
          <a class="link-secondary" rel="noopener"> v1.0.0-beta1 </a>
        </li>
      </ul>
    </div>
  </div>
</div>

  `,
  styles: [
  ]
})
export class FooterComponent {

  currentYear: number = new Date().getFullYear();

}

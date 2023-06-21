import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
<header class="navbar-expand-md">
  <div class="collapse navbar-collapse" id="navbar-menu">
    <div class="navbar">
      <div class="container-xl">
        <ul class="navbar-nav">
          <li
            class="nav-item"
            [routerLink]="['/']"
            queryParamsHandling="merge"
            [routerLinkActive]="['active']"
            [routerLinkActiveOptions]="{ exact: true }"
          >
            <a class="nav-link" href="/">
              <span class="nav-link-icon d-md-none d-lg-inline-block"
                ><!-- Download SVG icon from http://tabler-icons.io/i/home -->
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="icon"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>
                  <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>
                  <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path>
                </svg>
              </span>
              <span class="nav-link-title"> Home </span>
            </a>
          </li>
          <li
            class="nav-item"
            [routerLink]="['/about']"
            [routerLinkActive]="['active']"
            [routerLinkActiveOptions]="{ exact: true }"
          >
            <a class="nav-link" href="/about">
              <span class="nav-link-icon d-md-none d-lg-inline-block"
                ><!-- Download SVG icon from http://tabler-icons.io/i/home -->
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="icon icon-tabler icon-tabler-layout-dashboard"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M4 4h6v8h-6z"></path>
                  <path d="M4 16h6v4h-6z"></path>
                  <path d="M14 12h6v8h-6z"></path>
                  <path d="M14 4h6v4h-6z"></path>
                </svg>
              </span>
              <span class="nav-link-title"> About </span>
            </a>
          </li>          
          <li
            class="nav-item"
            [routerLink]="['/dashboard']"
            [routerLinkActive]="['active']"
            [routerLinkActiveOptions]="{ exact: true }"
          >
            <a class="nav-link" href="/dashboard">
              <span class="nav-link-icon d-md-none d-lg-inline-block"
                ><!-- Download SVG icon from http://tabler-icons.io/i/home -->
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="icon icon-tabler icon-tabler-layout-dashboard"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M4 4h6v8h-6z"></path>
                  <path d="M4 16h6v4h-6z"></path>
                  <path d="M14 12h6v8h-6z"></path>
                  <path d="M14 4h6v4h-6z"></path>
                </svg>
              </span>
              <span class="nav-link-title"> Dashboard </span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</header>

  `,
  styles: [
  ]
})
export class MenuComponent {

}

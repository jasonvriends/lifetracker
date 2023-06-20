import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';
import { ColorSchemeService } from '../services/colorscheme.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
  ],
  template: `

  <header class="navbar navbar-expand-md d-print-none">
  <div class="container-xl">
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbar-menu"
      aria-controls="navbar-menu"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <h1
      class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3"
    >
      <a href=".">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon icon-tabler icon-tabler-activity-heartbeat"
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
          <path d="M3 12h4.5l1.5 -6l4 12l2 -9l1.5 3h4.5"></path>
        </svg>
        Lifetracker
      </a>
    </h1>
    <div class="navbar-nav flex-row order-md-last">
      <div class="d-none d-md-flex">
        <a
          href=""
          (click)="$event.preventDefault(); toggleTheme();"
          class="nav-link px-0 hide-theme-dark"
          data-bs-toggle="tooltip"
          data-bs-placement="bottom"
          aria-label="Enable dark mode"
          data-bs-original-title="Enable dark mode"
        >
          <!-- Download SVG icon from http://tabler-icons.io/i/moon -->
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
            <path
              d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"
            ></path>
          </svg>
        </a>
        <a
          href=""
          (click)="$event.preventDefault(); toggleTheme()"
          class="nav-link px-0 hide-theme-light"
          data-bs-toggle="tooltip"
          data-bs-placement="bottom"
          aria-label="Enable light mode"
          data-bs-original-title="Enable light mode"
        >
          <!-- Download SVG icon from http://tabler-icons.io/i/sun -->
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
            <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path>
            <path
              d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"
            ></path>
          </svg>
        </a>
      </div>

      <!-- logged in-->
      <div *ngIf="isLoggedIn" class="nav-item dropdown">
        <a
          href="#"
          class="nav-link d-flex lh-1 text-reset p-0"
          data-bs-toggle="dropdown"
          aria-label="Open user menu"
        >
          <span class="avatar avatar-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-user-circle"
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
              <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
              <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
              <path
                d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855"
              ></path>
            </svg>
          </span>
          <div class="d-none d-xl-block ps-2">
            <div>{{ claims?.fields.name }}</div>
            <div class="mt-1 small text-muted">Free User</div>
          </div>
        </a>

        <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
          <a href="#" class="dropdown-item">Dashboard</a>
          <a href="./settings.html" class="dropdown-item">Settings</a>
          <div class="dropdown-divider"></div>
          <a
            href=""
            (click)="$event.preventDefault(); loginOrLogout()"
            class="dropdown-item"
            >Logout</a
          >
        </div>

        <div
          *ngIf="!isLoggedIn"
          class="dropdown-menu dropdown-menu-end dropdown-menu-arrow"
        >
          <a
            href=""
            (click)="$event.preventDefault(); loginOrLogout()"
            class="dropdown-item"
            >{{ isLoggedIn ? "Logout" : "Login" }}</a
          >
          <a
            href="https://thevriends.fief.dev/lifetracker/register"
            class="dropdown-item"
            >Register</a
          >
        </div>
      </div>

      <!-- not logged in-->

      <div *ngIf="!isLoggedIn" class="nav-item dropdown">
        <a
          href="#"
          class="nav-link d-flex lh-1 text-reset p-0"
          data-bs-toggle="dropdown"
          aria-label="Open user menu"
        >
          <span class="avatar avatar-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-user-circle"
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
              <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
              <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
              <path
                d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855"
              ></path>
            </svg>
          </span>
        </a>

        <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
          <a
            href=""
            (click)="$event.preventDefault(); loginOrLogout()"
            class="dropdown-item"
            >Login</a
          >
          <a
            href="https://thevriends.fief.dev/lifetracker/register"
            class="dropdown-item"
            >Register</a
          >
        </div>
      </div>
    </div>
  </div>
</header>

  `,
  styles: [
  ]
})
export class HeaderComponent {

  constructor(
    private colorSchemeService: ColorSchemeService,
    private authService: AuthService
  ) {  }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  loginOrLogout(): void {
    this.authService.handleLoginClick();
  }

  toggleTheme(): void {
    this.colorSchemeService.toggleTheme();
  }

  get claims(): any {
    return this.authService.claims;
  }

}

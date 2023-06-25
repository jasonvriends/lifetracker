import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ColorSchemeService } from '../services/colorscheme.service';
import { CookieConsentService } from '../services/cookieconsent.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'layout-default',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="page">
      
      <!-- Navbar -->
      <header class="navbar navbar-expand-md d-print-none">
        <div class="container-xl">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu" aria-controls="navbar-menu" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <h1 class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-jacket" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
            <path d="M16 3l-4 5l-4 -5"></path>
            <path d="M12 19a2 2 0 0 1 -2 2h-4a2 2 0 0 1 -2 -2v-8.172a2 2 0 0 1 .586 -1.414l.828 -.828a2 2 0 0 0 .586 -1.414v-2.172a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v2.172a2 2 0 0 0 .586 1.414l.828 .828a2 2 0 0 1 .586 1.414v8.172a2 2 0 0 1 -2 2h-4a2 2 0 0 1 -2 -2z"></path>
            <path d="M20 13h-3a1 1 0 0 0 -1 1v2a1 1 0 0 0 1 1h3"></path>
            <path d="M4 17h3a1 1 0 0 0 1 -1v-2a1 1 0 0 0 -1 -1h-3"></path>
            <path d="M12 19v-11"></path>
            </svg>  
            <a href=".">
                Lifetracker
            </a>
          </h1>
          <div class="navbar-nav flex-row order-md-last">
            <div class="d-none d-md-flex">
              <a (click)="$event.preventDefault(); toggleTheme()" href="" class="nav-link px-0 hide-theme-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable dark mode" data-bs-original-title="Enable dark mode">
                <!-- Download SVG icon from http://tabler-icons.io/i/moon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path></svg>
              </a>
              <a (click)="$event.preventDefault(); toggleTheme()" href="" class="nav-link px-0 hide-theme-light" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable light mode" data-bs-original-title="Enable light mode">
                <!-- Download SVG icon from http://tabler-icons.io/i/sun -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path><path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"></path></svg>
              </a>
              <div class="nav-item dropdown d-none d-md-flex me-3">
              </div>
            </div>
            <div class="nav-item dropdown">
              <a href="#" class="nav-link d-flex lh-1 text-reset p-0" data-bs-toggle="dropdown" aria-label="Open user menu">
                <span class="avatar avatar-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-user-circle" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                  <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
                  <path d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855"></path>
                  </svg>
                </span>
                <div *ngIf="isLoggedIn" class="d-none d-xl-block ps-2">
                  <div>{{ claims?.fields.name}}</div>
                  <div class="mt-1 small text-muted">Free User</div>
                </div>
              </a>
              <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
                <a (click)="$event.preventDefault(); loginOrLogout()" href="" class="dropdown-item">{{ isLoggedIn ? 'Sign Out' : 'Sign In' }}</a>
                <a *ngIf="!isLoggedIn" href="https://thevriends.fief.dev/lifetracker/register" class="dropdown-item">Sign Up</a>
              </div>
            </div>
          </div>
          <div class="collapse navbar-collapse" id="navbar-menu">
            <div class="d-flex flex-column flex-md-row flex-fill align-items-stretch align-items-md-center">
              <ul class="navbar-nav">
                <li class="nav-item active">
                  <a class="nav-link" href="./">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler-icons.io/i/home -->
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-layout-dashboard" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M4 4h6v8h-6z"></path>
                        <path d="M4 16h6v4h-6z"></path>
                        <path d="M14 12h6v8h-6z"></path>
                        <path d="M14 4h6v4h-6z"></path>
                      </svg>
                    </span>
                    <span class="nav-link-title">
                      Dashboard
                    </span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </header>

      <!-- Page -->
      <div class="page-wrapper">
        
        <router-outlet></router-outlet>
        
        <!-- cookie consent -->
        <div *ngIf="!hasConsented()" class="offcanvas offcanvas-bottom h-auto show" tabindex="-1" id="offcanvasBottom" aria-modal="true" role="dialog" data-bs-backdrop="static" data-bs-keyboard="false">
          <div class="offcanvas-body">
            <div class="container">
              <div class="row align-items-center">
                <div class="col">
                  <strong>Do you like cookies?</strong> 🍪 We use cookies on this site to improve your experience as explained in our Cookie Policy. You can reject cookies by changing your browser settings. <a href="/privacy" target="_blank">Learn more</a>
                </div>
                <div class="col-auto">
                  <button (click)="setConsent(true)" type="button" class="btn btn-primary" data-bs-dismiss="offcanvas">
                    Allow Cookies
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- footer -->
        <footer class="footer footer-transparent d-print-none">
          <div class="container-xl">
            <div class="row text-center align-items-center flex-row-reverse">
              <div class="col-lg-auto ms-lg-auto">
                <ul class="list-inline list-inline-dots mb-0">
                  <li class="list-inline-item"><a href="/privacy" class="link-secondary" rel="noopener">Privacy & Cookies</a></li>
                  <li class="list-inline-item"><a href="https://github.com/jasonvriends/lifetracker" class="link-secondary" rel="noopener">Source code</a></li>
                </ul>
              </div>
              <div class="col-12 col-lg-auto mt-3 mt-lg-0">
                <ul class="list-inline list-inline-dots mb-0">
                  <li class="list-inline-item">
                    Copyright © {{ currentYear }}
                    <a href="." class="link-secondary">Lifetracker</a>.
                    All rights reserved.
                  </li>
                  <li class="list-inline-item">
                    <a href="./changelog.html" class="link-secondary" rel="noopener">
                      v1.0.0-beta1
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
`,
  styles: [
  ]
})
export class DefaultComponent {

  constructor(
    private colorSchemeService: ColorSchemeService,
    private authService: AuthService,
    private cookieConsentService: CookieConsentService
  ) {  }

  currentYear: number = new Date().getFullYear();

  hasConsented(): boolean {
    return this.cookieConsentService.hasConsented();
  }

  setConsent(consent: boolean) {
    this.cookieConsentService.setConsent(consent);
  }

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

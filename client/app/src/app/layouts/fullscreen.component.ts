import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ColorSchemeService } from '../services/colorscheme.service';
import { CookieConsentService } from '../services/cookieconsent.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'layout-fullscreen',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="page page-center">
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

    </div>
  `,
  styles: [
  ]
})
export class FullscreenComponent {
  
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

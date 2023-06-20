import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { ColorSchemeService } from './services/colorscheme.service';
import { AuthService } from './services/auth.service';
import { provideHttpClient } from '@angular/common/http';
import { provideOAuthClient } from 'angular-oauth2-oidc';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    ColorSchemeService,
    provideHttpClient(),
    provideOAuthClient(),
    AuthService
  ]
};
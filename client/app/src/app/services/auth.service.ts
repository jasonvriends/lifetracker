import { Injectable } from '@angular/core';
import { authConfig } from '../configs/auth-config';
import { OAuthService } from "angular-oauth2-oidc";
import { JwksValidationHandler } from 'angular-oauth2-oidc-jwks';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private oauthService: OAuthService) {
    this.configureOAuthService();
  }

  private configureOAuthService() {
    this.oauthService.configure(authConfig);
    this.oauthService.tokenValidationHandler = new JwksValidationHandler();
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
  }

  isLoggedIn(): boolean {
    const idToken = this.oauthService.getIdToken();
    return !!idToken;
  }
  
  handleLoginClick = () => {
    if (this.isLoggedIn()) {
      return this.oauthService.logOut();
    } else {
      return this.oauthService.initLoginFlow();
    }
  };
  
  get claims(): any {
    return this.oauthService.getIdentityClaims() as any;
  }

}

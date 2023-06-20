import { AuthConfig } from 'angular-oauth2-oidc';
import { environment } from '../../environments/environment';

export const authConfig: AuthConfig = {
  issuer: environment.issuer,
  redirectUri: environment.redirectUri,
  clientId: environment.clientId,
  responseType: 'code',
  scope: 'openid profile email offline_access api',
  requireHttps: environment.production ? true : false,
  showDebugInformation: environment.production ? false : true,
}